# API Connection Fix - Deployment Instructions

## Problem Fixed

The frontend was trying to connect to `http://localhost:3001` even in production. This is because the `.env.production` file had a placeholder URL.

## Solution Applied

Updated `.env.production` to use the correct Heroku backend URL:

```dotenv
VITE_API_URL=https://tailia-malloy.herokuapp.com
```

## Environment Configuration

### Local Development (`.env.development`)
```dotenv
VITE_API_URL=http://localhost:3001
```
Used when running `npm run dev`

### Production (`.env.production`)
```dotenv
VITE_API_URL=https://tailia-malloy.herokuapp.com
```
Used when running `npm run build` for production

## How It Works

The Vue components check for the API URL in this order:

1. **window.__API_URL__** - Set dynamically if needed
2. **import.meta.env.VITE_API_URL** - From environment files (.env.production or .env.development)
3. **http://localhost:3001** - Fallback for local development

## Deployment Steps

To deploy with the fix:

```bash
# 1. Make sure changes are committed
git status

# 2. Rebuild the production build
npm run build

# 3. Deploy to Heroku
git push heroku main

# 4. Or if deploying to GitHub Pages/Netlify, the build will use .env.production
```

## Verification

After deployment, the console should no longer show:
```
POST http://localhost:3001/api/interactive-submissions net::ERR_CONNECTION_REFUSED
```

Instead, it should show successful requests to:
```
POST https://tailia-malloy.herokuapp.com/api/interactive-submissions
```

## Testing Locally

To test the production build locally:

```bash
# Build production version (uses .env.production)
npm run build

# Preview production build
npm run preview

# Or manually test with curl
curl -X POST https://tailia-malloy.herokuapp.com/api/responses \
  -H "Content-Type: application/json" \
  -d '{"pageTitle":"Test","sectionTitle":"Test","sectionIndex":0,"responseText":"test"}'
```

## Troubleshooting

If you get `CORS` errors after fixing this:
- The backend (server.js) should have CORS enabled, which it does via `app.use(cors())`
- Verify the backend is running: `heroku logs --tail --app tailia-malloy`

If you get connection errors:
- Check backend is deployed: `heroku ps --app tailia-malloy`
- Check backend health: `curl https://tailia-malloy.herokuapp.com/health`

## Files Changed

- `.env.production` - Updated VITE_API_URL to actual Heroku app URL
