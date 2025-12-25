import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from pathlib import Path

def create_charts():
    print("📊 CREATING DATA VISUALIZATIONS...")
    
    # Load data - FIXED PATH
    data_path = Path("data/books.json")
    
    if not data_path.exists():
        # Try alternative path
        data_path = Path("../data/books.json")
    
    if not data_path.exists():
        print("❌ Could not find books.json. Please check the path.")
        return
    
    try:
        # Load the data
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        print(f"✅ Loaded {len(df)} books from {data_path}")
        
    except json.JSONDecodeError:
        print("⚠️  JSON parsing error, trying manual extraction...")
        # Try the regex approach from earlier
        with open(data_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        import re
        pattern = r'\{\s*"title":.*?\}\s*(?=,\s*\{|$)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        books = []
        for match in matches:
            try:
                clean_match = match.replace('\\n', ' ').replace('\\r', ' ')
                clean_match = re.sub(r',\s*\}$', '}', clean_match)
                book = json.loads(clean_match)
                books.append(book)
            except:
                continue
        
        df = pd.DataFrame(books)
        print(f"✅ Loaded {len(df)} books using manual extraction")
    
    # Clean price data
    if 'price' in df.columns:
        df['price_numeric'] = df['price'].astype(str).str.extract(r'([\d\.]+)')[0]
        df['price_numeric'] = pd.to_numeric(df['price_numeric'], errors='coerce')
    
    # Create visualizations directory
    os.makedirs('visualization/charts', exist_ok=True)
    
    # Set style for better looking charts
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1. Price Distribution Histogram
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    if 'price_numeric' in df.columns:
        df['price_numeric'].hist(bins=30, edgecolor='black', color='skyblue', alpha=0.7)
        plt.title('Book Price Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Price (£)', fontsize=12)
        plt.ylabel('Number of Books', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        # Add mean line
        mean_price = df['price_numeric'].mean()
        plt.axvline(mean_price, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: £{mean_price:.2f}')
        plt.legend()
    
    # 2. Top Categories Bar Chart
    plt.subplot(1, 2, 2)
    if 'category' in df.columns:
        top_cats = df['category'].value_counts().head(10)
        colors = plt.cm.Set3(range(len(top_cats)))
        bars = plt.barh(range(len(top_cats)), top_cats.values, color=colors, edgecolor='black')
        plt.yticks(range(len(top_cats)), top_cats.index)
        plt.title('Top 10 Book Categories', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Books', fontsize=12)
        
        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{int(width)}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('visualization/charts/book_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: visualization/charts/book_analysis.png")
    
    # 3. Price by Category (Box Plot)
    if 'category' in df.columns and 'price_numeric' in df.columns:
        plt.figure(figsize=(14, 8))
        # Get top 8 categories for readability
        top_categories = df['category'].value_counts().head(8).index
        df_top = df[df['category'].isin(top_categories)]
        
        # Create box plot with better styling
        boxprops = dict(linestyle='-', linewidth=2, color='darkblue')
        whiskerprops = dict(linestyle='-', linewidth=1.5, color='black')
        capprops = dict(linestyle='-', linewidth=1.5, color='black')
        medianprops = dict(linestyle='-', linewidth=2.5, color='red')
        
        box_data = []
        categories = []
        for category in top_categories:
            cat_prices = df_top[df_top['category'] == category]['price_numeric'].dropna()
            if len(cat_prices) > 0:
                box_data.append(cat_prices)
                categories.append(category)
        
        bp = plt.boxplot(box_data, patch_artist=True, labels=categories,
                        boxprops=boxprops, whiskerprops=whiskerprops,
                        capprops=capprops, medianprops=medianprops)
        
        # Color the boxes
        colors = plt.cm.Pastel1(range(len(box_data)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        plt.title('Price Distribution by Category', fontsize=16, fontweight='bold')
        plt.xlabel('Category', fontsize=14)
        plt.ylabel('Price (£)', fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('visualization/charts/price_by_category.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("✅ Created: visualization/charts/price_by_category.png")
    
    # 4. Create a simple HTML dashboard with proper escaping
    # Calculate statistics first
    total_books = len(df)
    unique_cats = df["category"].nunique() if "category" in df.columns else 0
    avg_price = df["price_numeric"].mean() if "price_numeric" in df.columns else 0
    min_price = df["price_numeric"].min() if "price_numeric" in df.columns else 0
    max_price = df["price_numeric"].max() if "price_numeric" in df.columns else 0
    
    # Get current date
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Get top categories for HTML list
    top_cats_html = ""
    if 'category' in df.columns:
        top_cats = df['category'].value_counts().head(5)
        for cat, count in top_cats.items():
            top_cats_html += f'<li><strong>{cat}</strong>: {count} books</li>\n'
    
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Book Scraper Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .stats {{ display: flex; justify-content: space-between; margin: 30px 0; flex-wrap: wrap; }}
        .stat-box {{ background: #3498db; color: white; padding: 20px; border-radius: 5px; text-align: center; flex: 1; margin: 10px; min-width: 200px; }}
        .stat-box h2 {{ margin: 0; font-size: 28px; }}
        .stat-box p {{ margin: 5px 0; font-size: 14px; }}
        .charts {{ margin: 40px 0; }}
        .chart {{ margin: 30px 0; text-align: center; }}
        .chart img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 5px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }}
        footer {{ margin-top: 40px; text-align: center; color: #7f8c8d; padding-top: 20px; border-top: 1px solid #eee; }}
        .data-summary {{ background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .data-summary h3 {{ margin-top: 0; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 8px 0; }}
        @media (max-width: 768px) {{ 
            .stats {{ flex-direction: column; }}
            .stat-box {{ margin: 10px 0; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Book Scraper Analytics Dashboard</h1>
        
        <div class="stats">
            <div class="stat-box" style="background: #3498db;">
                <h2>{total_books}</h2>
                <p>Total Books Scraped</p>
            </div>
            <div class="stat-box" style="background: #2ecc71;">
                <h2>{unique_cats}</h2>
                <p>Unique Categories</p>
            </div>
            <div class="stat-box" style="background: #e74c3c;">
                <h2>£{avg_price:.2f}</h2>
                <p>Average Price</p>
            </div>
            <div class="stat-box" style="background: #f39c12;">
                <h2>£{min_price:.2f} - £{max_price:.2f}</h2>
                <p>Price Range</p>
            </div>
        </div>
        
        <div class="data-summary">
            <h3>📋 Project Summary</h3>
            <p>This dashboard displays analytics from {total_books} books scraped from books.toscrape.com.</p>
            <p>The data includes {unique_cats} different categories with prices ranging from £{min_price:.2f} to £{max_price:.2f}.</p>
        </div>
        
        <div class="charts">
            <div class="chart">
                <h3>📊 Book Analysis Overview</h3>
                <p>Left: Price distribution of all books | Right: Top 10 categories by book count</p>
                <img src="charts/book_analysis.png" alt="Book Analysis Charts">
            </div>
            
            <div class="chart">
                <h3>💰 Price Distribution by Category</h3>
                <p>Box plot showing price variations across top categories (median, quartiles, outliers)</p>
                <img src="charts/price_by_category.png" alt="Price by Category">
            </div>
        </div>
        
        <div class="data-summary">
            <h3>🏆 Top 5 Categories</h3>
            <ul>
                {top_cats_html}
            </ul>
        </div>
        
        <footer>
            <p>📅 Generated on {current_date}</p>
            <p>📂 Data Source: books.toscrape.com | 🎯 Project: Web Scraper Portfolio Project</p>
            <p>💡 Tip: The charts above show the complete analysis of your scraped book data!</p>
        </footer>
    </div>
</body>
</html>'''
    
    # Save HTML dashboard
    with open('visualization/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Created: visualization/dashboard.html")
    print("\n" + "="*50)
    print("🎉 VISUALIZATION COMPLETE!")
    print("="*50)
    print("\n📊 Your visualizations are ready:")
    print("   1. 📈 Price distribution & category analysis charts")
    print("   2. 📊 Box plots of prices by category")
    print("   3. 🌐 Interactive HTML dashboard")
    
    print("\n🎯 To view your dashboard:")
    print("   1. Open 'visualization/dashboard.html' in your browser")
    print("   2. Or run this command: start visualization/dashboard.html")
    
    print("\n💾 Files created:")
    print("   📁 visualization/charts/book_analysis.png")
    print("   📁 visualization/charts/price_by_category.png")
    print("   📁 visualization/dashboard.html")

if __name__ == '__main__':
    create_charts()
