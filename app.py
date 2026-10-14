import json
from dataclasses import dataclass
from typing import List, Optional
import streamlit as st

@dataclass
class Jarat:
    tipus: str  # "Busz" vagy "Vonat"
    honnan: str
    hova: str
    jaratszam: str
    indulas: str  # pl. "14:30"

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class UtazasiRendszer:
    FAJL_NEV = "jaratok.json"

    def __init__(self):
        self.varosok = ["Kovászna", "Kézdi", "Szentgyörgy"]
        self.jaratok: List[Jarat] = []
        self.adatok_betoltese()

    def adatok_mentese(self):
        try:
            with open(self.FAJL_NEV, "w", encoding="utf-8") as f:
                json.dump(
                    [j.to_dict() for j in self.jaratok],
                    f,
                    ensure_ascii=False,
                    indent=4,
                )
        except Exception as e:
            st.error(f"Hiba a mentés során: {e}")

    def adatok_betoltese(self):
        try:
            with open(self.FAJL_NEV, "r", encoding="utf-8") as f:
                adatok = json.load(f)
                self.jaratok = [Jarat.from_dict(d) for d in adatok]
        except FileNotFoundError:
            self.jaratok = []

# Streamlit UI felépítése
st.title("🚆 Kovászna - Kézdi - Szentgyörgy Utazási Rendszer")

rendszer = UtazasiRendszer()

menu = st.sidebar.selectbox("Menü", ["Járatok keresése", "Új járat felvétele"])

if menu == "Járatok keresése":
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

elif menu == "Új járat felvétele":
    st.header("➕ Új járat felvétele")
    
    honnan = st.selectbox("Indulási város:", rendszer.varosok, key="uj_honnan")
    hova = st.selectbox("Célváros:", rendszer.varosok, key="uj_hova")
    tipus = st.selectbox("Típus:", ["Busz", "Vonat"])
    jaratszam = st.text_input("Járat azonosító/szám (pl. Regio #11261 vagy Codreanu):")
    indulas = st.text_input("Indulási idő (HH:MM formátum, pl. 08:45):")
    
    if st.button("Mentés"):
        if honnan == hova:
            st.error("Hiba: Az indulási és érkezési város nem lehet ugyanaz!")
        elif not jaratszam or not indulas:
            st.error("Hiba: Minden mezőt tölts ki!")
        else:
            uj_jarat = Jarat(tipus, honnan, hova, jaratszam, indulas)
            rendszer.jaratok.append(uj_jarat)
            rendszer.adatok_mentese()
            st.success("✅ Járat sikeresen elmentve!")