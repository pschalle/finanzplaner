import streamlit as st
from ruhestand_logik import berechne_verlauf, fruehestes_rentenalter, zusaetzliche_sparrate

st.set_page_config(page_title="Finanzplaner", page_icon="📈")
def formatiere(betrag):
    return f"{betrag:,.0f}".replace(",", ".") + " €"

st.title("Willkommen in Ihrem persönlichen Finanzplaner")
st.subheader("Über Sie")
st.divider()
links,rechts = st.columns(2)
aktuelles_alter = links.slider("Alter:", min_value=0, max_value=100, value=45)
rentenalter = rechts.slider("Renteneintrittsalter:", min_value=18, max_value=80, value=65)

st.subheader("Ihre Finanzen")
st.divider()
vermoegen = st.number_input("Ihr aktuelles Vermögen in €", min_value=0, value=100000, step=10000)
nettogehalt = st.number_input("Ihr monatliches Nettogehalt in €", min_value=0, value=4000, step=500)
ausgaben = st.number_input("Ihre durchschnittlichen Ausgaben pro Monat in €", min_value=0, value=3000, step=500)
rendite = st.slider("Ihre durchschnittliche jährliche Rendite aller Cash-Assets in %", min_value=0.0, max_value=20.0, value=5.0, step=0.2)
zielvermoegen = st.number_input("Ihr gewünschtes Zielvermögen in €", min_value=0 , value=1000000, step=50000)

sparrate = nettogehalt - ausgaben
n = rentenalter - aktuelles_alter
if n < 0:
    st.error("Das aktuelle Alter darf das Rentenalter nicht überschreiten")
    st.stop()

verlauf = berechne_verlauf(vermoegen, rendite / 100, sparrate, n)
luecke = zielvermoegen - verlauf[-1]

st.subheader("Wichtige Werte")
st.divider()
spalten = st.columns(3)

spalten[0].metric("Vermögen bei Rente", formatiere(verlauf[-1]))

if luecke <= 0:
    st.success("Glückwunsch Sie haben Ihr Zielvermögen erreicht!")

else:
    spalten[1].metric("Lücke zum Zielvermögen:", formatiere(luecke))

ergebnis = fruehestes_rentenalter(aktuelles_alter, vermoegen, zielvermoegen, rendite/100, sparrate)

if ergebnis is None:
    spalten[2].error("Leider ist Ihr Zielvermögen nicht mehr erreichbar")

else:
    spalten[2].metric("Frühestes Rentenalter ", f"{ergebnis} Jahre")

if luecke > 0:
    zusatz = zusaetzliche_sparrate(luecke, rendite/100, n)

    if zusatz is None:
        st.warning("Bis zum gewünschten Rentenalter bleibt keine Zeit mehr zum Sparen.")
    else:
        gesamt = sparrate + zusatz
        st.metric("Nötige Sparrate pro Monat", formatiere(gesamt),"+" + formatiere(zusatz))
alter_liste = list(range(aktuelles_alter, rentenalter+1))

daten = {"Alter": alter_liste, "Vermögen": verlauf}
st.line_chart(daten, x="Alter", y="Vermögen")

st.caption("Vereinfachte Modellrechnung: konstante Rendite, ohne Inflation und Steuern. Keine Anlageberatung.")
