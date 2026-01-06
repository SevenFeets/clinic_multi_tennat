# Main Terraform configuration for Clinic Management SaaS
# This file sets up AWS infrastructure for the application

terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Backend configuration (uncomment and configure for remote state)
  # backend "s3" {
  #   bucket = "clinic-terraform-state"
  #   key    = "terraform.tfstate"
  #   region = "us-east-1"
  # }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "Clinic Management SaaS"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr             = var.vpc_cidr
  availability_zones   = data.aws_availability_zones.available.names
  environment          = var.environment
  project_name         = var.project_name
}

# Security Groups Module
module "security_groups" {
  source = "./modules/security_groups"
  
  vpc_id      = module.vpc.vpc_id
  environment = var.environment
}

# RDS Database Module
module "rds" {
  source = "./modules/rds"
  
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.private_subnet_ids
  security_group_id   = module.security_groups.rds_security_group_id
  db_instance_class   = var.db_instance_class
  db_name             = var.db_name
  db_username         = var.db_username
  db_password         = var.db_password
  environment         = var.environment
  backup_retention    = var.backup_retention
}

# EC2 Instance for Backend
module "ec2_backend" {
  source = "./modules/ec2"
  
  instance_name       = "${var.project_name}-backend"
  instance_type       = var.backend_instance_type
  vpc_id              = module.vpc.vpc_id
  subnet_id           = module.vpc.public_subnet_ids[0]
  security_group_ids  = [module.security_groups.backend_security_group_id]
  key_pair_name       = var.key_pair_name
  environment         = var.environment
  user_data           = file("${path.module}/scripts/backend-init.sh")
  
  tags = {
    Role = "Backend"
  }
}

# EC2 Instance for Frontend (optional - can use S3 + CloudFront instead)
module "ec2_frontend" {
  source = "./modules/ec2"
  
  instance_name       = "${var.project_name}-frontend"
  instance_type       = var.frontend_instance_type
  vpc_id              = module.vpc.vpc_id
  subnet_id           = module.vpc.public_subnet_ids[0]
  security_group_ids  = [module.security_groups.frontend_security_group_id]
  key_pair_name       = var.key_pair_name
  environment         = var.environment
  user_data           = file("${path.module}/scripts/frontend-init.sh")
  
  tags = {
    Role = "Frontend"
  }
}

# Application Load Balancer
module "alb" {
  source = "./modules/alb"
  
  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.public_subnet_ids
  security_group_id   = module.security_groups.alb_security_group_id
  environment         = var.environment
  project_name        = var.project_name
}

# Outputs
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "backend_instance_ip" {
  value = module.ec2_backend.public_ip
}

output "frontend_instance_ip" {
  value = module.ec2_frontend.public_ip
}

output "rds_endpoint" {
  value     = module.rds.rds_endpoint
  sensitive = true
}

output "alb_dns_name" {
  value = module.alb.alb_dns_name
}

