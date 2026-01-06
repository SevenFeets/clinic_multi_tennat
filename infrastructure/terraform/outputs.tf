# Output values from Terraform

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "backend_instance_ip" {
  description = "Public IP of backend EC2 instance"
  value       = module.ec2_backend.public_ip
}

output "frontend_instance_ip" {
  description = "Public IP of frontend EC2 instance"
  value       = module.ec2_frontend.public_ip
}

output "rds_endpoint" {
  description = "RDS database endpoint"
  value       = module.rds.rds_endpoint
  sensitive   = true
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.alb.alb_dns_name
}

output "backend_target_group_arn" {
  description = "ARN of backend target group"
  value       = module.alb.backend_target_group_arn
}

output "frontend_target_group_arn" {
  description = "ARN of frontend target group"
  value       = module.alb.frontend_target_group_arn
}

