import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz
import sys
import io

# Force UTF-8 output for Windows terminals
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

try:
    # Universal renderer for notebook or .py
    import plotly.io as pio
    try:
        get_ipython  # Check if running in notebook
        pio.renderers.default = "notebook_connected"
    except NameError:
        pio.renderers.default = "browser"  # Use browser for .py files

    # Load dataset
    df = pd.read_csv(r"C:\Users\Tamilarasan K\Downloads\Play Store Project\data\google_play_store_data.csv")

    # Clean Reviews → numeric
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

    # Clean Installs → remove + and , then convert to numeric
    df['Installs'] = df['Installs'].astype(str).str.replace(r'[\+,]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

    # Drop rows with missing critical values
    df = df.dropna(subset=['App', 'Category', 'Reviews', 'Installs', 'Last Updated'])

    # Filter dataset
    df = df[
        (~df['App'].str.startswith(('X', 'Y', 'Z'))) &
        (~df['App'].str.contains('S', case=False, na=False)) &
        (df['Reviews'] > 500) &
        (df['Category'].str.startswith(('E', 'C', 'B')))
    ]

    # Translate categories (case-insensitive)
    category_map = {
        'BEAUTY': 'सौंदर्य',   # Hindi
        'BUSINESS': 'வணிகம்',  # Tamil
        'DATING': 'Dating'     # German
    }
    df['Category'] = df['Category'].str.upper().replace(category_map)

    # Convert Last Updated to datetime
    df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

    # Create YearMonth column
    df['YearMonth'] = df['Last Updated'].dt.to_period('M')

    # Group installs by YearMonth & Category
    installs_trend = df.groupby(['YearMonth', 'Category'])['Installs'].sum().reset_index()
    installs_trend['YearMonth'] = installs_trend['YearMonth'].dt.to_timestamp()

    # Calculate Month-over-Month Growth
    installs_trend['Growth'] = installs_trend.groupby('Category')['Installs'].pct_change()

    # Mark High Growth Periods (>20%)
    installs_trend['HighGrowth'] = installs_trend['Growth'] > 0.2

    # Get current IST time
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    
    if 18 <= now.hour < 21:  # 6 PM - 9 PM IST
        fig = go.Figure()
        categories = installs_trend['Category'].unique()

        for cat in categories:
            cat_data = installs_trend[installs_trend['Category'] == cat]

            # Line chart
            fig.add_trace(go.Scatter(
                x=cat_data['YearMonth'],
                y=cat_data['Installs'],
                mode='lines+markers',
                name=f"{cat} Installs"
            ))

            # Highlight high growth periods
            high_growth_data = cat_data[cat_data['HighGrowth']]
            if not high_growth_data.empty:
                fig.add_trace(go.Scatter(
                    x=high_growth_data['YearMonth'],
                    y=high_growth_data['Installs'],
                    fill='tozeroy',
                    mode='none',
                    name=f"{cat} >20% Growth",
                    opacity=0.3
                ))

        # Layout
        fig.update_layout(
            title="Total Installs Over Time (with >20% Growth Highlighted)",
            xaxis_title="Time",
            yaxis_title="Total Installs",
            template="plotly_white"
        )

        fig.show()
    else:
        print("[INFO] Graph is visible only between 6 PM and 9 PM IST. Outside this time, it is hidden from dashboard.")

except FileNotFoundError:
    print("[ERROR] CSV file not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print("[ERROR] CSV file is empty.")
except pd.errors.ParserError:
    print("[ERROR] Error parsing CSV file. Please check its format.")
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
