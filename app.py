import json
from dataclasses import dataclass
from typing import List
import streamlit as st

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
        self.varosok = ["Kovászna", "Kézdi", "Szentgyörgy"]
        self.jaratok: List[Jarat] = []
        self.adatok_betoltese()

    def adatok_betoltese(self):
        try:
            with open(self.FAJL_NEV, "r", encoding="utf-8") as f:
                adatok = json.load(f)
                self.jaratok = [Jarat.from_dict(d) for d in adatok]
        except FileNotFoundError:
            self.jaratok = []

st.title("🚆 Kovászna - Kézdi - Szentgyörgy Utazási Rendszer")

rendszer = UtazasiRendszer()

st.header("🔍 Járatok keresése")

honnan = st.selectbox("Indulási város:", rendszer.varosok, key="keres_honnan")
hova = st.selectbox("Célváros:", rendszer.varosok, key="keres_hova")

if st.button("Keresés"):
    if honnan == hova:
        st.warning("Az indulási és érkezési város nem lehet ugyanaz!")
    else:
        talalatok = [
            j for j in rendszer.jaratok if j.honnan == honnan and j.hova == hova
        ]
        
        st.subheader(f"Találatok: {honnan} ➔ {hova}")
        
        if not talalatok:
            st.info("Nincs elérhető járat ezen az útvonalon.")
        else:
            buszok = [j for j in talalatok if j.tipus == "Busz"]
            vonatok = [j for j in talalatok if j.tipus == "Vonat"]
            
            st.markdown("### 🚌 Buszjáratok")
            if buszok:
                for b in buszok:
                    st.write(f"- **[{b.jaratszam}]** Indulás: `{b.indulas}`")
            else:
                st.write("Nincs buszjárat.")
                
            st.markdown("### 🚆 Vonatjáratok")
            if vonatok:
                for v in vonatok:
                    st.write(f"- **[{v.jaratszam}]** Indulás: `{v.indulas}`")
            else:
                st.write("Nincs vonatjárat.")