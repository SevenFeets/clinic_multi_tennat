# Variable definitions for Terraform configuration

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (production, staging, development)"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "clinic-saas"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "clinic_db"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

variable "backup_retention" {
  description = "RDS backup retention period in days"
  type        = number
  default     = 7
}

variable "backend_instance_type" {
  description = "EC2 instance type for backend (t3.micro is free tier eligible)"
  type        = string
  default     = "t3.micro"  # Changed from t3.small to save money
}

variable "frontend_instance_type" {
  description = "EC2 instance type for frontend (t3.micro is free tier eligible)"
  type        = string
  default     = "t3.micro"
}

variable "key_pair_name" {
  description = "AWS Key Pair name for EC2 instances"
  type        = string
}

