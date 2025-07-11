import streamlit as st

# Farbdefinitionen (angepasst)
KRÄFTIG_ORANGE = "#FF6A00"  # Kräftiges Orange ohne Schwarzanteil
DUNKELGRAU = "#333333"         # Gut lesbares Dunkelgrau
HINTERGRUND = "#F9F9F9"       # Heller Hintergrund

# --- Design-Anpassung via HTML/CSS ---
st.markdown(
    f"""
    <style>
    body {{
        background-color: {HINTERGRUND};
        color: {DUNKELGRAU};
    }}
    .stApp {{
        background-color: {HINTERGRUND};
    }}
    h1, h2, h3 {{
        color: {KRÄFTIG_ORANGE};
        font-weight: 600;
    }}
    h1 {{ font-size: 28px !important; }}
    h2 {{ font-size: 20px !important; }}
    h3 {{ font-size: 18px !important; }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    .stButton > button {{
        background-color: {KRÄFTIG_ORANGE};
        color: white;
        border-radius: 8px;
    }}
    input[type="text"], input[type="number"], input[type="password"] {{
        background-color: white !important;
        border: 3px solid {KRÄFTIG_ORANGE} !important;
        color: {DUNKELGRAU} !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }}
    .stTextInput input,
    .stNumberInput input {{
        background-color: white !important;
        border: 3px solid {KRÄFTIG_ORANGE} !important;
        color: {DUNKELGRAU} !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }}
    label, .stTextInput label, .stNumberInput label {{
        color: {DUNKELGRAU} !important;
        font-weight: 600;
    }}
    div, p, .markdown-text-container, .stMarkdown {{
        color: {DUNKELGRAU} !important;
        font-size: 17px !important;
        font-weight: 500;
    }}
    .stSuccess {{
        background-color: #FFF5E6 !important;
        border: 2px solid {KRÄFTIG_ORANGE} !important;
        color: {DUNKELGRAU} !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }}
    .stInfo {{
        background-color: #F0F0F0 !important;
        border: 2px solid {KRÄFTIG_ORANGE} !important;
        color: {DUNKELGRAU} !important;
        font-size: 17px !important;
        font-weight: 500 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Passwortschutz ---
PASSWORT = "fernwaerme2025"
pass_eingabe = st.text_input("Bitte Passwort eingeben:", type="password")

if pass_eingabe != PASSWORT:
    st.warning("Zugriff verweigert. Bitte gültiges Passwort eingeben.")
    st.stop()

# --- Funktionsauswahl ---
funktion = st.selectbox("Funktion auswählen:", [
    "Fernwärmekostenberechnung",
    "Heizöl → kWh & kW",
    "Pellets → kWh",
    "kWh → Heizöl",
    "kWh → Pellets"
])

if funktion == "Heizöl → kWh & kW":
    st.title("Heizölverbrauch umrechnen")
    liter = st.number_input("Verbrauch in Liter Heizöl:", min_value=0.0, format="%.2f")
    zeith = 1400  # Stunden pro Jahr

    if liter > 0:
        kwh = liter * 10  # Heizwert ca. 10 kWh/l
        kw = kwh / zeith
        st.success(f"{liter:.2f} Liter Heizöl entsprechen ca. {kwh:.2f} kWh")
        st.info(f"Erforderliche Heizleistung: {kw:.2f} kW bei {zeith} Betriebsstunden pro Jahr")

elif funktion == "Pellets → kWh":
    st.title("Pelletsverbrauch umrechnen")
    tonnen = st.number_input("Verbrauch in Tonnen Pellets:", min_value=0.0, format="%.2f")

    if tonnen > 0:
        kwh_pellets = tonnen * 4800  # Heizwert ca. 4800 kWh/t
        kw = kwh_pellets / 1400
        st.success(f"{tonnen:.2f} Tonnen Pellets entsprechen ca. {kwh_pellets:.2f} kWh")
        st.info(f"Erforderliche Heizleistung: {kw:.2f} kW bei 1400 Betriebsstunden pro Jahr")

elif funktion == "kWh → Heizöl":
    st.title("kWh in Heizöl umrechnen")
    kwh = st.number_input("Energieverbrauch in kWh:", min_value=0.0, format="%.2f")
    if kwh > 0:
        liter = kwh / 10  # 10 kWh/l
        st.success(f"{kwh:.2f} kWh entsprechen ca. {liter:.2f} Liter Heizöl")

elif funktion == "kWh → Pellets":
    st.title("kWh in Pellets umrechnen")
    kwh = st.number_input("Energieverbrauch in kWh:", min_value=0.0, format="%.2f")
    if kwh > 0:
        tonnen = kwh / 4800  # 4800 kWh/t
        st.success(f"{kwh:.2f} kWh entsprechen ca. {tonnen:.2f} Tonnen Pellets")

elif funktion == "Fernwärmekostenberechnung":
    # --- Titel ---
    st.title("Fernwärmekostenberechnung pro Jahr")
    st.subheader("Ausgabe auf Basis Preisblatt gültig ab 010924 -rabattiert-nach")

    # --- Konstante Preise ---
    ENERGIEPREIS_CENT_PRO_KWH = 8.0469     # in Cent
    GRUNDPREIS_EURO_PRO_KW_JAHR = 42.9324  # in Euro
    WAERMEZAEHLER_MONATLICH = 2.8414       # Euro pro Monat (netto)
    OEKO_UMWELT_CENT_PRO_KWH = 0.1624      # in Cent pro kWh

    # --- Funktion zur Berechnung der Messleistungskosten ---
    def berechne_messleistungskosten(anschlussleistung_kw):
        if anschlussleistung_kw <= 105:
            return 8.8986 * 12
        elif anschlussleistung_kw <= 245:
            return 17.1616 * 12
        elif anschlussleistung_kw <= 420:
            return 21.6109 * 12
        elif anschlussleistung_kw <= 1050:
            return 26.0602 * 12
        elif anschlussleistung_kw <= 1750:
            return 28.6027 * 12
        else:
            return 28.6027 * 12

    # --- Benutzereingabe ---
    anschlussleistung_kw = st.number_input("Anschlussleistung (kW):", min_value=0.0, format="%.2f")
    verbrauch_kwh = st.number_input("Jahresverbrauch (kWh):", min_value=0.0, format="%.2f")

    if anschlussleistung_kw > 0 and verbrauch_kwh > 0:
        # Einzelkosten berechnen
        energiekosten = verbrauch_kwh * (ENERGIEPREIS_CENT_PRO_KWH / 100)
        grundkosten = anschlussleistung_kw * GRUNDPREIS_EURO_PRO_KW_JAHR
        messleistungskosten = berechne_messleistungskosten(anschlussleistung_kw)
        waermezaehler_kosten = WAERMEZAEHLER_MONATLICH * 12

        # Zwischensumme netto
        zwischensumme = energiekosten + grundkosten + messleistungskosten + waermezaehler_kosten

        # Abgaben
        oekobeitrag = verbrauch_kwh * (OEKO_UMWELT_CENT_PRO_KWH / 100)
        benutzungsabgabe = (zwischensumme + oekobeitrag) * 0.06
        netto_gesamt = zwischensumme + oekobeitrag + benutzungsabgabe
        mehrwertsteuer = netto_gesamt * 0.20
        brutto_gesamt = netto_gesamt + mehrwertsteuer

        # --- Ausgabe ---
        st.subheader("Kostenaufstellung Fernwärme")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Energiekosten:")
            st.write(f"Grundpreis:")
            st.write(f"Messleistungskosten:")
            st.write(f"Wärmezählerkosten:")
            st.markdown("---")
            st.write(f"Öko- und Umweltbeitrag:")
            st.write(f"Benutzungsabgabe (6%):")
            st.markdown("---")
            st.write(f"**Gesamtkosten netto:**")
            st.write(f"Mehrwertsteuer (20%):")
            st.markdown("---")
            st.write(f"**Gesamtkosten (brutto):**")

        with col2:
            st.write(f"{energiekosten:10.2f} €")
            st.write(f"{grundkosten:10.2f} €")
            st.write(f"{messleistungskosten:10.2f} €")
            st.write(f"{waermezaehler_kosten:10.2f} €")
            st.markdown("---")
            st.write(f"{oekobeitrag:10.2f} €")
            st.write(f"{benutzungsabgabe:10.2f} €")
            st.markdown("---")
            st.write(f"{netto_gesamt:10.2f} €")
            st.write(f"{mehrwertsteuer:10.2f} €")
            st.markdown("---")
            st.success(f"{brutto_gesamt:10.2f} € / Jahr")

        # --- Hinweistext ---
        st.markdown(f"""
        <div style='margin-top: 2rem; color: {DUNKELGRAU}; font-size: 16px; font-style: italic; font-weight: 500; background-color: #FFF5E6; border-left: 4px solid {KRÄFTIG_ORANGE}; padding: 0.8rem;'>
            Hinweis: Diese Berechnung basiert auf den eingegebenen Werten und aktuellen Tarifinformationen. Sie stellt keine rechtsverbindliche Auskunft dar und dient ausschließlich einer Prognose. Fehler in den Daten können nicht ausgeschlossen werden.
        </div>
        """, unsafe_allow_html=True)
