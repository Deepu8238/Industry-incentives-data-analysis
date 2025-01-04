import pandas as pd
import streamlit as st
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Industry Incentives Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load the dataset
@st.cache_data
def load_data():
    file_path = 'ts_industry_incentives_01-12-2024_31-12-2024.csv'
    data = pd.read_csv(file_path)
    return data

# Load data
try:
    data = load_data()

    # Title and description
    st.title('📊 Telangana Industry Incentives Dashboard')
    st.markdown('---')

    # Key Metrics Overview
    st.header('Key Metrics Overview')
    total_incentives = len(data)
    unique_districts = data['district'].nunique()
    unique_incentives = data['incentive_name'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incentives", f"{total_incentives:,}")
    col2.metric("Unique Districts", f"{unique_districts}")
    col3.metric("Unique Incentive Types", f"{unique_incentives}")

    # Incentives by District
    st.markdown('---')
    st.header('Incentives by District')
    district_data = data['district'].value_counts().reset_index()
    district_data.columns = ['District', 'Number of Incentives']
    fig = px.bar(district_data, x='District', y='Number of Incentives',
                 title='Number of Incentives by District',
                 labels={'Number of Incentives': 'Number of Incentives', 'District': 'District'},
                 hover_data=['District'])
    st.plotly_chart(fig, use_container_width=True)

    # Incentive Distribution by Type
    st.markdown('---')
    st.header('Incentive Distribution by Type')
    incentive_data = data['incentive_name'].value_counts().reset_index()
    incentive_data.columns = ['Incentive Type', 'Count']
    fig = px.pie(incentive_data, names='Incentive Type', values='Count',
                 title='Distribution of Incentives by Type',
                 hover_data=['Count'])
    st.plotly_chart(fig, use_container_width=True)

  
    # Incentive Distribution Across Mandals
    st.markdown('---')
    st.header('Incentive Distribution Across Mandals')
    mandal_data = data['mandal'].value_counts().reset_index()
    mandal_data.columns = ['Mandal', 'Number of Incentives']
    fig = px.bar(mandal_data, x='Mandal', y='Number of Incentives',
                 title='Number of Incentives by Mandal',
                 labels={'Number of Incentives': 'Number of Incentives', 'Mandal': 'Mandal'},
                 hover_data=['Mandal'])
    st.plotly_chart(fig, use_container_width=True)

    # Top Incentive Types by District
    st.markdown('---')
    st.header('Top Incentive Types by District')
    top_incentives = data.groupby(['district', 'incentive_name']).size().reset_index(name='Count')
    selected_district_for_top = st.selectbox('Select District for Top Incentives', ['All'] + list(data['district'].unique()))
    filtered_top_incentives = top_incentives if selected_district_for_top == 'All' else top_incentives[top_incentives['district'] == selected_district_for_top]

    fig = px.bar(filtered_top_incentives, x='incentive_name', y='Count', color='district',
                 title=f'Top Incentives in {selected_district_for_top}' if selected_district_for_top != 'All' else 'Top Incentives by District',
                 labels={'incentive_name': 'Incentive Type', 'Count': 'Number of Incentives', 'district': 'District'},
                 hover_data=['district'])
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please ensure the dataset is correctly formatted and accessible.")
