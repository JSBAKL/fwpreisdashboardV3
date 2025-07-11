import streamlit as st

# Farbdefinitionen (angepasst)
KRÄFTIG_ORANGE = "#FF6A00"
DUNKELGRAU = "#333333"
HINTERGRUND = "#F9F9F9"

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
        border: 2px solid {KRÄFTIG_ORANGE} !important;
        color: {DUNKELGRAU} !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }}
    div[data-baseweb="select"] {{
        background-color: white !important;
        border: 1.5px solid {KRÄFTIG_ORANGE} !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        padding: 2px !important;
        min-height: 38px !important;
    }}
    div[data-baseweb="select"] * {{
        color: {DUNKELGRAU} !important;
        font-weight: 500 !important;
        font-size: 16px !important;
    }}
    div[data-baseweb="select"] div[role="option"] {{
        background-color: white !important;
        color: {DUNKELGRAU} !important;
    }}
    div[data-baseweb="select"] div[role="option"]:hover,
    div[data-baseweb="select"] div[role="option"][aria-selected="true"] {{
        background-color: #FFEFE0 !important;
        color: #333333 !important;
    }}
    div[data-baseweb="popover"] {{
        background-color: white !important;
        color: {DUNKELGRAU} !important;
        border: 1.5px solid {KRÄFTIG_ORANGE} !important;
        border-radius: 6px !important;
    }}
    .css-1dimb5e-singleValue {{
        color: {DUNKELGRAU} !important;
    }}
    .css-1xc3v61-menu {{
        background-color: white !important;
        border: 1.5px solid {KRÄFTIG_ORANGE} !important;
        border-radius: 6px !important;
        color: {DUNKELGRAU} !important;
    }}
    .css-1n76uvr-control {{
        background-color: white !important;
        color: {DUNKELGRAU} !important;
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

PASSWORT = "fernwaerme2025"
if "passwort_ok" not in st.session_state:
    st.session_state.passwort_ok = False

if not st.session_state.passwort_ok:
    st.markdown("### 🔐 Zugang erforderlich")
    pass_eingabe = st.text_input("Bitte Passwort eingeben:", value="", type="password")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login = st.button("Einloggen")

    if login and pass_eingabe == PASSWORT:
        st.session_state.passwort_ok = True
        st.success("✅ Zugang gewährt. Die App ist freigeschaltet.")
    elif login and pass_eingabe != PASSWORT:
        st.warning("❌ Zugriff verweigert. Bitte gültiges Passwort eingeben.")
        st.stop()

    if not st.session_state.passwort_ok:
        st.stop()

st.markdown("""
### 📌 Bitte gewünschte Funktion auswählen:
""")
funktion = st.selectbox(
    label="Funktion auswählen",
    options=[
        "Fernwärmekostenberechnung",
        "Heizöl → kWh & kW",
        "Pellets → kWh & kW",
        "kWh → Heizöl",
        "kWh → Pellets"
    ],
    key="funktion-box"
)

if funktion == "Heizöl → kWh & kW":
    liter = st.number_input("Verbrauch in Liter Heizöl pro Jahr:", min_value=0.0, step=10.0)
    if liter:
        kwh = liter * 10.0
        kw = kwh / 1400
        st.success(f"Entspricht {kwh:.0f} kWh und einer Heizleistung von {kw:.2f} kW bei 1400h/Jahr")

elif funktion == "Pellets → kWh & kW":
    tonnen = st.number_input("Verbrauch in Tonnen Pellets pro Jahr:", min_value=0.0, step=0.1)
    if tonnen:
        kwh = tonnen * 4800
        kw = kwh / 1400
        st.success(f"Entspricht {kwh:.0f} kWh und einer Heizleistung von {kw:.2f} kW bei 1400h/Jahr")

elif funktion == "kWh → Heizöl":
    kwh = st.number_input("Energie in kWh:", min_value=0.0, step=50.0)
    if kwh:
        liter = kwh / 10.0
        st.success(f"Entspricht ca. {liter:.1f} Liter Heizöl")

elif funktion == "kWh → Pellets":
    kwh = st.number_input("Energie in kWh:", min_value=0.0, step=50.0)
    if kwh:
        tonnen = kwh / 4800.0
        st.success(f"Entspricht ca. {tonnen:.2f} Tonnen Pellets")

elif funktion == "Fernwärmekostenberechnung":
    st.header("Fernwärmekostenberechnung pro Jahr")

    anschlussleistung_kw = st.number_input("Anschlussleistung (kW):", min_value=0.0, step=1.0)
    verbrauch_kwh = st.number_input("Jahresverbrauch (kWh):", min_value=0.0, step=100.0)

    ENERGIEPREIS_CENT_PRO_KWH = 8.0469
    GRUNDPREIS_EURO_PRO_KW_JAHR = 42.9324
    WAERMEZAEHLER_MONATLICH = 2.8414

    def berechne_messleistungskosten(kw):
        if kw <= 105:
            return 8.8986 * 12
        elif kw <= 245:
            return 17.1616 * 12
        elif kw <= 420:
            return 21.6109 * 12
        elif kw <= 1050:
            return 26.0602 * 12
        elif kw <= 1750:
            return 28.6027 * 12
        else:
            return 28.6027 * 12

    if anschlussleistung_kw > 0 and verbrauch_kwh > 0:
        energiekosten = verbrauch_kwh * (ENERGIEPREIS_CENT_PRO_KWH / 100)
        grundkosten = anschlussleistung_kw * GRUNDPREIS_EURO_PRO_KW_JAHR
        messleistungskosten = berechne_messleistungskosten(anschlussleistung_kw)
        waermezaehler_kosten = WAERMEZAEHLER_MONATLICH * 12

        zwischensumme = energiekosten + grundkosten + messleistungskosten + waermezaehler_kosten
        benutzungsabgabe = zwischensumme * 0.06
        netto_gesamt = zwischensumme + benutzungsabgabe
        mehrwertsteuer = netto_gesamt * 0.20
        brutto_gesamt = netto_gesamt + mehrwertsteuer

        st.subheader("Ausgabe auf Basis des gültigen Preisblatts")
        ausgabe_text = f"""
        <h3>Ergebnisse</h3>
        <p><b>Energiekosten:</b> {energiekosten:.2f} €<br>
        <b>Grundpreis:</b> {grundkosten:.2f} €<br>
        <b>Messleistungskosten:</b> {messleistungskosten:.2f} €<br>
        <b>Wärmezählerkosten:</b> {waermezaehler_kosten:.2f} €<br>
        <b>Benutzungsabgabe (6%):</b> {benutzungsabgabe:.2f} €<br>
        <b>Netto gesamt:</b> {netto_gesamt:.2f} €<br>
        <b>Mehrwertsteuer (20%):</b> {mehrwertsteuer:.2f} €<br>
        <b><u>Bruttokosten pro Jahr:</u></b> {brutto_gesamt:.2f} €</p>
        """
        st.markdown(ausgabe_text, unsafe_allow_html=True)

        st.info("Hinweis: Diese Berechnung basiert auf den eingegebenen Werten und aktuellen Tarifinformationen. "
                "Sie stellt keine rechtsverbindliche Auskunft dar und dient ausschließlich einer Prognose. "
                "Fehler in den Daten können nicht ausgeschlossen werden.")

