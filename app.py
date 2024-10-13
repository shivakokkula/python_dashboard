import pandas as pd
import plotly.express as px
import streamlit as st

# Step 1: Define Constants
AGENCY_NAMES = [
    'MD HEALTH CARE LLC', 
    'Brigham Home Care Services, Inc.', 
    'Peace and Harmony Homecare LLC', 
    'Omega Homecare Systems, Inc', 
    'CORNERSTONE HEALTHCARE SYSTEMS LLC', 
    'Pinnacle Health Services Inc.', 
    'Luna Vista Home Healthcare', 
    'LA FAMILIA HEALTH, INC.', 
    'KAL HOME HEALTH INC', 
    'Century Home Healthcare Services LLC', 
    'Total'
]

DA_UNSIGNED_VALUES = [62, 3042, 14, 31, 42, 1, 179, 364, 1, 46, 3782]
DA_PREPARED_3M_VALUES = [38, 8, 6, 4, 7, 0, 24, 0, 0, 0, 87]
RPA_FOUND_VALUES = [3, 1, 1, 0, 2, 0, 4, 0, 0, 0, 11]
EHR_SIGNED_VALUES = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]

# Colors
# GRAPH = '#4B0082'
GRAPH = '#4B0082'
GRAPH_BG = 'white'
BODY_BG = '#E6E6FA'
# BODY_BG = '#FFDBBB'

# Step 2: Load Data into DataFrame
data = {
    'AGENCY': AGENCY_NAMES,
    'DA_UNSIGNED': DA_UNSIGNED_VALUES,
    'DA_PREPARED_3M': DA_PREPARED_3M_VALUES,
    'RPA_FOUND': RPA_FOUND_VALUES,
    'EHR_SIGNED': EHR_SIGNED_VALUES,
    'DA_FILED': [0] * len(AGENCY_NAMES)  # Assuming all filed are zero
}

df = pd.DataFrame(data)

# Step 3: Calculate Totals
totals = {
    "unsigned": df['DA_UNSIGNED'].sum(),
    "prepared": df['DA_PREPARED_3M'].sum(),
    "rpa_found": df['RPA_FOUND'].sum(),
    "ehr_signed": df['EHR_SIGNED'].sum()
}

# Step 4: Create Visualizations
def create_bar_chart(y_data, title):
    return px.bar(df, x='AGENCY', y=y_data, title=title, 
                  labels={y_data: title}, 
                  color_discrete_sequence=[GRAPH] * len(df))

# Create bar charts
fig1 = create_bar_chart('DA_UNSIGNED', 'DA Unsigned per Agency')
fig2 = create_bar_chart('DA_PREPARED_3M', 'DA Prepared in Last 3 Months')
fig3 = create_bar_chart('RPA_FOUND', 'RPA DB Unsigned per Agency')
fig4 = create_bar_chart('EHR_SIGNED', 'EHR Signed per Agency')
fig5 = create_bar_chart('DA_FILED', 'DA Filed per Agency')

# Set the font color to black for all figures
for fig in [fig1, fig2, fig3, fig4, fig5]:
    fig.update_layout(plot_bgcolor=GRAPH_BG, paper_bgcolor=GRAPH_BG, font=dict(color='black'))

# Total Summary Pie Chart
totals_pie_data = {
    'Category': ['DA Unsigned', 'DA Prepared 3M', 'RPA DB Unsigned', 'EHR Signed'],
    'Total': list(totals.values())
}
totals_pie_df = pd.DataFrame(totals_pie_data)
fig_totals_pie = px.pie(totals_pie_df, values='Total', names='Category', title='Total Summary', 
                         color_discrete_sequence=[GRAPH, '#6A5ACD', '#8A2BE2', '#9370DB'])
fig_totals_pie.update_layout(plot_bgcolor=GRAPH_BG, paper_bgcolor=GRAPH_BG, font=dict(color='black'))

# Step 5: Set up the Streamlit Layout
st.set_page_config(page_title="Agency DA Dashboard", layout="wide")

# Background color for the body
st.markdown(
    f"""
    <style>
    body {{
        background-color: {BODY_BG};  /* Light orange background */
        color: #333;
        margin: 0;  /* Remove default margin */
        padding: 0; /* Remove default padding */
    }}
    .stApp {{
        background-color: {BODY_BG};  /* Set Streamlit app background */
    }}
    .metric-container {{
        border: 2px solid {GRAPH}; /* Dark violet border */
        border-radius: 10px;  /* Rounded corners */
        padding: 10px;  /* Padding around the text */
        background-color: #ffffff;  /* White background for metrics */
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);  /* Shadow effect */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Row 1: Display totals with boxes
col1, col2, col3, col4 = st.columns(4)
for col, key in zip([col1, col2, col3, col4], totals.keys()):
    with col:
        st.markdown("<h3 class='metric-container'>"+key.replace('total_', '').replace('_', ' ').upper()+" : "+str(totals[key])+"</h3>", unsafe_allow_html=True)

# Graph Background
graph_bg = f"""
<style>
    .plotly-graph-div {{
        background-color: {GRAPH_BG};  /* Graph background */
        border-radius: 10px;  /* Rounded corners */
    }}
</style>
"""
st.markdown(graph_bg, unsafe_allow_html=True)

# Create columns for charts
col1, col2, col3 = st.columns(3)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)
col3.plotly_chart(fig3, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.plotly_chart(fig_totals_pie, use_container_width=True)
col2.plotly_chart(fig4, use_container_width=True)  # EHR Signed Chart
col3.plotly_chart(fig5, use_container_width=True)  # DA Filed Chart