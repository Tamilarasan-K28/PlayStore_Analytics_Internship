import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pytz
import sys
import io

# Force UTF-8 output to avoid Unicode errors on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

try:
    # Load dataset
    df = pd.read_csv(r"C:\Users\Tamilarasan K\Downloads\Play Store Project\data\google_play_store_data.csv")

    # Convert Size column to MB
    def size_to_mb(size):
        if pd.isna(size) or size == 'Varies with device':
            return None
        size = str(size).strip()
        if size.endswith('M'):
            return float(size.replace('M',''))
        elif size.endswith('k'):
            return float(size.replace('k','')) / 1024
        else:
            return None

    df['Size_MB'] = df['Size'].apply(size_to_mb)

    # Convert Reviews and Installs to numeric
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    df['Installs'] = df['Installs'].astype(str).str.replace('+','', regex=False).str.replace(',','', regex=False)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

    # Convert Last Updated to datetime
    df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

    # Filter conditions: Rating >= 4.0, Size >= 10MB, Last Update = January
    filtered = df[
        (df['Rating'] >= 4.0) &
        (df['Size_MB'] >= 10) &
        (df['Last Updated'].dt.month == 1)
    ]

    # Aggregate statistics by category
    category_stats = filtered.groupby("Category").agg({
        "Rating": "mean",
        "Reviews": "sum",
        "Installs": "sum"
    }).reset_index()

    # Top 10 categories by Installs
    top10 = category_stats.sort_values("Installs", ascending=False).head(10)

    # Time-based restriction: 3 PM to 5 PM IST
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india)

    if 15 <= now.hour < 17:  # 3 PM to 5 PM IST
        # Create grouped bar chart
        fig, ax1 = plt.subplots(figsize=(14,8))
        x = np.arange(len(top10))
        bar_width = 0.4

        # Left y-axis: Average Rating
        ax1.bar(x - bar_width/2, top10["Rating"], width=bar_width, label="Average Rating", color="skyblue")
        ax1.set_ylabel("Average Rating (0–5)")
        ax1.set_ylim(0, 5)

        # Right y-axis: Total Reviews
        ax2 = ax1.twinx()
        ax2.bar(x + bar_width/2, top10["Reviews"], width=bar_width, label="Total Reviews", color="orange")
        ax2.set_ylabel("Total Reviews")

        # X-axis labels
        ax1.set_xticks(x)
        ax1.set_xticklabels(top10["Category"], rotation=30, ha="right")

        # Legends and title
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        ax1.set_title("Top 10 App Categories by Installs — Avg Rating vs Total Reviews (Jan, Rating>=4, Size>=10MB)")

        plt.tight_layout()
        plt.show()

    else:
        # Message when outside time window
        print("[INFO] The graph is only visible between 3 PM and 5 PM IST.")

except FileNotFoundError:
    print("[ERROR] CSV file not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print("[ERROR] CSV file is empty.")
except pd.errors.ParserError:
    print("[ERROR] Error parsing CSV file. Please check its format.")
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
