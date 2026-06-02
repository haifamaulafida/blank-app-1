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
    --bg: #f8fafc;         /* Slate 50 - Latar belakang utama */
    --surface: #ffffff;    /* Putih murni untuk kartu */
    --surface2: #f1f5f9;   /* Slate 100 - Latar belakang sekunder/input */
    --border: #cbd5e1;     /* Slate 300 - Garis batas */
    --accent: #0284c7;     /* Light Blue 600 */
    --accent2: #6366f1;    /* Indigo 500 */
    --accent3: #059669;    /* Emerald 600 */
    --text: #0f172a;       /* Slate 900 - Teks utama gelap */
    --text-muted: #475569; /* Slate 600 - Teks pendukung */
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

/* ─── Komponen Portal & Tim ─── */
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

/* Kartu Tim Pengembang di Depan */
.team-banner {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 1.5rem; text-align: center; margin: 1.5rem auto 3rem; max-width: 900px;
    box-shadow: var(--shadow); border-top: 4px solid var(--accent);
}
.team-banner h4 { font-size: 1rem; color: var(--accent); margin-bottom: 0.8rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
.team-banner p { font-size: 0.95rem; color: var(--text); font-weight: 500; line-height: 1.8; margin: 0; }

.portal-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 20px;
    padding: 2.5rem 2rem; text-align: center; transition: all 0.3s ease; height: 100%; box-shadow: var(--shadow);
}
.portal-card:hover { border-color: var(--accent); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); transform: translateY(-5px); }
.portal-card h3 { color: var(--text); font-weight: 700; margin-top: 10px; }

/* ─── Komponen Spesifik ─── */
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.2rem; margin-top: 2rem; }
.feature-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.6rem; box-shadow: var(--shadow); }
.page-title { font-family: var(--font-display) !important; font-size: 2rem !important; color: var(--text) !important; margin-bottom: 0.3rem !important; }
.page-sub { color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.5rem; }
.app-header { font-size: 32px; font-weight: 800; color: var(--accent); margin-bottom: 5px; }

/* ─── General Streamlit Override ─── */
.stButton > button {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; border-radius: 8px !important;
    font-weight: 600 !important; box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}
.stButton > button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, var(--accent), var(--accent2)) !important; border-color: transparent !important; color: white !important; }
.stButton > button[kind="primary"]:hover { opacity: 0.9 !important; color: white !important; }

.stTextInput > div > div > input, .stSelectbox > div > div { background: var(--surface) !important; border: 1px solid var(--border) !important; color: var(--text) !important; }
.streamlit-expanderHeader { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; color: var(--text) !important; font-weight: 600 !important; }
.streamlit-expanderContent { background: var(--surface) !important; border: 1px solid var(--border) !important; border-top: none !important; }
hr { border-color: var(--border) !important; }
code, pre { background: var(--surface2) !important; border: 1px solid var(--border) !important; color: var(--accent2) !important; border-radius: 6px !important; }
.stAlert { background: var(--surface) !important; border: 1px solid var(--border) !important; color: var(--text) !important; }

.result-box { background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; margin-top: 1.5rem; }
.result-item { background: var(--surface); border-radius: 8px; padding: 1rem; margin-bottom: 0.8rem; border-left: 4px solid var(--accent3); box-shadow: var(--shadow); }
.result-golongan { font-family: var(--font-mono); font-weight: 700; color: var(--accent3); }
.tag { display: inline-block; background: #e0f2fe; border: 1px solid #bae6fd; color: #0369a1; font-size: 0.78rem; padding: 0.25rem 0.7rem; border-radius: 999px; margin: 0.2rem; }
</style>""", unsafe_allow_html=True)

# ─── 3. DATABASE & FUNGSI ORGANIK (DIKEMBALIKAN UTUH) ───────────────────────
SENYAWA_DB = [
    {"Nama": "Etanol", "Rumus": "C₂H₅OH", "Golongan": "Alkohol", "Uji Positif": "Esterifikasi, Iodoform", "CAS": "64-17-5"},
    {"Nama": "Metanol", "Rumus": "CH₃OH", "Golongan": "Alkohol", "Uji Positif": "Esterifikasi", "CAS": "67-56-1"},
    {"Nama": "Aseton", "Rumus": "CH₃COCH₃", "Golongan": "Keton", "Uji Positif": "2,4-DNPH", "CAS": "67-64-1"},
    {"Nama": "Formaldehid", "Rumus": "HCHO", "Golongan": "Aldehid", "Uji Positif": "Tollens, Fehling", "CAS": "50-00-0"},
    {"Nama": "Asetaldehid", "Rumus": "CH₃CHO", "Golongan": "Aldehid", "Uji Positif": "Tollens, Fehling, Iodoform", "CAS": "75-07-0"},
    {"Nama": "Asam Asetat", "Rumus": "CH₃COOH", "Golongan": "Asam Karboksilat", "Uji Positif": "Lakmus, Esterifikasi", "CAS": "64-19-7"},
    {"Nama": "Asam Format", "Rumus": "HCOOH", "Golongan": "Asam Karboksilat", "Uji Positif": "Tollens, Lakmus", "CAS": "64-18-6"},
    {"Nama": "Etil Asetat", "Rumus": "CH₃COOC₂H₅", "Golongan": "Ester", "Uji Positif": "Hidrolisis", "CAS": "141-78-6"},
    {"Nama": "Fenol", "Rumus": "C₆H₅OH", "Golongan": "Fenol", "Uji Positif": "FeCl₃ (ungu)", "CAS": "108-95-2"},
    {"Nama": "Etilena", "Rumus": "CH₂=CH₂", "Golongan": "Alkena", "Uji Positif": "Bromin, Baeyer", "CAS": "74-85-1"},
    {"Nama": "Benzena", "Rumus": "C₆H₆", "Golongan": "Aromatik", "Uji Positif": "Nitrasi", "CAS": "71-43-2"},
    {"Nama": "Glukosa", "Rumus": "C₆H₁₂O₆", "Golongan": "Karbohidrat", "Uji Positif": "Tollens, Fehling, Benedict", "CAS": "50-99-7"},
    {"Nama": "Sukrosa", "Rumus": "C₁₂H₂₂O₁₁", "Golongan": "Karbohidrat", "Uji Positif": "Molisch", "CAS": "57-50-1"},
    {"Nama": "Albumin", "Rumus": "Protein", "Golongan": "Protein", "Uji Positif": "Biuret, Ninhidrin", "CAS": "—"},
    {"Nama": "Anilin", "Rumus": "C₆H₅NH₂", "Golongan": "Amina", "Uji Positif": "Reaksi diazonium", "CAS": "62-53-3"},
]

MATERI_UJI = {
    "🟡 Uji Bromin": {
        "tujuan": "Mendeteksi ikatan rangkap (C=C) pada senyawa tak jenuh.",
        "pereaksi": "Larutan Br₂ dalam CCl₄ atau air.",
        "prinsip": "Bromin bereaksi adisi dengan ikatan rangkap. Warna coklat-merah bromin akan hilang (dekolorisasi) bila bereaksi dengan alkena atau alkuna.",
        "reaksi": "Alkena + Br₂ → Dibromoalkana (tak berwarna)",
        "positif": "Warna bromin (coklat-merah) hilang menjadi bening.",
        "negatif": "Warna bromin tetap / tidak berubah.",
        "contoh_positif": ["Etilena", "Propena", "Butadiena"],
    },
    "🟣 Uji Baeyer": {
        "tujuan": "Mendeteksi ketidakjenuhan (ikatan rangkap) dan gugus yang mudah dioksidasi.",
        "pereaksi": "KMnO₄ encer (0,1%) dalam suasana netral/basa.",
        "prinsip": "KMnO₄ mengoksidasi ikatan rangkap atau gugus aldehid. Mn⁷⁺ (ungu) tereduksi menjadi MnO₂ (coklat).",
        "reaksi": "3 R-CH=CH-R' + 2 KMnO₄ + 4H₂O → 3 R-CHOH-CHOH-R' + 2 MnO₂ + 2 KOH",
        "positif": "Warna ungu hilang, terbentuk endapan coklat MnO₂.",
        "negatif": "Warna ungu tetap.",
        "contoh_positif": ["Alkena", "Alkuna", "Aldehid", "Alkohol primer"],
    },
    "⚪ Uji Tollens": {
        "tujuan": "Identifikasi spesifik gugus aldehid (−CHO).",
        "pereaksi": "Pereaksi Tollens: [Ag(NH₃)₂]⁺ (larutan perak-amonia).",
        "prinsip": "Aldehid mereduksi ion perak (Ag⁺) menjadi logam perak (Ag⁰) yang mengendap di dinding tabung membentuk cermin perak.",
        "reaksi": "R-CHO + 2[Ag(NH₃)₂]⁺ + 2OH⁻ → R-COO⁻ + 2Ag↓ + 4NH₃ + H₂O",
        "positif": "Terbentuk cermin perak (silver mirror) di dinding tabung.",
        "negatif": "Tidak ada perubahan / larutan tetap bening.",
        "contoh_positif": ["Formaldehid", "Asetaldehid", "Glukosa", "Asam Format"],
    },
    "🔵 Uji Fehling": {
        "tujuan": "Membedakan aldehid alifatik dari keton.",
        "pereaksi": "Fehling A (CuSO₄) + Fehling B (NaOH + Na-Kalium tartrat).",
        "prinsip": "Cu²⁺ (biru) dalam kompleks tartrat direduksi oleh aldehid menjadi Cu⁺ (merah bata Cu₂O).",
        "reaksi": "R-CHO + 2Cu²⁺ + 5OH⁻ → R-COO⁻ + Cu₂O↓ + 3H₂O",
        "positif": "Endapan merah bata (Cu₂O).",
        "negatif": "Larutan tetap biru.",
        "contoh_positif": ["Formaldehid", "Glukosa", "Maltosa"],
    },
    "🟤 Uji Iodoform": {
        "tujuan": "Mendeteksi gugus metil keton (CH₃CO−) atau alkohol sekunder dengan gugus metil (CH₃CHOH−).",
        "pereaksi": "I₂ dalam NaOH (KI/I₂ + NaOH).",
        "prinsip": "Metil keton bereaksi dengan I₂/NaOH membentuk iodoform (CHI₃) yang berwarna kuning dengan bau khas.",
        "reaksi": "CH₃COR + 3I₂ + 3NaOH → CHI₃↓ + RCOONa + 3NaI + 3H₂O",
        "positif": "Endapan kuning CHI₃ berbau antiseptik.",
        "negatif": "Tidak ada endapan kuning.",
        "contoh_positif": ["Aseton", "Etanol", "Asetaldehid", "2-Propanol"],
    },
    "🟢 Uji FeCl₃": {
        "tujuan": "Mendeteksi senyawa fenol (gugus −OH aromatik).",
        "pereaksi": "FeCl₃ 1% dalam air.",
        "prinsip": "Ion Fe³⁺ membentuk kompleks berwarna dengan gugus fenolat.",
        "reaksi": "3 ArOH + FeCl₃ → [Fe(OAr)₃] + 3 HCl",
        "positif": "Terbentuk warna ungu, biru, atau hijau tergantung senyawa.",
        "negatif": "Tidak ada perubahan warna.",
        "contoh_positif": ["Fenol", "Resorsinol", "Katekin"],
    },
    "🔴 Uji Biuret": {
        "tujuan": "Mendeteksi protein (ikatan peptida −CO−NH−).",
        "pereaksi": "NaOH + CuSO₄ encer.",
        "prinsip": "Ion Cu²⁺ membentuk kompleks dengan dua atau lebih ikatan peptida menghasilkan warna ungu-violet.",
        "reaksi": "Cu²⁺ + ikatan peptida → Kompleks ungu",
        "positif": "Warna ungu-violet muncul.",
        "negatif": "Larutan tetap biru muda.",
        "contoh_positif": ["Albumin", "Kasein", "Gelatin"],
    },
    "🟠 Uji Molisch": {
        "tujuan": "Uji umum keberadaan karbohidrat.",
        "pereaksi": "α-naftol dalam etanol + H₂SO₄ pekat.",
        "prinsip": "H₂SO₄ mendehidrasi karbohidrat menjadi furfural yang bereaksi dengan α-naftol membentuk cincin berwarna.",
        "reaksi": "Karbohidrat →(H₂SO₄) Furfural + α-naftol → Kompleks ungu-merah",
        "positif": "Cincin ungu-merah di batas dua lapisan cairan.",
        "negatif": "Tidak ada cincin berwarna.",
        "contoh_positif": ["Glukosa", "Sukrosa", "Amilum", "Selulosa"],
    },
}

def identifikasi_senyawa(jawaban: dict) -> list:
    kandidat = []
    larut, bromin, baeyer = jawaban.get("larut"), jawaban.get("bromin"), jawaban.get("baeyer")
    tollens, fehling, iodoform = jawaban.get("tollens"), jawaban.get("fehling"), jawaban.get("iodoform")
    fecl3, biuret, molisch, asam = jawaban.get("fecl3"), jawaban.get("biuret"), jawaban.get("molisch"), jawaban.get("asam")

    if tollens == "Ya" and fehling == "Ya":
        if molisch == "Ya": kandidat.append(("Karbohidrat (Gula Pereduksi)", "Tollens ✅ + Fehling ✅ + Molisch ✅ → Aldosa seperti Glukosa"))
        else: kandidat.append(("Aldehid", "Tollens ✅ + Fehling ✅ → Aldehid alifatik (Formaldehid, Asetaldehid)"))
    elif tollens == "Ya" and fehling == "Tidak":
        kandidat.append(("Aldehid Aromatik / Asam Format", "Tollens ✅ + Fehling ❌ → Kemungkinan benzaldehid atau asam format"))
    if iodoform == "Ya" and tollens == "Tidak":
        kandidat.append(("Keton (Metil Keton)", "Iodoform ✅ + Tollens ❌ → Metil keton seperti Aseton"))
    elif iodoform == "Ya" and tollens == "Ya":
        kandidat.append(("Asetaldehid", "Iodoform ✅ + Tollens ✅ → Kemungkinan besar Asetaldehid (CH₃CHO)"))
    if fecl3 == "Ya":
        kandidat.append(("Fenol", "FeCl₃ ✅ → Gugus fenol terdeteksi (warna ungu/biru/hijau)"))
    if bromin == "Ya" and baeyer == "Ya" and tollens == "Tidak" and fecl3 == "Tidak":
        kandidat.append(("Alkena / Alkuna", "Bromin ✅ + Baeyer ✅ + Tollens ❌ → Senyawa tak jenuh"))
    if iodoform == "Ya" and tollens == "Tidak" and fecl3 == "Tidak" and bromin == "Tidak":
        kandidat.append(("Alkohol (Etanol / 2-Propanol)", "Iodoform ✅ + Tollens ❌ + Bromin ❌ → Alkohol dengan gugus CH₃CHOH−"))
    if asam == "Ya" and tollens == "Tidak" and fehling == "Tidak":
        kandidat.append(("Asam Karboksilat", "Sifat asam ✅ + Tollens ❌ → Kemungkinan asam karboksilat"))
    if biuret == "Ya":
        kandidat.append(("Protein", "Biuret ✅ → Ikatan peptida terdeteksi. Kemungkinan protein"))
    if molisch == "Ya" and tollens == "Tidak" and fehling == "Tidak":
        kandidat.append(("Karbohidrat (Non-Pereduksi)", "Molisch ✅ + Tollens ❌ → Karbohidrat non-pereduksi (Sukrosa, Amilum)"))
    if not kandidat:
        kandidat.append(("Tidak Teridentifikasi", "Kombinasi hasil uji tidak cocok dengan pola yang ada. Coba periksa kembali hasil uji Anda."))
    return kandidat


# ─── 4. DATABASE & FUNGSI METATESIS ─────────────────────────────────────────
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
    'C2O4': (-2, True), 'S2O3': (-2, True), 'HPO4': (-2, True),
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
    if kation == 'H' and anion in ['OH', 'O']: return False
    if kation in ['Na', 'K', 'NH4', 'Li', 'Rb', 'Cs']: return False
    if anion in ['NO3', 'CH3COO']: return False
    if anion in ['Cl', 'Br', 'I']: return True if kation in ['Ag', 'Pb', 'Hg'] else False
    if anion == 'SO4': return True if kation in ['Ba', 'Ca', 'Sr', 'Pb'] else False
    if anion == 'OH': return False if kation in ['Ca', 'Sr', 'Ba'] else True
    if anion in ['CO3', 'PO4', 'CrO4', 'S', 'O']: return True
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
        <p>✨ Agung Nugraha (NIM: 2560557) &nbsp; | &nbsp; ✨ Alifia Citra Nabila &nbsp; | &nbsp; ✨ Haifa Maulafida<br>✨ Nabila Putri Khorinnisa &nbsp; | &nbsp; ✨ Rania Ayudia</p>
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
#  B. MODUL: IDENTIFIKASI SENYAWA ORGANIK (KINI SUDAH LENGKAP KEMBALI)
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.app_mode == "organik":
    
    if st.session_state.halaman_org == "landing":
        st.button("🏠 Kembali ke Portal Utama", on_click=go_portal)
        st.markdown("""
        <div class="landing-hero" style="padding-top:1rem;">
            <div class="hero-badge">⚗️ Kimia Organik Kualitatif</div>
            <h1 class="hero-title">Sistem Identifikasi<br><span class="hero-accent">Senyawa Organik</span></h1>
            <p class="hero-desc">Platform edukasi interaktif untuk mengidentifikasi golongan senyawa organik berdasarkan hasil pengujian laboratorium.</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔬 Mulai Identifikasi", use_container_width=True, type="primary"): nav_org("identifikasi")
        with col2:
            if st.button("📚 Materi Uji Organik", use_container_width=True): nav_org("materi")
        with col3:
            if st.button("🗄️ Database Senyawa", use_container_width=True): nav_org("database")

        st.markdown("""
        <div class="feature-grid">
            <div class="feature-card"><div class="feature-icon">🔬</div><h3>Identifikasi Senyawa</h3><p>Jawab pertanyaan berdasarkan hasil praktikum dan dapatkan identifikasi golongan.</p></div>
            <div class="feature-card"><div class="feature-icon">📚</div><h3>Materi Lengkap</h3><p>Pelajari teori, prinsip, pereaksi, dan interpretasi 8 jenis uji kualitatif organik.</p></div>
            <div class="feature-card"><div class="feature-icon">🗄️</div><h3>Database Senyawa</h3><p>Akses database 15+ senyawa organik dengan rumus, golongan, dan uji positifnya.</p></div>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.halaman_org == "identifikasi":
        if st.button("← Kembali ke Menu Organik"): nav_org("landing")
        st.markdown('<h2 class="page-title">🔬 Identifikasi Senyawa Organik</h2>', unsafe_allow_html=True)
        st.markdown('<p class="page-sub">Jawab pertanyaan berikut berdasarkan hasil pengujian di laboratorium Anda.</p>', unsafe_allow_html=True)

        st.markdown('<div class="feature-card" style="padding:2rem;">', unsafe_allow_html=True)
        jawaban = {}
        st.markdown("#### 💧 Kelarutan")
        jawaban["larut"] = st.radio("Apakah sampel larut dalam air?", ["Ya", "Tidak", "Sebagian"], horizontal=True)
        st.divider()
        st.markdown("#### 🧪 Uji Ikatan Rangkap")
        col1, col2 = st.columns(2)
        with col1: jawaban["bromin"] = st.radio("Warna bromin hilang (Uji Bromin)?", ["Ya", "Tidak"], horizontal=True)
        with col2: jawaban["baeyer"] = st.radio("Warna ungu hilang (Uji Baeyer)?", ["Ya", "Tidak"], horizontal=True)
        st.divider()
        st.markdown("#### ⚗️ Uji Oksidasi-Reduksi")
        col1, col2 = st.columns(2)
        with col1: jawaban["tollens"] = st.radio("Terbentuk cermin perak (Uji Tollens)?", ["Ya", "Tidak"], horizontal=True)
        with col2: jawaban["fehling"] = st.radio("Endapan merah bata (Uji Fehling)?", ["Ya", "Tidak"], horizontal=True)
        st.divider()
        st.markdown("#### 🔍 Uji Spesifik Gugus Fungsi")
        col1, col2, col3 = st.columns(3)
        with col1: jawaban["iodoform"] = st.radio("Endapan kuning (Uji Iodoform)?", ["Ya", "Tidak"], horizontal=True)
        with col2: jawaban["fecl3"] = st.radio("Warna ungu/biru (Uji FeCl₃)?", ["Ya", "Tidak"], horizontal=True)
        with col3: jawaban["asam"] = st.radio("Mengubah lakmus merah (asam)?", ["Ya", "Tidak"], horizontal=True)
        st.divider()
        st.markdown("#### 🧬 Uji Biomolekul")
        col1, col2 = st.columns(2)
        with col1: jawaban["biuret"] = st.radio("Warna ungu-violet (Uji Biuret)?", ["Ya", "Tidak"], horizontal=True)
        with col2: jawaban["molisch"] = st.radio("Cincin ungu-merah (Uji Molisch)?", ["Ya", "Tidak"], horizontal=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔎 Identifikasi Sekarang!", type="primary", use_container_width=True):
            hasil = identifikasi_senyawa(jawaban)
            st.markdown('<div class="result-box"><h3>📊 Hasil Identifikasi</h3>', unsafe_allow_html=True)
            for golongan, alasan in hasil:
                st.markdown(f'<div class="result-item"><div class="result-golongan">✅ {golongan}</div><div class="result-alasan">{alasan}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if len(hasil) > 1: st.info("💡 **Catatan:** Beberapa golongan terdeteksi. Lakukan uji tambahan untuk memastikan.")

    elif st.session_state.halaman_org == "materi":
        if st.button("← Kembali ke Menu Organik"): nav_org("landing")
        st.markdown('<h2 class="page-title">📚 Materi Uji Kualitatif</h2>', unsafe_allow_html=True)
        for nama_uji, data in MATERI_UJI.items():
            with st.expander(f"{nama_uji}", expanded=False):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**🎯 Tujuan:**\n{data['tujuan']}\n\n**🧪 Pereaksi:**\n{data['pereaksi']}\n\n**⚙️ Prinsip:**\n{data['prinsip']}")
                with c2:
                    st.markdown("**🔬 Reaksi:**")
                    st.code(data["reaksi"], language=None)
                    st.markdown(f"**✅ Positif:** {data['positif']}\n\n**❌ Negatif:** {data['negatif']}")
                st.markdown("**🔬 Contoh Senyawa Positif:**")
                cols = st.columns(len(data["contoh_positif"]))
                for i, senyawa in enumerate(data["contoh_positif"]): cols[i].markdown(f'<span class="tag">{senyawa}</span>', unsafe_allow_html=True)

    elif st.session_state.halaman_org == "database":
        if st.button("← Kembali ke Menu Organik"): nav_org("landing")
        st.markdown('<h2 class="page-title">🗄️ Database Senyawa</h2>', unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1: cari = st.text_input("🔍 Cari senyawa...")
        with c2: filter_golongan = st.selectbox("Filter", ["Semua"] + sorted(list(set(s["Golongan"] for s in SENYAWA_DB))))
        df = pd.DataFrame(SENYAWA_DB)
        if cari: df = df[df["Nama"].str.contains(cari, case=False) | df["Golongan"].str.contains(cari, case=False)]
        if filter_golongan != "Semua": df = df[df["Golongan"] == filter_golongan]
        st.dataframe(df, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════════
#  C. MODUL: REAKSI METATESIS (DENGAN 3 REAKTAN)
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
            # Urai semua reaktan yang diinput
            parsed_reactants = [urai_senyawa(r) for r in input_raw]
            
            if not all(k and a for k, a in parsed_reactants):
                st.error("❌ Salah satu senyawa tidak dikenali. Pastikan kaidah penulisan huruf kapital sudah benar.")
            else:
                kations = [p[0] for p in parsed_reactants]
                anions = [p[1] for p in parsed_reactants]
                
                # Buat semua kemungkinan produk silang
                produk_kemungkinan = set()
                for i, k in enumerate(kations):
                    for j, a in enumerate(anions):
                        if i != j:  # Jangan gabungkan kation dan anion dari reaktan yang sama
                            produk_kemungkinan.add(gabung_ion(k, a))
                
                try:
                    # Penyetaraan menggunakan ChemPy
                    r_setara, p_setara = balance_stoichiometry(set(input_raw), produk_kemungkinan)
                    
                    # Format string reaksi
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
                    
                    # Cek Driving Force pada produk yang BENAR-BENAR terbentuk
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
                    
                    # --- Lembar Kerja Analisis ---
                    st.markdown("### 🔍 Lembar Kerja Analisis Ion")
                    cols_urai = st.columns(len(input_raw))
                    
                    # Tampilkan Penguraian (Dinamis 2 atau 3 kolom)
                    for idx, (k, a) in enumerate(parsed_reactants):
                        c_k, c_a = fmt_muatan(kation_db[k][0], '+'), fmt_muatan(abs(anion_db[a][0]), '-')
                        with cols_urai[idx]:
                            st.markdown(f"**Penguraian Reaktan {idx+1}:**")
                            st.latex(f"{input_raw[idx]} \\longrightarrow {k}^{{{c_k}}} + {a}^{{{c_a}}}")
                            
                    st.info("💡 **Aturan Silang Muatan:** Kation (positif) dari satu reaktan bertukar pasangan dengan Anion (negatif) dari reaktan lain membentuk senyawa baru: $A^{x+} + B^{y-} \\rightarrow A_yB_x$")
                    
                    # Tampilkan Pembentukan Produk yang berhasil disetarakan
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
