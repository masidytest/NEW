# 🚂 Railway Deployment - Simple All-in-One

Deploy your entire AI Platform (backend + frontend) to a single Railway service in 5 minutes.

## What You're Deploying

Everything runs from one Railway service:
- ✅ FastAPI backend (API endpoints)
- ✅ Static web UI (HTML/CSS/JS)
- ✅ PostgreSQL database (separate service)
- ✅ Plugin system
- ✅ Per-user agents
- ✅ Automatic HTTPS

## Architecture

```
┌─────────────────────────────────────────┐
│  Railway Project                        │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Single Service                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  FastAPI Backend            │ │ │
│  │  │  - /auth/* endpoints        │ │ │
│  │  │  - /chat, /goals, etc.      │ │ │
│  │  │  - Plugin system            │ │ │
│  │  └─────────────────────────────┘ │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  Static Web UI              │ │ │
│  │  │  - /, /login.html           │ │ │
│  │  │  - /chat.html, /goals.html  │ │ │
│  │  │  - /capabilities.html       │ │ │
│  │  └─────────────────────────────┘ │ │
│  │                                   │ │
│  │  URL: your-app.railway.app       │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  PostgreSQL Database              │ │
│  │  - Auto-injected DATABASE_URL     │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Prerequisites

- GitHub account with your code
- Railway account (free at https://railway.app)

## Deployment Steps

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access GitHub
5. Select your repository
6. Railway auto-detects `Dockerfile` and deploys

### Step 3: Add PostgreSQL

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically injects `DATABASE_URL` into your service

### Step 4: Set Environment Variables

1. Click on your service (not the database)
2. Go to **"Variables"** tab
3. Add these variables:

```bash
SECRET_KEY=<paste-generated-key-here>
ENV=production
```

To generate `SECRET_KEY`:
```bash
openssl rand -hex 32
```

Or use an online generator: https://generate-secret.vercel.app/32

### Step 5: Get Your URL

1. Go to **"Settings"** tab
2. Scroll to **"Domains"**
3. Railway provides a URL like: `https://your-app-production.up.railway.app`
4. Click **"Generate Domain"** if not already generated

### Step 6: Test Your Deployment

Open your Railway URL in a browser:

1. **Test Homepage**: Should show login page
2. **Register**: Create a new account
3. **Dashboard**: Should redirect after registration
4. **Chat**: Test sending messages
5. **Goals**: Create a goal
6. **Capabilities**: View capabilities

## Verification Checklist

- [ ] Railway URL opens and shows login page
- [ ] Can register new account
- [ ] Redirects to dashboard after registration
- [ ] Can navigate to chat, goals, capabilities
- [ ] Chat responds to messages
- [ ] Goals can be created
- [ ] Capabilities show plugins (13+ total)
- [ ] No errors in browser console
- [ ] Logout works

## Troubleshooting

### "Application failed to respond"

**Check Railway logs**:
1. Click on your service
2. Go to **"Deployments"** tab
3. Click latest deployment
4. View logs for errors

**Common fixes**:
- Verify `DATABASE_URL` is injected (check Variables tab)
- Verify `SECRET_KEY` is set
- Check for Python errors in logs

### "Cannot connect to database"

**Solution**:
1. Verify PostgreSQL service is running
2. Check that both services are in the same project
3. Railway auto-injects `DATABASE_URL` - no manual config needed

### "502 Bad Gateway"

**Solution**:
- Wait 1-2 minutes for deployment to complete
- Check logs for startup errors
- Verify Dockerfile builds successfully

### Login doesn't work

**Solution**:
1. Check browser console for errors
2. Verify `SECRET_KEY` is set in Railway
3. Check Railway logs for authentication errors

## What You Get

✅ **Single URL** for everything:
- Homepage: `https://your-app.railway.app/`
- Login: `https://your-app.railway.app/login.html`
- Chat: `https://your-app.railway.app/chat.html`
- API: `https://your-app.railway.app/chat` (POST)

✅ **Automatic HTTPS** - Railway handles SSL certificates

✅ **Auto-scaling** - Scales based on traffic

✅ **Zero configuration** - No nginx, no separate frontend deployment

✅ **One service to manage** - Simpler than multi-service setup

## Cost

### Hobby Plan (Free)
- $5 free credit/month
- Good for testing and small projects
- ~500 hours of uptime

### Pro Plan ($20/month)
- $20 credit included
- Production-ready
- Estimated cost: $10-20/month
  - Single service: ~$8-12
  - PostgreSQL: ~$5-8

## Updating Your Deployment

After making code changes:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Railway automatically:
1. Detects the push
2. Rebuilds the Docker image
3. Deploys the new version
4. Zero downtime deployment

## Custom Domain (Optional)

### Add Your Domain

1. In Railway service → **"Settings"** → **"Domains"**
2. Click **"Custom Domain"**
3. Enter: `app.yourdomain.com`
4. Add CNAME record in your DNS:
   ```
   CNAME app.yourdomain.com → your-app.railway.app
   ```
5. Railway automatically provisions SSL

## Monitoring

### View Logs

1. Click on your service
2. Go to **"Deployments"** tab
3. Click latest deployment
4. Real-time logs appear

### Monitor Resources

Railway dashboard shows:
- CPU usage
- Memory usage
- Network traffic
- Request count

## Next Steps

### 1. Add Real Plugins

Create new files in `plugins/` folder:

```python
# plugins/openai_plugin.py
import os
from openai import OpenAI

def register(cap_registry):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def gpt4_query(prompt: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    cap_registry.register(
        name="gpt4",
        func=gpt4_query,
        tags=["llm", "openai"],
        input_schema={"prompt": "str"},
        output_schema={"response": "str"},
        description="Query GPT-4"
    )
```

Add API key to Railway variables:
```bash
OPENAI_API_KEY=sk-...
```

### 2. Enhance Features

- Email verification
- Password reset
- User profiles
- Usage analytics
- Rate limiting

### 3. Scale Up

- Upgrade Railway plan
- Add Redis for caching
- Implement background workers
- Add monitoring/alerts

## Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app

## Success!

Your AI Platform is now live at:
```
https://your-app.railway.app
```

Share it with users, test it thoroughly, and start building amazing AI experiences! 🚀

---

**Deployment Type**: All-in-One (Backend + Frontend)
**Services**: 2 (App + PostgreSQL)
**Estimated Time**: 5-10 minutes
**Estimated Cost**: $10-20/month (Pro plan)
**Complexity**: ⭐ Simple

