#!/usr/bin/env python3
"""
Jupyter notebook setup helper.

Place this file in your notebook directory and run:
    %run setup_notebook.py

This will load your data into notebook-ready variables.
"""

import os
import sys
from pathlib import Path
import pandas as pd

# Try to load from parent backend directory
backend_path = Path.cwd().parent / 'backend'
if backend_path.exists():
    sys.path.insert(0, str(backend_path))

try:
    from download_database import download_database_to_csv
    from analyze_data import DataAnalyzer
    print("✓ Database scripts loaded successfully")
except ImportError:
    print("⚠️  Could not import backend scripts")
    print("   Make sure setup_notebook.py is in a directory next to 'backend/'")


def load_data_from_database():
    """Load data from remote PostgreSQL database."""
    print("\n🔗 Loading data from database...")
    try:
        responses_df, submissions_df = download_database_to_csv()
        print("✓ Data loaded successfully")
        return responses_df, submissions_df
    except Exception as e:
        print(f"❌ Could not load from database: {e}")
        return None, None


def load_data_from_csv():
    """Load data from local CSV files."""
    print("\n📂 Loading data from CSV files...")
    data_dir = Path('backend/data')
    
    if not data_dir.exists():
        print("❌ No data directory found")
        return None, None
    
    # Find latest CSV files
    responses_files = sorted(data_dir.glob('student_responses_*.csv'))
    submissions_files = sorted(data_dir.glob('interactive_submissions_*.csv'))
    
    if not responses_files or not submissions_files:
        print("❌ No CSV files found in backend/data/")
        print("   Run 'python download_database.py' first")
        return None, None
    
    responses_df = pd.read_csv(responses_files[-1])
    submissions_df = pd.read_csv(submissions_files[-1])
    
    print(f"✓ Loaded responses from {responses_files[-1].name}")
    print(f"✓ Loaded submissions from {submissions_files[-1].name}")
    
    return responses_df, submissions_df


def setup_notebook_variables():
    """Set up variables in the notebook namespace."""
    import inspect
    frame = inspect.currentframe().f_back
    
    # Try database first, fallback to CSV
    responses_df, submissions_df = load_data_from_database()
    
    if responses_df is None:
        responses_df, submissions_df = load_data_from_csv()
    
    if responses_df is None:
        print("\n❌ Could not load any data!")
        return
    
    # Set variables in notebook namespace
    frame.f_locals['responses_df'] = responses_df
    frame.f_locals['submissions_df'] = submissions_df
    frame.f_locals['analyzer'] = DataAnalyzer()
    frame.f_locals['analyzer'].responses_df = responses_df
    frame.f_locals['analyzer'].submissions_df = submissions_df
    
    print("\n" + "="*60)
    print("📊 NOTEBOOK READY")
    print("="*60)
    print(f"\n✓ responses_df: {len(responses_df)} rows")
    print(f"✓ submissions_df: {len(submissions_df)} rows")
    print(f"✓ analyzer: DataAnalyzer instance")
    
    print("\n📝 Quick start commands:")
    print("   responses_df.head()")
    print("   submissions_df.info()")
    print("   analyzer.responses_summary()")
    print("   analyzer.submissions_summary()")
    print("   responses_df.groupby('page_title').size()")
    print("   submissions_df['submission_type'].value_counts()")


# Run setup when imported
setup_notebook_variables()
