import json
from dataclasses import dataclass
from typing import List
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Covasna Travel | Cloud",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- FELHŐ-KÖNYED / HALVÁNYKÉK & FEHÉR DESIGN (CUSTOM CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

    /* Globális hátterek: tiszta, világos felhő hatás */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f4f8fb 0%, #e9f2f9 100%) !important;
        color: #2c3e50 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Oldalsáv stílus - lágy pasztellkék hangulat */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #d0e1ed !important;
        box-shadow: 2px 0 10px rgba(180, 200, 220, 0.1);
    }

    /* Fejlécek és szövegek */
    h1, h2, h3, h4, p, label, div, span {
        color: #2b3a4a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    h1 {
        font-weight: 600;
        letter-spacing: -0.5px;
        color: #1a365d !important;
    }

    /* Vékony, halványkék vonalak (Divider) */
    hr {
        border: none;
        height: 1px;
        background-color: #d2e3f3 !important;
        margin: 25px 0;
    }

    /* Levegős, finom keretes kártyák (Felhő stílus) */
    .cloud-card {
        border: 1px solid #cce0f0;
        background-color: #ffffff;
        padding: 18px;
        margin-bottom: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(170, 200, 230, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .cloud-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(170, 200, 230, 0.25);
    }

    .cloud-card-header {
        font-weight: 600;
        color: #1d4ed8;
        border-bottom: 1px solid #e2edf7;
        padding-bottom: 8px;
        margin-bottom: 10px;
        font-size: 1.05rem;
    }

    /* Gombok – Köned, elegáns kék design */
    .stButton > button, div[data-testid="stLinkButton"] > a {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        border: 1px solid #93c5fd !important;
        border-radius: 10px !important;
        width: 100% !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton > button:hover, div[data-testid="stLinkButton"] > a:hover {
        background: linear-gradient(135deg, #2563eb 100%, #1d4ed8 0%) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.35) !important;
        transform: translateY(-1px);
    }

    /* Input mezők (Selectboxok) vékony kék kerettel */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #3b82f6 !important;
    }

    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* Info és Warning üzenetek lágy pasztell háttérrel */
    .stAlert {
        background-color: #f0f7ff !important;
        border: 1px solid #bae6fd !important;
        color: #0369a1 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)


# --- NYELVI SZÓTÁRAK ---
szotar = {
    "Magyar": {
        "cim": "☁️ Kovászna — Kézdi — Szentgyörgy",
        "alcim": "Légies, gyors utazási és járatkereső rendszer",
        "kereses_fejlec": "🔍 Útvonal keresése",
        "honnan": "Honnan indulnál?",
        "hova": "Hova utaznál?",
        "gomb": "Járatok keresése",
        "hiba_ugyanaz": "Az indulási és az érkezési város nem lehet azonos!",
        "talalat": "Találatok",
        "nincs_jarat": "Nem találtunk járatot ezen az útvonalon.",
        "buszok": "🚌 Buszjáratok",
        "vonatok": "🚆 Vonatjáratok",
        "nincs_busz": "Nincs elérhető busz.",
        "nincs_vonat": "Nincs elérhető vonat.",
        "indulas_szoveg": "Indulás",
        "urlap_cim": "✈️ Új járat javaslása",
        "urlap_szoveg": "Hiányzó járatot találtál? Küldd el nekünk!",
        "urlap_gomb": "Beküldési űrlap",
    },
    "Română": {
        "cim": "☁️ Covasna — Târgu Secuiesc — Sfântu Gheorghe",
        "alcim": "Sistem de căutare curse simplu și aerisit",
        "kereses_fejlec": "🔍 Căutare rute",
        "honnan": "Oraș plecare:",
        "hova": "Oraș destinație:",
        "gomb": "Caută curse",
        "hiba_ugyanaz": "Orașul de plecare și cel de destinație nu pot fi identice!",
        "talalat": "Rezultate",
        "nincs_jarat": "Nu am găsit curse pe această rută.",
        "buszok": "🚌 Curse de autobuz",
        "vonatok": "🚆 Curse de tren",
        "nincs_busz": "Nu există autobuze.",
        "nincs_vonat": "Nu există trenuri.",
        "indulas_szoveg": "Plecare",
        "urlap_cim": "✈️ Propune o cursă",
        "urlap_szoveg": "Ai găsit o cursă lipsă? Trimite-o!",
        "urlap_gomb": "Formular trimitere",
    },
    "English": {
        "cim": "☁️ Covasna — Târgu Secuiesc — Sfântu Gheorghe",
        "alcim": "Smooth & lightweight travel guide system",
        "kereses_fejlec": "🔍 Search Routes",
        "honnan": "Departure city:",
        "hova": "Destination city:",
        "gomb": "Search Rides",
        "hiba_ugyanaz": "Departure and destination cities cannot be the same!",
        "talalat": "Results",
        "nincs_jarat": "No available rides on this route.",
        "buszok": "🚌 Bus Services",
        "vonatok": "🚆 Train Services",
        "nincs_busz": "No buses available.",
        "nincs_vonat": "No trains available.",
        "indulas_szoveg": "Departure",
        "urlap_cim": "✈️ Propose a ride",
        "urlap_szoveg": "Found a missing ride? Send it to us!",
        "urlap_gomb": "Submit Form",
    }
}

varos_nevek = {
    "Magyar": {
        "Kovászna": "Kovászna",
        "Kézdivásárhely": "Kézdi",
        "Sepsiszentgyörgy": "Szentgyörgy"
    },
    "Română": {
        "Covasna": "Kovászna",
        "Târgu Secuiesc": "Kézdi",
        "Sfântu Gheorghe": "Szentgyörgy"
    },
    "English": {
        "Covasna": "Kovászna",
        "Târgu Secuiesc": "Kézdi",
        "Sfântu Gheorghe": "Szentgyörgy"
    }
}

# Oldalsáv nyelvválasztó
st.sidebar.markdown("### 🌐 Nyelv / Limba / Language")
valasztott_nyelv = st.sidebar.selectbox("Nyelv", ["Magyar", "Română", "English"], label_visibility="collapsed")
t = szotar[valasztott_nyelv]  
aktualis_varosok = varos_nevek[valasztott_nyelv]  
megjelenitendo_varosok = list(aktualis_varosok.keys())

@dataclass
class Jarat:
    tipus: str
    honnan: str
    hova: str
    jaratszam: str
    indulas: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class UtazasiRendszer:
    FAJL_NEV = "jaratok.json"

    def __init__(self):
        self.jaratok: List[Jarat] = []
        self.adatok_betoltese()

    def adatok_betoltese(self):
        try:
            with open(self.FAJL_NEV, "r", encoding="utf-8") as f:
                adatok = json.load(f)
                self.jaratok = [Jarat.from_dict(d) for d in adatok]
        except FileNotFoundError:
            self.jaratok = []

# --- FŐOLDAL ---

st.title(t["cim"])
st.caption(t["alcim"])
st.markdown("---")

rendszer = UtazasiRendszer()

st.subheader(t["kereses_fejlec"])

# Oszlopos elrendezés mobilos/asztali reszponzivitással
col1, col2 = st.columns(2)

with col1:
    valasztott_honnan_nev = st.selectbox(t["honnan"], megjelenitendo_varosok, key="keres_honnan")

with col2:
    valasztott_hova_nev = st.selectbox(t["hova"], megjelenitendo_varosok, key="keres_hova", index=1 if len(megjelenitendo_varosok) > 1 else 0)

honnan = aktualis_varosok[valasztott_honnan_nev]
hova = aktualis_varosok[valasztott_hova_nev]

st.markdown("<br>", unsafe_allow_html=True)
kereses_inditva = st.button(t["gomb"])

if kereses_inditva:
    st.markdown("---")
    if honnan == hova:
        st.warning(t["hiba_ugyanaz"])
    else:
        talalatok = [
            j for j in rendszer.jaratok if j.honnan == honnan and j.hova == hova
        ]
        
        st.markdown(f"### {t['talalat']}: `{valasztott_honnan_nev}` ➔ `{valasztott_hova_nev}`")
        
        if not talalatok:
            st.info(t["nincs_jarat"])
        else:
            buszok = [j for j in talalatok if j.tipus == "Busz"]
            vonatok = [j for j in talalatok if j.tipus == "Vonat"]
            
            col_b, col_v = st.columns(2)
            
            with col_b:
                st.markdown(f"#### {t['buszok']}")
                if buszok:
                    for b in buszok:
                        st.markdown(f"""
                        <div class="cloud-card">
                            <div class="cloud-card-header">🚌 Járat: {b.jaratszam}</div>
                            <div><b>{t['indulas_szoveg']}:</b> <code>{b.indulas}</code></div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write(t["nincs_busz"])
                    
            with col_v:
                st.markdown(f"#### {t['vonatok']}")
                if vonatok:
                    for v in vonatok:
                        st.markdown(f"""
                        <div class="cloud-card">
                            <div class="cloud-card-header">🚆 Járat: {v.jaratszam}</div>
                            <div><b>{t['indulas_szoveg']}:</b> <code>{v.indulas}</code></div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write(t["nincs_vonat"])

# Oldalsáv alsó része (Űrlap)
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['urlap_cim']}")
st.sidebar.write(t["urlap_szoveg"])

urlap_link = "https://forms.gle/kCtmR8P4gRP7acGG7"
st.sidebar.link_button(t["urlap_gomb"], urlap_link)