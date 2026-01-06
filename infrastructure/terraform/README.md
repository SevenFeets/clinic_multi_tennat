# Terraform Infrastructure as Code

This directory contains Terraform configurations for deploying the Clinic Management SaaS to AWS.

## Prerequisites

1. **AWS CLI** installed and configured
   ```bash
   aws configure
   ```

2. **Terraform** installed (>= 1.5.0)
   ```bash
   terraform version
   ```

3. **AWS Account** with appropriate permissions

## Structure

```
infrastructure/terraform/
├── main.tf                 # Main configuration
├── variables.tf           # Variable definitions
├── outputs.tf             # Output values
├── modules/               # Reusable modules
│   ├── vpc/              # VPC, subnets, NAT gateway
│   ├── security_groups/  # Security groups
│   ├── rds/              # PostgreSQL database
│   ├── ec2/              # EC2 instances
│   └── alb/              # Application Load Balancer
└── environments/         # Environment-specific configs
    ├── production/
    └── staging/
```

## Quick Start

1. **Set up variables**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```

3. **Plan the deployment**:
   ```bash
   terraform plan
   ```

4. **Apply the configuration**:
   ```bash
   terraform apply
   ```

5. **Destroy resources** (when done):
   ```bash
   terraform destroy
   ```

## Required Variables

Create a `terraform.tfvars` file with:

```hcl
aws_region          = "us-east-1"
environment         = "production"
project_name        = "clinic-saas"
db_username         = "admin"
db_password         = "your-secure-password"
key_pair_name       = "your-key-pair-name"
```

## What Gets Created

- **VPC** with public and private subnets
- **Internet Gateway** and **NAT Gateway**
- **RDS PostgreSQL** database in private subnet
- **EC2 instances** for backend and frontend
- **Application Load Balancer**
- **Security Groups** with appropriate rules

## Cost Estimation

Approximate monthly costs (us-east-1):
- EC2 instances (t3.small + t3.micro): ~$30-40
- RDS (db.t3.micro): ~$15-20
- NAT Gateway: ~$32
- Data transfer: Variable
- **Total**: ~$80-100/month (production)

## Security Notes

- Database is in private subnet (not directly accessible)
- Security groups restrict access appropriately
- Use AWS Secrets Manager for sensitive data in production
- Enable CloudTrail for audit logging
- Use AWS WAF for additional protection

## Next Steps

1. Set up remote state (S3 backend)
2. Configure CI/CD for automated deployments
3. Add CloudWatch alarms and monitoring
4. Set up auto-scaling groups
5. Configure SSL/TLS certificates (ACM)

