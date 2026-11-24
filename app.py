import json
import os
import urllib.request
from datetime import datetime
from dataclasses import dataclass
from typing import List
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Utazás",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #12161c !important;
        color: #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background-color: #181d24 !important;
        border-right: 1px solid #2a3441 !important;
    }

    h1, h2, h3, h4, p, label, div, span {
        color: #f1f5f9 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    h1 {
        font-weight: 600;
        letter-spacing: -0.5px;
        color: #38bdf8 !important;
    }

    hr {
        border: none;
        height: 1px;
        background-color: #2a3441 !important;
        margin: 25px 0;
    }

    .stButton > button, div[data-testid="stLinkButton"] > a {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 10px !important;
        width: 100% !important;
        padding: 10px 20px !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #181f29 !important;
        border: 1px solid #2d3b4e !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }

    /* Oldalsáv navigáció (radio) gombosítása */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 8px;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        background-color: #181f29 !important;
        border: 1px solid #2a3441 !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        margin-bottom: 0 !important;
        transition: all 0.2s ease;
        cursor: pointer;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        border-color: #38bdf8 !important;
        background-color: #1e2736 !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"],
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.25) 0%, rgba(3, 105, 161, 0.25) 100%) !important;
        border-color: #38bdf8 !important;
    }

    /* APK letöltő kártya */
    .apk-box {
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.14) 0%, rgba(24, 29, 36, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.45);
        border-radius: 12px;
        padding: 16px 18px;
        margin: 14px 0 18px 0;
    }

    .apk-title {
        font-size: 1rem;
        font-weight: 600;
        color: #38bdf8 !important;
        margin-bottom: 4px;
    }

    .apk-desc {
        font-size: 0.9rem;
        color: #cbd5e1 !important;
        margin-bottom: 0;
    }

    /* Taxi kártyák stílusa */
    .taxi-card {
        background-color: #181d24;
        border: 1px solid #2a3441;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: border-color 0.2s ease, transform 0.15s ease;
    }

    .taxi-card:hover {
        border-color: #38bdf8;
    }

    .taxi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .taxi-name {
        font-size: 1.05rem;
        font-weight: 600;
        color: #f8fafc !important;
    }

    .taxi-badge {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 999px;
        background-color: rgba(56, 189, 248, 0.15);
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.35);
    }

    .taxi-phones {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .taxi-phone-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #12161c;
        border: 1px solid #2d3b4e;
        color: #38bdf8 !important;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 0.92rem;
        padding: 7px 12px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }

    .taxi-phone-btn:hover {
        background-color: #0284c7;
        border-color: #38bdf8;
        color: #ffffff !important;
    }

    /* Narancssárga figyelmeztető jelmagyarázat */
    .orange-legend {
        background-color: rgba(249, 115, 22, 0.14);
        border: 1px solid rgba(251, 146, 60, 0.65);
        border-left: 4px solid #f97316;
        border-radius: 10px;
        padding: 10px 14px;
        margin-top: 10px;
        font-size: 0.9rem;
        color: #fdba74 !important;
    }
</style>
""", unsafe_allow_html=True)

szotar = {
    "Magyar": {
        "cim": "Utazás",
        "alcim": "Kovászna — Kézdi — Szentgyörgy",
        "menu_cim": "🧭 Navigáció",
        "ful_helyi": "🚌 Kovásznai helyi járatok",
        "ful_tavolsagi": "🚆 Interurbán járatok (Kézdi / Szentgyörgy)",
        "ful_szentgyorgy": "🚌 Szentgyörgy (Multitrans)",
        "ful_taxi": "🚕 Taxi elérhetőségek",
        "kereses_fejlec": "🔍 Útvonal keresése",
        "honnan": "Honnan indulnál?",
        "hova": "Hova utaznál?",
        "gomb": "Járatok keresése",
        "hiba_ugyanaz": "Az indulási és az érkezési helyszín nem lehet azonos!",
        "talalat": "Találatok",
        "nincs_jarat": "Nem találtunk közvetlen járatot. Átszállásos lehetőségek:",
        "nincs_semmi": "Nem találtunk sem közvetlen, sem átszállásos járatot.",
        "buszok": "🚌 Buszjáratok",
        "vonatok": "🚆 Vonatjáratok",
        "nincs_busz": "Nincs elérhető busz.",
        "nincs_vonat": "Nincs elérhető vonat.",
        "indulas_szoveg": "Indulás",
        "megjegyzes": "Megjegyzés",
        "nincs_hetvegen": "Nem közlekedik hétvégén és ünnepnapokon",
        "hetvegi_magyarazat": "🟠 Narancssárga sorok: ezek a Codreanu járatok nem közlekednek hétvégén, illetve ünnepnapokon.",
        "urlap_cim": "✈️ Új járat javaslása",
        "urlap_szoveg": "Hiányzó járatot találtál? Küldd el nekünk!",
        "urlap_gomb": "Beküldési űrlap",
        "szentgyorgy_cim": "Sepsiszentgyörgy Helyi Menetrend",
        "szentgyorgy_alcim": "Multitrans okos kereső (Időalapú rendezés)",
        "apk_cim": "📱 Android alkalmazás offline móddal",
        "apk_leiras": "A sepsiszentgyörgyi helyi járatok offline is böngészhetők telefonon a CVTravel Android appal.",
        "apk_gomb": "⬇️ cvtravel.apk letöltése",
        "frissites_sikeres": "A menetrend sikeresen frissítve!",
        "frissites_hiba": "Hiba történt a frissítés során.",
        "vonal": "Vonal",
        "celallomas": "Célállomás",
        "atszallas": "🔄 Átszállásos találatok",
        "kozvetlen": "✨ Közvetlen járatok",
        "nincs_ma_jarat": "A megadott útvonalra nincs közvetlen járat. Átszállásos lehetőségek:",
        "talalatok_szama": "Találatok száma",
        "szuro_honnan": "Szűrés / Keresés megállóra:",
        "szuro_hova": "Szűrés / Keresés célállomásra:",
        "taxi_cim": "🚕 Helyi Taxi Elérhetőségek",
        "taxi_alcim": "Kattints a telefonszámra a közvetlen híváshoz",
        "taxi_varos_szuro": "Város kiválasztása:",
        "taxi_osszes_varos": "Összes város",
        "taxi_kereses": "Keresés név vagy telefonszám alapján:",
        "taxi_kereses_placeholder": "Pl. Capitaly, Tóth József, 0740...",
        "taxi_nincs_talalat": "Nincs a keresésnek megfelelő taxis elérhetőség.",
        "varos_kovaszna": "Kovászna",
        "varos_kezdi": "Kézdivásárhely",
        "varos_szentgyorgy": "Sepsiszentgyörgy",
    },
    "Română": {
        "cim": "Utazás",
        "alcim": "Covasna — Târgu Secuiesc — Sfântu Gheorghe",
        "menu_cim": "🧭 Navigare",
        "ful_helyi": "🚌 Curse locale Covasna",
        "ful_tavolsagi": "🚆 Curse interurbane (Târgu Secuiesc / Sf. Gheorghe)",
        "ful_szentgyorgy": "🚌 Sf. Gheorghe (Multitrans)",
        "ful_taxi": "🚕 Contacte Taxi",
        "kereses_fejlec": "🔍 Căutare rute",
        "honnan": "Locație plecare:",
        "hova": "Locație destinație:",
        "gomb": "Caută curse",
        "hiba_ugyanaz": "Locația de plecare și cea de destinație nu pot fi identice!",
        "talalat": "Rezultate",
        "nincs_jarat": "Nu am găsit curse directe. Opțiuni cu schimb:",
        "nincs_semmi": "Nu am găsit nicio cursă directă sau cu schimb.",
        "buszok": "🚌 Curse de autobuz",
        "vonatok": "🚆 Curse de tren",
        "nincs_busz": "Nu există autobuze.",
        "nincs_vonat": "Nu există trenuri.",
        "indulas_szoveg": "Plecare",
        "megjegyzes": "Mențiune",
        "nincs_hetvegen": "Nu circulă în weekend și de sărbători legale",
        "hetvegi_magyarazat": "🟠 Rândurile portocalii: aceste curse Codreanu nu circulă în weekend și de sărbători legale.",
        "urlap_cim": "✈️ Propune o cursă",
        "urlap_szoveg": "Ai găsit o cursă lipsă? Trimite-o!",
        "urlap_gomb": "Formular trimitere",
        "szentgyorgy_cim": "Orar Local Sfântu Gheorghe",
        "szentgyorgy_alcim": "Orar Multitrans căutare inteligentă",
        "apk_cim": "📱 Aplicație Android cu mod offline",
        "apk_leiras": "Poți consulta cursele locale din Sfântu Gheorghe și offline cu aplicația Android CVTravel.",
        "apk_gomb": "⬇️ Descarcă cvtravel.apk",
        "frissites_sikeres": "Orarul a fost actualizat cu succes!",
        "frissites_hiba": "Eroare la actualizare.",
        "vonal": "Linie",
        "celallomas": "Destinație",
        "atszallas": "🔄 Rute cu schimb",
        "kozvetlen": "✨ Curse directe",
        "nincs_ma_jarat": "Nu există curse directe. Opțiuni cu schimb:",
        "talalatok_szama": "Număr de rezultate",
        "szuro_honnan": "Filtrare stație plecare:",
        "szuro_hova": "Filtrare destinație:",
        "taxi_cim": "🚕 Contacte Taxi Locale",
        "taxi_alcim": "Apasă pe numărul de telefon pentru apelare directă",
        "taxi_varos_szuro": "Selectează orașul:",
        "taxi_osszes_varos": "Toate orașele",
        "taxi_kereses": "Caută după nume sau număr de telefon:",
        "taxi_kereses_placeholder": "Ex. Capitaly, Tóth József, 0740...",
        "taxi_nincs_talalat": "Nu s-au găsit contacte taxi pentru căutarea ta.",
        "varos_kovaszna": "Covasna",
        "varos_kezdi": "Târgu Secuiesc",
        "varos_szentgyorgy": "Sfântu Gheorghe",
    },
    "English": {
        "cim": "Utazás",
        "alcim": "Covasna — Târgu Secuiesc — Sfântu Gheorghe",
        "menu_cim": "🧭 Navigation",
        "ful_helyi": "🚌 Covasna Local Buses",
        "ful_tavolsagi": "🚆 Intercity Rides (Târgu Secuiesc / Sf. Gheorghe)",
        "ful_szentgyorgy": "🚌 Sf. Gheorghe Local (Multitrans)",
        "ful_taxi": "🚕 Taxi Contacts",
        "kereses_fejlec": "🔍 Search Routes",
        "honnan": "Departure location:",
        "hova": "Destination location:",
        "gomb": "Search Rides",
        "hiba_ugyanaz": "Departure and destination locations cannot be the same!",
        "talalat": "Results",
        "nincs_jarat": "No direct rides found. Options with transfer:",
        "nincs_semmi": "No direct or connecting rides found.",
        "buszok": "🚌 Bus Services",
        "vonatok": "🚆 Train Services",
        "nincs_busz": "No buses available.",
        "nincs_vonat": "No trains available.",
        "indulas_szoveg": "Departure",
        "megjegyzes": "Note",
        "nincs_hetvegen": "Does not operate on weekends and public holidays",
        "hetvegi_magyarazat": "🟠 Orange rows: these Codreanu services do not operate on weekends or public holidays.",
        "urlap_cim": "✈️ Propose a ride",
        "urlap_szoveg": "Found a missing ride? Send it to us!",
        "urlap_gomb": "Submit Form",
        "szentgyorgy_cim": "Sfântu Gheorghe Local Schedule",
        "szentgyorgy_alcim": "Multitrans smart search",
        "apk_cim": "📱 Android App with Offline Mode",
        "apk_leiras": "Browse Sfântu Gheorghe local transit offline on your phone using the CVTravel Android app.",
        "apk_gomb": "⬇️ Download cvtravel.apk",
        "frissites_sikeres": "Schedule successfully updated!",
        "frissites_hiba": "Error updating data.",
        "vonal": "Line",
        "celallomas": "Destination",
        "atszallas": "🔄 Connecting routes",
        "kozvetlen": "✨ Direct rides",
        "nincs_ma_jarat": "No direct rides. Options with transfer:",
        "talalatok_szama": "Number of results",
        "szuro_honnan": "Filter departure station:",
        "szuro_hova": "Filter destination:",
        "taxi_cim": "🚕 Local Taxi Contacts",
        "taxi_alcim": "Tap a phone number to call directly",
        "taxi_varos_szuro": "Select city:",
        "taxi_osszes_varos": "All cities",
        "taxi_kereses": "Search by name or phone number:",
        "taxi_kereses_placeholder": "E.g. Capitaly, Tóth József, 0740...",
        "taxi_nincs_talalat": "No matching taxi contacts found.",
        "varos_kovaszna": "Covasna",
        "varos_kezdi": "Târgu Secuiesc",
        "varos_szentgyorgy": "Sfântu Gheorghe",
    }
}

tavolsagi_helyszinek = {
    "Magyar": {"Kovászna": "Kovászna", "Kézdivásárhely": "Kézdi", "Sepsiszentgyörgy": "Szentgyörgy"},
    "Română": {"Covasna": "Kovászna", "Târgu Secuiesc": "Kézdi", "Sfântu Gheorghe": "Szentgyörgy"},
    "English": {"Covasna": "Kovászna", "Târgu Secuiesc": "Kézdi", "Sfântu Gheorghe": "Szentgyörgy"}
}

helyi_helyszinek = ["Centru", "Voinesti", "Gara"]

taxi_adatok = [
    {"varos_kulcs": "varos_kovaszna", "nev": "Tóth József", "telefonok": ["0740074870"]},
    {"varos_kulcs": "varos_kovaszna", "nev": "Beder Csaba", "telefonok": ["0745298037"]},
    {"varos_kulcs": "varos_kovaszna", "nev": "Blöki", "telefonok": ["0760320594"]},
    {"varos_kulcs": "varos_kovaszna", "nev": "Raduly József", "telefonok": ["0744168021"]},
    {"varos_kulcs": "varos_kezdi", "nev": "Bomba", "telefonok": ["0766949229"]},
    {"varos_kulcs": "varos_kezdi", "nev": "West", "telefonok": ["0741203080"]},
    {"varos_kulcs": "varos_szentgyorgy", "nev": "Capitaly", "telefonok": ["0744839707", "0720450303", "0766103000", "0267306100"]},
    {"varos_kulcs": "varos_szentgyorgy", "nev": "Herr taxi", "telefonok": ["0740 439 999"]},
    {"varos_kulcs": "varos_szentgyorgy", "nev": "Day taxi", "telefonok": ["0740 848 034"]},
]

# Hétvégén és ünnepnapokon közlekedő Codreanu járatok (normalizált HH:MM formátumban)
CODREANU_HETVEGI_IDOPONTOK = {
    ("Kovászna", "Szentgyörgy"): {"06:00", "10:00", "17:00"},
    ("Szentgyörgy", "Kovászna"): {"08:45", "12:45", "18:00"},
}

def normalizal_ido(ido_str: str) -> str:
    try:
        reszek = ido_str.strip().split(":")
        return f"{int(reszek[0]):02d}:{int(reszek[1]):02d}"
    except Exception:
        return ido_str.strip()

def nem_kozlekedik_hetvegen_es_unnepnapokon(honnan: str, hova: str, jaratszam: str, indulas: str) -> bool:
    if jaratszam.strip().lower() != "codreanu":
        return False
    engedelyezett = CODREANU_HETVEGI_IDOPONTOK.get((honnan, hova))
    if engedelyezett is None:
        return False
    return normalizal_ido(indulas) not in engedelyezett

# --- OLDALSÁV (SIDEBAR) ---
if os.path.exists("Logo.jpeg"):
    st.sidebar.image("Logo.jpeg", use_container_width=True)

st.sidebar.markdown("### 🌐 Nyelv / Limba / Language")
valasztott_nyelv = st.sidebar.selectbox("Nyelv", ["Magyar", "Română", "English"], label_visibility="collapsed")
t = szotar[valasztott_nyelv]

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['menu_cim']}")

menu_opciok = {
    "tavolsagi": t["ful_tavolsagi"],
    "helyi": t["ful_helyi"],
    "szentgyorgy": t["ful_szentgyorgy"],
    "taxi": t["ful_taxi"],
}

valasztott_oldal = st.sidebar.radio(
    "Menü",
    options=list(menu_opciok.keys()),
    format_func=lambda k: menu_opciok[k],
    label_visibility="collapsed"
)

aktualis_tavolsagi_varosok = tavolsagi_helyszinek[valasztott_nyelv]
megjelenitendo_tavolsagi = list(aktualis_tavolsagi_varosok.keys())

@dataclass
class Jarat:
    tipus: str
    honnan: str
    hova: str
    jaratszam: str
    indulas: str
    megjegyzes: str = ""

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class UtazasiRendszer:
    FAJL_NEV = "jaratok.json"

    def __init__(self):
        self.jaratok: List[Jarat] = []
        self.adatok_betoltese()
        self.helyi_jaratok_hozzaadasa()

    def adatok_betoltese(self):
        try:
            with open(self.FAJL_NEV, "r", encoding="utf-8") as f:
                adatok = json.load(f)
                self.jaratok = [Jarat.from_dict(d) for d in adatok if d.get("tipus") in ["Busz", "Vonat"]]
        except FileNotFoundError:
            self.jaratok = []

    def helyi_jaratok_hozzaadasa(self):
        helyi_adatok = [
            ("Centru", "Voinesti", [
                ("6:00", ""), ("6:50", ""), ("7:20", ""), ("7:50", ""), ("9:00", ""),
                ("10:10", ""), ("10:40", ""), ("11:15", ""), ("11:35", ""), ("12:30", "Csak hétköznap"),
                ("13:25", ""), ("14:00", ""), ("14:45", "Csak hétköznap"), ("15:30", ""),
                ("16:10", ""), ("17:30", ""), ("18:40", ""), ("20:40", "")
            ]),
            ("Centru", "Gara", [
                ("6:30", ""), ("8:30", ""), ("11:55", ""), ("15:10", ""),
                ("17:15", ""), ("18:20", ""), ("20:10", "")
            ]),
            ("Voinesti", "Centru", [
                ("6:15", ""), ("7:35", ""), ("8:10", ""), ("9:15", ""), ("10:20", ""),
                ("10:55", ""), ("11:25", ""), ("11:45", ""), ("12:40", "Csak hétköznap"),
                ("13:40", ""), ("14:20", ""), ("15:00", "Csak hétköznap"), ("15:45", ""),
                ("16:20", ""), ("17:45", ""), ("18:50", ""), ("20:50", "")
            ]),
            ("Gara", "Centru", [
                ("6:45", ""), ("8:50", ""), ("12:10", ""), ("15:25", ""),
                ("16:00", "Csak hétköznap"), ("17:25", ""), ("18:35", ""), ("20:25", "")
            ])
        ]

        for honnan, hova, lista in helyi_adatok:
            for idx, (ido, megj) in enumerate(lista, 1):
                self.jaratok.append(Jarat(
                    tipus="Helyi Busz",
                    honnan=honnan,
                    hova=hova,
                    jaratszam=f"Helyi-{idx:02d}",
                    indulas=ido,
                    megjegyzes=megj
                ))

JSON_URL = "https://raw.githubusercontent.com/picasso2010/CVTravel/main/multitrans_tiszta.json"
JSON_FILENAME = "multitrans_tiszta.json"
APK_URL = "https://raw.githubusercontent.com/picasso2010/CVTravel/main/cvtravel.apk"
APK_FILENAME = "cvtravel.apk"

def json_ellenorzes_es_letoltes():
    if not os.path.exists(JSON_FILENAME):
        try:
            urllib.request.urlretrieve(JSON_URL, JSON_FILENAME)
        except Exception:
            pass

json_ellenorzes_es_letoltes()

def adatok_betoltese_multitrans():
    try:
        with open(JSON_FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

st.title(t["cim"])
st.caption(t["alcim"])
st.markdown("---")

rendszer = UtazasiRendszer()

def ido_perc(ido_str):
    reszek = ido_str.split(":")
    return int(reszek[0]) * 60 + int(reszek[1])

# --- 1. NÉZET: HELYI JÁRATOK (Kovászna) ---
if valasztott_oldal == "helyi":
    st.subheader(t["ful_helyi"])
    col1, col2 = st.columns(2)
    with col1:
        helyi_honnan = st.selectbox(t["honnan"], helyi_helyszinek, key="helyi_honnan")
    with col2:
        helyi_hova = st.selectbox(t["hova"], helyi_helyszinek, key="helyi_hova", index=1)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t["gomb"], key="gomb_helyi"):
        st.markdown("---")
        if helyi_honnan == helyi_hova:
            st.warning(t["hiba_ugyanaz"])
        else:
            talalatok = [j for j in rendszer.jaratok if j.tipus == "Helyi Busz" and j.honnan == helyi_honnan and j.hova == helyi_hova]
            st.markdown(f"### {t['talalat']}: `{helyi_honnan}` ➔ `{helyi_hova}`")

            if talalatok:
                st.markdown(f"#### {t['kozvetlen']}")
                df_data = []
                for b in talalatok:
                    df_data.append({
                        t["vonal"] if "vonal" in t else "Járat": b.jaratszam,
                        t["indulas_szoveg"]: b.indulas,
                        t["megjegyzes"]: b.megjegyzes if b.megjegyzes else "-"
                    })
                st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)
            else:
                atszallasok = []
                elso_lab = [j for j in rendszer.jaratok if j.tipus == "Helyi Busz" and j.honnan == helyi_honnan]
                for j1 in elso_lab:
                    kozos_megallo = j1.hova
                    if kozos_megallo != helyi_hova:
                        masodik_lab = [j for j in rendszer.jaratok if j.tipus == "Helyi Busz" and j.honnan == kozos_megallo and j.hova == helyi_hova]
                        for j2 in masodik_lab:
                            if ido_perc(j2.indulas) >= ido_perc(j1.indulas) + 5:
                                atszallasok.append({
                                    "1. Indulás": j1.indulas,
                                    "1. Járat": j1.jaratszam,
                                    "Átszállás": kozos_megallo,
                                    "2. Indulás": j2.indulas,
                                    "2. Járat": j2.jaratszam,
                                    t["megjegyzes"]: f"{j1.megjegyzes} / {j2.megjegyzes}".strip(" /")
                                })

                if atszallasok:
                    st.info(t["nincs_jarat"])
                    st.markdown(f"#### {t['atszallas']}")
                    st.dataframe(pd.DataFrame(atszallasok), use_container_width=True, hide_index=True)
                else:
                    st.info(t["nincs_semmi"])

# --- 2. NÉZET: TÁVOLSÁGI / INTERURBÁN JÁRATOK ---
elif valasztott_oldal == "tavolsagi":
    st.subheader(t["ful_tavolsagi"])
    col3, col4 = st.columns(2)
    with col3:
        valasztott_honnan_nev = st.selectbox(t["honnan"], megjelenitendo_tavolsagi, key="tav_honnan")
    with col4:
        valasztott_hova_nev = st.selectbox(t["hova"], megjelenitendo_tavolsagi, key="tav_hova", index=1 if len(megjelenitendo_tavolsagi) > 1 else 0)

    tav_honnan = aktualis_tavolsagi_varosok[valasztott_honnan_nev]
    tav_hova = aktualis_tavolsagi_varosok[valasztott_hova_nev]

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t["gomb"], key="gomb_tav"):
        st.markdown("---")
        if tav_honnan == tav_hova:
            st.warning(t["hiba_ugyanaz"])
        else:
            talalatok = [j for j in rendszer.jaratok if j.tipus in ["Busz", "Vonat"] and j.honnan == tav_honnan and j.hova == tav_hova]
            st.markdown(f"### {t['talalat']}: `{valasztott_honnan_nev}` ➔ `{valasztott_hova_nev}`")

            buszok = [j for j in talalatok if j.tipus == "Busz"]
            vonatok = [j for j in talalatok if j.tipus == "Vonat"]

            if buszok or vonatok:
                if buszok:
                    st.markdown(f"#### {t['buszok']}")
                    van_narancs_busz = False
                    sorok_b = []
                    narancs_indexek = []

                    for idx, b in enumerate(buszok):
                        nincs_hetvegen = nem_kozlekedik_hetvegen_es_unnepnapokon(
                            b.honnan, b.hova, b.jaratszam, b.indulas
                        )
                        if nincs_hetvegen:
                            van_narancs_busz = True
                            narancs_indexek.append(idx)

                        sorok_b.append({
                            "Járat": b.jaratszam,
                            t["indulas_szoveg"]: normalizal_ido(b.indulas),
                            t["megjegyzes"]: t["nincs_hetvegen"] if nincs_hetvegen else (b.megjegyzes if b.megjegyzes else "-")
                        })

                    df_b = pd.DataFrame(sorok_b)

                    def szinez_narancs(row):
                        if row.name in narancs_indexek:
                            return [
                                "background-color: rgba(249, 115, 22, 0.28); color: #fed7aa; font-weight: 600;"
                            ] * len(row)
                        return [""] * len(row)

                    styled_df_b = df_b.style.apply(szinez_narancs, axis=1)
                    st.dataframe(styled_df_b, use_container_width=True, hide_index=True)

                    if van_narancs_busz:
                        st.markdown(
                            f'<div class="orange-legend">{t["hetvegi_magyarazat"]}</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.write(t["nincs_busz"])

                if vonatok:
                    st.markdown(f"#### {t['vonatok']}")
                    df_v = pd.DataFrame([{"Járat": v.jaratszam, t["indulas_szoveg"]: v.indulas} for v in vonatok])
                    st.dataframe(df_v, use_container_width=True, hide_index=True)
                else:
                    st.write(t["nincs_vonat"])
            else:
                st.info(t["nincs_semmi"])

# --- 3. NÉZET: SEPSISZENTGYÖRGY MULTITRANS ---
elif valasztott_oldal == "szentgyorgy":
    st.subheader(t["szentgyorgy_cim"])
    st.caption(t["szentgyorgy_alcim"])

    st.markdown(f"""
    <div class="apk-box">
        <div class="apk-title">{t['apk_cim']}</div>
        <p class="apk-desc">{t['apk_leiras']}</p>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists(APK_FILENAME):
        with open(APK_FILENAME, "rb") as apk_file:
            st.download_button(
                label=t["apk_gomb"],
                data=apk_file,
                file_name=APK_FILENAME,
                mime="application/vnd.android.package-archive",
                key="btn_download_apk_local",
                use_container_width=True
            )
    else:
        st.link_button(t["apk_gomb"], APK_URL, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    multitrans_adatok = adatok_betoltese_multitrans()

    all_stations = sorted(list(set(s["hu"] for s in multitrans_adatok if "hu" in s)))
    all_destinations = sorted(list(set(line["dest"] for s in multitrans_adatok for line in s.get("lines", []))))

    col5, col6 = st.columns(2)

    with col5:
        st.markdown(f"**{t['honnan']}**")
        szuro_from = st.text_input(t["szuro_honnan"], key="szuro_from_input", placeholder="Pl. Központ...")
        szurt_allomasok = [stn for stn in all_stations if szuro_from.strip().lower() in stn.lower()] if szuro_from.strip() else all_stations

        szentgyorgy_honnan = st.selectbox("Válaszd ki a megállót", szurt_allomasok if szurt_allomasok else all_stations, key="select_honnan_st", label_visibility="collapsed")

    with col6:
        st.markdown(f"**{t['hova']}**")
        szuro_to = st.text_input(t["szuro_hova"], key="szuro_to_input", placeholder="Pl. Állomás...")
        szurt_celok = [dst for dst in all_destinations if szuro_to.strip().lower() in dst.lower()] if szuro_to.strip() else all_destinations

        szentgyorgy_hova = st.selectbox("Válaszd ki a célállomást", szurt_celok if szurt_celok else all_destinations, key="select_hova_st", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t["gomb"], key="gomb_szentgyorgy"):
        st.markdown("---")
        if szentgyorgy_honnan == szentgyorgy_hova:
            st.warning(t["hiba_ugyanaz"])
        else:
            now = datetime.now()
            current_time_str = now.strftime("%H:%M")
            is_weekend = now.weekday() >= 5

            talalatok = []
            for station in multitrans_adatok:
                stn_name = station.get("hu", "")
                if stn_name.lower() == szentgyorgy_honnan.lower():
                    for line in station.get("lines", []):
                        dest_name = line.get("dest", "")
                        if szentgyorgy_hova.lower() in dest_name.lower():
                            vonal_szam = str(line.get("num", ""))

                            for orare in line.get("orare", []):
                                title = orare.get("title", "").lower()
                                if is_weekend and ("szombat" not in title and "sâmbătă" not in title):
                                    continue
                                if not is_weekend and ("munkanapok" not in title and "zile lucrătoare" not in title):
                                    continue

                                for row in orare.get("rows", []):
                                    ora = row.get("h")
                                    percek = row.get("m", []) if hasattr(row, 'get') else []
                                    for perc in percek:
                                        jarat_idopont = f"{str(ora).zfill(2)}:{str(perc).zfill(2)}"
                                        if jarat_idopont > current_time_str:
                                            talalatok.append({
                                                "vonal": vonal_szam,
                                                "cel": dest_name,
                                                "indulas": jarat_idopont
                                            })

            talalatok = sorted(talalatok, key=lambda x: x["indulas"])

            st.markdown(f"### {t['talalat']}: `{szentgyorgy_honnan}` ➔ `{szentgyorgy_hova}`")

            if talalatok:
                st.markdown(f"**{t['talalatok_szama']}:** {len(talalatok)}")
                df_multi = pd.DataFrame([
                    {
                        t['indulas_szoveg']: j['indulas'],
                        t['vonal']: j['vonal'],
                        t['celallomas']: j['cel']
                    } for j in talalatok
                ])
                st.dataframe(df_multi, use_container_width=True, hide_index=True)
            else:
                st.info(t["nincs_ma_jarat"])

                atszallasok = []
                for s1 in multitrans_adatok:
                    s1_name = s1.get("hu", "")
                    if s1_name.lower() == szentgyorgy_honnan.lower():
                        for l1 in s1.get("lines", []):
                            koztes = l1.get("dest", "")
                            if koztes.lower() != szentgyorgy_hova.lower():
                                for s2 in multitrans_adatok:
                                    if s2.get("hu", "").lower() == koztes.lower():
                                        for l2 in s2.get("lines", []):
                                            if szentgyorgy_hova.lower() in l2.get("dest", "").lower():
                                                for o1 in l1.get("orare", []):
                                                    for r1 in o1.get("rows", []):
                                                        for p1 in r1.get("m", []):
                                                            t1 = f"{str(r1.get('h')).zfill(2)}:{str(p1).zfill(2)}"
                                                            if t1 > current_time_str:
                                                                for o2 in l2.get("orare", []):
                                                                    for r2 in o2.get("rows", []):
                                                                        for p2 in r2.get("m", []):
                                                                            t2 = f"{str(r2.get('h')).zfill(2)}:{str(p2).zfill(2)}"
                                                                            if ido_perc(t2) >= ido_perc(t1) + 5:
                                                                                atszallasok.append({
                                                                                    "1. Indulás": t1,
                                                                                    "Vonal 1": l1.get("num"),
                                                                                    "Átszállási hely": koztes,
                                                                                    "2. Indulás": t2,
                                                                                    "Vonal 2": l2.get("num"),
                                                                                    "Célállomás": l2.get("dest")
                                                                                })

                if atszallasok:
                    atszallasok = sorted(atszallasok, key=lambda x: x["1. Indulás"])
                    unique_atszallasok = [dict(item) for item in {tuple(d.items()) for d in atszallasok}]

                    st.markdown(f"#### {t['atszallas']}")
                    st.dataframe(pd.DataFrame(unique_atszallasok), use_container_width=True, hide_index=True)
                else:
                    st.warning("Nem található átszállásos útvonal sem.")

# --- 4. NÉZET: TAXI ELÉRHETŐSÉGEK ---
elif valasztott_oldal == "taxi":
    st.subheader(t["taxi_cim"])
    st.caption(t["taxi_alcim"])

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        varos_opciok = {
            "all": t["taxi_osszes_varos"],
            "varos_kovaszna": t["varos_kovaszna"],
            "varos_kezdi": t["varos_kezdi"],
            "varos_szentgyorgy": t["varos_szentgyorgy"],
        }
        valasztott_varos = st.selectbox(
            t["taxi_varos_szuro"],
            options=list(varos_opciok.keys()),
            format_func=lambda k: varos_opciok[k],
            key="taxi_varos_select"
        )

    with col_t2:
        taxi_keresoszo = st.text_input(
            t["taxi_kereses"],
            placeholder=t["taxi_kereses_placeholder"],
            key="taxi_search_input"
        ).strip().lower()

    st.markdown("<br>", unsafe_allow_html=True)

    szurt_taxik = []
    for item in taxi_adatok:
        if valasztott_varos != "all" and item["varos_kulcs"] != valasztott_varos:
            continue
        if taxi_keresoszo:
            nev_egyezes = taxi_keresoszo in item["nev"].lower()
            tel_egyezes = any(taxi_keresoszo.replace(" ", "") in tel.replace(" ", "") for tel in item["telefonok"])
            if not (nev_egyezes or tel_egyezes):
                continue
        szurt_taxik.append(item)

    if not szurt_taxik:
        st.info(t["taxi_nincs_talalat"])
    else:
        for item in szurt_taxik:
            varos_nev = t[item["varos_kulcs"]]
            gombok_html = "".join(
                f'<a class="taxi-phone-btn" href="tel:{tel.replace(" ", "")}">📞 {tel}</a>'
                for tel in item["telefonok"]
            )
            st.markdown(f"""
            <div class="taxi-card">
                <div class="taxi-header">
                    <span class="taxi-name">{item['nev']}</span>
                    <span class="taxi-badge">{varos_nev}</span>
                </div>
                <div class="taxi-phones">{gombok_html}</div>
            </div>
            """, unsafe_allow_html=True)

# --- OLDALSÁV LÁBLÉC ---
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['urlap_cim']}")
st.sidebar.write(t["urlap_szoveg"])
st.sidebar.link_button(t["urlap_gomb"], "https://forms.gle/kCtmR8P4gRP7acGG7")