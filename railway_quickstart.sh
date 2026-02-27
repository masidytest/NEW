#!/bin/bash
# Quick start script for Railway deployment

echo "🚂 Railway Deployment Quick Start"
echo "=================================="
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI not found. Installing..."
    echo ""
    echo "Run one of these commands:"
    echo "  npm install -g @railway/cli"
    echo "  brew install railway"
    echo "  curl -fsSL https://railway.app/install.sh | sh"
    echo ""
    exit 1
fi

echo "✅ Railway CLI found"
echo ""

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Not logged in to Railway. Logging in..."
    railway login
else
    echo "✅ Already logged in to Railway"
fi

echo ""
echo "📋 Pre-deployment checklist:"
echo ""

# Check for required files
files=("Dockerfile" "railway.json" "requirements.txt" "app_multiuser.py" "db.py")
all_present=true

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
        all_present=false
    fi
done

echo ""

if [ "$all_present" = false ]; then
    echo "❌ Some required files are missing. Please ensure all files are present."
    exit 1
fi

echo "✅ All required files present"
echo ""

# Generate SECRET_KEY if not exists
if [ ! -f ".env" ]; then
    echo "🔑 Generating SECRET_KEY..."
    SECRET_KEY=$(openssl rand -hex 32)
    echo "SECRET_KEY=$SECRET_KEY" > .env
    echo "ENV=production" >> .env
    echo "✅ Created .env file with SECRET_KEY"
    echo ""
else
    echo "ℹ️  .env file already exists"
    echo ""
fi

echo "🚀 Ready to deploy!"
echo ""
echo "Next steps:"
echo ""
echo "1. Initialize Railway project:"
echo "   railway init"
echo ""
echo "2. Add PostgreSQL database:"
echo "   railway add --database postgresql"
echo ""
echo "3. Set environment variables:"
echo "   railway variables set SECRET_KEY=\$(openssl rand -hex 32)"
echo "   railway variables set ENV=production"
echo ""
echo "4. Deploy:"
echo "   railway up"
echo ""
echo "5. Get your deployment URL:"
echo "   railway domain"
echo ""
echo "6. Update web files with backend URL:"
echo "   python update_api_url.py https://your-backend.railway.app"
echo ""
echo "For detailed instructions, see RAILWAY_DEPLOYMENT.md"
echo ""
