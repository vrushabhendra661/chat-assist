# Deployment Guide

Guide for deploying the AI Chat Assistant to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Backend Deployment](#backend-deployment)
- [Frontend Deployment](#frontend-deployment)
- [Database Setup](#database-setup)
- [Security Considerations](#security-considerations)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Production server (VPS, cloud instance, etc.)
- Domain name (optional but recommended)
- SSL certificate
- OpenAI API key with production billing

## Environment Configuration

### Production Environment Variables

**Backend (.env):**
```env
# Production values
OPENAI_API_KEY=sk-prod-your-key-here
HOST=0.0.0.0
PORT=8000
DATABASE_URL=postgresql://user:pass@host:5432/dbname  # Or SQLite path
MAX_CONTEXT_MESSAGES=10

# Security
ALLOWED_ORIGINS=https://yourdomain.com
```

**Frontend (.env.production):**
```env
REACT_APP_API_URL=https://api.yourdomain.com
```

## Backend Deployment

### Option 1: Traditional VPS (Ubuntu)

#### 1. Install Dependencies

```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-venv nginx supervisor
```

#### 2. Setup Application

```bash
cd /var/www
git clone <your-repo>
cd chat-bot/backend

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Create .env File

```bash
nano .env
# Add production values
```

#### 4. Configure Supervisor

Create `/etc/supervisor/conf.d/chatbot.conf`:

```ini
[program:chatbot]
directory=/var/www/chat-bot/backend
command=/var/www/chat-bot/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/chatbot/err.log
stdout_logfile=/var/log/chatbot/out.log
```

```bash
sudo mkdir -p /var/log/chatbot
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start chatbot
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/chatbot`:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 6. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

### Option 2: Docker

#### 1. Create Dockerfile (Backend)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/chatbot
    depends_on:
      - db
    restart: always

  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=chatbot
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always

volumes:
  postgres_data:
```

#### 3. Deploy

```bash
docker-compose up -d
```

### Option 3: Cloud Platforms

#### Heroku

**backend/Procfile:**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**backend/runtime.txt:**
```
python-3.9.16
```

**Deploy:**
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

#### AWS Elastic Beanstalk

```bash
eb init -p python-3.9 chatbot-backend
eb create production
eb setenv OPENAI_API_KEY=your-key
eb deploy
```

#### Google Cloud Run

```bash
gcloud run deploy chatbot-backend \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key
```

#### DigitalOcean App Platform

1. Connect repository
2. Select backend directory
3. Add environment variables
4. Deploy

## Frontend Deployment

### Option 1: Static Hosting

#### 1. Build Production Bundle

```bash
cd frontend
npm run build
```

This creates an optimized `build/` directory.

#### 2. Deploy to Netlify

**netlify.toml:**
```toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  REACT_APP_API_URL = "https://api.yourdomain.com"
```

**Deploy:**
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

#### 3. Deploy to Vercel

```bash
npm install -g vercel
vercel --prod
```

#### 4. Deploy to AWS S3 + CloudFront

```bash
aws s3 sync build/ s3://your-bucket-name
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

#### 5. Deploy to GitHub Pages

**package.json:**
```json
{
  "homepage": "https://yourusername.github.io/chat-bot",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

```bash
npm install gh-pages
npm run deploy
```

### Option 2: Nginx (Same Server as Backend)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    root /var/www/chat-bot/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (optional if different domain)
    location /api {
        proxy_pass http://127.0.0.1:8000/api;
    }
}
```

### Option 3: Docker

**frontend/Dockerfile:**
```dockerfile
# Build stage
FROM node:16 as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**frontend/nginx.conf:**
```nginx
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

## Database Setup

### SQLite (Development/Small Scale)

Default configuration works out of the box. Just ensure the file path is writable.

### PostgreSQL (Production)

#### 1. Install PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib
```

#### 2. Create Database and User

```bash
sudo -u postgres psql

CREATE DATABASE chatbot;
CREATE USER chatbot_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE chatbot TO chatbot_user;
\q
```

#### 3. Update Backend .env

```env
DATABASE_URL=postgresql://chatbot_user:secure_password@localhost:5432/chatbot
```

#### 4. Update database.py

```python
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)  # Remove check_same_thread for PostgreSQL
```

#### 5. Run Migrations

```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Managed Databases

- **AWS RDS**: Fully managed PostgreSQL
- **Google Cloud SQL**: Managed database service
- **DigitalOcean Managed Databases**: Easy setup
- **Heroku Postgres**: Add-on for Heroku apps

## Security Considerations

### 1. Environment Variables

Never commit `.env` files. Use:
- Environment variables on server
- Secrets management services (AWS Secrets Manager, etc.)
- CI/CD encrypted variables

### 2. API Key Security

```python
# Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: Request, ...):
    ...
```

### 3. CORS Configuration

```python
# main.py - Restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### 4. HTTPS Only

- Use SSL certificates (Let's Encrypt)
- Redirect HTTP to HTTPS
- Set secure headers

### 5. Input Validation

Already implemented via Pydantic models. Ensure all endpoints validate input.

### 6. Authentication (Optional Enhancement)

Add JWT or OAuth2 for production:

```python
from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.post("/api/chat")
async def chat(request: ChatRequest, token: str = Depends(security)):
    # Verify token
    ...
```

## Monitoring

### 1. Application Monitoring

**Backend Logging:**
```python
import logging
logging.basicConfig(
    filename='/var/log/chatbot/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Error Tracking:**
- Sentry
- Rollbar
- New Relic

### 2. Server Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs
```

**Services:**
- Datadog
- Prometheus + Grafana
- AWS CloudWatch

### 3. Uptime Monitoring

- UptimeRobot
- Pingdom
- StatusCake

### 4. Health Checks

Already implemented at `/api/health`. Set up monitoring to ping this endpoint.

## Performance Optimization

### Backend

1. **Use production ASGI server:**
```bash
uvicorn main:app --workers 4 --limit-concurrency 100
```

2. **Enable caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(param):
    ...
```

3. **Database connection pooling:**
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)
```

### Frontend

1. **Enable compression in Nginx:**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

2. **Use CDN for static assets**

3. **Implement caching headers:**
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Backup Strategy

### Database Backups

```bash
# PostgreSQL
pg_dump chatbot > backup_$(date +%Y%m%d).sql

# Automate with cron
0 2 * * * /path/to/backup_script.sh
```

### Application Backups

```bash
# Backup application files
tar -czf chatbot_backup_$(date +%Y%m%d).tar.gz /var/www/chat-bot
```

## Troubleshooting

### Check Service Status

```bash
sudo supervisorctl status chatbot
sudo systemctl status nginx
```

### View Logs

```bash
sudo tail -f /var/log/chatbot/out.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
sudo supervisorctl restart chatbot
sudo systemctl restart nginx
```

### Database Connection Issues

```bash
# Test connection
psql -h localhost -U chatbot_user -d chatbot
```

### Port Conflicts

```bash
sudo netstat -tulpn | grep :8000
```

## Scaling

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy)
- Deploy multiple backend instances
- Share database across instances
- Use Redis for session storage

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Implement caching

## CI/CD Pipeline

### GitHub Actions Example

**.github/workflows/deploy.yml:**
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          ssh user@server 'cd /var/www/chat-bot && git pull && supervisorctl restart chatbot'
      
      - name: Deploy Frontend
        run: |
          cd frontend
          npm install
          npm run build
          # Deploy to hosting service
```

## Checklist

Before going live:

- [ ] All environment variables set
- [ ] SSL certificate installed
- [ ] Database backed up
- [ ] Monitoring configured
- [ ] Error tracking setup
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Health checks working
- [ ] Logs being written
- [ ] Backup strategy in place
- [ ] Domain DNS configured
- [ ] Security headers set
- [ ] Performance tested
- [ ] Documentation updated

## Support

For deployment issues:
- Check server logs
- Verify environment variables
- Test API endpoints manually
- Check OpenAI API status
- Review firewall rules

---

**Note:** Always test deployment in staging environment before production!

