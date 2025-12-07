import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# 1. Load the processed data
# Make sure this file exists: data/pink_morsel_sales.csv
df = pd.read_csv("data/pink_morsel_sales.csv")

# 2. Convert Date column to datetime and sort
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# 3. Aggregate sales by date (sum over all regions)
daily_sales = (
    df.groupby("Date", as_index=False)["Sales"]
    .sum()
    .sort_values("Date")
)

# 4. Create line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Daily Sales of Pink Morsels",
    labels={
        "Date": "Date",
        "Sales": "Total Sales (Revenue)"
    }
)

# 5. Build Dash app
app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={
                "textAlign": "center",
                "marginBottom": "10px",
                "marginTop": "20px"
            }
        ),
        html.P(
            "Daily sales of Pink Morsels before and after the price increase on 15 January 2021.",
            style={
                "textAlign": "center",
                "marginBottom": "30px"
            }
        ),
        dcc.Graph(
            id="pink-morsel-sales-chart",
            figure=fig
        ),
    ],
    style={"maxWidth": "900px", "margin": "0 auto"}
)

if __name__ == "__main__":
    app.run(debug=True)
