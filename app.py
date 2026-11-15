import json
import os
import urllib.request
from datetime import datetime
from dataclasses import dataclass
from typing import List
import streamlit as st

st.set_page_config(
    page_title="Utazás",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

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

    .dark-card {
        border: 1px solid #283649;
        background-color: #181f29;
        padding: 18px;
        margin-bottom: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .dark-card-header {
        font-weight: 600;
        color: #38bdf8;
        border-bottom: 1px solid #283649;
        padding-bottom: 8px;
        margin-bottom: 10px;
        font-size: 1.05rem;
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

    div[data-baseweb="select"] > div {
        background-color: #181f29 !important;
        border: 1px solid #2d3b4e !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)

szotar = {
    "Magyar": {
        "cim": "Utazás",
        "alcim": "Kovászna — Kézdi — Szentgyörgy",
        "ful_helyi": "🚌 Kovásznai helyi járatok",
        "ful_tavolsagi": "🚆 Interurbán járatok (Kézdi / Szentgyörgy)",
        "ful_szentgyorgy": "🚌 Szentgyörgy (Multitrans)",
        "kereses_fejlec": "🔍 Útvonal keresése",
        "honnan": "Honnan indulnál?",
        "hova": "Hova utaznál?",
        "gomb": "Járatok keresése",
        "hiba_ugyanaz": "Az indulási és az érkezési helyszín nem lehet azonos!",
        "talalat": "Találatok",
        "nincs_jarat": "Nem találtunk járatot ezen az útvonalon.",
        "buszok": "🚌 Buszjáratok",
        "vonatok": "🚆 Vonatjáratok",
        "nincs_busz": "Nincs elérhető busz.",
        "nincs_vonat": "Nincs elérhető vonat.",
        "indulas_szoveg": "Indulás",
        "megjegyzes": "Megjegyzés",
        "urlap_cim": "✈️ Új járat javaslása",
        "urlap_szoveg": "Hiányzó járatot találtál? Küldd el nekünk!",
        "urlap_gomb": "Beküldési űrlap",
        "szentgyorgy_cim": "Sepsiszentgyörgy Helyi Menetrend",
        "szentgyorgy_alcim": "Multitrans okos kereső",
        "frissites_gomb": "🔄 Adatok frissítése GitHubról",
        "frissites_sikeres": "A menetrend sikeresen frissítve!",
        "frissites_hiba": "Hiba történt a frissítés során.",
        "vonal": "Vonal",
        "celallomas": "Célállomás",
        "nincs_ma_jarat": "A megadott útvonalra mára már nincs közvetlen járat.",
        "talalatok_szama": "Találatok száma",
        "szuro_honnan": "Szűrés / Keresés megállóra:",
        "szuro_hova": "Szűrés / Keresés célállomásra:",
    },
    "Română": {
        "cim": "Utazás",
        "alcim": "Covasna — Târgu Secuiesc — Sfântu Gheorghe",
        "ful_helyi": "🚌 Curse locale Covasna",
        "ful_tavolsagi": "🚆 Curse interurbane (Târgu Secuiesc / Sf. Gheorghe)",
        "ful_szentgyorgy": "🚌 Sf. Gheorghe (Multitrans)",
        "kereses_fejlec": "🔍 Căutare rute",
        "honnan": "Locație plecare:",
        "hova": "Locație destinație:",
        "gomb": "Caută curse",
        "hiba_ugyanaz": "Locația de plecare și cea de destinație nu pot fi identice!",
        "talalat": "Rezultate",
        "nincs_jarat": "Nu am găsit curse pe această rută.",
        "buszok": "🚌 Curse de autobuz",
        "vonatok": "🚆 Curse de tren",
        "nincs_busz": "Nu există autobuze.",
        "nincs_vonat": "Nu există trenuri.",
        "indulas_szoveg": "Plecare",
        "megjegyzes": "Mențiune",
        "urlap_cim": "✈️ Propune o cursă",
        "urlap_szoveg": "Ai găsit o cursă lipsă? Trimite-o!",
        "urlap_gomb": "Formular trimitere",
        "szentgyorgy_cim": "Orar Local Sfântu Gheorghe",
        "szentgyorgy_alcim": "Orar Multitrans căutare inteligentă",
        "frissites_gomb": "🔄 Actualizare date de pe GitHub",
        "frissites_sikeres": "Orarul a fost actualizat cu succes!",
        "frissites_hiba": "Eroare la actualizare.",
        "vonal": "Linie",
        "celallomas": "Destinație",
        "nincs_ma_jarat": "Nu mai există curse directe pe această rută astăzi.",
        "talalatok_szama": "Număr de rezultate",
        "szuro_honnan": "Filtrare stație plecare:",
        "szuro_hova": "Filtrare destinație:",
    },
    "English": {
        "cim": "Utazás",
        "alcim": "Covasna — Târgu Secuiesc — Sfântu Gheorghe",
        "ful_helyi": "🚌 Covasna Local Buses",
        "ful_tavolsagi": "🚆 Intercity Rides (Târgu Secuiesc / Sf. Gheorghe)",
        "ful_szentgyorgy": "🚌 Sf. Gheorghe Local (Multitrans)",
        "kereses_fejlec": "🔍 Search Routes",
        "honnan": "Departure location:",
        "hova": "Destination location:",
        "gomb": "Search Rides",
        "hiba_ugyanaz": "Departure and destination locations cannot be the same!",
        "talalat": "Results",
        "nincs_jarat": "No available rides on this route.",
        "buszok": "🚌 Bus Services",
        "vonatok": "🚆 Train Services",
        "nincs_busz": "No buses available.",
        "nincs_vonat": "No trains available.",
        "indulas_szoveg": "Departure",
        "megjegyzes": "Note",
        "urlap_cim": "✈️ Propose a ride",
        "urlap_szoveg": "Found a missing ride? Send it to us!",
        "urlap_gomb": "Submit Form",
        "szentgyorgy_cim": "Sfântu Gheorghe Local Schedule",
        "szentgyorgy_alcim": "Multitrans smart search",
        "frissites_gomb": "🔄 Update Data from GitHub",
        "frissites_sikeres": "Schedule successfully updated!",
        "frissites_hiba": "Error updating data.",
        "vonal": "Line",
        "celallomas": "Destination",
        "nincs_ma_jarat": "No more direct rides on this route today.",
        "talalatok_szama": "Number of results",
        "szuro_honnan": "Filter departure station:",
        "szuro_hova": "Filter destination:",
    }
}

# --- LOGÓ BEILLESZTÉSE AZ OLDALSÁVBA ---
if os.path.exists("Logo.jpeg"):
    st.sidebar.image("Logo.jpeg", use_container_width=True)

st.sidebar.markdown("### 🌐 Nyelv / Limba / Language")
valasztott_nyelv = st.sidebar.selectbox("Nyelv", ["Magyar", "Română", "English"], label_visibility="collapsed")
t = szotar[valasztott_nyelv]  
aktualis_tavolsagi_varosok = tavolsagi_helyszinek[valasztott_nyelv]
megjelenitendo_tavolsagi = list(aktualis_tavolsagi_varosok.keys())

# Helyi járatok megállói (Kovászna)
helyi_helyszinek = ["Centru", "Voinesti", "Gara"]

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

# Multitrans JSON kezelés
JSON_URL = "https://raw.githubusercontent.com/picasso2010/CVTravel/main/multitrans_tiszta.json"
JSON_FILENAME = "multitrans_tiszta.json"

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

# Három fül létrehozása
ful_2, ful_1, ful_3 = st.tabs([t["ful_tavolsagi"], t["ful_helyi"], t["ful_szentgyorgy"]])

# --- 1. FÜL: HELYI JÁRATOK (Kovászna) ---
with ful_1:
    st.subheader(t["kereses_fejlec"])
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
            
            if not talalatok:
                st.info(t["nincs_jarat"])
            else:
                st.markdown(f"#### 🚌 {t['buszok']}")
                for b in talalatok:
                    megj_html = f"<br><small style='color: #38bdf8;'><b>{t['megjegyzes']}:</b> {b.megjegyzes}</small>" if b.megjegyzes else ""
                    st.markdown(f"""
                    <div class="dark-card">
                        <div class="dark-card-header">🚌 Járat: {b.jaratszam}</div>
                        <div><b>{t['indulas_szoveg']}:</b> <code>{b.indulas}</code>{megj_html}</div>
                    </div>
                    """, unsafe_allow_html=True)

# --- 2. FÜL: TÁVOLSÁGI / INTERURBÁN JÁRATOK ---
with ful_2:
    st.subheader(t["kereses_fejlec"])
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
                            <div class="dark-card">
                                <div class="dark-card-header">🚌 Járat: {b.jaratszam}</div>
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
                            <div class="dark-card">
                                <div class="dark-card-header">🚆 Járat: {v.jaratszam}</div>
                                <div><b>{t['indulas_szoveg']}:</b> <code>{v.indulas}</code></div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.write(t["nincs_vonat"])

# --- 3. FÜL: SEPSISZENTGYÖRGY MULTITRANS (Okos, mobilosbarát legördülős kereső) ---
with ful_3:
    st.subheader(t["szentgyorgy_cim"])
    st.caption(t["szentgyorgy_alcim"])
    
    if st.button(t["frissites_gomb"], key="btn_frissites_szentgyorgy"):
        try:
            cache_buster_url = f"{JSON_URL}?t={os.urandom(4).hex()}"
            urllib.request.urlretrieve(cache_buster_url, JSON_FILENAME)
            st.success(t["frissites_sikeres"])
        except Exception:
            st.error(t["frissites_hiba"])

    multitrans_adatok = adatok_betoltese_multitrans()
    
    all_stations = sorted(list(set(s["hu"] for s in multitrans_adatok if "hu" in s)))
    all_destinations = sorted(list(set(line["dest"] for s in multitrans_adatok for line in s.get("lines", []))))

    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown(f"**{t['honnan']}**")
        szuro_from = st.text_input(t["szuro_honnan"], key="szuro_from_input", placeholder="Pl. Központ...")
        szurt_allomasok = [stn for stn in all_stations if szuro_from.strip().lower() in stn.lower()] if szuro_from.strip() else all_stations
        
        szentgyorgy_honnan = st.selectbox("Valaszd ki a megallot", szurt_allomasok if szurt_allomasok else all_stations, key="select_honnan_st", label_visibility="collapsed")

    with col6:
        st.markdown(f"**{t['hova']}**")
        szuro_to = st.text_input(t["szuro_hova"], key="szuro_to_input", placeholder="Pl. Állomás...")
        szurt_celok = [dst for dst in all_destinations if szuro_to.strip().lower() in dst.lower()] if szuro_to.strip() else all_destinations
        
        szentgyorgy_hova = st.selectbox("Valaszd ki a celallomast", szurt_celok if szurt_celok else all_destinations, key="select_hova_st", label_visibility="collapsed")

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
                                        jarat_idopont = f"{ora}:{perc}"
                                        if jarat_idopont > current_time_str:
                                            talalatok.append({
                                                "vonal": vonal_szam,
                                                "cel": dest_name,
                                                "indulas": jarat_idopont
                                            })

            st.markdown(f"### {t['talalat']}: `{szentgyorgy_honnan}` ➔ `{szentgyorgy_hova}`")
            
            if not talalatok:
                st.info(t["nincs_ma_jarat"])
            else:
                st.markdown(f"**{t['talalatok_szama']}:** {len(talalatok)}")
                for j in talalatok:
                    st.markdown(f"""
                    <div class="dark-card">
                        <div class="dark-card-header">🚌 {t['vonal']}: {j['vonal']} | {t['celallomas']}: {j['cel']}</div>
                        <div><b>{t['indulas_szoveg']}:</b> <code>{j['indulas']}</code></div>
                    </div>
                    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['urlap_cim']}")
st.sidebar.write(t["urlap_szoveg"])
st.sidebar.link_button(t["urlap_gomb"], "https://forms.gle/kCtmR8P4gRP7acGG7")