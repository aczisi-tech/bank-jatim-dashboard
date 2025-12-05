```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64
import os

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(
    page_title="Bank Jatim Financial Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== WARNA CORPORATE BANK JATIM ==========
PRIMARY_RED = "#D92B2B"      # Merah utama dari logo
DARK_BLUE = "#001C56"        # Biru tua untuk header
LIGHT_GRAY = "#F0F0F0"       # Abu-abu untuk background
WHITE = "#FFFFFF"
BLACK = "#000000"

# ========== FUNGSI UNTUK LOGO ==========
def load_logo(logo_path="logo_bankjatim.png"):
    """
    Fungsi untuk memuat logo dengan beberapa fallback:
    1. Coba file lokal
    2. Coba base64 encoded fallback
    3. Gunakan placeholder
    """
    # Coba file lokal terlebih dahulu
    if os.path.exists(logo_path):
        try:
            return logo_path
        except:
            pass
    
    # Jika file tidak ditemukan, buat placeholder base64
    # Ini adalah fallback jika logo tidak ditemukan di cloud
    placeholder_svg = f"""
    <svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="120" height="120" rx="10" fill="{PRIMARY_RED}"/>
        <text x="60" y="50" font-family="Arial, sans-serif" font-size="14" font-weight="bold" 
              text-anchor="middle" fill="white">BANK</text>
        <text x="60" y="70" font-family="Arial, sans-serif" font-size="14" font-weight="bold" 
              text-anchor="middle" fill="white">JATIM</text>
        <text x="60" y="90" font-family="Arial, sans-serif" font-size="10" 
              text-anchor="middle" fill="white">BPD No. 1</text>
    </svg>
    """
    
    # Convert ke base64
    b64_encoded = base64.b64encode(placeholder_svg.encode()).decode()
    return f"data:image/svg+xml;base64,{b64_encoded}"

# ========== DATA SAMPLE (DARI LAPORAN 2024) ==========
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
    'Target 2025 (Triliun Rp)': [12.1, 14.5, 8.0, 36.0],
    'Warna': [PRIMARY_RED, DARK_BLUE, "#4CAF50", "#FF9800"]
})

# Data untuk chart bar (pertumbuhan tahunan)
growth_data = pd.DataFrame({
    'Tahun': ['2020-2021', '2021-2022', '2022-2023', '2023-2024'],
    'Pertumbuhan Aset (%)': [20.45, 2.29, 0.80, 13.76],
    'Pertumbuhan Kredit (%)': [2.22, 9.68, 18.98, 37.06],
    'Pertumbuhan DPK (%)': [21.83, -1.79, -2.16, 15.10]
})

# ========== HEADER DASHBOARD ==========
col1, col2 = st.columns([1, 5])

with col1:
    # Load dan tampilkan logo
    logo_source = load_logo()
    
    # Jika logo_source adalah file path
    if isinstance(logo_source, str) and logo_source.endswith('.png'):
        st.image(logo_source, width=120)
    else:
        # Jika base64 placeholder
        st.markdown(f'<img src="{logo_source}" width="120">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center; margin-top: 5px;">
        <p style="color: {DARK_BLUE}; font-weight: bold; margin: 0; font-size: 14px;">BANK JATIM</p>
        <p style="color: #666; margin: 0; font-size: 10px;">PT Bank Pembangunan Daerah<br>Jawa Timur Tbk</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color: {DARK_BLUE}; padding: 25px; border-radius: 10px;">
        <h1 style="color: white; margin: 0; font-size: 32px;">Strategic Performance Management</h1>
        <h2 style="color: {PRIMARY_RED}; margin: 5px 0 0 0; font-size: 24px;">Financial Report Dashboard</h2>
        <p style="color: {LIGHT_GRAY}; margin: 10px 0 0 0;">PT Bank Pembangunan Daerah Jawa Timur Tbk | Laporan Konsolidasi 2020-2024</p>
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
        <p style="color: {PRIMARY_RED}; margin: 5px 0;">• Merah ({PRIMARY_RED}): Perhatian Khusus</p>
        <p style="color: {DARK_BLUE}; margin: 5px 0;">• Biru ({DARK_BLUE}): Kinerja Utama</p>
        <p style="color: '#4CAF50'; margin: 5px 0;">• Hijau: Pencapaian Target</p>
    </div>
    """, unsafe_allow_html=True)

# ========== ROW 1: BAR CHART - PERTUMBUHAN TAHUNAN ==========
st.subheader("📊 Pertumbuhan Tahunan (Bar Chart)")
st.markdown("*Perbandingan pertumbuhan Aset, Kredit, dan DPK*")

fig_bar = go.Figure()

# Tambahkan bar untuk Pertumbuhan Aset
fig_bar.add_trace(go.Bar(
    x=growth_data['Tahun'],
    y=growth_data['Pertumbuhan Aset (%)'],
    name='Pertumbuhan Aset',
    marker_color=DARK_BLUE,
    text=growth_data['Pertumbuhan Aset (%)'].apply(lambda x: f'{x:.1f}%'),
    textposition='auto',
))

# Tambahkan bar untuk Pertumbuhan Kredit
fig_bar.add_trace(go.Bar(
    x=growth_data['Tahun'],
    y=growth_data['Pertumbuhan Kredit (%)'],
    name='Pertumbuhan Kredit',
    marker_color=PRIMARY_RED,
    text=growth_data['Pertumbuhan Kredit (%)'].apply(lambda x: f'{x:.1f}%'),
    textposition='auto',
))

# Tambahkan bar untuk Pertumbuhan DPK
fig_bar.add_trace(go.Bar(
    x=growth_data['Tahun'],
    y=growth_data['Pertumbuhan DPK (%)'],
    name='Pertumbuhan DPK',
    marker_color='#4CAF50',
    text=growth_data['Pertumbuhan DPK (%)'].apply(lambda x: f'{x:.1f}%'),
    textposition='auto',
))

fig_bar.update_layout(
    height=400,
    plot_bgcolor=WHITE,
    paper_bgcolor=WHITE,
    barmode='group',
    title="Pertumbuhan Tahunan (%) - Perbandingan Aset, Kredit, dan DPK",
    title_font=dict(size=16, color=DARK_BLUE),
    xaxis=dict(title="Periode", tickangle=0),
    yaxis=dict(title="Persentase Pertumbuhan (%)"),
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_bar, use_container_width=True)

# ========== ROW 2: KEY FINANCIAL METRICS ==========
st.subheader("🎯 Key Financial Performance Indicators")
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

# ========== ROW 3: TREND ANALYSIS ==========
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Trend Total Aset & Kredit")
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=financial_data['