# CogOS Website

Modern landing page for CogOS - Multi-Agent Cognitive System for AI.

## 🚀 Quick Start

### Deploy to Vercel (Free)

```bash
# Option 1: Use the deploy script
./deploy.sh

# Option 2: Manual deployment
vercel login
vercel --yes
```

### Or Drag & Drop

1. Go to [vercel.com/new](https://vercel.com/new)
2. Drag this folder onto the page
3. Click "Deploy"

## 📁 Structure

```
cogos-site/
├── index.html      # Main landing page
├── styles.css      # Modern dark theme styles
├── vercel.json     # Vercel configuration
├── deploy.sh       # One-command deploy script
├── DEPLOY.md       # Detailed deployment guide
└── README.md       # This file
```

## 🎨 Features

- Modern dark theme design
- Fully responsive (mobile-first)
- Gradient accents and animations
- Comparison table (CogOS vs LLMs)
- Feature cards with hover effects
- Stats section
- Installation command copy-ready
- Call-to-action buttons

## 📝 Customization

### Change Colors

Edit `styles.css`:
```css
:root {
    --primary: #6366f1;      /* Main brand color */
    --secondary: #10b981;    /* Accent color */
    --bg: #0f172a;           /* Background */
}
```

### Edit Content

Edit `index.html` to update:
- Headlines and descriptions
- Feature cards
- Module lists
- Installation commands
- Links to GitHub/docs

### Add Pages

1. Create new HTML files (e.g., `docs.html`)
2. Add navigation links in `index.html`
3. Deploy with `vercel --prod`

## 🔗 Links

- **Live Site:** [cogos.vercel.app](https://cogos.vercel.app) (after deployment)
- **GitHub:** [github.com/corbybender/cog](https://github.com/corbybender/cog)
- **Vercel Dashboard:** [vercel.com/dashboard](https://vercel.com/dashboard)

## 💡 Tips

- All features are **100% free** on Vercel
- Custom domains work free (just add in Vercel dashboard)
- Auto-deploys from GitHub if you connect your repo
- Preview deployments for every pull request
- Analytics included

## 📊 What's Included

✅ 24+ expert modules showcase
✅ Multi-agent intelligence explanation
✅ Comparison with single-pass LLMs
✅ Installation instructions
✅ GitHub links
✅ Mobile-responsive design
✅ Modern gradient design
✅ Fast loading (static HTML/CSS)

## 🚦 Next Steps

1. **Deploy to Vercel** - Run `./deploy.sh`
2. **Add custom domain** - Configure in Vercel dashboard
3. **Connect GitHub** - Enable auto-deploys on push
4. **Add analytics** - Vercel Analytics is free
5. **Expand content** - Add docs, blog, examples

---

Built with ❤️ for the CogOS project
