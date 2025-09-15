import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
import pytz

# Universal renderer: works in notebook + .py
try:
    get_ipython
    pio.renderers.default = "notebook_connected"
except NameError:
    pio.renderers.default = "browser"

# Load dataset
df = pd.read_csv(r"C:\Users\Tamilarasan K\Downloads\Play Store Project\data\google_play_store_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Clean and convert Installs
df['Installs'] = pd.to_numeric(df['Installs'].str.replace(r'[+,]', '', regex=True), errors='coerce')

# Clean and convert Price
df['Price'] = pd.to_numeric(df['Price'].str.replace(r'[$]', '', regex=True), errors='coerce')

# Convert Size to MB
def size_to_mb(size_str):
    if pd.isna(size_str):
        return None
    size_str = str(size_str).strip()
    if size_str.endswith('M'):
        return float(size_str[:-1])
    elif size_str.endswith('k'):
        return float(size_str[:-1]) / 1024
    elif size_str.endswith('G'):
        return float(size_str[:-1]) * 1024
    else:
        return None

df['Size_MB'] = df['Size'].apply(size_to_mb)

# Extract and clean Android Version
df['Android_Ver'] = pd.to_numeric(df['Android Ver'].str.extract(r'(\d+\.\d+)')[0], errors='coerce')

# Strip spaces from Type column
df['Type'] = df['Type'].str.strip()

# Revenue calculation
df['Revenue'] = df['Price'] * df['Installs']

# === Filter separately for Free and Paid ===
df_free = df[
    (df['Type'] == 'Free') &
    (df['Installs'] >= 10000) &
    (df['Android_Ver'] > 4.0) &
    (df['Size_MB'] > 15) &
    (df['Content Rating'] == "Everyone") &
    (df['App'].str.len() <= 30)
]

df_paid = df[
    (df['Type'] == 'Paid') &
    (df['Installs'] >= 10000) &
    (df['Revenue'] >= 10000) &  # Keep revenue filter for Paid
    (df['Android_Ver'] > 4.0) &
    (df['Size_MB'] > 15) &
    (df['Content Rating'] == "Everyone") &
    (df['App'].str.len() <= 30)
]

# Combine them
filtered = pd.concat([df_free, df_paid], ignore_index=True)

# Get top 3 categories
top_categories = filtered['Category'].value_counts().head(3).index.tolist()
filtered_top = filtered[filtered['Category'].isin(top_categories)]

# Create pivot tables
installs_pivot = filtered_top.pivot_table(index='Category', columns='Type', values='Installs', aggfunc='mean')
revenue_pivot = filtered_top.pivot_table(index='Category', columns='Type', values='Revenue', aggfunc='mean')

# Current IST time
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)
current_hour = current_time.hour

if 13 <= current_hour < 14:  # 1 PM - 2 PM IST
    fig = go.Figure()

    # Add Avg Installs (Bars)
    for t in ['Free', 'Paid']:
        if t in installs_pivot.columns:
            fig.add_trace(go.Bar(
                x=installs_pivot.index,
                y=installs_pivot[t],
                name=f'Avg Installs ({t})',
                yaxis='y1',
                offsetgroup=t
            ))

    # Add Avg Revenue (Lines)
    for t in ['Free', 'Paid']:
        if t in revenue_pivot.columns:
            fig.add_trace(go.Scatter(
                x=revenue_pivot.index,
                y=revenue_pivot[t],
                name=f'Avg Revenue ({t})',
                yaxis='y2',
                mode='lines+markers'
            ))

    # Layout
    fig.update_layout(
        title='Average Installs vs Revenue (Free vs Paid) for Top 3 Categories',
        xaxis_title='Category',
        yaxis=dict(title='Average Installs', showgrid=False, side='left'),
        yaxis2=dict(title='Average Revenue', overlaying='y', side='right'),
        barmode='group'
    )

    fig.show()
else:
    print("Graph is visible only between 1 PM and 2 PM IST.")




