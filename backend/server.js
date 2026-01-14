require('dotenv').config();
const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// Database connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from the dist directory
app.use(express.static(path.join(__dirname, '../dist')));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', message: 'Backend API is running' });
});

// Initialize database table (run this once)
async function initializeDatabase() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS student_responses (
        id SERIAL PRIMARY KEY,
        page_title VARCHAR(255) NOT NULL,
        section_title VARCHAR(255) NOT NULL,
        section_index INTEGER NOT NULL,
        response_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    console.log('Database table initialized successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
  }
}

// Save student response endpoint
app.post('/api/responses', async (req, res) => {
  const { pageTitle, sectionTitle, sectionIndex, responseText } = req.body;

  // Validate required fields
  if (!pageTitle || !sectionTitle || sectionIndex === undefined || !responseText) {
    return res.status(400).json({
      error: 'Missing required fields: pageTitle, sectionTitle, sectionIndex, responseText'
    });
  }

  try {
    const result = await pool.query(
      `INSERT INTO student_responses (page_title, section_title, section_index, response_text)
       VALUES ($1, $2, $3, $4)
       RETURNING id, created_at;`,
      [pageTitle, sectionTitle, sectionIndex, responseText]
    );

    res.status(201).json({
      success: true,
      id: result.rows[0].id,
      message: 'Response saved successfully',
      timestamp: result.rows[0].created_at
    });
  } catch (error) {
    console.error('Error saving response:', error);
    res.status(500).json({
      error: 'Failed to save response',
      message: error.message
    });
  }
});

// Get all responses (optional - for admin/viewing)
app.get('/api/responses', async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT * FROM student_responses ORDER BY created_at DESC;`
    );
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching responses:', error);
    res.status(500).json({ error: 'Failed to fetch responses' });
  }
});

// Get responses for a specific page
app.get('/api/responses/:pageTitle', async (req, res) => {
  const { pageTitle } = req.params;

  try {
    const result = await pool.query(
      `SELECT * FROM student_responses WHERE page_title = $1 ORDER BY created_at DESC;`,
      [pageTitle]
    );
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching responses:', error);
    res.status(500).json({ error: 'Failed to fetch responses' });
  }
});

// Catch-all route to serve index.html for client-side routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../dist/index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
  console.log(`Serving static files from: ${path.join(__dirname, '../dist')}`);
  initializeDatabase();
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  pool.end();
  process.exit(0);
});
