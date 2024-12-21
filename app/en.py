import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(page_title="University Data Filter", layout="wide")

# Cache the data loading step
@st.cache_resource
def load_data():
    return pd.read_csv('topuniversities.csv')

df = load_data()

# Set up the sidebar for filters
st.sidebar.title('Filters')
filter_by = st.sidebar.selectbox('Filter by:', ['City', 'University Name'])

# Initialize filtered_df
filtered_df = df  # Default to full dataset

# Apply filter based on user selection
if filter_by == 'City':
    selected_city = st.sidebar.selectbox('Select City:', df['City'].unique())
    filtered_df = df[df['City'] == selected_city]
elif filter_by == 'University Name':
    selected_university = st.sidebar.selectbox('Select University Name:', df['University Name'].unique())
    filtered_df = df[df['University Name'] == selected_university]

# Main page title
st.title('University Data Explorer')

# Display filter criteria
st.write(f'Filtered by **{filter_by}**: **{selected_city if filter_by == "City" else selected_university}**')

# Check if filtered data is not empty
if not filtered_df.empty:
    # DataFrame display in one column
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Styled DataFrame
        styled_df = filtered_df.style.highlight_max(axis=0)
        st.dataframe(styled_df)
    
    with col2:
        # Create an interactive chart
        chart_data = filtered_df[['University Name', 'Overall Score', 'Citations per Paper']]
        chart = alt.Chart(chart_data).mark_bar().encode(
            x='University Name',
            y='Overall Score',
            color='Citations per Paper'
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name='filtered_university_data.csv',
        mime='text/csv',
    )
else:
    st.warning('No data matches the selected filter.')