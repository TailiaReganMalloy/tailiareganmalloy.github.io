#!/usr/bin/env python3
"""
Download remote PostgreSQL database tables as CSVs and load into pandas DataFrames.

This script connects to the PostgreSQL database using the DATABASE_URL environment variable,
queries the student_responses and interactive_submissions tables, exports them as CSV files,
and loads them into pandas DataFrames for analysis.

Usage:
    python download_database.py
"""

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
env_example_path = Path(__file__).parent / '.env.example'

if env_path.exists():
    load_dotenv(env_path)
    print("✓ Loaded environment from .env")
else:
    print("⚠️  No .env file found. Trying .env.example...")
    if env_example_path.exists():
        load_dotenv(env_example_path)
        print("✓ Loaded environment from .env.example")
    else:
        load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ Error: DATABASE_URL environment variable not set.")
    print("   Please ensure DATABASE_URL is in .env, .env.example, or your environment.")
    sys.exit(1)


def download_database_to_csv():
    """
    Connect to PostgreSQL database and export tables to CSV files.
    
    Returns:
        tuple: (responses_df, submissions_df) - DataFrames loaded from database
    """
    try:
        print("🔗 Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Create data directory if it doesn't exist
        data_dir = Path(__file__).parent / 'data'
        data_dir.mkdir(exist_ok=True)
        
        # Timestamp for file naming
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export student_responses table
        print("📥 Downloading student_responses table...")
        responses_df = pd.read_sql_query(
            "SELECT * FROM student_responses ORDER BY created_at DESC;",
            conn
        )
        responses_csv = data_dir / f'student_responses_{timestamp}.csv'
        responses_df.to_csv(responses_csv, index=False)
        print(f"   ✓ Saved to {responses_csv}")
        print(f"   📊 Rows: {len(responses_df)}")
        
        # Export interactive_submissions table
        print("📥 Downloading interactive_submissions table...")
        submissions_df = pd.read_sql_query(
            "SELECT * FROM interactive_submissions ORDER BY created_at DESC;",
            conn
        )
        submissions_csv = data_dir / f'interactive_submissions_{timestamp}.csv'
        submissions_df.to_csv(submissions_csv, index=False)
        print(f"   ✓ Saved to {submissions_csv}")
        print(f"   📊 Rows: {len(submissions_df)}")
        
        conn.close()
        
        return responses_df, submissions_df
        
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error downloading database: {e}")
        sys.exit(1)


def display_summary(responses_df, submissions_df):
    """Display summary statistics about the downloaded data."""
    print("\n" + "="*60)
    print("📊 DATABASE SUMMARY")
    print("="*60)
    
    print(f"\n📋 Student Responses Table:")
    print(f"   Total responses: {len(responses_df)}")
    if len(responses_df) > 0:
        print(f"   Pages: {responses_df['page_title'].nunique()}")
        print(f"   Sections: {responses_df['section_title'].nunique()}")
        print(f"\n   Column names: {list(responses_df.columns)}")
        print(f"\n   Sample response:")
        sample = responses_df.iloc[0]
        for col, val in sample.items():
            if col == 'response_text' and len(str(val)) > 100:
                print(f"      {col}: {str(val)[:100]}...")
            else:
                print(f"      {col}: {val}")
    
    print(f"\n💬 Interactive Submissions Table:")
    print(f"   Total submissions: {len(submissions_df)}")
    if len(submissions_df) > 0:
        print(f"   Pages: {submissions_df['page_title'].nunique()}")
        print(f"   Submission types: {submissions_df['submission_type'].nunique()}")
        print(f"\n   Column names: {list(submissions_df.columns)}")
        print(f"\n   Sample submission:")
        sample = submissions_df.iloc[0]
        for col, val in sample.items():
            if col in ['original_text', 'updated_text'] and len(str(val)) > 50:
                print(f"      {col}: {str(val)[:50]}...")
            else:
                print(f"      {col}: {val}")
    
    print("\n" + "="*60)


def main():
    """Main function."""
    print("🚀 Database Download Script")
    print("-" * 60)
    
    # Download database
    responses_df, submissions_df = download_database_to_csv()
    
    # Display summary
    display_summary(responses_df, submissions_df)
    
    print("\n✅ Success! DataFrames are ready for analysis.")
    print("\nTo use in Python:")
    print("   >>> import pandas as pd")
    print("   >>> responses = pd.read_csv('backend/data/student_responses_*.csv')")
    print("   >>> submissions = pd.read_csv('backend/data/interactive_submissions_*.csv')")


if __name__ == '__main__':
    main()
