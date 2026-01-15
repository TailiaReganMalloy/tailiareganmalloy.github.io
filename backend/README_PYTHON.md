# Backend Python Scripts - Complete Guide

## 📦 What's Included

Created 4 Python scripts (542 lines of code) for downloading and analyzing your educational experiment data from PostgreSQL.

### Scripts Summary

| Script | Purpose | Size | Use Case |
|--------|---------|------|----------|
| `download_database.py` | Download database to CSV & load to pandas | 5.2 KB | Automated data export |
| `analyze_data.py` | Advanced analytics and reporting | 8.0 KB | Data exploration & summaries |
| `quick_start.py` | Combined download + analyze in one | 1.8 KB | Getting started quickly |
| `setup_notebook.py` | Jupyter notebook setup helper | 3.5 KB | Interactive analysis |

## 🚀 Getting Started (30 seconds)

### 1. Install Requirements
```bash
pip install pandas psycopg2-binary python-dotenv
```

### 2. Make Sure DATABASE_URL is Set
```bash
# Check your .env file
cat backend/.env | grep DATABASE_URL

# Or get from Heroku
heroku config:get DATABASE_URL --app tailia-malloy
```

### 3. Run Download Script
```bash
cd backend
python download_database.py
```

**Output:**
```
🚀 Database Download Script
------------------------------------------
🔗 Connecting to database...
📥 Downloading student_responses table...
   ✓ Saved to backend/data/student_responses_20250115_123456.csv
   📊 Rows: 42
📥 Downloading interactive_submissions table...
   ✓ Saved to backend/data/interactive_submissions_20250115_123456.csv
   📊 Rows: 156

✅ Success! DataFrames are ready for analysis.
```

## 📚 Detailed Usage

### Option 1: Quick Download (recommended for first time)

```bash
python quick_start.py
```

Downloads data and displays comprehensive summary statistics.

### Option 2: Just Download as CSV

```bash
python download_database.py
```

Exports to `data/student_responses_*.csv` and `data/interactive_submissions_*.csv`.

### Option 3: Deep Analysis

```bash
python analyze_data.py
```

Generates summary statistics and exports `analysis_report.txt` with full data.

### Option 4: Jupyter Notebook

Create a notebook in the backend directory and run:

```python
%run setup_notebook.py

# Now you have:
# - responses_df: pandas DataFrame with all responses
# - submissions_df: pandas DataFrame with all submissions
# - analyzer: DataAnalyzer instance

responses_df.head()
responses_df.groupby('page_title').size()
submissions_df['submission_type'].value_counts()
```

## 🔧 Python Usage Examples

### Direct Script Import

```python
from download_database import download_database_to_csv

responses_df, submissions_df = download_database_to_csv()

print(responses_df.info())
print(f"Total responses: {len(responses_df)}")
print(f"Pages covered: {responses_df['page_title'].nunique()}")
```

### Using DataAnalyzer Class

```python
from analyze_data import DataAnalyzer

analyzer = DataAnalyzer()
analyzer.load_from_database()  # or load_from_csv(csv_path)

# Get summaries
analyzer.responses_summary()
analyzer.submissions_summary()

# Access DataFrames
responses = analyzer.responses_df
submissions = analyzer.submissions_df

# Export analysis
analyzer.export_analysis('my_analysis.txt')
```

### Load from CSV Files

```python
import pandas as pd
from pathlib import Path

data_dir = Path('backend/data')

# Auto-detect latest files
responses = pd.read_csv(sorted(data_dir.glob('student_responses_*.csv'))[-1])
submissions = pd.read_csv(sorted(data_dir.glob('interactive_submissions_*.csv'))[-1])
```

## 📊 Data Analysis Examples

```python
# Responses per page
responses_df.groupby('page_title').size()

# Average response length
responses_df.groupby('page_title')['response_text'].apply(
    lambda x: x.str.len().mean()
)

# Submission type distribution
submissions_df['submission_type'].value_counts()

# Text change analysis
submissions_df['change'] = (
    submissions_df['updated_text'].str.len() - 
    submissions_df['original_text'].str.len()
)
submissions_df.groupby('submission_type')['change'].describe()

# Filter by user session (completion token)
token = responses_df.iloc[0]['completionToken']
user_data = responses_df[responses_df['completionToken'] == token]
```

## 📁 File Structure

```
backend/
├── download_database.py      # Main download script
├── analyze_data.py           # Analysis tool
├── quick_start.py            # Quick start script
├── setup_notebook.py         # Jupyter helper
├── PYTHON_SCRIPTS.md         # Full documentation
├── DATABASE_SCRIPTS.md       # Database info
├── data/                     # (auto-created)
│   ├── student_responses_20250115_123456.csv
│   ├── interactive_submissions_20250115_123456.csv
│   └── analysis_report.txt
├── server.js                 # Node.js backend
└── package.json
```

## 🗄️ Database Tables

### `student_responses`
- Stores written responses from each section
- Fields: id, page_title, section_title, section_index, response_text, completionToken, created_at, updated_at

### `interactive_submissions`
- Stores interactive button clicks and text updates
- Fields: id, page_title, section_title, section_index, original_text, updated_text, submission_type, completionToken, created_at

Both tables use `completionToken` to track individual user sessions.

## ⚙️ Requirements

- Python 3.6+
- pandas
- psycopg2-binary
- python-dotenv
- PostgreSQL database (local or remote)

Install all with:
```bash
pip install pandas psycopg2-binary python-dotenv
```

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "DATABASE_URL not set" | Add to `.env`: `DATABASE_URL=postgres://...` |
| Connection refused | Check PostgreSQL is running: `brew services start postgresql` |
| "No module named pandas" | Run: `pip install pandas` |
| "No CSV files found" | Run: `python download_database.py` first |
| Module not found errors | Ensure scripts are in `backend/` directory |

## 📈 Workflow Recommendations

### For Initial Data Export
```bash
python quick_start.py  # Downloads data and shows summary
```

### For Regular Exports
```bash
python download_database.py  # Exports with timestamp
python analyze_data.py        # Generates summary report
```

### For Data Analysis
```python
# In Jupyter or Python script
from analyze_data import DataAnalyzer
analyzer = DataAnalyzer()
analyzer.load_from_database()
analyzer.responses_summary()
```

### For Research/Reports
```python
# Export complete dataset
analyzer.export_analysis('research_data.txt')

# Or use pandas to filter and export
responses_df.to_csv('filtered_responses.csv')
submissions_df.to_csv('filtered_submissions.csv')
```

## 📝 Notes

- All scripts handle errors gracefully with helpful messages
- CSV files are timestamped to prevent overwriting
- Scripts automatically create `data/` directory
- Works both with local PostgreSQL and remote Heroku databases
- Can fallback from database to CSV files if needed
- All data includes `completionToken` for session tracking

---

For more details, see [PYTHON_SCRIPTS.md](PYTHON_SCRIPTS.md) and [DATABASE_SCRIPTS.md](DATABASE_SCRIPTS.md).
