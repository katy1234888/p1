import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Seashells Logistic | Festive Surge Diagnostic",
    page_icon="🐚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Branding and Design
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #1E3A8A;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .story-text {
        font-size: 1.1rem;
        color: #4B5563;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar: Navigation & Data Upload ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/shipping-container.png", width=80)
    st.title("Seashells Logistic")
    st.info("Logistics Intelligence Portal")
    
    st.markdown("---")
    menu = st.radio(
        "Navigation",
        ["The Grand Overview", "Customer Pulse (NPS)", "Operational Deep-Dive", "Recovery Roadmap"]
    )
    
    st.markdown("---")
    st.subheader("📁 Data Source")
    uploaded_files = st.file_uploader(
        "Upload Logistics CSVs", 
        type="csv", 
        accept_multiple_files=True,
        help="Upload orders.csv, nps.csv, hub_performance.csv, etc."
    )

# Helper function to load data
def load_data(files):
    data_dict = {}
    if files:
        for file in files:
            name = file.name.lower()
            if 'order' in name: data_dict['orders'] = pd.read_csv(file)
            elif 'nps' in name: data_dict['nps'] = pd.read_csv(file)
            elif 'hub' in name: data_dict['hubs'] = pd.read_csv(file)
            elif 'courier' in name: data_dict['couriers'] = pd.read_csv(file)
            elif 'complaint' in name: data_dict['complaints'] = pd.read_csv(file)
    return data_dict

data = load_data(uploaded_files)

# Fallback: Warning if no data
if not data:
    st.warning("Please upload the diagnostic CSV files in the sidebar to populate the story.")
    st.stop()

# --- Pre-processing Logic ---
if 'orders' in data:
    data['orders']['order_date'] = pd.to_datetime(data['orders']['order_date'])
    data['orders']['month'] = data['orders']['order_date'].dt.strftime('%B')

# --- Chapter 1: The Grand Overview ---
if menu == "The Grand Overview":
    st.title("🚢 The Storm After the Surge")
    st.markdown("""
    <p class='story-text'>Between October and December, <b>Seashells Logistic</b> faced an unprecedented 
    volume of festive orders. While the sales team celebrated, our infrastructure buckled. 
    This diagnostic reveals the scale of the failure and the path to stability.</p>
    """, unsafe_allow_html=True)

    # Hero KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Net Promoter Score", "-63.7", delta="-42% vs Q3", delta_color="inverse")
    with col2:
        st.metric("Avg. SLA Breach", "65.4%", delta="Critical", delta_color="inverse")
    with col3:
        st.metric("Tier-2 RTO Rate", "23.1%", delta="High Risk", delta_color="inverse")
    with col4:
        st.metric("Late Deliveries", "842", delta="Volume Spike")

    # Volume Chart
    st.subheader("The Festive Volume Tsunami")
    if 'orders' in data:
        vol_chart = data['orders'].groupby('month').size().reset_index(name='Orders')
        # Simple sorting for month order
        m_order = ['October', 'November', 'December']
        vol_chart['month'] = pd.Categorical(vol_chart['month'], categories=m_order, ordered=True)
        vol_chart = vol_chart.sort_values('month')
        
        fig = px.area(vol_chart, x='month', y='Orders', 
                      title="Order Volume Trend (Oct-Dec)",
                      color_discrete_sequence=['#1E3A8A'])
        fig.update_layout(plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

# --- Chapter 2: Customer Pulse (NPS) ---
elif menu == "Customer Pulse (NPS)":
    st.title("🗣️ The Voice of the Customer")
    st.markdown("<p class='story-text'>Numbers don't lie, but words hurt. Our NPS plummeted as customers faced 'Fake Delivery' attempts and silence.</p>", unsafe_allow_html=True)

    if 'nps' in data:
        # NPS Distribution
        fig_nps = px.histogram(data['nps'], x='score', nbins=11, 
                               title="NPS Score Distribution",
                               color_discrete_sequence=['#EF4444'])
        fig_nps.add_vrect(x0=0, x1=6, fillcolor="red", opacity=0.1, annotation_text="Detractors")
        fig_nps.add_vrect(x0=9, x1=10, fillcolor="green", opacity=0.1, annotation_text="Promoters")
        st.plotly_chart(fig_nps, use_container_width=True)

        # Feedback Analysis
        st.subheader("Common Complaint Themes")
        feedback_counts = data['nps']['feedback_text'].value_counts().reset_index()
        fig_feed = px.bar(feedback_counts, x='feedback_text', y='count', 
                          color='count', color_continuous_scale='Reds')
        st.plotly_chart(fig_feed, use_container_width=True)

# --- Chapter 3: Operational Deep-Dive ---
elif menu == "Operational Deep-Dive":
    st.title("⚙️ Operational Bottlenecks")
    
    tab1, tab2 = st.tabs(["City/Hub Performance", "Courier Efficiency"])
    
    with tab1:
        if 'hubs' in data:
            st.subheader("Tier-2 Cities: The Weakest Link")
            # Calculate breach percentage
            data['hubs']['Breach Rate'] = (1 - (data['hubs']['on_time_delivery'] / data['hubs']['total_orders'])) * 100
            fig_hub = px.bar(data['hubs'].sort_values('Breach Rate', ascending=False), 
                             x='city', y='Breach Rate', color='city',
                             title="SLA Breach Rate by Hub (%)")
            st.plotly_chart(fig_hub, use_container_width=True)
            
            st.info("💡 Indore and Nagpur hubs exceeded 83% breach rates due to capacity exhaustion.")

    with tab2:
        if 'couriers' in data:
            st.subheader("Partner Accountability Matrix")
            fig_courier = px.scatter(data['couriers'], x='avg_delivery_time', y='sla_breach_rate',
                                     size='complaint_rate', color='courier_partner',
                                     hover_name='courier_partner',
                                     title="Delivery Time vs. SLA Breach (Size = Complaint Rate)")
            st.plotly_chart(fig_courier, use_container_width=True)

# --- Chapter 4: Recovery Roadmap ---
elif menu == "Recovery Roadmap":
    st.title("🚀 The Path to +20 NPS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("### Quick Wins (30 Days)")
        st.markdown("""
        - **Dynamic SLA Buffers**: Add 48-72h to ETAs during spikes.
        - **'Delayed but Safe' SMS**: Proactive communication before breach.
        - **Partner Re-allocation**: Shift Indore/Nagpur volume from QuickShip to local heroes.
        """)
        
    with col2:
        st.info("### Long-Term Strategy")
        st.markdown("""
        - **Hub Automation**: Sorting tech in Nagpur & Indore.
        - **Loyalty Recovery**: Targeted vouchers for festive detractors.
        - **Real-time Monitoring**: Dashboard for failed attempt tracking.
        """)

    st.subheader("Projected KPI Recovery")
    roadmap_data = pd.DataFrame({
        "Month": ["Dec (Actual)", "Jan (Proj)", "Feb (Proj)", "Mar (Proj)"],
        "NPS": [-63, -40, -10, 20],
        "SLA Compliance": [35, 55, 75, 92]
    })
    fig_proj = go.Figure()
    fig_proj.add_trace(go.Scatter(x=roadmap_data['Month'], y=roadmap_data['NPS'], name="NPS Improvement", line=dict(color='firebrick', width=4)))
    fig_proj.add_trace(go.Scatter(x=roadmap_data['Month'], y=roadmap_data['SLA Compliance'], name="SLA Compliance %", line=dict(color='royalblue', width=4)))
    st.plotly_chart(fig_proj, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Seashells Logistic Pvt Ltd | Data Analytics Division")
