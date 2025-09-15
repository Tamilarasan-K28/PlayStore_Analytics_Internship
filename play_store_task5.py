import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz
import sys
import io

# Force UTF-8 output for Windows terminals
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

try:
    # Universal snippet for notebooks or .py
    import matplotlib
    try:
        get_ipython  # notebook check
    except NameError:
        matplotlib.use('TkAgg')  # for .py scripts on Windows

    # ==============================
    # Load datasets
    # ==============================
    apps = pd.read_csv(r"C:\Users\Tamilarasan K\Downloads\Play Store Project\data\google_play_store_data.csv")
    reviews = pd.read_csv(r"C:\Users\Tamilarasan K\Downloads\Play Store Project\data\user_reviews.csv")

    # Compute average sentiment subjectivity per app
    reviews_avg = reviews.groupby("App", as_index=False)["Sentiment_Subjectivity"].mean()

    # Merge with main dataset
    df = pd.merge(apps, reviews_avg, on="App", how="inner")

    # ==============================
    # Data Cleaning
    # ==============================
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    df['Installs'] = df['Installs'].astype(str).str.replace(r'[\+,]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

    # Convert Size to MB
    def convert_size(size):
        if isinstance(size, str):
            size = size.strip()
            if size.endswith("M"):
                return float(size.replace("M",""))
            elif size.endswith("k"):
                return float(size.replace("k","")) / 1024
            elif size == "Varies with device":
                return None
        return None

    df['SizeMB'] = df['Size'].apply(convert_size)
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # ==============================
    # Apply Filters
    # ==============================
    valid_categories = [
        "GAME", "BEAUTY", "BUSINESS", "COMICS",
        "COMMUNICATION", "DATING", "ENTERTAINMENT",
        "SOCIAL", "EVENT"
    ]

    filtered = df[
        (df['Rating'] > 3.5) &
        (df['Category'].isin(valid_categories)) &
        (df['Reviews'] > 500) &
        (~df['App'].str.contains("S", case=False, na=False)) &
        (df['Sentiment_Subjectivity'] > 0.5) &
        (df['Installs'] > 50000)
    ].copy()

    # ==============================
    # Translate Categories
    # ==============================
    category_map = {
        "BEAUTY": "सौंदर्य",      # Hindi
        "BUSINESS": "வணிகம்",   # Tamil
        "DATING": "Dating (DE)"  # German
    }
    filtered['Category'] = filtered['Category'].str.upper().replace(category_map)

    # ==============================
    # Time Restriction (5 PM – 7 PM IST)
    # ==============================
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist)
    current_hour = now_ist.hour

    matplotlib.rcParams['font.family'] = 'Nirmala UI'  # Supports Hindi & Tamil

    if 17 <= current_hour < 19:
        plt.figure(figsize=(12, 8))

        # Assign base palette
        base_palette = sns.color_palette("tab10", n_colors=len(filtered['Category'].unique()))
        palette = dict(zip(filtered['Category'].unique(), base_palette))

        # Force Game category to pink
        for cat in palette.keys():
            if "GAME" in cat:
                palette[cat] = "pink"

        sns.scatterplot(
            data=filtered,
            x="SizeMB",
            y="Rating",
            size="Installs",
            hue="Category",
            sizes=(50, 1000),
            palette=palette,
            alpha=0.6
        )

        plt.title("Bubble Chart: App Size vs Rating (Bubble = Installs)", fontsize=14)
        plt.xlabel("App Size (MB)")
        plt.ylabel("Average Rating")
        plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    else:
        print("[INFO] This graph is only visible between 5 PM and 7 PM IST. Outside this time, it is hidden from dashboard.")

except FileNotFoundError:
    print("[ERROR] CSV file not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print("[ERROR] CSV file is empty.")
except pd.errors.ParserError:
    print("[ERROR] Error parsing CSV file. Please check its format.")
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
