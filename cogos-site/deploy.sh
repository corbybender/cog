#!/bin/bash

echo "🚀 Deploying CogOS Site to Vercel..."
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "✅ Vercel CLI ready"
echo ""
echo "🔐 Logging into Vercel..."
echo "A browser window will open. Please log in to your Vercel account."
echo ""

# Login to Vercel
vercel login

echo ""
echo "🌐 Deploying site..."
echo ""

# Deploy to Vercel
vercel --yes

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your site is now live. Check the URL above to view it."
echo ""
echo "To add a custom domain or manage your site, visit:"
echo "https://vercel.com/dashboard"
echo ""
echo "To update your site, simply edit index.html and run:"
echo "  vercel --prod"
