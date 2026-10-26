import json
from dataclasses import dataclass
from typing import List
import streamlit as st

# Page Configuration - Retro Cím és Ikon
st.set_page_config(
    page_title="Covasna Travel DOS v1.0",
    page_icon="🖥️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- MODERN RETRO / MS-DOS STÍLUS (CUSTOM CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&display=swap');

    /* Globális hátterek és betűtípus */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b0f19 !important;
        color: #00ff66 !important;
        font-family: 'Fira Code', 'Courier New', monospace !important;
    }

    /* Oldalsáv stílus */
    [data-testid="stSidebar"] {
        background-color: #05080f !important;
        border-right: 2px solid #00ff66 !important;
    }

    /* Fejlécek Retro zöld/fehér neon fénye */
    h1, h2, h3, p, label, div, span {
        color: #00ff66 !important;
        font-family: 'Fira Code', 'Courier New', monospace !important;
    }

    h1 {
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.5);
        border-bottom: 2px dashed #00ff66;
        padding-bottom: 10px;
    }

    /* Kártyák / Dobozok MS-DOS kerettel */
    .retro-card {
        border: 2px solid #00ff66;
        background-color: #011409;
        padding: 16px;
        margin-bottom: 15px;
        border-radius: 4px;
        box-shadow: 4px 4px 0px 0px #008837;
    }

    .retro-card-header {
        font-weight: bold;
        border-bottom: 1px solid #00ff66;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }

    /* Gombok – Retro Terminal Stílus */
    .stButton > button, div[data-testid="stLinkButton"] > a {
        background-color: #00ff66 !important;
        color: #05080f !important;
        font-weight: bold !important;
        font-family: 'Fira Code', monospace !important;
        border: 2px solid #00ff66 !important;
        border-radius: 2px !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 3px 3px 0px 0px #005522 !important;
    }

    .stButton > button:hover, div[data-testid="stLinkButton"] > a:hover {
        background-color: #05080f !important;
        color: #00ff66 !important;
        box-shadow: 1px 1px 0px 0px #00ff66 !important;
        transform: translate(2px, 2px);
    }

    /* Bekérő mezők (Selectboxok) Mobilbarát és Retro dizájnnal */
    div[data-baseweb="select"] > div {
        background-color: #05080f !important;
        border: 1px solid #00ff66 !important;
        color: #00ff66 !important;
    }

    div[data-baseweb="popover"] {
        background-color: #05080f !important;
    }

    /* Info és Warning üzenetek retro színezése */
    .stAlert {
        background-color: #0b190f !important;
        border: 1px solid #00ff66 !important;
        color: #00ff66 !important;
    }
</style>
""", unsafe_allow_html=True)


# --- NYELVI SZÓTÁRAK ---
szotar = {
    "Magyar": {
        "cim": "📟 SYSTEM://KOVASZNA-TRAVEL-DOS v1.0",
        "kereses_fejlec": "► UTAVALASZTO TERMINAL",
        "honnan": "[INDIRALAS / ORIGIN]:",
        "hova": "[ERKEZES / DESTINATION]:",
        "gomb": "[ KERESES / SEARCH ]",
        "hiba_ugyanaz": "HIBA: Az indulási és érkezési város megegyezik!",
        "talalat": "TALALATOK",
        "nincs_jarat": ">>> Nincs elérhető járat ezen az útvonalon.",
        "buszok": "🚌 AUTOBUSZ JARATOK",
        "vonatok": "🚆 VONAT JARATOK",
        "nincs_busz": "Nincs elérhető buszjárat.",
        "nincs_vonat": "Nincs elérhető vonatjárat.",
        "indulas_szoveg": "INDULAS",
        "urlap_cim": "► UJ JARAT BEKULDÉSE",
        "urlap_szoveg": "Hiányzó járatot találtál? Küldd el a rendszerbe!",
        "urlap_gomb": "ŰRLAP MEGNYITÁSA",
    },
    "Română": {
        "cim": "📟 SYSTEM://COVASNA-TRAVEL-DOS v1.0",
        "kereses_fejlec": "► TERMINAL CAUTARE",
        "honnan": "[PLECARE / ORIGIN]:",
        "hova": "[SOSIRE / DESTINATION]:",
        "gomb": "[ CAUTA / SEARCH ]",
        "hiba_ugyanaz": "EROARE: Orașul de plecare și destinația sunt identice!",
        "talalat": "REZULTATE",
        "nincs_jarat": ">>> Nu există curse disponibile pe această rută.",
        "buszok": "🚌 CURSE AUTOBUZ",
        "vonatok": "🚆 CURSE TREN",
        "nincs_busz": "Nu există autobuze disponibile.",
        "nincs_vonat": "Nu există trenuri disponibile.",
        "indulas_szoveg": "PLECARE",
        "urlap_cim": "► PROPUNE O CURSA",
        "urlap_szoveg": "Ai găsit o cursă lipsă? Trimite-o în sistem!",
        "urlap_gomb": "DESCHIDE FORMULARUL",
    },
    "English": {
        "cim": "📟 SYSTEM://COVASNA-TRAVEL-DOS v1.0",
        "kereses_fejlec": "► ROUTE SEARCH TERMINAL",
        "honnan": "[DEPARTURE]:",
        "hova": "[DESTINATION]:",
        "gomb": "[ SEARCH RIDES ]",
        "hiba_ugyanaz": "ERROR: Departure and destination cannot be the same!",
        "talalat": "RESULTS",
        "nincs_jarat": ">>> No available rides on this route.",
        "buszok": "🚌 BUS SERVICES",
        "vonatok": "🚆 TRAIN SERVICES",
        "nincs_busz": "No bus services found.",
        "nincs_vonat": "No train services found.",
        "indulas_szoveg": "DEPARTURE",
        "urlap_cim": "► SUBMIT NEW RIDE",
        "urlap_szoveg": "Found a missing ride? Send it to our system!",
        "urlap_gomb": "OPEN FORM",
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

# Oldalsáv setup
st.sidebar.markdown("### 🌐 LANGUAGE / NYELV")
valasztott_nyelv = st.sidebar.selectbox("Válassz nyelvet / Select language", ["Magyar", "Română", "English"], label_visibility="collapsed")
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

# --- FŐOLDAL TARTALMA ---

st.title(t["cim"])
st.caption("SYS_STATUS: ONLINE | TERMINAL ID: 08-COV")

rendszer = UtazasiRendszer()

st.markdown(f"### {t['kereses_fejlec']}")

# Két oszlop a városválasztáshoz (Desktopon egymás mellett, Mobilon egymás alatt tör fel)
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
        st.error(t["hiba_ugyanaz"])
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
            
            # Mobilbarát retro kártyás megjelenítés
            col_b, col_v = st.columns(2)
            
            with col_b:
                st.markdown(f"#### {t['buszok']}")
                if buszok:
                    for b in buszok:
                        st.markdown(f"""
                        <div class="retro-card">
                            <div class="retro-card-header">🚌 {b.jaratszam}</div>
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
                        <div class="retro-card">
                            <div class="retro-card-header">🚆 {v.jaratszam}</div>
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