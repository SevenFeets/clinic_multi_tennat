# Cost-Optimized Terraform Configuration
# This version minimizes costs by using free tier eligible resources

# Override default instance types for cost optimization
locals {
  # Use free tier eligible instances
  backend_instance_type  = "t3.micro"   # Free tier eligible (750 hrs/month)
  frontend_instance_type = "t3.micro"   # Free tier eligible (750 hrs/month)
  db_instance_class      = "db.t3.micro" # Free tier eligible (750 hrs/month)
  
  # Disable NAT Gateway to save $32/month (use public subnets only for dev)
  # For production, you'd want NAT Gateway for security
  use_nat_gateway = var.environment == "production" ? true : false
}

# Modified VPC module that can skip NAT Gateway
module "vpc_cost_optimized" {
  source = "./modules/vpc"
  
  vpc_cidr             = var.vpc_cidr
  availability_zones   = data.aws_availability_zones.available.names
  environment          = var.environment
  project_name         = var.project_name
  use_nat_gateway      = local.use_nat_gateway
}

# Cost-optimized EC2 instances
module "ec2_backend_cost_optimized" {
  source = "./modules/ec2"
  
  instance_name       = "${var.project_name}-backend"
  instance_type       = local.backend_instance_type  # t3.micro (free tier)
  vpc_id              = module.vpc_cost_optimized.vpc_id
  subnet_id           = module.vpc_cost_optimized.public_subnet_ids[0]  # Public for dev
  security_group_ids  = [module.security_groups.backend_security_group_id]
  key_pair_name       = var.key_pair_name
  environment         = var.environment
  
  # User data to install Docker and run container
  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ec2-user
    
    # Install Docker Compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    # Your app deployment would go here
    # docker pull your-image:latest
    # docker run -d -p 8000:8000 your-image:latest
  EOF
  
  tags = {
    Role = "Backend"
    CostOptimized = "true"
  }
}

# Single EC2 instance for both frontend and backend (saves money)
# Or use separate t3.micro instances (both free tier eligible)
module "ec2_frontend_cost_optimized" {
  source = "./modules/ec2"
  
  instance_name       = "${var.project_name}-frontend"
  instance_type       = local.frontend_instance_type  # t3.micro (free tier)
  vpc_id              = module.vpc_cost_optimized.vpc_id
  subnet_id           = module.vpc_cost_optimized.public_subnet_ids[0]
  security_group_ids  = [module.security_groups.frontend_security_group_id]
  key_pair_name       = var.key_pair_name
  environment         = var.environment
  
  tags = {
    Role = "Frontend"
    CostOptimized = "true"
  }
}

# Cost-optimized RDS
module "rds_cost_optimized" {
  source = "./modules/rds"
  
  vpc_id              = module.vpc_cost_optimized.vpc_id
  subnet_ids          = local.use_nat_gateway ? module.vpc_cost_optimized.private_subnet_ids : module.vpc_cost_optimized.public_subnet_ids
  security_group_id   = module.security_groups.rds_security_group_id
  db_instance_class   = local.db_instance_class  # db.t3.micro (free tier)
  db_name             = var.db_name
  db_username         = var.db_username
  db_password         = var.db_password
  environment         = var.environment
  backup_retention    = var.environment == "production" ? 7 : 1  # Less backups = cheaper
}

