#!/usr/bin/env python3
"""
Advanced data analysis script for educational experiment data.

This script provides utilities for analyzing student responses and interactive submissions
from the language model experiment. Includes functions for data cleaning, filtering,
text analysis, and statistical summaries.

Usage:
    python analyze_data.py
"""

import os
import sys
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import json

# Load environment variables
env_path = Path(__file__).parent / '.env'
env_example_path = Path(__file__).parent / '.env.example'

if env_path.exists():
    load_dotenv(env_path)
else:
    if env_example_path.exists():
        load_dotenv(env_example_path)
    else:
        load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class DataAnalyzer:
    """Analyze educational experiment data."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.responses_df = None
        self.submissions_df = None
    
    def load_from_database(self):
        """Load data directly from database."""
        if not DATABASE_URL:
            print("❌ DATABASE_URL not set")
            return False
        
        try:
            print("🔗 Connecting to database...")
            conn = psycopg2.connect(DATABASE_URL)
            
            self.responses_df = pd.read_sql_query(
                "SELECT * FROM student_responses ORDER BY created_at DESC;",
                conn
            )
            self.submissions_df = pd.read_sql_query(
                "SELECT * FROM interactive_submissions ORDER BY created_at DESC;",
                conn
            )
            
            conn.close()
            print("✓ Data loaded from database")
            return True
        except Exception as e:
            print(f"❌ Error loading from database: {e}")
            return False
    
    def load_from_csv(self, responses_csv=None, submissions_csv=None):
        """Load data from CSV files."""
        try:
            if responses_csv:
                self.responses_df = pd.read_csv(responses_csv)
                print(f"✓ Loaded responses from {responses_csv}")
            
            if submissions_csv:
                self.submissions_df = pd.read_csv(submissions_csv)
                print(f"✓ Loaded submissions from {submissions_csv}")
            
            return True
        except Exception as e:
            print(f"❌ Error loading CSV files: {e}")
            return False
    
    def responses_summary(self):
        """Get summary statistics for responses."""
        if self.responses_df is None or len(self.responses_df) == 0:
            print("❌ No response data loaded")
            return
        
        df = self.responses_df
        
        print("\n" + "="*60)
        print("📋 STUDENT RESPONSES SUMMARY")
        print("="*60)
        
        print(f"\nTotal responses: {len(df)}")
        print(f"Unique pages: {df['page_title'].nunique()}")
        print(f"Unique sections: {df['section_title'].nunique()}")
        
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            print(f"Date range: {df['created_at'].min()} to {df['created_at'].max()}")
        
        print("\n📄 Responses per page:")
        page_counts = df['page_title'].value_counts()
        for page, count in page_counts.items():
            print(f"   {page}: {count}")
        
        print("\n📝 Average response length by page:")
        avg_length = df.groupby('page_title')['response_text'].apply(
            lambda x: x.str.len().mean()
        ).round(2)
        for page, length in avg_length.items():
            print(f"   {page}: {length:.0f} characters")
        
        return df
    
    def submissions_summary(self):
        """Get summary statistics for interactive submissions."""
        if self.submissions_df is None or len(self.submissions_df) == 0:
            print("❌ No submission data loaded")
            return
        
        df = self.submissions_df
        
        print("\n" + "="*60)
        print("💬 INTERACTIVE SUBMISSIONS SUMMARY")
        print("="*60)
        
        print(f"\nTotal submissions: {len(df)}")
        print(f"Unique pages: {df['page_title'].nunique()}")
        print(f"Unique sections: {df['section_title'].nunique()}")
        
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            print(f"Date range: {df['created_at'].min()} to {df['created_at'].max()}")
        
        print("\n🏷️  Submission types:")
        type_counts = df['submission_type'].value_counts()
        for sub_type, count in type_counts.items():
            print(f"   {sub_type}: {count}")
        
        print("\n📄 Submissions per page:")
        page_counts = df['page_title'].value_counts()
        for page, count in page_counts.items():
            print(f"   {page}: {count}")
        
        print("\n✏️  Average text change length by submission type:")
        df['original_len'] = df['original_text'].str.len()
        df['updated_len'] = df['updated_text'].str.len()
        df['change'] = df['updated_len'] - df['original_len']
        
        change_stats = df.groupby('submission_type').agg({
            'original_len': 'mean',
            'updated_len': 'mean',
            'change': 'mean'
        }).round(2)
        
        for sub_type in change_stats.index:
            orig = change_stats.loc[sub_type, 'original_len']
            upd = change_stats.loc[sub_type, 'updated_len']
            chg = change_stats.loc[sub_type, 'change']
            print(f"   {sub_type}: {orig:.0f} → {upd:.0f} (Δ {chg:+.0f})")
        
        return df
    
    def export_analysis(self, output_file='analysis_report.txt'):
        """Export complete analysis to file."""
        with open(output_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("EDUCATIONAL EXPERIMENT DATA ANALYSIS\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            if self.responses_df is not None and len(self.responses_df) > 0:
                f.write("STUDENT RESPONSES\n")
                f.write("-" * 60 + "\n")
                f.write(self.responses_df.to_string())
                f.write("\n\n")
            
            if self.submissions_df is not None and len(self.submissions_df) > 0:
                f.write("INTERACTIVE SUBMISSIONS\n")
                f.write("-" * 60 + "\n")
                f.write(self.submissions_df.to_string())
                f.write("\n")
        
        print(f"✓ Analysis exported to {output_file}")


def main():
    """Main function."""
    print("🔬 Data Analysis Tool")
    print("-" * 60)
    
    analyzer = DataAnalyzer()
    
    # Try to load from database first
    if not analyzer.load_from_database():
        print("\nℹ️  Database connection failed. Trying local CSV files...")
        
        # Look for latest CSV files in data directory
        data_dir = Path(__file__).parent / 'data'
        responses_csv = None
        submissions_csv = None
        
        if data_dir.exists():
            # Find latest responses CSV
            responses_files = sorted(data_dir.glob('student_responses_*.csv'))
            if responses_files:
                responses_csv = str(responses_files[-1])
            
            # Find latest submissions CSV
            submissions_files = sorted(data_dir.glob('interactive_submissions_*.csv'))
            if submissions_files:
                submissions_csv = str(submissions_files[-1])
        
        if not analyzer.load_from_csv(responses_csv, submissions_csv):
            print("❌ Could not load data from database or CSV files")
            sys.exit(1)
    
    # Generate summaries
    analyzer.responses_summary()
    analyzer.submissions_summary()
    
    # Export analysis
    analyzer.export_analysis()
    
    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()
