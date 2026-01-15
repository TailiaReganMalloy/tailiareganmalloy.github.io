# Python Database Scripts

This directory contains Python scripts for downloading and analyzing your educational experiment data from PostgreSQL.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install pandas psycopg2-binary python-dotenv
```

### 2. Set Your Database URL

Make sure your `.env` file contains your DATABASE_URL. On Heroku, you can get it with:

```bash
heroku config:get DATABASE_URL --app tailia-malloy
```

### 3. Run the Scripts

**Option A: Quick download and analyze**
```bash
python quick_start.py
```

**Option B: Just download data**
```bash
python download_database.py
```

**Option C: Detailed analysis**
```bash
python analyze_data.py
```

## 📋 Available Scripts

### `download_database.py`

Downloads database tables as CSV files and loads them into pandas DataFrames.

```bash
python download_database.py
```

**Creates:**
- `data/student_responses_YYYYMMDD_HHMMSS.csv` - All student responses
- `data/interactive_submissions_YYYYMMDD_HHMMSS.csv` - All interactive submissions

**Outputs:**
- Row counts and summary statistics
- Sample data preview

### `analyze_data.py`

Advanced analysis tool with detailed statistics and reporting.

```bash
python analyze_data.py
```

**Outputs:**
- Summary statistics for responses and submissions
- Submission type breakdown
- Text change analysis
- `analysis_report.txt` with full dataset

### `quick_start.py`

Combined download and analysis in one script. Best for getting started.

```bash
python quick_start.py
```

## 🐍 Use in Python Code

### Direct Import

```python
from download_database import download_database_to_csv

responses_df, submissions_df = download_database_to_csv()

# Now you have pandas DataFrames
print(responses_df.head())
print(submissions_df.info())
```

### Using the Analyzer Class

```python
from analyze_data import DataAnalyzer

analyzer = DataAnalyzer()
analyzer.load_from_database()

# Get DataFrames
responses = analyzer.responses_df
submissions = analyzer.submissions_df

# Generate analysis
analyzer.responses_summary()
analyzer.submissions_summary()
analyzer.export_analysis('my_report.txt')
```

### Load from CSV Files

```python
import pandas as pd
from pathlib import Path

data_dir = Path('data')

# Find the latest CSV files
responses = pd.read_csv(sorted(data_dir.glob('student_responses_*.csv'))[-1])
submissions = pd.read_csv(sorted(data_dir.glob('interactive_submissions_*.csv'))[-1])
```

## 📊 Data Schema

### `student_responses` Table
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| page_title | VARCHAR | Name of the experiment page |
| section_title | VARCHAR | Section heading |
| section_index | INTEGER | 0-based section number |
| response_text | TEXT | Student's written response |
| completionToken | VARCHAR | Unique session identifier |
| created_at | TIMESTAMP | When response was created |
| updated_at | TIMESTAMP | Last update time |

### `interactive_submissions` Table
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| page_title | VARCHAR | Name of the experiment page |
| section_title | VARCHAR | Section heading |
| section_index | INTEGER | 0-based section number |
| original_text | TEXT | Original text before update |
| updated_text | TEXT | Updated text from submission |
| submission_type | VARCHAR | Type: "sentence_update", "pair_update", etc. |
| completionToken | VARCHAR | Unique session identifier |
| created_at | TIMESTAMP | When submission occurred |

## 🔍 Example Analysis

```python
from analyze_data import DataAnalyzer

analyzer = DataAnalyzer()
analyzer.load_from_database()

# Responses per page
print(analyzer.responses_df.groupby('page_title').size())

# Average response length
print(analyzer.responses_df.groupby('page_title')['response_text'].apply(lambda x: x.str.len().mean()))

# Submission type distribution
print(analyzer.submissions_df['submission_type'].value_counts())

# Text changes by submission type
df = analyzer.submissions_df.copy()
df['change'] = df['updated_text'].str.len() - df['original_text'].str.len()
print(df.groupby('submission_type')['change'].describe())

# Filter by completion token to track a single user session
token = analyzer.responses_df.iloc[0]['completionToken']
user_responses = analyzer.responses_df[analyzer.responses_df['completionToken'] == token]
user_submissions = analyzer.submissions_df[analyzer.submissions_df['completionToken'] == token]
```

## 🛠️ Troubleshooting

### "DATABASE_URL not set"
```bash
# Check your .env file exists and has DATABASE_URL
cat .env | grep DATABASE_URL

# Or set it from Heroku
heroku config:get DATABASE_URL --app tailia-malloy
```

### "Connection refused"
- Local PostgreSQL: Make sure postgres is running (`brew services start postgresql`)
- Remote: Check your DATABASE_URL is correct
- Heroku: Credentials may have changed, re-run `heroku config:get DATABASE_URL`

### "psycopg2: No module named psycopg2"
```bash
pip install psycopg2-binary
```

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas
```

### "No .env file found"
Create `.env` file in the backend directory:
```
DATABASE_URL=your_postgres_connection_string
```

## 💾 Data Export

All scripts automatically create timestamped CSV files in `data/` directory. This lets you:
- Track data changes over time
- Archive snapshots of your data
- Work offline with CSV files
- Share data without database access

## 📝 Notes

- Scripts connect to PostgreSQL using the `DATABASE_URL` environment variable
- CSV files are created with timestamps to avoid overwriting previous exports
- Analysis automatically detects if database is available or falls back to CSV files
- All scripts include error handling and helpful error messages
