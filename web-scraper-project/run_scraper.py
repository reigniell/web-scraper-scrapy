import os
import subprocess
import json
import pandas as pd

def main():
    print('🚀 Starting Web Scraper Project')
    print('=' * 50)
    
    # Run the scraper from the correct directory
    print('1. Running Scrapy spider...')
    
    # The scrapy.cfg file is inside the 'scraper' directory.
    result = subprocess.run(
        ['scrapy', 'crawl', 'books', '-o', '../data/books.json'],
        capture_output=True,
        text=True,
        cwd='scraper'  # Run command from the 'scraper' folder
    )
    
    if result.returncode == 0:
        print('✅ Scraping completed successfully!')
        
        # Load and display data
        print('\n2. Loading scraped data...')
        try:
            with open('data/books.json', 'r', encoding='utf-8') as f:
                books = json.load(f)
            
            df = pd.DataFrame(books)
            print(f'📊 Total books scraped: {len(df)}')
            
            # Show sample
            print('\n📋 Sample data:')
            print(df[['title', 'price', 'category']].head())
            
            # Save to CSV
            df.to_csv('data/books.csv', index=False)
            print(f'\n💾 Data saved to: data/books.csv')
            
        except Exception as e:
            print(f'❌ Error loading data: {e}')
    else:
        print('❌ Scraping failed!')
        print(f'Error output:\n{result.stderr}')

if __name__ == '__main__':
    main()
