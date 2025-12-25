import json
import pandas as pd
import os

def main():
    print('📊 WEB SCRAPER PROJECT - DATA ANALYSIS')
    print('=' * 50)
    
    # Try the cleaned file first, then original
    data_files = ['data/books_clean.json', 'data/books.json']
    data_file = None
    
    for file in data_files:
        if os.path.exists(file):
            data_file = file
            break
    
    if not data_file:
        print('❌ No data files found!')
        return
    
    print(f'📁 Using data file: {data_file}')
    
    try:
        # Load the data
        with open(data_file, 'r', encoding='utf-8') as f:
            books = json.load(f)
        
        print(f'✅ Successfully loaded {len(books)} books!')
        
        # Create DataFrame
        df = pd.DataFrame(books)
        
        # Display basic info
        print(f'\\n📈 BASIC STATISTICS:')
        print(f'   • Total books: {len(df)}')
        print(f'   • Unique categories: {df["category"].nunique()}')
        
        # Clean price column
        if 'price' in df.columns:
            # Remove any weird characters and keep only numbers and decimal point
            df['price_clean'] = df['price'].astype(str).str.replace('[^\\d.]', '', regex=True)
            df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')
            
            print(f'   • Average price: £{df["price_clean"].mean():.2f}')
            print(f'   • Most expensive: £{df["price_clean"].max():.2f}')
            print(f'   • Least expensive: £{df["price_clean"].min():.2f}')
        
        # Show categories
        print(f'\\n📚 TOP CATEGORIES:')
        top_cats = df['category'].value_counts().head(10)
        for i, (cat, count) in enumerate(top_cats.items(), 1):
            print(f'   {i}. {cat}: {count} books')
        
        # Show sample data
        print(f'\\n📋 SAMPLE DATA (first 3 books):')
        print(df[['title', 'price', 'category']].head(3).to_string())
        
        # Save to CSV
        csv_file = 'data/books_analysis.csv'
        df.to_csv(csv_file, index=False)
        print(f'\\n💾 Data saved to: {csv_file}')
        
        # Create summary file
        summary = f'''WEB SCRAPER PROJECT SUMMARY
=======================
Total Books Scraped: {len(df)}
Scraping Date: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}
Data Source: books.toscrape.com

CATEGORY BREAKDOWN:
{df['category'].value_counts().to_string()}

PRICE STATISTICS:
Average Price: £{df['price_clean'].mean():.2f}
Price Range: £{df['price_clean'].min():.2f} - £{df['price_clean'].max():.2f}
'''
        
        with open('data/project_summary.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f'📝 Project summary saved to: data/project_summary.txt')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
