import streamlit as st
import secrets
import time

st.set_page_config(
    page_title="Zahlen-Würfelspiel",
    page_icon="🎲",
    layout="wide"
)

# Sidebar nach rechts verschieben
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    left: auto;
    right: 0;
}
</style>
""", unsafe_allow_html=True)

MAX_ZAHL = 10000000000000000000000000000000
RANKING_LAENGE = 10

st.title("🎲 Extremes Zahlen-Würfelspiel")

st.write("""
Klicke auf **Würfeln** oder starte den **Auto-Modus**.

- Zahlen von **1 bis 1000** gewinnen.
- Wenn alle Zahlen größer als **1000** sind, verlierst du.
- Bei jeder Niederlage kommt **eine neue Zahl** dazu.
- Alle vorhandenen Zahlen werden bei jedem Würfeln **neu generiert**.
- Die **kleinste aktuelle Zahl** steht immer ganz oben.
- Das Spiel endet, wenn mindestens eine Zahl kleiner als **100** ist.
""")

# Session State vorbereiten
if "anzahl_zahlen" not in st.session_state:
    st.session_state.anzahl_zahlen = 1

if "spiel_beendet" not in st.session_state:
    st.session_state.spiel_beendet = False

if "aktuelle_zahlen" not in st.session_state:
    st.session_state.aktuelle_zahlen = []

if "beste_kleinste_zahlen" not in st.session_state:
    st.session_state.beste_kleinste_zahlen = []

if "beste_nahe_1000" not in st.session_state:
    st.session_state.beste_nahe_1000 = []

if "auto_laeuft" not in st.session_state:
    st.session_state.auto_laeuft = False

if "klicks_pro_sekunde" not in st.session_state:
    st.session_state.klicks_pro_sekunde = 10

if "gesamt_wuerfe" not in st.session_state:
    st.session_state.gesamt_wuerfe = 0

if "gesamt_zahlen" not in st.session_state:
    st.session_state.gesamt_zahlen = 0

if "letzte_meldung" not in st.session_state:
    st.session_state.letzte_meldung = "Noch nicht gewürfelt."


def zufallszahl():
    return secrets.randbelow(MAX_ZAHL) + 1


def ranking_aktualisieren(neue_zahlen):
    # Ranking: kleinste Zahlen bisher
    alle_kleinsten = st.session_state.beste_kleinste_zahlen + neue_zahlen
    st.session_state.beste_kleinste_zahlen = sorted(alle_kleinsten)[:RANKING_LAENGE]

    # Ranking: am nächsten an 1000
    alle_nahe = st.session_state.beste_nahe_1000 + neue_zahlen
    st.session_state.beste_nahe_1000 = sorted(
        alle_nahe,
        key=lambda zahl: abs(zahl - 1000)
    )[:RANKING_LAENGE]


def eine_runde_wuerfeln():
    if st.session_state.spiel_beendet:
        st.session_state.auto_laeuft = False
        return

    neue_zahlen = []

    for _ in range(st.session_state.anzahl_zahlen):
        neue_zahlen.append(zufallszahl())

    neue_zahlen.sort()

    st.session_state.aktuelle_zahlen = neue_zahlen
    st.session_state.gesamt_wuerfe += 1
    st.session_state.gesamt_zahlen += len(neue_zahlen)

    ranking_aktualisieren(neue_zahlen)

    # Spielende: mindestens eine Zahl kleiner als 100
    if any(zahl < 100 for zahl in neue_zahlen):
        st.session_state.spiel_beendet = True
        st.session_state.auto_laeuft = False
        st.session_state.letzte_meldung = "🏆 Eine Zahl ist kleiner als 100! Das Spiel ist beendet."

    # Gewinn: mindestens eine Zahl zwischen 1 und 1000
    elif any(1 <= zahl <= 1000 for zahl in neue_zahlen):
        st.session_state.letzte_meldung = "🎉 Gewonnen! Mindestens eine Zahl liegt zwischen 1 und 1000."

    # Niederlage: alle Zahlen größer als 1000
    else:
        st.session_state.anzahl_zahlen += 1
        st.session_state.letzte_meldung = (
            f"😢 Verloren! In der nächsten Runde gibt es "
            f"{st.session_state.anzahl_zahlen} Zahlen."
        )


def reset_game():
    st.session_state.anzahl_zahlen = 1
    st.session_state.spiel_beendet = False
    st.session_state.aktuelle_zahlen = []
    st.session_state.beste_kleinste_zahlen = []
    st.session_state.beste_nahe_1000 = []
    st.session_state.auto_laeuft = False
    st.session_state.gesamt_wuerfe = 0
    st.session_state.gesamt_zahlen = 0
    st.session_state.letzte_meldung = "Noch nicht gewürfelt."


# Einstellungen
st.divider()

st.subheader("⚙️ Steuerung")

st.session_state.klicks_pro_sekunde = st.slider(
    "Automatische Würfe pro Sekunde",
    min_value=10,
    max_value=100,
    value=st.session_state.klicks_pro_sekunde,
    step=10
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎲 Einmal würfeln", disabled=st.session_state.auto_laeuft or st.session_state.spiel_beendet):
        eine_runde_wuerfeln()

with col2:
    if st.button("▶️ Auto-Modus starten", disabled=st.session_state.spiel_beendet):
        st.session_state.auto_laeuft = True

with col3:
    if st.button("⏹️ Auto-Modus stoppen"):
        st.session_state.auto_laeuft = False

if st.button("🔄 Spiel zurücksetzen"):
    reset_game()
    st.rerun()


# Auto-Modus ausführen
if st.session_state.auto_laeuft and not st.session_state.spiel_beendet:
    # Die Anzeige wird etwa 5-mal pro Sekunde aktualisiert.
    # Dadurch entstehen trotzdem 10 bis 100 Würfe pro Sekunde.
    wuerfe_pro_aktualisierung = st.session_state.klicks_pro_sekunde // 5

    for _ in range(wuerfe_pro_aktualisierung):
        eine_runde_wuerfeln()

        if st.session_state.spiel_beendet:
            break


# Status anzeigen
st.divider()

st.subheader("📊 Status")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.metric("Aktuelle Anzahl Zahlen", st.session_state.anzahl_zahlen)

with col_b:
    st.metric("Gesamte Würfe", st.session_state.gesamt_wuerfe)

with col_c:
    st.metric("Generierte Zahlen insgesamt", st.session_state.gesamt_zahlen)

if st.session_state.auto_laeuft:
    st.info(f"▶️ Auto-Modus läuft mit {st.session_state.klicks_pro_sekunde} Würfen pro Sekunde.")
else:
    st.warning("⏸️ Auto-Modus ist gestoppt.")


# Letzte Meldung
st.subheader("📢 Ergebnis")

meldung = st.session_state.letzte_meldung

if "Gewonnen" in meldung:
    st.success(meldung)
elif "Verloren" in meldung:
    st.error(meldung)
elif "beendet" in meldung:
    st.success(meldung)
else:
    st.info(meldung)


# Aktuelle Zahlen anzeigen
st.divider()

st.subheader("🎲 Aktuelle Zahlen")

if len(st.session_state.aktuelle_zahlen) == 0:
    st.info("Noch keine Zahlen gewürfelt.")
else:
    kleinste_zahl = st.session_state.aktuelle_zahlen[0]
    st.success(f"🥇 Kleinste aktuelle Zahl: **{kleinste_zahl}**")

    st.write("Alle aktuellen Zahlen, sortiert von klein nach groß:")

    # Damit die Seite nicht zu lang wird, werden nur die ersten 50 direkt angezeigt.
    # Die kleinste Zahl ist aber immer ganz oben.
    max_anzeigen = 50
    angezeigte_zahlen = st.session_state.aktuelle_zahlen[:max_anzeigen]

    for index, zahl in enumerate(angezeigte_zahlen, start=1):
        st.write(f"Zahl {index}: **{zahl}**")

    if len(st.session_state.aktuelle_zahlen) > max_anzeigen:
        st.info(
            f"Es gibt insgesamt {len(st.session_state.aktuelle_zahlen)} aktuelle Zahlen. "
            f"Angezeigt werden die kleinsten {max_anzeigen}."
        )


# Rechte Ranking-Leiste
with st.sidebar:
    st.header("🏆 Overall Ranking")

    st.metric("Gesamte Würfe", st.session_state.gesamt_wuerfe)
    st.metric("Generierte Zahlen", st.session_state.gesamt_zahlen)

    st.divider()

    st.subheader("🔽 Kleinste Zahlen bisher")

    if len(st.session_state.beste_kleinste_zahlen) == 0:
        st.info("Noch keine Zahlen gewürfelt.")
    else:
        for platz, zahl in enumerate(st.session_state.beste_kleinste_zahlen, start=1):
            st.write(f"**Platz {platz}:** {zahl}")

    st.divider()

    st.subheader("🎯 Am nächsten an 1000")

    if len(st.session_state.beste_nahe_1000) == 0:
        st.info("Noch keine Zahlen gewürfelt.")
    else:
        for platz, zahl in enumerate(st.session_state.beste_nahe_1000, start=1):
            abstand = abs(zahl - 1000)
            st.write(f"**Platz {platz}:** {zahl}")
            st.caption(f"Abstand zu 1000: {abstand}")


# Automatisch neu laden, solange der Auto-Modus läuft
if st.session_state.auto_laeuft and not st.session_state.spiel_beendet:
    time.sleep(0.2)
    st.rerun()
