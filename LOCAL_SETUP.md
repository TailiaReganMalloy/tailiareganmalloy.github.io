# Local Development Setup

## Prerequisites
- Docker and Docker Compose installed
- Node.js and pnpm installed
- PostgreSQL port 5432 available

## Running Locally

### 1. Start PostgreSQL Database
```bash
docker-compose up -d
```

This will:
- Pull the PostgreSQL 15 Alpine image
- Create a container named `tailia-postgres`
- Initialize the database with credentials from `.env`
- Expose PostgreSQL on `localhost:5432`

### 2. Install Dependencies
```bash
pnpm install
cd backend && npm install && cd ..
```

### 3. Build Frontend
```bash
pnpm build
```

### 4. Start Backend Server
```bash
npm run start
```

The server will:
- Listen on `http://localhost:3001`
- Serve the frontend from `/dist`
- Connect to PostgreSQL using `DATABASE_URL` from `.env`
- Create tables automatically on startup

### 5. Access the Application
Open `http://localhost:3001` in your browser

## Database Management

### View PostgreSQL Logs
```bash
docker-compose logs postgres
```

### Connect to Database
```bash
docker-compose exec postgres psql -U postgres -d tailia_db
```

### Query Responses
```sql
SELECT * FROM student_responses;
SELECT * FROM interactive_submissions;
```

### Stop Database
```bash
docker-compose down
```

### Stop and Remove Data
```bash
docker-compose down -v
```

## Environment Variables

The `.env` file contains:
- `DATABASE_URL`: PostgreSQL connection string for local development

Format: `postgresql://user:password@host:port/database`

## Troubleshooting

### Port 5432 Already in Use
If PostgreSQL is already running:
```bash
# Stop existing PostgreSQL
brew services stop postgresql
# Or change the port in docker-compose.yml
```

### Connection Refused
Wait a few seconds for PostgreSQL to be ready, or check:
```bash
docker-compose ps
```

### Reset Database
```bash
docker-compose down -v
docker-compose up -d
npm run start
```
