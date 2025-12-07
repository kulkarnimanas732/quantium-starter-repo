import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load processed data
df = pd.read_csv("data/pink_morsel_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Available regions for filter
regions = ["north", "east", "south", "west", "all"]

app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

# Layout
app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={
                "textAlign": "center",
                "color": "#ff4f79",
                "fontFamily": "Arial",
                "marginTop": "30px",
            },
        ),
        
        html.P(
            "View daily Pink Morsel sales before and after the price increase on 15 January 2021.",
            style={
                "textAlign": "center",
                "color": "#444",
                "fontSize": "18px",
                "marginBottom": "30px",
            },
        ),

        # Radio Buttons
        html.Div(
            children=[
                html.Label(
                    "Select Region:",
                    style={"fontSize": "18px", "fontWeight": "bold"},
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[{"label": region.capitalize(), "value": region} for region in regions],
                    value="all",
                    inline=True,
                    style={
                        "padding": "10px",
                        "marginBottom": "20px",
                        "fontSize": "16px",
                    },
                ),
            ],
            style={
                "textAlign": "center",
                "marginBottom": "20px",
                "backgroundColor": "#f8f8f8",
                "padding": "10px",
                "borderRadius": "8px",
                "width": "60%",
                "marginLeft": "auto",
                "marginRight": "auto",
            },
        ),

        # Graph
        html.Div(
            dcc.Graph(
                id="sales-chart"
            ),
            style={"padding": "20px"}
        ),
    ],
    style={"maxWidth": "1000px", "margin": "0 auto"},
)

# CALLBACK: Update graph when selecting region
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    # Filter data
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["Region"] == selected_region]

    # Aggregate by date
    daily_sales = (
        filtered_df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    # Build line chart
    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title=f"Sales Trend ({selected_region.capitalize()} Region)" if selected_region != "all" else "Sales Trend (All Regions)",
        labels={"Date": "Date", "Sales": "Total Sales"},
    )

    fig.update_layout(
        plot_bgcolor="#fdfdfd",
        paper_bgcolor="#ffffff",
        title_font_size=24,
        title_font_color="#ff4f79",
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
