import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(
    page_title="Bank Jatim Financial Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== WARNA CORPORATE BANK JATIM ==========
# Berdasarkan analisis identitas visual
PRIMARY_RED = "#D92B2B"      # Merah utama dari logo
DARK_BLUE = "#001C56"        # Biru tua untuk header
LIGHT_GRAY = "#F0F0F0"       # Abu-abu untuk background
WHITE = "#FFFFFF"
BLACK = "#000000"

# ========== DATA SAMPLE (DARI LAPORAN 2024) ==========
# Data ini bisa diganti dengan koneksi database/file CSV
financial_data = pd.DataFrame({
    'Tahun': [2020, 2021, 2022, 2023, 2024],
    'Total Aset (Triliun Rp)': [83.62, 100.72, 103.03, 103.85, 118.14],
    'Laba Bersih (Triliun Rp)': [1.49, 1.52, 1.54, 1.47, 1.30],
    'Total Kredit (Triliun Rp)': [40.03, 40.92, 44.88, 53.40, 73.24],
    'DPK (Triliun Rp)': [66.79, 81.39, 79.93, 78.20, 90.01],
    'NPL Gross (%)': [4.00, 4.48, 2.83, 2.49, 3.45],
    'ROA (%)': [1.95, 2.05, 1.95, 1.87, 1.60],
    'ROE (%)': [18.77, 17.26, 16.24, 13.96, 11.89],
    'BOPO (%)': [77.76, 75.95, 76.15, 77.27, 81.89],
    'LDR (%)': [60.58, 51.38, 56.50, 70.03, 82.05],
    'CAR (%)': [21.64, 23.52, 24.74, 25.71, 23.49]
})

# Data untuk per segmen (2024)
segment_data = pd.DataFrame({
    'Segmen': ['Kredit Mikro', 'Kredit Ritel & Menengah', 'Kredit Korporasi', 'Kredit Konsumer'],
    'Nilai (Triliun Rp)': [9.33, 11.18, 7.38, 33.37],
    'Pertumbuhan (%)': [39.77, 68.56, 8.35, 10.29],
    'Target 2025 (Triliun Rp)': [12.1, 14.5, 8.0, 36.0]
})

# ========== HEADER DASHBOARD ==========
with col1:
    import os
    
    # Cek apakah file ada di beberapa lokasi umum
    logo_found = False
    
    # Coba lokasi untuk Streamlit Cloud
    if os.path.isfile("logo_bankjatim.png"):
        st.image("logo_bankjatim.png", width=120)
        logo_found = True
    elif os.path.isfile("./logo_bankjatim.png"):
        st.image("./logo_bankjatim.png", width=120)
        logo_found = True
    
    # Jika tidak ketemu, tampilkan placeholder
    if not logo_found:
        st.warning("Logo file not found, using placeholder")
        st.markdown("""
        <div style="background-color: #D92B2B; padding: 15px; border-radius: 10px; text-align: center;">
            <h3 style="color: white; margin: 0;">BANK</h3>
            <h3 style="color: white; margin: 0;">JATIM</h3>
        </div>
        """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style="background-color: {DARK_BLUE}; padding: 25px; border-radius: 10px;">
        <h1 style="color: white; margin: 0; font-size: 32px;">Strategic Performance Management</h1>
        <h2 style="color: {PRIMARY_RED}; margin: 5px 0 0 0; font-size: 24px;">Financial Report Dashboard</h2>
        <p style="color: {LIGHT_GRAY}; margin: 10px 0 0 0;">PT Bank Pembangunan Daerah Jawa Timur Tbk | Laporan Konsolidasi</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ========== SIDEBAR FILTER ==========
with st.sidebar:
    st.markdown(f"""
    <div style="background-color: {DARK_BLUE}; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: white; text-align: center;">FILTER DATA</h3>
    </div>
    """, unsafe_allow_html=True)
    
    tahun_terpilih = st.select_slider(
        "Rentang Tahun Analisis:",
        options=financial_data['Tahun'].tolist(),
        value=(2020, 2024)
    )
    
    metrik_prioritas = st.multiselect(
        "Metrik Prioritas:",
        options=['Total Aset', 'Laba Bersih', 'NPL Gross', 'ROA', 'BOPO', 'LDR'],
        default=['Total Aset', 'Laba Bersih', 'NPL Gross']
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background-color: {LIGHT_GRAY}; padding: 15px; border-radius: 10px;">
        <h4 style="color: {DARK_BLUE}; margin-top: 0;">Keterangan Warna:</h4>
        <p style="color: {PRIMARY_RED}; margin: 5px 0;">• Merah: Perhatian Khusus</p>
        <p style="color: {DARK_BLUE}; margin: 5px 0;">• Biru: Kinerja Utama</p>
        <p style="color: '#4CAF50'; margin: 5px 0;">• Hijau: Pencapaian Target</p>
    </div>
    """, unsafe_allow_html=True)

# ========== ROW 1: KEY FINANCIAL METRICS ==========
st.subheader("📊 Key Financial Performance Indicators")
st.markdown("*Update: Laporan Tahunan 2024*")

cols = st.columns(4)
with cols[0]:
    delta_aset = ((financial_data.loc[financial_data['Tahun'] == 2024, 'Total Aset (Triliun Rp)'].values[0] / 
                   financial_data.loc[financial_data['Tahun'] == 2023, 'Total Aset (Triliun Rp)'].values[0]) - 1) * 100
    st.metric(
        label="Total Aset (Triliun Rp)",
        value=f"{financial_data.loc[financial_data['Tahun'] == 2024, 'Total Aset (Triliun Rp)'].values[0]:.2f}",
        delta=f"{delta_aset:.1f}%",
        delta_color="normal"
    )

with cols[1]:
    delta_laba = ((financial_data.loc[financial_data['Tahun'] == 2024, 'Laba Bersih (Triliun Rp)'].values[0] / 
                   financial_data.loc[financial_data['Tahun'] == 2023, 'Laba Bersih (Triliun Rp)'].values[0]) - 1) * 100
    st.metric(
        label="Laba Bersih (Triliun Rp)",
        value=f"{financial_data.loc[financial_data['Tahun'] == 2024, 'Laba Bersih (Triliun Rp)'].values[0]:.2f}",
        delta=f"{delta_laba:.1f}%",
        delta_color="inverse" if delta_laba < 0 else "normal"
    )

with cols[2]:
    st.metric(
        label="NPL Gross (%)",
        value=f"{financial_data.loc[financial_data['Tahun'] == 2024, 'NPL Gross (%)'].values[0]:.2f}",
        delta=f"+{financial_data.loc[financial_data['Tahun'] == 2024, 'NPL Gross (%)'].values[0] - financial_data.loc[financial_data['Tahun'] == 2023, 'NPL Gross (%)'].values[0]:.2f}%",
        delta_color="inverse"
    )

with cols[3]:
    st.metric(
        label="CAR (%)",
        value=f"{financial_data.loc[financial_data['Tahun'] == 2024, 'CAR (%)'].values[0]:.2f}",
        delta=f"{financial_data.loc[financial_data['Tahun'] == 2024, 'CAR (%)'].values[0] - financial_data.loc[financial_data['Tahun'] == 2023, 'CAR (%)'].values[0]:.2f}%",
        delta_color="normal" if financial_data.loc[financial_data['Tahun'] == 2024, 'CAR (%)'].values[0] > 20 else "inverse"
    )

# ========== ROW 2: TREND ANALYSIS ==========
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Trend Pertumbuhan Aset & Kredit")
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=financial_data['Tahun'], 
        y=financial_data['Total Aset (Triliun Rp)'],
        mode='lines+markers',
        name='Total Aset',
        line=dict(color=DARK_BLUE, width=3),
        marker=dict(size=8)
    ))
    fig1.add_trace(go.Scatter(
        x=financial_data['Tahun'], 
        y=financial_data['Total Kredit (Triliun Rp)'],
        mode='lines+markers',
        name='Total Kredit',
        line=dict(color=PRIMARY_RED, width=3),
        marker=dict(size=8)
    ))
    fig1.update_layout(
        height=400,
        plot_bgcolor=LIGHT_GRAY,
        paper_bgcolor=WHITE,
        hovermode='x unified',
        title="Trend 5 Tahun (2020-2024)",
        title_font=dict(size=16, color=DARK_BLUE)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 🎯 Kinerja Rasio Keuangan")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=financial_data['Tahun'], 
        y=financial_data['ROA (%)'],
        mode='lines+markers',
        name='ROA',
        line=dict(color=DARK_BLUE, width=3)
    ))
    fig2.add_trace(go.Scatter(
        x=financial_data['Tahun'], 
        y=financial_data['BOPO (%)'],
        mode='lines+markers',
        name='BOPO',
        line=dict(color=PRIMARY_RED, width=3)
    ))
    fig2.add_trace(go.Scatter(
        x=financial_data['Tahun'], 
        y=financial_data['NPL Gross (%)'],
        mode='lines+markers',
        name='NPL Gross',
        line=dict(color='#FF9800', width=3)
    ))
    fig2.update_layout(
        height=400,
        plot_bgcolor=LIGHT_GRAY,
        paper_bgcolor=WHITE,
        hovermode='x unified',
        title="Efisiensi & Kualitas Aset",
        title_font=dict(size=16, color=DARK_BLUE),
        yaxis=dict(title="Persentase (%)")
    )
    st.plotly_chart(fig2, use_container_width=True)

# ========== ROW 3: SEGMENT ANALYSIS ==========
st.subheader("📋 Analisis Kredit per Segmen 2024")

cols = st.columns(4)
for i, segmen in enumerate(segment_data['Segmen']):
    with cols[i]:
        data = segment_data.iloc[i]
        capaian = (data['Nilai (Triliun Rp)'] / data['Target 2025 (Triliun Rp)']) * 100
        
        st.markdown(f"""
        <div style="border-left: 4px solid {PRIMARY_RED}; padding-left: 10px; margin-bottom: 15px;">
            <h4 style="color: {DARK_BLUE}; margin-bottom: 5px;">{segmen}</h4>
            <p style="font-size: 24px; font-weight: bold; color: {DARK_BLUE}; margin: 5px 0;">
                Rp {data['Nilai (Triliun Rp)']:.2f} T
            </p>
            <p style="color: {'#4CAF50' if data['Pertumbuhan (%)'] > 0 else PRIMARY_RED}; margin: 5px 0;">
                📈 {data['Pertumbuhan (%)']:.1f}% Growth
            </p>
            <p style="color: {DARK_BLUE}; margin: 5px 0; font-size: 12px;">
                Target 2025: Rp {data['Target 2025 (Triliun Rp)']:.1f} T
            </p>
            <div style="background-color: {LIGHT_GRAY}; height: 8px; border-radius: 4px; margin-top: 5px;">
                <div style="background-color: {PRIMARY_RED}; width: {min(capaian, 100)}%; height: 100%; border-radius: 4px;"></div>
            </div>
            <p style="text-align: right; font-size: 11px; margin: 2px 0 0 0;">
                {capaian:.1f}% tercapai
            </p>
        </div>
        """, unsafe_allow_html=True)

# ========== ROW 4: DATA TABLE ==========
st.subheader("📄 Detail Data Historis")
st.dataframe(
    financial_data.style.format({
        'Total Aset (Triliun Rp)': '{:.2f}',
        'Laba Bersih (Triliun Rp)': '{:.2f}',
        'Total Kredit (Triliun Rp)': '{:.2f}',
        'DPK (Triliun Rp)': '{:.2f}',
        'NPL Gross (%)': '{:.2f}',
        'ROA (%)': '{:.2f}',
        'ROE (%)': '{:.2f}',
        'BOPO (%)': '{:.2f}',
        'LDR (%)': '{:.2f}',
        'CAR (%)': '{:.2f}'
    }).applymap(
        lambda x: f"color: {PRIMARY_RED}" if isinstance(x, (int, float)) and x < 0 else "", 
        subset=['Laba Bersih (Triliun Rp)']
    ).applymap(
        lambda x: f"color: {PRIMARY_RED}" if isinstance(x, (int, float)) and x > 3 else f"color: #4CAF50", 
        subset=['NPL Gross (%)']
    ),
    use_container_width=True,
    height=300
)

# ========== FOOTER ==========
st.divider()
st.markdown(f"""
<div style="text-align: center; padding: 20px; background-color: {LIGHT_GRAY}; border-radius: 10px;">
    <p style="color: {DARK_BLUE}; margin: 0;">
        <strong>PT Bank Pembangunan Daerah Jawa Timur Tbk</strong> | Strategic Performance Management Dashboard
    </p>
    <p style="color: #666; font-size: 12px; margin: 5px 0 0 0;">
        Data sumber: Laporan Tahunan 2020-2024 | Dashboard ini untuk tujuan analisis internal
    </p>
    <p style="color: {PRIMARY_RED}; font-size: 11px; margin: 5px 0 0 0;">
        ⚠️ Perhatian khusus diperlukan pada peningkatan NPL Gross (2024: 3.45%) dan BOPO (2024: 81.89%)
    </p>
</div>

""", unsafe_allow_html=True)

