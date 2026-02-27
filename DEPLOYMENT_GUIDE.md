# Deployment Guide - AI Platform

## Quick Start (Local Docker)

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

Access at: http://localhost

## Production Deployment (VPS)

### Prerequisites

- VPS with Ubuntu 20.04+ (Hetzner, DigitalOcean, AWS, etc.)
- Domain name pointed to your VPS IP
- SSH access to the server

### Step 1: Server Setup

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Create app directory
mkdir -p /opt/ai-platform
cd /opt/ai-platform
```

### Step 2: Upload Code

```bash
# From your local machine
scp -r * root@your-server-ip:/opt/ai-platform/

# Or use git
cd /opt/ai-platform
git clone your-repo-url .
```

### Step 3: Configure Environment

```bash
# Create .env file
cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///./ai_platform.db
EOF

# Update nginx.conf with your domain
sed -i 's/server_name _;/server_name your-domain.com;/' nginx.conf
```

### Step 4: Get SSL Certificate

```bash
# First, start without HTTPS
docker-compose up -d

# Get certificate
docker-compose run --rm certbot certonly --webroot \
  --webroot-path /var/www/certbot \
  -d your-domain.com \
  --email your@email.com \
  --agree-tos \
  --no-eff-email

# Uncomment HTTPS server block in nginx.conf
# Then restart
docker-compose restart nginx
```

### Step 5: Update Web UI

Update `web/` files to use your domain:

```javascript
// Change in all web/*.html files
const API_URL = 'https://your-domain.com/api';
```

### Step 6: Start Services

```bash
# Build and start
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
```

## Verification

1. **API**: https://your-domain.com/api/
2. **Docs**: https://your-domain.com/docs
3. **Web UI**: https://your-domain.com/

## Monitoring

```bash
# View logs
docker-compose logs -f

# Check resource usage
docker stats

# Restart services
docker-compose restart

# Update code
git pull
docker-compose up -d --build
```

## Backup

```bash
# Backup database
docker-compose exec api cp /app/ai_platform.db /app/backup.db
docker cp ai_platform_api:/app/backup.db ./backup-$(date +%Y%m%d).db

# Restore database
docker cp backup.db ai_platform_api:/app/ai_platform.db
docker-compose restart api
```

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  api:
    deploy:
      replicas: 3
    # ... rest of config
```

### Database Upgrade (PostgreSQL)

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ai_platform
      POSTGRES_USER: ai_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    environment:
      - DATABASE_URL=postgresql://ai_user:${DB_PASSWORD}@db:5432/ai_platform
    depends_on:
      - db

volumes:
  postgres_data:
```

## Security Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Configure firewall (ufw)
- [ ] Set up fail2ban
- [ ] Enable rate limiting (already in nginx.conf)
- [ ] Regular backups
- [ ] Monitor logs
- [ ] Update dependencies regularly

## Troubleshooting

### API not responding
```bash
docker-compose logs api
docker-compose restart api
```

### Database locked
```bash
docker-compose down
docker-compose up -d
```

### SSL certificate renewal
```bash
docker-compose run --rm certbot renew
docker-compose restart nginx
```

### Out of memory
```bash
# Check usage
docker stats

# Increase swap
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

## Cost Estimates

### VPS Options

**Hetzner** (Recommended):
- CX11: €4.15/month (2GB RAM, 20GB SSD) - Good for start
- CX21: €5.83/month (4GB RAM, 40GB SSD) - Recommended
- CX31: €10.59/month (8GB RAM, 80GB SSD) - Production

**DigitalOcean**:
- Basic: $6/month (1GB RAM) - Minimal
- Basic: $12/month (2GB RAM) - Good for start
- Basic: $24/month (4GB RAM) - Recommended

**AWS Lightsail**:
- $5/month (1GB RAM) - Minimal
- $10/month (2GB RAM) - Good for start
- $20/month (4GB RAM) - Recommended

### Domain
- Namecheap: ~$10/year
- Cloudflare: Free DNS + CDN

### Total Monthly Cost
- **Minimal**: $10-15/month (VPS + domain)
- **Recommended**: $20-30/month (better VPS)
- **Production**: $50+/month (scaling, backups, monitoring)

## Performance Tuning

### Nginx
```nginx
# Add to nginx.conf
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
}
```

### Uvicorn
```bash
# In Dockerfile CMD
CMD ["uvicorn", "app_multiuser:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Database
```python
# Use connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

## Maintenance

### Weekly
- Check logs for errors
- Monitor disk space
- Review user activity

### Monthly
- Update dependencies
- Backup database
- Review security logs
- Check SSL certificate expiry

### Quarterly
- Update system packages
- Review and optimize database
- Performance testing
- Security audit

## Next Steps

After deployment:
1. Test registration and login
2. Create test account
3. Verify all features work
4. Set up monitoring (optional: Grafana, Prometheus)
5. Configure backups
6. Add custom domain email
7. Set up status page

## Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Restart services: `docker-compose restart`
3. Check GitHub issues
4. Community Discord (if available)

---

**You now have a publicly accessible AI platform!**

Send users to: https://your-domain.com
They can register and get their own autonomous AI agent.
