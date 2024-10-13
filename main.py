import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# Step 1: Load Data (manually added for this example)
data = {
    'AGENCY': ['MD HEALTH CARE LLC', 'Brigham Home Care Services, Inc.', 'Peace and Harmony Homecare LLC', 
               'Omega Homecare Systems, Inc', 'CORNERSTONE HEALTHCARE SYSTEMS LLC', 
               'Pinnacle Health Services Inc.', 'Luna Vista Home Healthcare', 
               'LA FAMILIA HEALTH, INC.', 'KAL HOME HEALTH INC', 'Century Home Healthcare Services LLC', 'Total'],
    'DA_UNSIGNED': [62, 3042, 14, 31, 42, 1, 179, 364, 1, 46, 3782],
    'DA_PREPARED_3M': [38, 8, 6, 4, 7, 0, 24, 0, 0, 0, 87],
    'RPA_DB_UNSIGNED': [3, 1, 1, 0, 2, 0, 4, 0, 0, 0, 11],
    'EHR_SIGNED': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    'DA_FILED': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Step 2: Calculate Totals
total_unsigned = df['DA_UNSIGNED'].sum()
total_prepared = df['DA_PREPARED_3M'].sum()
total_rpa_db_unsigned = df['RPA_DB_UNSIGNED'].sum()
total_ehr_signed = df['EHR_SIGNED'].sum()

# Step 3: Create Visualizations using Plotly with dark violet colors
fig1 = px.bar(df[:-1], x='AGENCY', y='DA_UNSIGNED', title='DA Unsigned per Agency', 
              labels={'DA_UNSIGNED': 'DA Unsigned'}, color_discrete_sequence=['#4B0082'])  # Dark violet

fig2 = px.bar(df[:-1], x='AGENCY', y='DA_PREPARED_3M', title='DA Prepared in Last 3 Months', 
              labels={'DA_PREPARED_3M': 'DA Prepared (3M)'}, color_discrete_sequence=['#4B0082'])  # Dark violet

fig3 = px.bar(df[:-1], x='AGENCY', y='RPA_DB_UNSIGNED', title='RPA DB Unsigned per Agency', 
              labels={'RPA_DB_UNSIGNED': 'RPA DB Unsigned'}, color_discrete_sequence=['#4B0082'])  # Dark violet

fig4 = px.pie(df[:-1], values='EHR_SIGNED', names='AGENCY', title='EHR Signed Distribution', 
              color_discrete_sequence=px.colors.qualitative.Pastel)

# Total Summary Pie Chart
totals_pie_data = {
    'Category': ['DA Unsigned', 'DA Prepared 3M', 'RPA DB Unsigned', 'EHR Signed'],
    'Total': [total_unsigned, total_prepared, total_rpa_db_unsigned, total_ehr_signed]
}
totals_pie_df = pd.DataFrame(totals_pie_data)
fig_totals_pie = px.pie(totals_pie_df, values='Total', names='Category', title='Total Summary', 
                        color_discrete_sequence=['#4B0082', '#6A5ACD', '#8A2BE2', '#9370DB'])  # Dark violet and light colors

# Step 4: Create Dash Layout with Text Boxes and Background
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([

    # Header
    dbc.Row([ 
        dbc.Col(html.H1("Agency DA Dashboard", className="text-center mb-4"), width=12)
    ], style={"background-color": "#FFA500"}),  # Orange background

    # Metrics Row
    dbc.Row([
        dbc.Col(html.Div([
            html.H4("Total DA Unsigned"),
            html.H2(f"{total_unsigned}", className="text-info")
        ], className="text-center bg-light p-3"), width=3),

        dbc.Col(html.Div([
            html.H4("Total DA Prepared (3M)"),
            html.H2(f"{total_prepared}", className="text-success")
        ], className="text-center bg-light p-3"), width=3),

        dbc.Col(html.Div([
            html.H4("Total RPA DB Unsigned"),
            html.H2(f"{total_rpa_db_unsigned}", className="text-warning")
        ], className="text-center bg-light p-3"), width=3),

        dbc.Col(html.Div([
            html.H4("Total EHR Signed"),
            html.H2(f"{total_ehr_signed}", className="text-primary")
        ], className="text-center bg-light p-3"), width=3)
    ], className="mb-4", style={"background-color": "#FFB6C1"}),  # Light pink background for metrics

    # Row 1: First two charts (Bar Chart and Bar Chart)
    dbc.Row([
        dbc.Col(dcc.Graph(id='da-unsigned', figure=fig1), width=6),
        dbc.Col(dcc.Graph(id='da-prepared', figure=fig2), width=6)
    ], className="mb-4", style={"background-color": "#FFB6C1"}),  # Light pink background for graphs

    # Row 2: Last two charts (Bar Chart and Pie Chart)
    dbc.Row([
        dbc.Col(dcc.Graph(id='rpa-db-unsigned', figure=fig3), width=6),
        dbc.Col(dcc.Graph(id='ehr-signed', figure=fig4), width=6)
    ], className="mb-4", style={"background-color": "#FFB6C1"}),  # Light pink background for graphs

    # Total Summary Pie Chart
    dbc.Row([
        dbc.Col(dcc.Graph(id='totals-pie-chart', figure=fig_totals_pie), width=12)
    ], className="mb-4", style={"background-color": "#FFB6C1"}),  # Light pink background for the pie chart

    # Footer
    dbc.Row([ 
        dbc.Col(html.P("Data Source: Agency Dashboard Data", className="text-center"))
    ], className="mt-4")
], fluid=True, style={"background-color": "#FFA500"})  # Orange background for the entire page

# Step 5: Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)