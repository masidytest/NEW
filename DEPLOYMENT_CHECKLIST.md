# 🚀 Railway Deployment Checklist

Use this checklist to ensure a smooth deployment to Railway.

## Pre-Deployment

### Code Preparation
- [ ] All code committed to GitHub
- [ ] `Dockerfile` present and tested locally
- [ ] `railway.json` configuration file present
- [ ] `requirements.txt` includes `psycopg2-binary`
- [ ] `db.py` updated to support PostgreSQL
- [ ] `app_multiuser.py` uses environment variables for CORS

### Environment Variables Prepared
- [ ] Generate SECRET_KEY: `openssl rand -hex 32`
- [ ] Note down your GitHub repository URL
- [ ] Have Railway account ready (https://railway.app)

## Backend Deployment

### Railway Setup
- [ ] Created Railway account
- [ ] Created new project from GitHub repo
- [ ] Railway detected Dockerfile automatically
- [ ] Service name set to `ai-platform-backend`

### Database Setup
- [ ] Added PostgreSQL database to project
- [ ] Verified `DATABASE_URL` is auto-injected
- [ ] Database tables created on first run

### Environment Variables Set
- [ ] `SECRET_KEY` = (your generated key)
- [ ] `ENV` = production
- [ ] `ALLOWED_ORIGINS` = (will update after frontend deployment)

### Backend Testing
- [ ] Backend deployed successfully
- [ ] Got Railway backend URL (e.g., `https://xxx.railway.app`)
- [ ] Test root endpoint: `curl https://your-backend.railway.app/`
- [ ] Test registration endpoint
- [ ] Test login endpoint
- [ ] Check logs for errors

## Frontend Deployment

### Update Web Files
- [ ] Run: `python update_api_url.py https://your-backend.railway.app`
- [ ] Verify all web files updated with Railway URL
- [ ] Commit and push changes to GitHub

### Deploy Frontend
- [ ] Created new Railway service for frontend
- [ ] Set root directory to `web`
- [ ] Frontend deployed successfully
- [ ] Got Railway frontend URL (e.g., `https://yyy.railway.app`)

### Update CORS
- [ ] Updated backend `ALLOWED_ORIGINS` with frontend URL
- [ ] Redeployed backend service
- [ ] Verified CORS working (no errors in browser console)

## Integration Testing

### Authentication Flow
- [ ] Open frontend URL in browser
- [ ] Register new account
- [ ] Redirects to dashboard after registration
- [ ] Can see user email and logout button
- [ ] Logout works and redirects to login
- [ ] Login with existing account works

### Feature Testing
- [ ] Chat page loads and works
- [ ] Can send messages and get AI responses
- [ ] Goals page loads and works
- [ ] Can create new goals
- [ ] Goals persist after page refresh
- [ ] Capabilities page loads and works
- [ ] Shows all capabilities including plugins

### API Testing
- [ ] All API requests include Authorization header
- [ ] 401 errors trigger logout and redirect
- [ ] No CORS errors in browser console
- [ ] Backend logs show successful requests

### Plugin System
- [ ] Backend logs show plugins loaded on startup
- [ ] Capabilities endpoint shows 13+ capabilities
- [ ] Math plugin works (test: "What's 5 doubled?")

## Production Readiness

### Security
- [ ] SECRET_KEY is secure random value (not default)
- [ ] ALLOWED_ORIGINS set to specific domains (not "*")
- [ ] HTTPS enabled on both frontend and backend
- [ ] Database credentials secure (managed by Railway)

### Performance
- [ ] Backend responds within 2 seconds
- [ ] Frontend loads within 3 seconds
- [ ] No memory leaks in logs
- [ ] Database connections properly pooled

### Monitoring
- [ ] Can access Railway logs
- [ ] No errors in backend logs
- [ ] No errors in frontend console
- [ ] Health endpoint returns 200

## Optional Enhancements

### Custom Domain
- [ ] Added custom domain to backend (api.yourdomain.com)
- [ ] Added custom domain to frontend (app.yourdomain.com)
- [ ] DNS records configured
- [ ] SSL certificates provisioned
- [ ] Updated ALLOWED_ORIGINS with custom domain
- [ ] Updated API_URL in frontend with custom domain

### Monitoring & Alerts
- [ ] Set up error alerts
- [ ] Set up uptime monitoring
- [ ] Configured log retention
- [ ] Set up performance monitoring

### Backups
- [ ] Database backups enabled (Railway Pro)
- [ ] Backup schedule configured
- [ ] Tested backup restoration

## Post-Deployment

### Documentation
- [ ] Updated README with live URLs
- [ ] Documented environment variables
- [ ] Created user guide
- [ ] Documented API endpoints

### Communication
- [ ] Announced launch to users
- [ ] Shared live URLs
- [ ] Provided support contact
- [ ] Created feedback channel

### Maintenance Plan
- [ ] Scheduled regular updates
- [ ] Monitoring plan in place
- [ ] Backup verification schedule
- [ ] Incident response plan

## Troubleshooting Reference

### Common Issues

**Backend won't start**
- Check logs for errors
- Verify all environment variables set
- Check DATABASE_URL is injected
- Verify Dockerfile builds locally

**CORS errors**
- Update ALLOWED_ORIGINS
- Redeploy backend
- Clear browser cache
- Check frontend uses correct API_URL

**Database connection failed**
- Verify PostgreSQL plugin added
- Check DATABASE_URL in logs
- Verify db.py handles postgres:// → postgresql://
- Check connection pooling settings

**Frontend shows old API URL**
- Run update_api_url.py script
- Commit and push changes
- Wait for Railway auto-deploy
- Clear browser cache

**Authentication not working**
- Check SECRET_KEY is set
- Verify JWT token in localStorage
- Check Authorization header in requests
- Verify backend /auth endpoints work

## Success Criteria

Your deployment is successful when:

✅ Backend is accessible via HTTPS
✅ Frontend is accessible via HTTPS
✅ Users can register and login
✅ All pages work with authentication
✅ Chat responds to messages
✅ Goals can be created and viewed
✅ Capabilities show plugins loaded
✅ No errors in logs or console
✅ Performance is acceptable
✅ CORS is properly configured

## Next Steps After Deployment

1. **Monitor for 24 hours**
   - Check logs regularly
   - Monitor error rates
   - Track response times

2. **Gather feedback**
   - Test with real users
   - Collect bug reports
   - Note feature requests

3. **Plan improvements**
   - Add real API integrations
   - Implement new plugins
   - Enhance UI/UX
   - Add analytics

4. **Scale as needed**
   - Upgrade Railway plan if needed
   - Add more resources
   - Implement caching
   - Optimize database queries

---

**Deployment Date**: _____________
**Backend URL**: _____________
**Frontend URL**: _____________
**Database**: Railway PostgreSQL
**Status**: ☐ In Progress  ☐ Complete  ☐ Live

