# Database Download & Analysis Scripts

Python scripts for exporting data from the PostgreSQL database and analyzing student responses and interactive submissions.

## Requirements

Install the required Python packages:

```bash
pip install pandas psycopg2-binary python-dotenv
```

## Scripts

### 1. `download_database.py`

Downloads the remote PostgreSQL database tables and exports them as CSV files. Also loads the data into pandas DataFrames for immediate use.

**Usage:**

```bash
python download_database.py
```

**What it does:**
- Connects to the PostgreSQL database using `DATABASE_URL` from `.env`
- Exports `student_responses` table to `data/student_responses_YYYYMMDD_HHMMSS.csv`
- Exports `interactive_submissions` table to `data/interactive_submissions_YYYYMMDD_HHMMSS.csv`
- Displays summary statistics

**Output:**
- CSV files in `backend/data/` directory with timestamps
- Console summary showing row counts and sample data

### 2. `analyze_data.py`

Advanced analysis tool for exploring the collected data. Can load from database or CSV files.

**Usage:**

```bash
python analyze_data.py
```

**What it does:**
- Loads data from PostgreSQL (or CSV if database unavailable)
- Generates summary statistics for responses and submissions
- Shows response counts, text lengths, and submission types
- Exports detailed analysis to `analysis_report.txt`

**Features:**
- Response summary by page and section
- Interactive submission analysis by type
- Text change statistics (original length → updated length)
- Exportable text report

## Setup

1. Ensure your `.env` file has the `DATABASE_URL` set:

```env
DATABASE_URL=postgres://user:password@host:port/database
```

2. Create the `data/` directory (scripts will create it automatically)

## Python Usage in Notebooks

Use these scripts to load data into your own Python analysis:

```python
import pandas as pd
from pathlib import Path

# Load latest CSV files
data_dir = Path('backend/data')
responses = pd.read_csv(sorted(data_dir.glob('student_responses_*.csv'))[-1])
submissions = pd.read_csv(sorted(data_dir.glob('interactive_submissions_*.csv'))[-1])

# Or use the analyzer class
from analyze_data import DataAnalyzer

analyzer = DataAnalyzer()
analyzer.load_from_database()
analyzer.responses_summary()
analyzer.submissions_summary()
```

## Database Schema

### `student_responses` table
- `id`: Primary key
- `page_title`: Title of the page
- `section_title`: Title of the section
- `section_index`: 0-based section number
- `response_text`: Student's written response
- `completionToken`: Unique session identifier
- `created_at`: Timestamp of response
- `updated_at`: Timestamp of last update

### `interactive_submissions` table
- `id`: Primary key
- `page_title`: Title of the page
- `section_title`: Title of the section
- `section_index`: 0-based section number
- `original_text`: Original text before update
- `updated_text`: Updated text after submission
- `submission_type`: Type of submission (e.g., "sentence_update", "pair_update")
- `completionToken`: Unique session identifier
- `created_at`: Timestamp of submission

## Troubleshooting

**"DATABASE_URL not set"**
- Ensure your `.env` file exists and has `DATABASE_URL` defined
- On Heroku: Run `heroku config:get DATABASE_URL`

**"Connection refused"**
- Check your PostgreSQL server is running
- Verify DATABASE_URL is correct
- On Heroku: The connection string should work automatically

**"psycopg2 not found"**
- Install with: `pip install psycopg2-binary`
