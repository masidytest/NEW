# 🚀 Deploy to Railway NOW - Quick Guide

Your AI Platform is ready to deploy. Everything (backend + frontend) goes to Railway in one service.

## ⚡ 5-Minute Deployment

### 1. Push to GitHub (1 min)

```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

### 2. Deploy on Railway (2 min)

1. Go to https://railway.app
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-deploys

### 3. Add Database (1 min)

1. Click **"+ New"** → **"Database"** → **"PostgreSQL"**
2. Done! `DATABASE_URL` auto-injected

### 4. Set Secret Key (1 min)

1. Click your service → **"Variables"**
2. Add:
   ```
   SECRET_KEY = (generate with: openssl rand -hex 32)
   ENV = production
   ```

### 5. Get Your URL (instant)

1. Go to **"Settings"** → **"Domains"**
2. Copy your URL: `https://your-app.railway.app`

## ✅ Test It

Open `https://your-app.railway.app`:
- Should show login page
- Register new account
- Test chat, goals, capabilities

## 📁 What Changed for Railway

### New Files Created:
- ✅ `serve_static.py` - Unified server (API + UI)
- ✅ `railway.json` - Railway config
- ✅ `Dockerfile` - Container config
- ✅ `.env.example` - Environment template

### Files Updated:
- ✅ `db.py` - PostgreSQL support
- ✅ `requirements.txt` - Added psycopg2-binary
- ✅ All `web/*.html` - Use `window.location.origin` for API URL

### Key Changes:
1. **Single Service**: Everything runs from one Railway service
2. **Same Origin**: Frontend and backend on same domain (no CORS issues)
3. **Auto HTTPS**: Railway handles SSL certificates
4. **PostgreSQL**: Replaces SQLite for production

## 🏗️ Architecture

```
https://your-app.railway.app
├── /                    → Login page
├── /chat.html           → Chat interface
├── /goals.html          → Goals management
├── /capabilities.html   → Capabilities browser
├── /auth/register       → API: Register
├── /auth/token          → API: Login
├── /chat                → API: Chat
├── /goals               → API: Goals
└── /capabilities        → API: Capabilities
```

## 💰 Cost

**Hobby Plan** (Free):
- $5 credit/month
- Good for testing

**Pro Plan** ($20/month):
- $20 credit included
- Production-ready
- ~$10-20/month total cost

## 🔧 Troubleshooting

### Application won't start
- Check Railway logs for errors
- Verify `DATABASE_URL` and `SECRET_KEY` are set

### Can't login
- Check browser console for errors
- Verify `SECRET_KEY` is set in Railway

### 502 Error
- Wait 1-2 minutes for deployment
- Check logs for startup errors

## 📚 Documentation

- **Simple Guide**: `RAILWAY_SIMPLE_DEPLOY.md`
- **Detailed Guide**: `RAILWAY_DEPLOYMENT.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`

## 🎯 Next Steps After Deployment

1. **Test everything**:
   - Register account
   - Send chat messages
   - Create goals
   - View capabilities

2. **Add custom domain** (optional):
   - Settings → Domains → Custom Domain
   - Add CNAME: `app.yourdomain.com`

3. **Add real plugins**:
   - OpenAI integration
   - Weather API
   - Web search

4. **Monitor**:
   - Check Railway logs
   - Monitor resource usage
   - Track errors

## ✨ What You Get

✅ **Live AI Platform** at `https://your-app.railway.app`
✅ **Automatic HTTPS** - Secure by default
✅ **Auto-scaling** - Handles traffic spikes
✅ **PostgreSQL** - Production database
✅ **Plugin system** - 13+ capabilities
✅ **Multi-user** - JWT authentication
✅ **Per-user agents** - Isolated memory
✅ **Zero downtime** - Auto-deploy on push

## 🚀 Ready?

```bash
# 1. Commit everything
git add .
git commit -m "Deploy to Railway"
git push

# 2. Go to Railway
open https://railway.app

# 3. Deploy from GitHub
# (Click through the UI)

# 4. Done!
```

Your AI Platform will be live in 5 minutes! 🎉

---

**Status**: ✅ Ready to Deploy
**Complexity**: ⭐ Simple (All-in-One)
**Time**: 5-10 minutes
**Cost**: $10-20/month

**Deploy now and share your live AI platform with the world!**

