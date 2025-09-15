# 1. Import required libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
import pytz

try:
    get_ipython
    pio.renderers.default = "notebook_connected"
except NameError:
    pio.renderers.default = "browser"

# 2. Load dataset
df = pd.read_csv(r"C:\Users\Tamilarasan K\Downloads\Play Store Project\data\google_play_store_data.csv")

# 3. Clean Installs column (remove + and , then convert to numeric)
df["Installs"] = (
    df["Installs"]
    .astype(str)
    .str.replace("+", "", regex=False)
    .str.replace(",", "", regex=False)
)
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

# 4. Filter out categories starting with A, C, G, S
df = df[~df["Category"].str.startswith(("A", "C", "G", "S"))]

# 5. Group installs by category
category_installs = df.groupby("Category", as_index=False)["Installs"].sum()

# 6. Select Top 5 categories by installs
top5 = category_installs.sort_values("Installs", ascending=False).head(5)

# 7. Add Highlight column for >1M installs
top5["Highlight"] = top5["Installs"].apply(lambda x: "Above 1M" if x > 1_000_000 else "Below 1M")

# 8. Create a bar chart (since no Country column is available for true choropleth)
fig = px.bar(
    top5,
    x="Category",
    y="Installs",
    color="Highlight",
    title="Top 5 App Categories by Global Installs (Filtered)",
    text="Installs",
    color_discrete_map={"Above 1M": "green", "Below 1M": "red"}
)

fig.update_traces(texttemplate="%{text:,}", textposition="outside")
fig.update_layout(xaxis_title="Category", yaxis_title="Total Installs")

# 9. Restrict output to between 6 PM and 8 PM IST
ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist).time()
start_time = datetime.strptime("18:00", "%H:%M").time()
end_time = datetime.strptime("22:00", "%H:%M").time()

if start_time <= current_time <= end_time:
    fig.show()
else:
    print("⏰ The graph is only visible between 6 PM and 8 PM IST.")
