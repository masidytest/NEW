# 🚂 Railway Deployment Guide

Complete guide to deploying your AI Platform on Railway with automatic HTTPS, PostgreSQL, and zero-ops scaling.

## Architecture Overview

Your platform will be deployed as:

```
┌─────────────────────────────────────────────┐
│  Railway Project                            │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Service 1: Backend API              │  │
│  │  - FastAPI + Uvicorn                 │  │
│  │  - Plugin system                     │  │
│  │  - Per-user agents                   │  │
│  │  - Auto HTTPS                        │  │
│  │  URL: backend.railway.app            │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Service 2: Static Web UI            │  │
│  │  - HTML/CSS/JS                       │  │
│  │  - Auto HTTPS                        │  │
│  │  URL: frontend.railway.app           │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Service 3: PostgreSQL Database      │  │
│  │  - Managed by Railway                │  │
│  │  - Automatic backups                 │  │
│  │  - Auto-injected DATABASE_URL        │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

## Prerequisites

1. GitHub account with your code pushed
2. Railway account (sign up at https://railway.app)
3. Your code ready with these files:
   - ✅ `Dockerfile`
   - ✅ `railway.json`
   - ✅ `requirements.txt`
   - ✅ `app_multiuser.py`
   - ✅ `db.py` (updated for Postgres)

## Step 1: Deploy Backend API

### 1.1 Create New Project

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your repository

### 1.2 Configure Backend Service

Railway will auto-detect your `Dockerfile` and `railway.json`.

1. Click on the deployed service
2. Go to **"Settings"** tab
3. Set **Service Name**: `ai-platform-backend`

### 1.3 Add PostgreSQL Database

1. In your project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically:
   - Creates the database
   - Injects `DATABASE_URL` into your backend service
   - Handles connection pooling

### 1.4 Set Environment Variables

In your backend service settings, add these variables:

```bash
# Required
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ENV=production

# Optional (will be set after frontend deployment)
ALLOWED_ORIGINS=https://your-frontend.railway.app
```

To generate a secure `SECRET_KEY`:
```bash
openssl rand -hex 32
```

### 1.5 Deploy

1. Click **"Deploy"**
2. Wait for build to complete (~2-3 minutes)
3. Railway will provide a public URL like:
   ```
   https://ai-platform-backend-production.up.railway.app
   ```
4. Save this URL - you'll need it for the frontend

### 1.6 Initialize Database

The database tables will be created automatically on first run (see `app_multiuser.py`):
```python
Base.metadata.create_all(bind=engine)
```

### 1.7 Test Backend

```bash
# Test health endpoint
curl https://your-backend.railway.app/

# Test registration
curl -X POST https://your-backend.railway.app/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Test login
curl -X POST https://your-backend.railway.app/auth/token \
  -d "username=test@example.com&password=testpass123"
```

## Step 2: Deploy Static Web UI

### 2.1 Update Web UI Configuration

Before deploying, update all your web files to use the Railway backend URL.

In `web/chat.html`, `web/goals.html`, `web/capabilities.html`, `web/index.html`, `web/login.html`:

Replace:
```javascript
const API_URL = 'http://localhost:8000';
```

With:
```javascript
const API_URL = 'https://your-backend.railway.app';
```

**Important**: Use your actual Railway backend URL from Step 1.5.

### 2.2 Create Static Site Deployment

Option A: **Separate Static Service** (Recommended)

1. In Railway, click **"+ New"** → **"Empty Service"**
2. Connect to your GitHub repo
3. Go to **"Settings"**
4. Set **Root Directory**: `web`
5. Set **Build Command**: `echo "Static files ready"`
6. Set **Start Command**: Leave empty (Railway serves static files automatically)
7. Deploy

Option B: **Use Netlify/Vercel for Frontend**

If you prefer, deploy the `web/` folder to Netlify or Vercel:
- Drag and drop the `web/` folder
- They'll provide a URL like `https://your-app.netlify.app`

### 2.3 Update CORS Settings

Go back to your backend service and update `ALLOWED_ORIGINS`:

```bash
ALLOWED_ORIGINS=https://your-frontend.railway.app,https://your-frontend.netlify.app
```

Redeploy the backend for CORS changes to take effect.

## Step 3: Test Full Deployment

### 3.1 Test Authentication Flow

1. Open your frontend URL in browser
2. Click **"Register"**
3. Create account with email/password
4. Should redirect to dashboard
5. Navigate to Chat, Goals, Capabilities
6. All should work with authentication

### 3.2 Test API Integration

Open browser DevTools → Network tab:
- All requests should go to your Railway backend URL
- All requests should include `Authorization: Bearer <token>`
- No CORS errors should appear

### 3.3 Test Plugin System

1. Chat with the AI
2. Try: "What's 5 doubled?" (should use math plugin)
3. Check `/capabilities` endpoint - should show 13+ capabilities

## Step 4: Custom Domain (Optional)

### 4.1 Add Custom Domain to Backend

1. In Railway backend service → **"Settings"** → **"Domains"**
2. Click **"Add Domain"**
3. Enter: `api.yourdomain.com`
4. Add CNAME record in your DNS:
   ```
   CNAME api.yourdomain.com → your-backend.railway.app
   ```
5. Railway automatically provisions SSL certificate

### 4.2 Add Custom Domain to Frontend

1. In Railway frontend service → **"Settings"** → **"Domains"**
2. Click **"Add Domain"**
3. Enter: `app.yourdomain.com`
4. Add CNAME record in your DNS:
   ```
   CNAME app.yourdomain.com → your-frontend.railway.app
   ```

### 4.3 Update Configuration

Update `ALLOWED_ORIGINS` in backend:
```bash
ALLOWED_ORIGINS=https://app.yourdomain.com
```

Update `API_URL` in frontend:
```javascript
const API_URL = 'https://api.yourdomain.com';
```

## Step 5: Monitoring & Logs

### 5.1 View Logs

In Railway:
1. Click on your service
2. Go to **"Deployments"** tab
3. Click on latest deployment
4. View real-time logs

### 5.2 Monitor Resources

Railway dashboard shows:
- CPU usage
- Memory usage
- Network traffic
- Request count

### 5.3 Set Up Alerts (Optional)

Railway Pro plan includes:
- Email alerts for crashes
- Slack/Discord webhooks
- Custom metrics

## Step 6: Scaling & Performance

### 6.1 Vertical Scaling

Railway automatically scales resources based on usage.

For more control:
1. Go to service **"Settings"**
2. Adjust **"Resources"**:
   - Memory: 512MB - 8GB
   - CPU: Shared - Dedicated

### 6.2 Horizontal Scaling

For multiple instances:
1. Railway Pro plan required
2. Enable **"Replicas"** in settings
3. Railway handles load balancing automatically

### 6.3 Database Optimization

For production workloads:
1. Upgrade to Railway Pro for larger database
2. Enable connection pooling (already configured in `db.py`)
3. Add database indexes for frequently queried fields

## Troubleshooting

### Issue: "Cannot connect to database"

**Solution**: Check that PostgreSQL plugin is added and `DATABASE_URL` is injected.

```bash
# In Railway service logs, verify:
echo $DATABASE_URL
```

### Issue: "CORS error in browser"

**Solution**: Update `ALLOWED_ORIGINS` environment variable with your frontend URL.

### Issue: "502 Bad Gateway"

**Solution**: Check logs for startup errors. Common causes:
- Missing environment variables
- Database connection failed
- Port binding issue (Railway uses `$PORT`)

### Issue: "Module not found"

**Solution**: Ensure all dependencies are in `requirements.txt` and rebuild.

### Issue: "Out of memory"

**Solution**: 
- Reduce PyTorch model size
- Increase Railway service memory
- Implement agent instance cleanup for inactive users

## Cost Estimation

### Railway Pricing

**Hobby Plan** (Free):
- $5 free credit/month
- Enough for development/testing
- ~500 hours of service uptime

**Pro Plan** ($20/month):
- $20 credit included
- Additional usage billed
- Priority support
- Custom domains
- Team collaboration

**Estimated Monthly Cost** (Pro Plan):
- Backend service: ~$10-15
- PostgreSQL: ~$5-10
- Static frontend: ~$0-5
- **Total**: ~$15-30/month for production

## Production Checklist

Before going live:

- [ ] Backend deployed and accessible
- [ ] PostgreSQL connected and initialized
- [ ] Frontend deployed with correct API_URL
- [ ] CORS configured correctly
- [ ] SECRET_KEY set to secure random value
- [ ] Environment variables set
- [ ] Test registration/login flow
- [ ] Test all web pages (chat, goals, capabilities)
- [ ] Test plugin system
- [ ] Monitor logs for errors
- [ ] Set up custom domain (optional)
- [ ] Configure backups (Railway Pro)
- [ ] Set up monitoring/alerts

## Next Steps

Once deployed, you can:

1. **Add Real Plugins**:
   - OpenAI/Anthropic integration
   - Weather API
   - Web search
   - Image generation

2. **Enhance Features**:
   - Email verification
   - Password reset
   - User profiles
   - Usage analytics
   - Billing integration

3. **Scale Up**:
   - Add Redis for caching
   - Implement background workers
   - Add rate limiting
   - Set up CDN for static assets

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Your project logs: Railway dashboard → Deployments

---

**Status**: Ready for deployment
**Platform**: Railway
**Estimated Setup Time**: 15-30 minutes
**Estimated Cost**: $15-30/month (production)

