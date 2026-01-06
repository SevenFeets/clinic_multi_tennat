# 🚀 Deployment Guide - Clinic Management SaaS

Complete guide for deploying the Clinic Management SaaS application with Docker, AWS, Terraform, and monitoring.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development with Docker](#local-development-with-docker)
3. [Testing Setup](#testing-setup)
4. [CI/CD with GitHub Actions](#cicd-with-github-actions)
5. [AWS Deployment with Terraform](#aws-deployment-with-terraform)
6. [Monitoring & Observability](#monitoring--observability)
7. [Production Checklist](#production-checklist)

---

## Prerequisites

### Required Tools

- **Docker** & **Docker Compose** - Containerization
- **Terraform** (>= 1.5.0) - Infrastructure as Code
- **AWS CLI** - AWS management
- **Python 3.11+** - Backend development
- **Node.js 20+** - Frontend development
- **Git** - Version control

### AWS Account Setup

1. Create AWS account
2. Configure AWS CLI:
   ```bash
   aws configure
   ```
3. Create IAM user with appropriate permissions:
   - EC2 Full Access
   - RDS Full Access
   - VPC Full Access
   - IAM (for creating roles)
   - S3 (for Terraform state)

4. Create EC2 Key Pair:
   ```bash
   aws ec2 create-key-pair --key-name clinic-key-pair --query 'KeyMaterial' --output text > clinic-key-pair.pem
   chmod 400 clinic-key-pair.pem
   ```

---

## Local Development with Docker

### Quick Start

1. **Clone and navigate to project**:
   ```bash
   cd "D:\clinic multi tennant SaaS"
   ```

2. **Create environment file**:
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **Access services**:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost
   - API Docs: http://localhost:8000/docs
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001 (admin/admin)

5. **View logs**:
   ```bash
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

6. **Stop services**:
   ```bash
   docker-compose down
   ```

### Database Migrations

Run Alembic migrations inside the backend container:

```bash
docker-compose exec backend alembic upgrade head
```

### Building Images

```bash
# Build backend
docker build -t clinic-backend:latest .

# Build frontend
docker build -t clinic-frontend:latest ./frontend
```

---

## Testing Setup

### Backend Tests

1. **Install test dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run all tests**:
   ```bash
   pytest
   ```

3. **Run with coverage**:
   ```bash
   pytest --cov=app --cov-report=html
   ```

4. **Run specific test file**:
   ```bash
   pytest tests/test_patients.py -v
   ```

5. **View coverage report**:
   ```bash
   # HTML report opens in browser
   open htmlcov/index.html  # macOS
   start htmlcov/index.html  # Windows
   ```

### Test Structure

- `tests/conftest.py` - Shared fixtures
- `tests/test_auth.py` - Authentication tests
- `tests/test_patients.py` - Patient CRUD tests
- `tests/test_appointments.py` - Appointment tests

### Frontend Tests (TODO)

```bash
cd frontend
npm install
npm test
```

---

## CI/CD with GitHub Actions

### Workflow Overview

The CI/CD pipeline (`.github/workflows/ci-cd.yml`) includes:

1. **Backend Tests** - Runs pytest with coverage
2. **Frontend Tests** - Linting and build verification
3. **Docker Build** - Builds and caches Docker images
4. **Security Scan** - Trivy vulnerability scanning

### Setup

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add CI/CD pipeline"
   git push origin main
   ```

2. **View workflow runs**:
   - Go to GitHub → Actions tab
   - See workflow status and logs

3. **Add secrets** (if needed):
   - GitHub → Settings → Secrets → Actions
   - Add AWS credentials for deployment

### Manual Trigger

Workflows run automatically on:
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

---

## AWS Deployment with Terraform

### Step 1: Configure Terraform

1. **Navigate to Terraform directory**:
   ```bash
   cd infrastructure/terraform
   ```

2. **Create `terraform.tfvars`**:
   ```hcl
   aws_region          = "us-east-1"
   environment         = "production"
   project_name        = "clinic-saas"
   db_username         = "admin"
   db_password         = "your-secure-password-here"
   key_pair_name       = "clinic-key-pair"
   backend_instance_type = "t3.small"
   frontend_instance_type = "t3.micro"
   db_instance_class   = "db.t3.micro"
   ```

3. **Initialize Terraform**:
   ```bash
   terraform init
   ```

### Step 2: Plan Deployment

```bash
terraform plan
```

Review the plan carefully. It will show:
- Resources to be created
- Estimated costs
- Configuration details

### Step 3: Apply Configuration

```bash
terraform apply
```

Type `yes` when prompted. This will create:
- VPC with subnets
- RDS PostgreSQL database
- EC2 instances
- Security groups
- Application Load Balancer

### Step 4: Get Outputs

```bash
terraform output
```

Save these values:
- `backend_instance_ip` - Backend server IP
- `frontend_instance_ip` - Frontend server IP
- `rds_endpoint` - Database connection string
- `alb_dns_name` - Load balancer URL

### Step 5: Deploy Application

1. **SSH into backend instance**:
   ```bash
   ssh -i clinic-key-pair.pem ec2-user@<backend_instance_ip>
   ```

2. **Install Docker**:
   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo systemctl start docker
   sudo usermod -aG docker ec2-user
   ```

3. **Deploy backend**:
   ```bash
   # Pull your Docker image or build from source
   docker run -d \
     -p 8000:8000 \
     -e DATABASE_URL="postgresql://admin:password@<rds_endpoint>:5432/clinic_db" \
     -e SECRET_KEY="your-secret-key" \
     clinic-backend:latest
   ```

4. **Deploy frontend** (similar process)

### Step 6: Update DNS (Optional)

Point your domain to the ALB DNS name using Route 53 or your DNS provider.

### Destroy Infrastructure

```bash
terraform destroy
```

⚠️ **Warning**: This will delete all resources!

---

## Monitoring & Observability

### Prometheus

- **URL**: http://localhost:9090 (local) or http://<prometheus-ip>:9090
- **Metrics Endpoint**: http://localhost:8000/metrics
- **Configuration**: `monitoring/prometheus/prometheus.yml`

### Grafana

- **URL**: http://localhost:3001 (local)
- **Default Credentials**: admin/admin
- **Data Source**: Auto-configured to Prometheus
- **Dashboards**: Place JSON files in `monitoring/grafana/dashboards/`

### Adding Custom Metrics

The backend automatically exposes metrics via Prometheus. View at:
```
http://localhost:8000/metrics
```

### CloudWatch (AWS)

For production, also set up CloudWatch:
- Logs aggregation
- Metrics and alarms
- Dashboards

---

## Production Checklist

### Security

- [ ] Change all default passwords
- [ ] Use AWS Secrets Manager for sensitive data
- [ ] Enable SSL/TLS (AWS Certificate Manager)
- [ ] Restrict SSH access to specific IPs
- [ ] Enable AWS WAF
- [ ] Set up CloudTrail for audit logging
- [ ] Regular security updates

### Performance

- [ ] Enable RDS Performance Insights
- [ ] Set up CloudWatch alarms
- [ ] Configure auto-scaling groups
- [ ] Use CDN for frontend (CloudFront)
- [ ] Enable database connection pooling

### Backup & Recovery

- [ ] Configure RDS automated backups
- [ ] Set up S3 backups for application data
- [ ] Test disaster recovery procedures
- [ ] Document recovery steps

### Monitoring

- [ ] Set up Prometheus alerts
- [ ] Configure Grafana dashboards
- [ ] Set up CloudWatch alarms
- [ ] Configure log aggregation
- [ ] Set up uptime monitoring

### Cost Optimization

- [ ] Use Reserved Instances for EC2
- [ ] Use Reserved Instances for RDS
- [ ] Set up cost alerts
- [ ] Review and optimize instance sizes
- [ ] Use Spot Instances for non-critical workloads

---

## Troubleshooting

### Docker Issues

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs backend

# Restart service
docker-compose restart backend
```

### Terraform Issues

```bash
# Validate configuration
terraform validate

# Refresh state
terraform refresh

# Show current state
terraform show
```

### Database Connection Issues

1. Check security group rules
2. Verify RDS endpoint
3. Check VPC routing
4. Verify credentials

### Application Issues

1. Check CloudWatch logs
2. Verify environment variables
3. Check health endpoints
4. Review Prometheus metrics

---

## Next Steps

1. **Set up Elasticsearch** for advanced search
2. **Implement Redux** for state management
3. **Add more monitoring** dashboards
4. **Set up staging environment**
5. **Implement blue-green deployments**
6. **Add automated backups**
7. **Set up disaster recovery**

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

---

**Need Help?** Check the troubleshooting section or review the logs for detailed error messages.

