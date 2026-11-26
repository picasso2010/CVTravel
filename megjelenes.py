from pathlib import Path
import pandas as pd
import streamlit as st


def alkalmaz_stilus(fajl_nev: str = "style.css") -> None:
    css_utvonal = Path(__file__).parent / fajl_nev
    if css_utvonal.exists():
        css_tartalom = css_utvonal.read_text(encoding="utf-8")
        st.markdown(f"<style>\n{css_tartalom}\n</style>", unsafe_allow_html=True)


def megjelenit_frissitesi_datum(datum: str, cimke: str) -> None:
    if datum:
        st.markdown(
            f'<div class="updated-meta">{cimke}: {datum}</div>',
            unsafe_allow_html=True,
        )


def megjelenit_narancs_jelmagyarazat(szoveg: str) -> None:
    st.markdown(
        f'<div class="orange-legend">{szoveg}</div>',
        unsafe_allow_html=True,
    )


def megjelenit_apk_kartya(cim: str, leiras: str) -> None:
    st.markdown(
        f"""
        <div class="apk-box">
            <div class="apk-title">{cim}</div>
            <p class="apk-desc">{leiras}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def megjelenit_taxi_kartya(nev: str, varos: str, telefonok: list[str]) -> None:
    gombok_html = "".join(
        f'<a class="taxi-phone-btn" href="tel:{tel.replace(" ", "")}">📞 {tel}</a>'
        for tel in telefonok
    )
    st.markdown(
        f"""
        <div class="taxi-card">
            <div class="taxi-header">
                <span class="taxi-name">{nev}</span>
                <span class="taxi-badge">{varos}</span>
            </div>
            <div class="taxi-phones">{gombok_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def formaz_narancs_soros_tabla(df: pd.DataFrame, narancs_indexek: list[int]):
    def szinez_narancs(row):
        if row.name in narancs_indexek:
            return [
                "background-color: rgba(249, 115, 22, 0.28); color: #fed7aa; font-weight: 600;"
            ] * len(row)
        return [""] * len(row)

    return df.style.apply(szinez_narancs, axis=1)