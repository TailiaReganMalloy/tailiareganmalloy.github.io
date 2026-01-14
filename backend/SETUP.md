# Backend API Setup Guide

This backend API collects student responses from the interactive pages and stores them in a Heroku Postgres database.

## Local Development Setup

### 1. Install Dependencies
```bash
cd backend
npm install
```

### 2. Create `.env` file
Copy `.env.example` to `.env` and update with your local database credentials:
```
DATABASE_URL=postgresql://user:password@localhost:5432/responses_db
NODE_ENV=development
PORT=3001
```

### 3. Run Locally
```bash
npm run dev
```

The API will start on `http://localhost:3001`

### 4. Test the API
```bash
# Health check
curl http://localhost:3001/health

# Save a test response
curl -X POST http://localhost:3001/api/responses \
  -H "Content-Type: application/json" \
  -d '{
    "pageTitle": "What Have Language Models Learned?",
    "sectionTitle": "Introduction",
    "sectionIndex": 0,
    "responseText": "Test response"
  }'

# Get all responses
curl http://localhost:3001/api/responses
```

## Deployment to Heroku

### 1. Create Heroku App
```bash
heroku create your-app-name
```

### 2. Add Postgres Database
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

This automatically sets the `DATABASE_URL` environment variable.

### 3. Configure Frontend
Update your frontend environment variables in the appropriate `.env` file:

For development: `.env.development` or `.env.local`
```
VITE_API_URL=http://localhost:3001
```

For production: `.env.production`
```
VITE_API_URL=https://your-heroku-app-name.herokuapp.com
```

### 4. Deploy to Heroku
```bash
# From the root directory
cd backend
git push heroku main
```

Or if your backend is in a subdirectory, use:
```bash
git push heroku `git subtree split --prefix backend main`:main
```

### 5. Initialize Database
The database table is automatically created on the first API call. To verify:
```bash
heroku logs --tail
```

## API Endpoints

### POST /api/responses
Save a student response
```json
{
  "pageTitle": "What Have Language Models Learned?",
  "sectionTitle": "Introduction",
  "sectionIndex": 0,
  "responseText": "User's response text"
}
```

**Response:**
```json
{
  "success": true,
  "id": 1,
  "message": "Response saved successfully",
  "timestamp": "2026-01-14T10:30:00.000Z"
}
```

### GET /api/responses
Get all responses from all pages

### GET /api/responses/:pageTitle
Get all responses from a specific page

## Database Schema

```sql
CREATE TABLE student_responses (
  id SERIAL PRIMARY KEY,
  page_title VARCHAR(255) NOT NULL,
  section_title VARCHAR(255) NOT NULL,
  section_index INTEGER NOT NULL,
  response_text TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Frontend Integration

The Vue components automatically send responses when the user clicks "Continue". The API URL is read from the environment variable `VITE_API_URL`:

```javascript
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3001';

// Response is sent automatically in nextSection()
```

## Troubleshooting

**CORS Issues?**
- The backend has CORS enabled for all origins
- Make sure the API URL in your frontend environment matches your deployed Heroku app

**Database Connection Issues?**
- Check `heroku logs --tail` for detailed error messages
- Verify `DATABASE_URL` is set: `heroku config`

**Responses Not Being Saved?**
- Check browser console for network errors
- Check `heroku logs --tail` on the backend
- Ensure the API endpoint is correctly set in your frontend `.env` file
