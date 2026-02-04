import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Strategic Asset Management | Olist", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    div.stButton > button {
        width: 100%; border-radius: 4px; height: 3.5em;
        background-color: #1F2937; color: #F3F4F6;
        margin-bottom: 12px; border: 1px solid #374151;
        text-align: left; padding-left: 20px;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background-color: #3B82F6; color: #FFFFFF; border: 1px solid #60A5FA;
    }
    .metric-container {
        background-color: #1F2937; padding: 20px;
        border-radius: 8px; border: 1px solid #374151;
    }
    .insight-card {
        background-color: #111827; padding: 15px;
        border-left: 4px solid #3B82F6; border-radius: 4px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

color_map = {
    'High-Value Asset': '#00FF41',      # Green
    'Growth Asset': '#00F5FF',           # Cyan
    'At-Risk / Low Engagement': '#FACC15', # Yellow
    'Critical Churn': '#EF4444'          # Red
}

# 4. Navigation & Data Loading
if 'segmento' not in st.session_state: 
    st.session_state.segmento = 'Overview'

@st.cache_data
def load_data():
    df = pd.read_csv('olist_rfm_summary.csv')
    
    if 'email' not in df.columns:
        df['email'] = df['customer_id'].str[:8] + "@olist-customer.br"
    
    bins = [0, 0.3, 0.6, 0.8, 1.0]
    labels = ['Critical Churn', 'At-Risk / Low Engagement', 'Growth Asset', 'High-Value Asset']
    df['Status_Estrategico'] = pd.cut(df['prob_alive'], bins=bins, labels=labels)
    return df

df = load_data()

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>MANAGEMENT</h2>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Portfolio Overview"): 
        st.session_state.segmento = 'Overview'
    
    st.markdown("<p style='color: #9CA3AF; font-size: 11px; margin-left: 5px;'>STRATEGIC SEGMENTATION</p>", unsafe_allow_html=True)
    for s in ['High-Value Asset', 'Growth Asset', 'At-Risk / Low Engagement', 'Critical Churn']:
        if st.button(s): 
            st.session_state.segmento = s

if st.session_state.segmento == 'Overview':
    st.title("Strategic Portfolio Overview")
    
    # KPIs Row
    c1, c2, c3, c4 = st.columns(4)
    total_clv = df['clv_12m'].sum()
    c1.metric("Projected Revenue (12m)", f"R$ {total_clv:,.0f}")
    c2.metric("Portfolio Health Score", f"{df['prob_alive'].mean()*100:.1f}%")
    
    revenue_at_risk = df[df['prob_alive'] < 0.6]['clv_12m'].sum()
    c3.metric("Capital at Risk", f"R$ {revenue_at_risk:,.0f}", delta=f"-{(revenue_at_risk/total_clv)*100:.1f}%")
    c4.metric("VIP Assets Count", len(df[df['Status_Estrategico'] == 'High-Value Asset']))

    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        fig = px.scatter(
            df, x="prob_alive", y="clv_12m", color="Status_Estrategico",
            title="Asset Value vs. Survival Probability Matrix",
            labels={'prob_alive': 'Survival Probability', 'clv_12m': 'Projected CLV'},
            color_discrete_map=color_map
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FFFFFF")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Business Intelligence Insights")
        
        top_10_perc_count = int(len(df) * 0.1)
        top_10_val = (df.sort_values('clv_12m', ascending=False).head(top_10_perc_count)['clv_12m'].sum() / total_clv) * 100
        st.markdown(f"""<div class='insight-card'>
            <strong>Pareto Efficiency</strong><br>
            Top 10% of customers generate {top_10_val:.1f}% of projected revenue. High dependency on top-tier assets.
        </div>""", unsafe_allow_html=True)

        recovery_val = df[df['Status_Estrategico'] == 'At-Risk / Low Engagement']['clv_12m'].sum()
        st.markdown(f"""<div class='insight-card'>
            <strong>Recovery Opportunity</strong><br>
            Targeting 'At-Risk' assets could recover up to R$ {recovery_val:,.0f} in annual revenue.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Regional Revenue Projection")
    col_geo_left, col_geo_right = st.columns([2, 1])

    with col_geo_left:
        state_data = df.groupby('state')['clv_12m'].sum().reset_index().sort_values('clv_12m', ascending=True).tail(10)
        fig_bar = px.bar(
            state_data, x='clv_12m', y='state', orientation='h',
            title="Top 10 States by Projected Sales",
            labels={'clv_12m': 'Projected Revenue', 'state': 'State'},
            color_discrete_sequence=['#3B82F6']
        )
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FFFFFF")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_geo_right:
        st.subheader("Regional Intelligence")
        top_state = state_data.iloc[-1]['state']
        st.markdown(f"""<div class='insight-card' style='border-left-color: #00F5FF;'>
            <strong>Market Leader: {top_state}</strong><br>
            Highest revenue density detected. Prioritize local fulfillment centers and specialized logistics in this state.
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div class='insight-card' style='border-left-color: #FACC15;'>
            <strong>Regional Expansion</strong><br>
            The top 5 states represent the core of your cash flow. Consider regional-specific marketing campaigns to reduce CAC.
        </div>""", unsafe_allow_html=True)

else:
    seg = st.session_state.segmento
    color_block = color_map.get(seg, '#3B82F6')
    df_seg = df[df['Status_Estrategico'] == seg].sort_values('clv_12m', ascending=False)
    
    col_title, col_download = st.columns([3, 1])
    with col_title:
        st.title(f"Segment Analysis: {seg}")
    with col_download:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_seg.to_excel(writer, index=False, sheet_name='Strategic_Report')
        processed_data = output.getvalue()
        
        st.download_button(
            label="DOWNLOAD REPORT",
            data=processed_data,
            file_name=f'strategic_report_{seg.replace(" ", "_").lower()}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    recom_dict = {
        'High-Value Asset': {
            'diag': 'Critical high-margin assets. Low price sensitivity.',
            'recom': 'Focus on dedicated Customer Success. Prioritize exclusive access and early-bird benefits.',
            'kpi': 'Maintain Survival Prob > 0.90'
        },
        'Growth Asset': {
            'diag': 'High purchase frequency. High potential to scale AOV.',
            'recom': 'Execute cross-selling campaigns. Implement volume-based free shipping thresholds.',
            'kpi': 'Increase CLV by 15% via Upselling'
        },
        'At-Risk / Low Engagement': {
            'diag': 'Significant decline in engagement. High risk of competitor migration.',
            'recom': 'Deploy immediate churn-prevention incentives. Personalized "We Miss You" offers.',
            'kpi': 'Stabilize Survival Probability'
        },
        'Critical Churn': {
            'diag': 'Technically lost assets. Acquisition cost is lower than recovery cost.',
            'recom': 'Perform Root Cause Analysis. Use automated win-back emails only.',
            'kpi': 'Churn Reason Documentation'
        }
    }

    info = recom_dict[seg]
    st.markdown(f"""
        <div style='background-color: #111827; padding: 25px; border-left: 5px solid {color_block}; border-radius: 8px;'>
            <h4 style='color: {color_block}; margin-top: 0;'>Strategic Roadmap</h4>
            <p><strong>Diagnosis:</strong> {info['diag']}</p>
            <p><strong>Recommendation:</strong> {info['recom']}</p>
            <p><strong>Target KPI:</strong> <span style='color: {color_block}'>{info['kpi']}</span></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### Operational Detail: Top 100 {seg} Contacts")
    st.dataframe(df_seg[['customer_id', 'email', 'clv_12m', 'prob_alive', 'state']].head(100), use_container_width=True)