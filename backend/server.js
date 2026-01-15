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
  ssl: true,
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
  // Skip database initialization if no DATABASE_URL is set (local development)
  if (!process.env.DATABASE_URL) {
    console.log('⚠️  DATABASE_URL not set. Running in offline mode - API endpoints will not work.');
    console.log('   To enable database: set DATABASE_URL environment variable');
    return;
  }

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
    await pool.query(`
      CREATE TABLE IF NOT EXISTS interactive_submissions (
        id SERIAL PRIMARY KEY,
        page_title VARCHAR(255) NOT NULL,
        section_title VARCHAR(255) NOT NULL,
        section_index INTEGER NOT NULL,
        original_text TEXT NOT NULL,
        updated_text TEXT NOT NULL,
        submission_type VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    console.log('✓ Database tables initialized successfully');
  } catch (error) {
    console.error('✗ Error initializing database:', error.message);
    console.log('  API endpoints will not work without a database connection.');
    console.log('  Ensure DATABASE_URL is set and PostgreSQL is running.');
  }
}

// Save student response endpoint
app.post('/api/responses', async (req, res) => {
  const { pageTitle, sectionTitle, sectionIndex, responseText } = req.body;

  // Check if database is available
  if (!process.env.DATABASE_URL) {
    return res.status(503).json({
      error: 'Database not available',
      message: 'DATABASE_URL environment variable not set'
    });
  }

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

// Save interactive submission endpoint (e.g., updated sentences)
app.post('/api/interactive-submissions', async (req, res) => {
  const { pageTitle, sectionTitle, sectionIndex, originalText, updatedText, submissionType } = req.body;

  // Check if database is available
  if (!process.env.DATABASE_URL) {
    return res.status(503).json({
      error: 'Database not available',
      message: 'DATABASE_URL environment variable not set'
    });
  }

  // Validate required fields
  if (!pageTitle || !sectionTitle || sectionIndex === undefined || !originalText || !updatedText || !submissionType) {
    return res.status(400).json({
      error: 'Missing required fields: pageTitle, sectionTitle, sectionIndex, originalText, updatedText, submissionType'
    });
  }

  try {
    const result = await pool.query(
      `INSERT INTO interactive_submissions (page_title, section_title, section_index, original_text, updated_text, submission_type)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING id, created_at;`,
      [pageTitle, sectionTitle, sectionIndex, originalText, updatedText, submissionType]
    );

    res.status(201).json({
      success: true,
      id: result.rows[0].id,
      message: 'Interactive submission saved successfully',
      timestamp: result.rows[0].created_at
    });
  } catch (error) {
    console.error('Error saving interactive submission:', error);
    res.status(500).json({
      error: 'Failed to save interactive submission',
      message: error.message
    });
  }
});

// Get interactive submissions endpoint
app.get('/api/interactive-submissions', async (req, res) => {
  if (!process.env.DATABASE_URL) {
    return res.status(503).json({
      error: 'Database not available',
      message: 'DATABASE_URL environment variable not set'
    });
  }

  try {
    const result = await pool.query(
      'SELECT * FROM interactive_submissions ORDER BY created_at DESC;'
    );
    res.json({
      success: true,
      submissions: result.rows,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Error retrieving interactive submissions:', error);
    res.status(500).json({
      error: 'Failed to retrieve interactive submissions',
      message: error.message
    });
  }
});

// Get interactive submissions by page
app.get('/api/interactive-submissions/:pageTitle', async (req, res) => {
  const { pageTitle } = req.params;

  if (!process.env.DATABASE_URL) {
    return res.status(503).json({
      error: 'Database not available',
      message: 'DATABASE_URL environment variable not set'
    });
  }

  try {
    const result = await pool.query(
      'SELECT * FROM interactive_submissions WHERE page_title = $1 ORDER BY created_at DESC;',
      [pageTitle]
    );
    res.json({
      success: true,
      submissions: result.rows,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Error retrieving interactive submissions:', error);
    res.status(500).json({
      error: 'Failed to retrieve interactive submissions',
      message: error.message
    });
  }
});

// Get all responses (optional - for admin/viewing)
app.get('/api/responses', async (req, res) => {
  if (!process.env.DATABASE_URL) {
    return res.status(503).json({
      error: 'Database not available',
      message: 'DATABASE_URL environment variable not set'
    });
  }

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

  if (!process.env.DATABASE_URL) {
    return res.status(503).json({
      error: 'Database not available',
      message: 'DATABASE_URL environment variable not set'
    });
  }

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
