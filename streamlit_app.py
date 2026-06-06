import streamlit as st
import pandas as pd
import math
from chempy import balance_stoichiometry

# ─── 1. KONFIGURASI HALAMAN ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Portal Analisis Kimia",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── 2. LOAD CSS GLOBAL (TEMA TERANG / LIGHT MODE) ──────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@700&display=swap');
:root {
    --bg: #f8fafc;         
    --surface: #ffffff;    
    --surface2: #f1f5f9;   
    --border: #cbd5e1;     
    --accent: #0284c7;     
    --accent2: #6366f1;    
    --accent3: #059669;    
    --text: #0f172a;       
    --text-muted: #475569; 
    --font-body: 'DM Sans', sans-serif; 
    --font-mono: 'Space Mono', monospace;
    --font-display: 'Playfair Display', serif; 
    --radius: 12px;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}
html, body, [class*="css"] { font-family: var(--font-body) !important; color: var(--text) !important; }
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.landing-hero { text-align: center; padding: 2rem 2rem 1rem; }
.hero-badge {
    display: inline-block; font-family: var(--font-mono); font-size: 0.75rem;
    letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent);
    border: 1px solid rgba(2, 132, 199, 0.3); padding: 0.4rem 1.2rem;
    border-radius: 999px; margin-bottom: 1rem; background: rgba(2, 132, 199, 0.05);
}
.hero-title {
    font-family: var(--font-display) !important; font-size: clamp(2rem, 4vw, 3rem) !important;
    font-weight: 700 !important; line-height: 1.15 !important; color: var(--text) !important;
    margin-bottom: 0.5rem !important;
}
.hero-accent {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-desc { font-size: 1.05rem; color: var(--text-muted); max-width: 600px; margin: 0 auto; line-height: 1.6; }

.team-banner {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 1.5rem; text-align: center; margin: 1.5rem auto 3rem; max-width: 900px;
    box-shadow: var(--shadow); border-top: 4px solid var(--accent);
}
.team-banner h4 { font-size: 1rem; color: var(--accent); margin-bottom: 0.8rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
.team-banner p { font-size: 0.95rem; color: var(--text); font-weight: 500; margin: 0; }

.portal-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 20px;
    padding: 2.5rem 2rem; text-align: center; transition: all 0.3s ease; height: 100%; box-shadow: var(--shadow);
}
.portal-card:hover { border-color: var(--accent); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); transform: translateY(-5px); }
.portal-card h3 { color: var(--text); font-weight: 700; margin-top: 10px; }

.feature-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.6rem; box-shadow: var(--shadow); }
.page-title { font-family: var(--font-display) !important; font-size: 2rem !important; color: var(--text) !important; margin-bottom: 0.3rem !important; }

.stButton > button {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; border-radius: 8px !important;
    font-weight: 600 !important; box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}
.stButton > button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, var(--accent), var(--accent2)) !important; border-color: transparent !important; color: white !important; }
.stButton > button[kind="primary"]:hover { opacity: 0.9 !important; color: white !important; }

.stTextInput > div > div > input, .stSelectbox > div > div { background: var(--surface) !important; border: 1px solid var(--border) !important; color: var(--text) !important; }
.result-box { background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; margin-top: 1.5rem; }
.result-item { background: var(--surface); border-radius: 8px; padding: 1rem; margin-bottom: 0.8rem; border-left: 4px solid var(--accent3); box-shadow: var(--shadow); }
.result-golongan { font-family: var(--font-mono); font-weight: 700; color: var(--accent3); font-size: 1.1rem; }
</style>""", unsafe_allow_html=True)

# ─── 3. DATABASE ORGANIK ────────────────────────────────────────────────────
SENYAWA_DB = [
    {"Nama Golongan": "Alkohol Primer/Sekunder", "Uji Spesifik": "Iodoform (jika metil karbinol), Uji Lucas"},
    {"Nama Golongan": "Alkohol Tersier", "Uji Spesifik": "Uji Lucas (langsung keruh)"},
    {"Nama Golongan": "Aldehida", "Uji Spesifik": "2,4-DNPH, Tollens, Fehling"},
    {"Nama Golongan": "Keton", "Uji Spesifik": "2,4-DNPH (Tanpa reaksi di Tollens/Fehling)"},
    {"Nama Golongan": "Fenol", "Uji Spesifik": "FeCl₃ (Warna ungu/hijau)"},
    {"Nama Golongan": "Karbohidrat / Gula Pereduksi", "Uji Spesifik": "Molisch, Fehling, Tollens"},
    {"Nama Golongan": "Protein / Peptida", "Uji Spesifik": "Biuret (Warna ungu)"},
]

def identifikasi_senyawa(jawaban: dict) -> list:
    kandidat = []
    if jawaban.get("dnph") == "Ya":
        if jawaban.get("tollens") == "Ya" or jawaban.get("fehling") == "Ya":
            kandidat.append(("Aldehida", "2,4-DNPH ✅ + Tollens/Fehling ✅"))
        else:
            kandidat.append(("Keton", "2,4-DNPH ✅ + Tollens/Fehling ❌"))
            if jawaban.get("iodoform") == "Ya":
                kandidat.append(("Metil Keton", "Iodoform ✅"))
    if jawaban.get("lucas") != "Tidak ada perubahan (Bening)":
        if jawaban.get("lucas") == "Keruh seketika":
            kandidat.append(("Alkohol Tersier", "Uji Lucas ✅ (Seketika bereaksi)"))
        elif jawaban.get("lucas") == "Keruh dalam 5-10 menit (Dipanaskan)":
            kandidat.append(("Alkohol Sekunder", "Uji Lucas ✅ (Reaksi lambat)"))
            if jawaban.get("iodoform") == "Ya":
                kandidat.append(("Alkohol Sekunder (Metil Karbinol)", "Iodoform ✅"))
    if jawaban.get("fecl3") == "Ya": kandidat.append(("Fenol / Golongan Fenolik", "FeCl₃ ✅"))
    if jawaban.get("biuret") == "Ya": kandidat.append(("Protein / Ikatan Peptida", "Biuret ✅"))
    if jawaban.get("molisch") == "Ya": 
        kandidat.append(("Karbohidrat", "Molisch ✅"))
        if jawaban.get("fehling") == "Ya":
            kandidat.append(("Karbohidrat (Gula Pereduksi)", "Fehling ✅"))
    if not kandidat: 
        kandidat.append(("Zat Tidak Dikenali", "Kombinasi hasil uji tidak spesifik."))
    return kandidat

# ─── 4. DATABASE & FUNGSI METATESIS KOMPREHENSIF ────────────────────────────
kation_db = {
    'H': (1, False), 'Li': (1, False), 'Na': (1, False), 'K': (1, False), 'Rb': (1, False), 'Cs': (1, False),
    'Be': (2, False), 'Mg': (2, False), 'Ca': (2, False), 'Sr': (2, False), 'Ba': (2, False),
    'Ag': (1, False), 'Zn': (2, False), 'Cd': (2, False), 'Al': (3, False), 'Bi': (3, False),
    'Cu': (2, False), 'Fe': (3, False), 'Pb': (2, False), 'Ni': (2, False), 'Co': (2, False), 
    'Mn': (2, False), 'Cr': (3, False), 'Sn': (2, False), 'Hg': (2, False), 'NH4': (1, True)
}

anion_db = {
    'F': (-1, False), 'Cl': (-1, False), 'Br': (-1, False), 'I': (-1, False),
    'OH': (-1, True), 'NO3': (-1, True), 'NO2': (-1, True), 'CN': (-1, True), 'SCN': (-1, True), 
    'CH3COO': (-1, True), 'ClO': (-1, True), 'ClO2': (-1, True), 'ClO3': (-1, True), 'ClO4': (-1, True), 
    'MnO4': (-1, True), 'HCO3': (-1, True), 'HSO4': (-1, True), 'H2PO4': (-1, True),
    'O': (-2, False), 'S': (-2, False),
    'SO4': (-2, True), 'SO3': (-2, True), 'CO3': (-2, True), 'CrO4': (-2, True), 'Cr2O7': (-2, True), 
    'C2O4': (-2, True), 'S2O3': (-2, True), 'HPO4': (-2, True), 'SiO3': (-2, True),
    'PO4': (-3, True), 'PO3': (-3, True), 'AsO4': (-3, True), 'N': (-3, False), 'P': (-3, False)
}

def urai_senyawa(senyawa):
    kation_terdeteksi, anion_terdeteksi = None, None
    for k in sorted(kation_db.keys(), key=len, reverse=True):
        if senyawa.startswith(k):
            kation_terdeteksi = k
            sisa_string = senyawa[len(k):]
            break
    if not kation_terdeteksi: return None, None
    for a in sorted(anion_db.keys(), key=len, reverse=True):
        if a in sisa_string:
            anion_terdeteksi = a
            break
    return kation_terdeteksi, anion_terdeteksi

def gabung_ion(kation, anion):
    muatan_k, muatan_a = abs(kation_db[kation][0]), abs(anion_db[anion][0])
    is_poliatomik_a = anion_db[anion][1]
    kpk = (muatan_k * muatan_a) // math.gcd(muatan_k, muatan_a)
    indeks_k, indeks_a = kpk // muatan_k, kpk // muatan_a
    hasil_k = kation if indeks_k == 1 else f"{kation}{indeks_k}"
    hasil_a = anion if indeks_a == 1 else (f"({anion}){indeks_a}" if is_poliatomik_a else f"{anion}{indeks_a}")
    senyawa_baru = f"{hasil_k}{hasil_a}"
    return "H2O" if senyawa_baru == "HOH" else senyawa_baru

def apakah_mengendap(kation, anion):
    kation_larut = ['Li', 'Na', 'K', 'Rb', 'Cs', 'NH4', 'H']
    anion_larut = ['NO3', 'CH3COO', 'ClO3', 'ClO4', 'MnO4', 'NO2', 'HCO3', 'HSO4']
    if kation in kation_larut: return False
    if anion in anion_larut: return False
    if anion in ['Cl', 'Br', 'I', 'SCN']:
        if kation in ['Ag', 'Pb', 'Hg', 'Cu']: return True
        return False
    if anion == 'F':
        if kation in ['Mg', 'Ca', 'Sr', 'Ba', 'Pb']: return True
        return False
    if anion == 'SO4':
        if kation in ['Ba', 'Sr', 'Ca', 'Pb', 'Ag', 'Hg']: return True
        return False
    if anion in ['OH', 'O']:
        if kation in ['Ba', 'Sr', 'Ca']: return False
        return True
    if anion == 'S':
        if kation in ['Mg', 'Ca', 'Sr', 'Ba']: return False
        return True
    anion_endapan = ['CO3', 'PO4', 'PO3', 'CrO4', 'Cr2O7', 'C2O4', 'SO3', 'AsO4', 'SiO3', 'CN']
    if anion in anion_endapan: return True
    return False

def fmt_muatan(nilai, tanda):
    return tanda if nilai == 1 else f"{nilai}{tanda}"

# ─── 5. PENGATURAN STATE & NAVIGASI ─────────────────────────────────────────
if "app_mode" not in st.session_state: st.session_state.app_mode = "portal"
if "halaman_org" not in st.session_state: st.session_state.halaman_org = "landing"

def go_portal(): st.session_state.app_mode = "portal"; st.rerun()
def nav_org(page): st.session_state.halaman_org = page; st.session_state.app_mode = "organik"; st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
#  A. PORTAL UTAMA
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.app_mode == "portal":
    st.markdown("""
    <div class="landing-hero">
        <div class="hero-badge">Aplikasi Pendidikan Interaktif</div>
        <h1 class="hero-title">Portal Analisis <span class="hero-accent">Kimia Terpadu</span></h1>
        <p class="hero-desc">Pilih modul simulasi laboratorium virtual yang ingin Anda akses di bawah ini.</p>
    </div>
    
    <div class="team-banner">
        <h4>👨‍🔬 Tim Pengembang Aplikasi (D3 Analisis Kimia - AKA Bogor)</h4>
        <p style="line-height: 2;">
            ✨ Agung Nugraha (2560557) &nbsp; | &nbsp; ✨ Alifia Citra Nabila (2560562) &nbsp; | &nbsp; ✨ Haifa Maulifida Falihah (2560638)<br>
            ✨ Nabila Putri Khorinnisa (2560695) &nbsp; | &nbsp; ✨ Rania Ayudia Amirru (2560746)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 4, 4, 1])
    with col2:
        st.markdown('<div class="portal-card"><h1>🔬</h1><h3>Identifikasi Organik</h3><p style="color:var(--text-muted); font-size:14px; margin-bottom:20px;">Analisis kualitatif berdasarkan pengujian pereaksi untuk identifikasi golongan organik.</p>', unsafe_allow_html=True)
        if st.button("Masuk Modul Organik ➔", use_container_width=True, type="primary"):
            st.session_state.halaman_org = "landing"; st.session_state.app_mode = "organik"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="portal-card"><h1>⚗️</h1><h3>Reaksi Metatesis</h3><p style="color:var(--text-muted); font-size:14px; margin-bottom:20px;">Prediksi produk reaksi pertukaran ganda dan penyetaraan persamaan kimia otomatis.</p>', unsafe_allow_html=True)
        if st.button("Masuk Modul Metatesis ➔", use_container_width=True, type="primary"):
            st.session_state.app_mode = "metatesis"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
#  B. MODUL: IDENTIFIKASI SENYAWA ORGANIK
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.app_mode == "organik":
    if st.session_state.halaman_org == "landing":
        st.button("🏠 Kembali ke Portal Utama", on_click=go_portal)
        st.markdown('<div class="landing-hero" style="padding-top:1rem;"><div class="hero-badge">⚗️ Kimia Organik</div><h1 class="hero-title">Sistem Identifikasi<br><span class="hero-accent">Senyawa Organik</span></h1></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔬 Mulai Identifikasi", use_container_width=True, type="primary"): nav_org("identifikasi")
        with col2:
            if st.button("🗄️ Database Senyawa", use_container_width=True): nav_org("database")
        with col3:
            if st.button("📚 Dasar Teori", use_container_width=True): nav_org("teori")

    elif st.session_state.halaman_org == "identifikasi":
        if st.button("← Kembali ke Menu Organik"): nav_org("landing")
        st.markdown('<h2 class="page-title">🔬 Form Identifikasi Laboratorium</h2>', unsafe_allow_html=True)
        st.markdown("Pilih hasil pengamatan dari reagen uji yang ditambahkan ke dalam sampel uji Anda.")
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("**Uji Gugus Karbonil & Alkohol**")
            jawaban = {
                "dnph": st.radio("Terbentuk endapan kuning/merah (2,4-DNPH)?", ["Tidak", "Ya"], horizontal=True),
                "tollens": st.radio("Terbentuk cermin perak (Uji Tollens)?", ["Tidak", "Ya"], horizontal=True),
                "fehling": st.radio("Terbentuk endapan merah bata (Uji Fehling)?", ["Tidak", "Ya"], horizontal=True),
                "iodoform": st.radio("Terbentuk endapan kuning (Uji Iodoform)?", ["Tidak", "Ya"], horizontal=True),
                "lucas": st.radio("Hasil Uji Lucas (HCl pekat + ZnCl₂):", ["Tidak ada perubahan (Bening)", "Keruh dalam 5-10 menit (Dipanaskan)", "Keruh seketika"]),
            }
            
        with col_b:
            st.markdown("**Uji Spesifik Lainnya**")
            jawaban.update({
                "fecl3": st.radio("Terjadi perubahan warna ungu/hijau pekat (Uji FeCl₃)?", ["Tidak", "Ya"], horizontal=True),
                "biuret": st.radio("Terbentuk kompleks warna ungu (Uji Biuret)?", ["Tidak", "Ya"], horizontal=True),
                "molisch": st.radio("Terbentuk cincin ungu (Uji Molisch)?", ["Tidak", "Ya"], horizontal=True),
            })
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🔎 Eksekusi Identifikasi!", type="primary"):
            hasil = identifikasi_senyawa(jawaban)
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### 📋 Hasil Analisis Sistem")
            if hasil[0][0] == "Zat Tidak Dikenali":
                st.warning("⚠️ " + hasil[0][1] + " Coba periksa kembali parameter hasil pengamatan laboratorium Anda.")
            else:
                st.success("✅ Karakteristik sampel berhasil dicocokkan dengan algoritma sistem.")
                for idx, (golongan, indikator) in enumerate(hasil):
                    st.markdown(f"""
                    <div class="result-item">
                        <span class="result-golongan">Kandidat {idx+1} : {golongan}</span><br>
                        <span style="font-size:0.95rem; color:var(--text-muted);"><b>Parameter Positif:</b> {indikator}</span>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.halaman_org == "database":
        if st.button("← Kembali ke Menu Organik"): nav_org("landing")
        st.markdown('<h2 class="page-title">🗄️ Database Senyawa Organik</h2>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(SENYAWA_DB), use_container_width=True, hide_index=True)

    elif st.session_state.halaman_org == "teori":
        if st.button("← Kembali ke Menu Organik"): nav_org("landing")
        st.markdown('<h2 class="page-title">📚 Dasar Teori Analisis Organik</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h3>Analisis Kualitatif Senyawa Organik</h3>
        <p>Analisis kualitatif senyawa organik merupakan serangkaian prosedur pengujian laboratorium yang bertujuan untuk mengidentifikasi keberadaan gugus fungsi spesifik dalam suatu sampel tak dikenal. Berdasarkan algoritma pada sistem Chemisfun, identifikasi difokuskan pada penggolongan aldehida, keton, alkohol, fenol, karbohidrat, dan protein melalui pengamatan visual terhadap perubahan warna, pembentukan endapan, atau kekeruhan.</p>
        
        <h4>1. Identifikasi Gugus Karbonil (Aldehida dan Keton)</h4>
        Senyawa aldehida dan keton memiliki kesamaan struktural berupa ikatan rangkap karbon-oksigen (gugus karbonil). Untuk membedakan dan mengidentifikasi keduanya, serangkaian uji spesifik dilakukan:
        <ul>
            <li><b>Uji 2,4-Dinitrofenilhidrazin (2,4-DNPH):</b> Reagen ini berfungsi sebagai uji penapisan awal untuk semua gugus karbonil. Reaksi kondensasi antara sampel dengan reagen Brady (2,4-DNPH) yang menghasilkan endapan berwarna kuning hingga jingga kemerahan mengonfirmasi keberadaan aldehida atau keton.</li>
            <li><b>Uji Tollens (Cermin Perak):</b> Digunakan untuk membedakan aldehida dari keton. Aldehida dapat dioksidasi oleh ion perak amoniakal $[Ag(NH_3)_2]^+$, sehingga mereduksi ion $Ag^+$ menjadi logam perak murni yang menempel pada dinding tabung reaksi membentuk "cermin perak". Keton tidak memberikan hasil positif pada uji ini.</li>
            <li><b>Uji Fehling:</b> Memiliki prinsip kerja yang serupa dengan uji Tollens. Aldehida mereduksi ion tembaga(II) kompleks menjadi tembaga(I) oksida ($Cu_2O$), yang menghasilkan endapan berwarna merah bata.</li>
            <li><b>Uji Iodoform:</b> Uji spesifik ini digunakan untuk mendeteksi keberadaan gugus metil keton (senyawa karbonil yang memiliki gugus metil yang terikat langsung pada karbon karbonil). Reaksi positif ditandai dengan terbentuknya endapan kuning iodoform ($CHI_3$).</li>
        </ul>

        <h4>2. Identifikasi Golongan Alkohol</h4>
        Alkohol diklasifikasikan menjadi primer, sekunder, dan tersier berdasarkan letak terikatnya gugus hidroksil (-OH).
        <ul>
            <li><b>Uji Lucas:</b> Reagen Lucas terdiri dari asam klorida (HCl) pekat dan seng klorida ($ZnCl_2$) anhidrat. Uji ini didasarkan pada kecepatan reaksi substitusi nukleofilik ($S_N1$) pembentukan alkil klorida yang tidak larut. 
                <ul>
                    <li><b>Alkohol tersier</b> bereaksi sangat cepat, menghasilkan kekeruhan atau pemisahan fase seketika.</li>
                    <li><b>Alkohol sekunder</b> bereaksi lebih lambat, umumnya membutuhkan waktu 5-10 menit dan pemanasan ringan untuk membentuk kekeruhan.</li>
                    <li><b>Alkohol primer</b> tidak bereaksi (tetap bening) pada suhu ruang.</li>
                </ul>
            </li>
            <li><b>Uji Iodoform untuk Alkohol:</b> Selain untuk metil keton, uji iodoform juga akan bernilai positif pada alkohol sekunder yang memiliki struktur metil karbinol (struktur di mana gugus -OH terikat pada karbon yang juga mengikat gugus metil).</li>
        </ul>

        <h4>3. Identifikasi Golongan Fenol</h4>
        Fenol merupakan senyawa organik di mana gugus hidroksil terikat langsung pada cincin aromatik.
        <ul>
            <li><b>Uji Besi(III) Klorida ($FeCl_3$):</b> Penambahan larutan $FeCl_3$ ke dalam sampel yang mengandung gugus fenolik bebas akan menghasilkan pembentukan kompleks besi-fenol yang sangat berwarna (umumnya ungu, hijau, atau biru pekat, bergantung pada struktur spesifik fenolnya).</li>
        </ul>

        <h4>4. Identifikasi Karbohidrat</h4>
        Karbohidrat merupakan polihidroksi aldehida atau keton. Pengujian pada kelompok ini mencakup uji umum dan uji spesifik gula pereduksi:
        <ul>
            <li><b>Uji Molisch:</b> Merupakan uji umum untuk semua jenis karbohidrat. Reaksi dehidrasi karbohidrat oleh asam sulfat pekat menghasilkan senyawa furfural atau derivatnya, yang kemudian berkondensasi dengan $\\alpha$-naftol membentuk cincin berwarna ungu di bidang batas larutan.</li>
            <li><b>Uji Gula Pereduksi:</b> Karbohidrat yang memiliki gugus aldehida bebas (atau keton yang dapat berisomerisasi) akan memberikan hasil positif (endapan merah bata) pada Uji Fehling maupun Uji Tollens, membedakannya dari karbohidrat non-pereduksi seperti sukrosa atau polisakarida kompleks.</li>
        </ul>

        <h4>5. Identifikasi Protein dan Peptida</h4>
        <ul>
            <li><b>Uji Biuret:</b> Reagen Biuret yang mengandung ion $Cu^{2+}$ dalam suasana basa digunakan untuk mengidentifikasi keberadaan ikatan peptida (ikatan amida) pada makromolekul protein. Reaksi pembentukan kompleks koordinasi antara ion tembaga dengan pasangan elektron bebas dari nitrogen amida akan menghasilkan perubahan warna larutan menjadi ungu violet.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
#  C. MODUL: REAKSI METATESIS
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.app_mode == "metatesis":
    st.button("🏠 Kembali ke Portal Utama", on_click=go_portal)
    st.markdown('<h1 class="page-title">🧪 Analisis Stoikiometri & Metatesis</h1>', unsafe_allow_html=True)
    st.markdown("Sistem mendeteksi muatan ion secara otomatis untuk menyilangkan produk reaktan secara instan.")
    st.divider()

    st.markdown("#### 📥 Masukkan Senyawa Reaktan (Maksimal 3)")
    col1, col2, col3 = st.columns(3)
    with col1: reaktan1 = st.text_input("Reaktan 1", "NaOH").strip().replace(" ", "")
    with col2: reaktan2 = st.text_input("Reaktan 2", "HCl").strip().replace(" ", "")
    with col3: reaktan3 = st.text_input("Reaktan 3 (Opsional)", "").strip().replace(" ", "")

    if st.button("Analisis Reaksi", type="primary"):
        input_raw = [r for r in [reaktan1, reaktan2, reaktan3] if r]
        
        if len(input_raw) < 2:
            st.warning("⚠️ Minimal masukkan 2 reaktan untuk melakukan reaksi silang.")
        elif "H2O" in input_raw:
            st.warning("⚠️ Reaktan H₂O memicu pelarutan fisik, bukan metatesis murni.")
        else:
            parsed_reactants = [urai_senyawa(r) for r in input_raw]
            
            if not all(k and a for k, a in parsed_reactants):
                st.error("❌ Salah satu senyawa tidak dikenali. Pastikan kaidah penulisan huruf kapital sudah benar.")
            else:
                kations = [p[0] for p in parsed_reactants]
                anions = [p[1] for p in parsed_reactants]
                
                produk_kemungkinan = set()
                for i, k in enumerate(kations):
                    for j, a in enumerate(anions):
                        if i != j:  
                            produk_kemungkinan.add(gabung_ion(k, a))
                
                try:
                    r_setara, p_setara = balance_stoichiometry(set(input_raw), produk_kemungkinan)
                    
                    def format_dict(senyawa_dict):
                        hasil = []
                        for seny, koef in senyawa_dict.items():
                            k, a = urai_senyawa(seny)
                            wujud = "(l)" if seny == "H2O" else ("(s)" if (k and a and apakah_mengendap(k, a)) else "(aq)")
                            prefix = "" if koef == 1 else f"{koef}"
                            hasil.append(f"{prefix}{seny}{wujud}")
                        return " + ".join(hasil)
                    
                    kiri = format_dict(r_setara)
                    kanan = format_dict(p_setara)
                    
                    alasan = []
                    for p in p_setara.keys():
                        if p == "H2O": 
                            alasan.append(f"**molekul air (H₂O)** (elektrolit lemah)")
                        else:
                            kp, ap = urai_senyawa(p)
                            if kp and ap and apakah_mengendap(kp, ap):
                                alasan.append(f"endapan **{p}**")
                                
                    st.success("✅ Secara Teori: REAKSI BERLANGSUNG (Valid)")
                    st.markdown("### Persamaan Reaksi Setara:")
                    st.latex(f"{kiri} \\rightarrow {kanan}")
                    
                    if alasan:
                        st.markdown(f"**Driving Force:** Reaksi dapat berlangsung ke arah produk karena terbentuk {', '.join(alasan)}.")
                    else:
                        st.info("ℹ️ Tidak ada endapan atau air yang terbentuk. Dalam dunia nyata, semua ion mungkin hanya bercampur dalam larutan (reaksi tidak berkesudahan).")
                    
                    st.divider()
                    
                    st.markdown("### 🔍 Lembar Kerja Analisis Ion")
                    cols_urai = st.columns(len(input_raw))
                    
                    for idx, (k, a) in enumerate(parsed_reactants):
                        c_k, c_a = fmt_muatan(kation_db[k][0], '+'), fmt_muatan(abs(anion_db[a][0]), '-')
                        with cols_urai[idx]:
                            st.markdown(f"**Penguraian Reaktan {idx+1}:**")
                            st.latex(f"{input_raw[idx]} \\longrightarrow {k}^{{{c_k}}} + {a}^{{{c_a}}}")
                            
                    st.info("💡 **Aturan Silang Muatan:** Kation (positif) dari satu reaktan bertukar pasangan dengan Anion (negatif) dari reaktan lain membentuk senyawa baru: $A^{x+} + B^{y-} \\rightarrow A_yB_x$")
                    
                    cols_prod = st.columns(len(p_setara))
                    for idx, p in enumerate(p_setara.keys()):
                        k_p, a_p = urai_senyawa(p)
                        if k_p and a_p:
                            c_k = fmt_muatan(kation_db[k_p][0], '+')
                            c_a = fmt_muatan(abs(anion_db[a_p][0]), '-')
                            with cols_prod[idx % len(cols_prod)]:
                                st.markdown(f"**Silang Produk {idx+1}:**")
                                st.latex(f"{k_p}^{{{c_k}}} + {a_p}^{{{c_a}}} \\longrightarrow {p}")
                                
                except Exception as e:
                    st.error("❌ Reaksi silang tidak dapat disetarakan secara matematis. Kombinasi ion antar reaktan mungkin tidak menghasilkan set produk yang valid secara persamaan kimia.")
