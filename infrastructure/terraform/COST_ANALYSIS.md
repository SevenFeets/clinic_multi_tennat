# 💰 AWS Cost Analysis & Optimization Guide

## Cost Breakdown

### Current Setup (Production-Ready)

| Resource | Type | Monthly Cost | Free Tier? |
|----------|------|--------------|------------|
| EC2 Backend | t3.small | ~$15 | ❌ No |
| EC2 Frontend | t3.micro | ~$7 | ✅ Yes (first 12 months) |
| RDS Database | db.t3.micro | ~$15 | ✅ Yes (first 12 months) |
| NAT Gateway | Standard | ~$32 | ❌ No |
| Data Transfer | Variable | ~$5-10 | ✅ 1GB free/month |
| **Total** | | **~$74/month** | |

### Cost-Optimized Setup (Development/Learning)

| Resource | Type | Monthly Cost | Free Tier? |
|----------|------|--------------|------------|
| EC2 Backend | t3.micro | **$0** (free tier) | ✅ Yes |
| EC2 Frontend | t3.micro | **$0** (free tier) | ✅ Yes |
| RDS Database | db.t3.micro | **$0** (free tier) | ✅ Yes |
| NAT Gateway | **Skipped** | **$0** | ✅ N/A |
| Data Transfer | Minimal | **$0** | ✅ Yes |
| **Total** | | **~$0/month** | ✅ **FREE!** |

### After Free Tier Expires

| Resource | Monthly Cost |
|----------|--------------|
| 2x EC2 t3.micro | ~$14 |
| RDS db.t3.micro | ~$15 |
| NAT Gateway (optional) | ~$32 |
| **Total (no NAT)** | **~$29/month** |
| **Total (with NAT)** | **~$61/month** |

---

## EC2 vs ECS Cost Comparison

### EC2 (What we're using)

**Cost:**
- You pay for EC2 instance: ~$7-15/month per instance
- No additional charges
- Simple to set up

**Best for:**
- Learning
- Small projects
- Full control needed

### ECS (Elastic Container Service)

**Cost:**
- ECS itself: **FREE** (no additional charge)
- You pay for underlying EC2 instances: Same as EC2 (~$7-15/month)
- OR use Fargate: ~$0.04/vCPU-hour + $0.004/GB-hour
  - Example: 0.25 vCPU + 0.5GB = ~$8/month per container

**Best for:**
- Production applications
- Auto-scaling needs
- Multiple containers
- Managed service benefits

**Cost Comparison:**
```
EC2:  $15/month (one instance, you manage it)
ECS:  $15/month (same EC2, but managed by AWS)
Fargate: $8-16/month (no EC2 to manage, pay per container)
```

**Winner for cost:** EC2 is cheapest for small projects!

---

## Cost Optimization Strategies

### 1. Use Free Tier Resources ✅

```hcl
# In terraform.tfvars
backend_instance_type = "t3.micro"   # Free tier eligible
frontend_instance_type = "t3.micro"  # Free tier eligible
db_instance_class = "db.t3.micro"    # Free tier eligible
```

### 2. Skip NAT Gateway for Development

**Saves: $32/month**

NAT Gateway is only needed if:
- Database must be in private subnet (security)
- Production environment

For development/learning:
- Use public subnets
- Save $32/month

### 3. Use Spot Instances (Advanced)

**Saves: 60-90%**

```hcl
# Spot instances are much cheaper but can be interrupted
instance_type = "t3.micro"
spot_price = "0.01"  # Much cheaper than on-demand
```

**Warning:** Spot instances can be terminated by AWS with 2-minute notice.

### 4. Single EC2 Instance (Ultra Cheap)

**Saves: $7/month**

Run both frontend and backend on one EC2 instance:

```hcl
# One t3.micro instance running both
# Use docker-compose to run multiple containers
```

**Cost:** ~$7/month (or free with free tier)

### 5. Use RDS Free Tier

**Saves: $15/month**

- db.t3.micro is free for 750 hours/month
- Perfect for development

### 6. Minimize Storage

```hcl
# RDS storage
allocated_storage = 20  # Minimum (cheaper)
max_allocated_storage = 100  # Auto-scales only when needed

# EC2 storage
volume_size = 20  # Minimum (cheaper)
```

---

## Recommended Setup by Use Case

### 🎓 Learning / Development

**Cost: $0/month (free tier)**

```hcl
backend_instance_type = "t3.micro"
frontend_instance_type = "t3.micro"
db_instance_class = "db.t3.micro"
# Skip NAT Gateway
```

### 🚀 Small Production

**Cost: ~$29/month**

```hcl
backend_instance_type = "t3.micro"  # Can upgrade to t3.small if needed
frontend_instance_type = "t3.micro"
db_instance_class = "db.t3.micro"
# Skip NAT Gateway (use public subnets with security groups)
```

### 🏢 Production (Secure)

**Cost: ~$61/month**

```hcl
backend_instance_type = "t3.small"  # More power
frontend_instance_type = "t3.micro"
db_instance_class = "db.t3.micro"
# Use NAT Gateway (database in private subnet)
```

---

## Cost Monitoring

### Set Up Billing Alerts

1. Go to AWS Billing Dashboard
2. Create budget alert at $10, $25, $50 thresholds
3. Get email notifications

### Use AWS Cost Explorer

- View costs by service
- Forecast future costs
- Identify cost spikes

---

## Free Alternatives (If Budget is Zero)

### Option 1: Local Development Only
- Run everything locally with Docker
- **Cost: $0**
- No cloud deployment

### Option 2: Free Tier Only
- Use AWS Free Tier (12 months)
- **Cost: $0**
- Limited to t3.micro instances

### Option 3: Other Free Services
- **Railway.app**: Free tier (limited)
- **Render.com**: Free tier (limited)
- **Fly.io**: Free tier (limited)
- **Heroku**: No longer free (was free before)

**Note:** AWS Free Tier is the most generous and reliable.

---

## Summary

| Setup | Monthly Cost | Best For |
|-------|--------------|----------|
| **Free Tier (EC2)** | **$0** | Learning, Development |
| **EC2 Small** | **~$29** | Small Production |
| **EC2 + NAT** | **~$61** | Secure Production |
| **ECS Fargate** | **~$16-32** | Container-focused |
| **Local Docker** | **$0** | Development only |

**Recommendation:** Start with free tier EC2 setup, upgrade as needed!

