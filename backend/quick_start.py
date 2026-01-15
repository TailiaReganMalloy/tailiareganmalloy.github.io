#!/usr/bin/env python3
"""
Quick start script to download database and perform basic analysis.

Run this to immediately get your data as pandas DataFrames:
    python quick_start.py
"""

import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from download_database import download_database_to_csv
from analyze_data import DataAnalyzer


def main():
    """Quick start function."""
    print("\n" + "="*60)
    print("🚀 QUICK START: Download & Analyze Database")
    print("="*60 + "\n")
    
    # Step 1: Download data
    print("Step 1️⃣  Downloading data from database...")
    try:
        responses_df, submissions_df = download_database_to_csv()
    except SystemExit:
        print("\n❌ Failed to download from database.")
        print("   Make sure DATABASE_URL is set in your .env file.")
        sys.exit(1)
    
    # Step 2: Analyze data
    print("\n\nStep 2️⃣  Analyzing data...\n")
    analyzer = DataAnalyzer()
    analyzer.responses_df = responses_df
    analyzer.submissions_df = submissions_df
    
    analyzer.responses_summary()
    analyzer.submissions_summary()
    
    # Step 3: Ready for use
    print("\n" + "="*60)
    print("✅ SUCCESS! Your data is ready.")
    print("="*60)
    print("\nYou can now use the DataFrames in Python:")
    print(f"  • responses_df: {len(responses_df)} rows")
    print(f"  • submissions_df: {len(submissions_df)} rows")
    print("\nExample analysis:")
    print("  >>> responses_df.groupby('page_title').size()")
    print("  >>> submissions_df['submission_type'].value_counts()")
    print("\nOr use in Jupyter:")
    print("  >>> %run quick_start.py")
    print("  >>> responses_df.head()")


if __name__ == '__main__':
    main()
