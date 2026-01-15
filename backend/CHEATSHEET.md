# 🐍 Python Database Scripts - Quick Cheat Sheet

## Installation (one-time)

```bash
cd backend
pip install pandas psycopg2-binary python-dotenv
```

## Common Commands

### Download Data
```bash
python download_database.py
```
Creates `data/student_responses_*.csv` and `data/interactive_submissions_*.csv`

### Quick Analysis
```bash
python quick_start.py
```
Downloads + shows summary + exports report

### Full Analysis
```bash
python analyze_data.py
```
Generates detailed `analysis_report.txt`

## Python Code Snippets

### Load Data in Python/Jupyter
```python
from download_database import download_database_to_csv
responses_df, submissions_df = download_database_to_csv()
```

### Analyze Data
```python
from analyze_data import DataAnalyzer
analyzer = DataAnalyzer()
analyzer.load_from_database()
analyzer.responses_summary()
analyzer.submissions_summary()
```

### Load from CSV
```python
import pandas as pd
responses_df = pd.read_csv('data/student_responses_*.csv')
submissions_df = pd.read_csv('data/interactive_submissions_*.csv')
```

### Jupyter Notebook Setup
```python
%run setup_notebook.py
# Now use: responses_df, submissions_df, analyzer
```

## Data Queries

### Response Statistics
```python
# Responses per page
responses_df.groupby('page_title').size()

# Average response length
responses_df.groupby('page_title')['response_text'].apply(lambda x: x.str.len().mean())

# Responses by date
responses_df.groupby(responses_df['created_at'].dt.date).size()
```

### Submission Statistics
```python
# Submission types
submissions_df['submission_type'].value_counts()

# Text changes
submissions_df['change'] = submissions_df['updated_text'].str.len() - submissions_df['original_text'].str.len()
submissions_df.groupby('submission_type')['change'].describe()

# Submissions per page
submissions_df.groupby('page_title').size()
```

### User Session Analysis
```python
# Get unique tokens
tokens = responses_df['completionToken'].unique()

# Analyze single user
token = tokens[0]
user_responses = responses_df[responses_df['completionToken'] == token]
user_submissions = submissions_df[submissions_df['completionToken'] == token]
```

## Troubleshooting

**Import Error?**
```bash
pip install pandas psycopg2-binary python-dotenv
```

**DATABASE_URL Error?**
```bash
# Check .env
cat .env | grep DATABASE_URL

# Or set from Heroku
heroku config:get DATABASE_URL --app tailia-malloy > .env
```

**psycopg2 Error?**
```bash
pip install psycopg2-binary
```

**Connection Refused?**
```bash
# Check PostgreSQL
brew services start postgresql
```

## Files Created

| File | Purpose |
|------|---------|
| `download_database.py` | Download to CSV + pandas |
| `analyze_data.py` | Analytics & reporting |
| `quick_start.py` | Quick download+analyze |
| `setup_notebook.py` | Jupyter helper |
| `README_PYTHON.md` | Full guide |
| `PYTHON_SCRIPTS.md` | Detailed docs |
| `DATABASE_SCRIPTS.md` | Database info |

## Key Features

✅ Download database to CSV with timestamps  
✅ Load directly into pandas DataFrames  
✅ Automatic fallback CSV→Database  
✅ Summary statistics & analysis  
✅ Export reports to text files  
✅ Jupyter notebook integration  
✅ Session tracking via completionToken  
✅ Error handling & helpful messages  

## Database Tables

**student_responses:** Written responses per section  
**interactive_submissions:** Button clicks & text updates  

Both include `completionToken` for tracking user sessions.

---

**Quick Start:**
```bash
cd backend
python quick_start.py
```

**Get Help:**
```bash
python download_database.py --help
```

See [README_PYTHON.md](README_PYTHON.md) for full documentation.
