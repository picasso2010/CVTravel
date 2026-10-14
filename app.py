import json
from dataclasses import dataclass
from typing import List
import streamlit as st

# Nyelvi szótárak
szotar = {
    "Magyar": {
        "cim": "🚆 Kovászna - Kézdi - Szentgyörgy Utazási Rendszer",
        "kereses_fejlec": "🔍 Járatok keresése",
        "honnan": "Indulási város:",
        "hova": "Célváros:",
        "gomb": "Keresés",
        "hiba_ugyanaz": "Az indulási és érkezési város nem lehet ugyanaz!",
        "talalat": "Találatok",
        "nincs_jarat": "Nincs elérhető járat ezen az útvonalon.",
        "buszok": "🚌 Buszjáratok",
        "vonatok": "🚆 Vonatjáratok",
        "nincs_busz": "Nincs buszjárat.",
        "nincs_vonat": "Nincs vonatjárat.",
        "urlap_cim": "✈️ Új járatot javasolnál?",
        "urlap_szoveg": "Ha hiányzó járatot találtál, küldd el nekünk!",
        "urlap_gomb": "Járat beküldése (Űrlap)",
    },
    "Română": {
        "cim": "🚆 Sistem de Transport Covasna - Târgu Secuiesc - Sfântu Gheorghe",
        "kereses_fejlec": "🔍 Căutare curse",
        "honnan": "Oraș plecare:",
        "hova": "Oraș destinație:",
        "gomb": "Caută",
        "hiba_ugyanaz": "Orașul de plecare și cel de destinație nu pot fi aceleași!",
        "talalat": "Rezultate",
        "nincs_jarat": "Nu există curse disponibile pe această rută.",
        "buszok": "🚌 Curse de autobuz",
        "vonatok": "🚆 Curse de tren",
        "nincs_busz": "Nu există autobuze.",
        "nincs_vonat": "Nu există trenuri.",
        "urlap_cim": "✈️ Dorești să propuni o cursă?",
        "urlap_szoveg": "Dacă ai găsit o cursă lipsă, trimite-ne-o!",
        "urlap_gomb": "Trimite cursa (Formular)",
    },
    "English": {
        "cim": "🚆 Covasna - Târgu Secuiesc - Sfântu Gheorghe Travel System",
        "kereses_fejlec": "🔍 Search Rides",
        "honnan": "Departure city:",
        "hova": "Destination city:",
        "gomb": "Search",
        "hiba_ugyanaz": "Departure and destination cities cannot be the same!",
        "talalat": "Results",
        "nincs_jarat": "No available rides on this route.",
        "buszok": "🚌 Bus Rides",
        "vonatok": "🚆 Train Rides",
        "nincs_busz": "No buses available.",
        "nincs_vonat": "No trains available.",
        "urlap_cim": "✈️ Propose a new ride?",
        "urlap_szoveg": "If you found a missing ride, send it to us!",
        "urlap_gomb": "Submit Ride (Form)",
    }
}

# Városnevek nyelvenként (Megjelenítendő név -> JSON-ban lévő belső kulcs)
varos_nevek = {
    "Magyar": {
        "Kovászna": "Kovászna",
        "Kézdi": "Kézdi",
        "Szentgyörgy": "Szentgyörgy"
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

# Nyelvválasztó a sáv tetején
valasztott_nyelv = st.sidebar.selectbox("🌐 Nyelv / Limba / Language", ["Magyar", "Română", "English"])
t = szotar[valasztott_nyelv]  # Aktuális szövegek
aktualis_varosok = varos_nevek[valasztott_nyelv]  # Aktuális városnevek szótára
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

st.title(t["cim"])

rendszer = UtazasiRendszer()

st.header(t["kereses_fejlec"])

# Kiválasztás a felületen (a felhasználó a választott nyelv szerinti nevet látja)
valasztott_honnan_nev = st.selectbox(t["honnan"], megjelenitendo_varosok, key="keres_honnan")
valasztott_hova_nev = st.selectbox(t["hova"], megjelenitendo_varosok, key="keres_hova")

# Visszaalakítjuk a belső kulcsra a szűréshez
honnan = aktualis_varosok[valasztott_honnan_nev]
hova = aktualis_varosok[valasztott_hova_nev]

if st.button(t["gomb"]):
    if honnan == hova:
        st.warning(t["hiba_ugyanaz"])
    else:
        talalatok = [
            j for j in rendszer.jaratok if j.honnan == honnan and j.hova == hova
        ]
        
        st.subheader(f"{t['talalat']}: {valasztott_honnan_nev} ➔ {valasztott_hova_nev}")
        
        if not talalatok:
            st.info(t["nincs_jarat"])
        else:
            buszok = [j for j in talalatok if j.tipus == "Busz"]
            vonatok = [j for j in talalatok if j.tipus == "Vonat"]
            
            st.markdown(f"### {t['buszok']}")
            if buszok:
                for b in buszok:
                    st.write(f"- **[{b.jaratszam}]** Indulás / Plecare / Departure: `{b.indulas}`")
            else:
                st.write(t["nincs_busz"])
                
            st.markdown(f"### {t['vonatok']}")
            if vonatok:
                for v in vonatok:
                    st.write(f"- **[{v.jaratszam}]** Indulás / Plecare / Departure: `{v.indulas}`")
            else:
                st.write(t["nincs_vonat"])

# Oldalsáv az űrlapecskénkhez
st.sidebar.markdown("---")
st.sidebar.subheader(t["urlap_cim"])
st.sidebar.write(t["urlap_szoveg"])

urlap_link = "https://forms.gle/kCtmR8P4gRP7acGG7"
st.sidebar.link_button(t["urlap_gomb"], urlap_link)