import streamlit as st
import secrets

st.set_page_config(
    page_title="Zahlen-Würfelspiel",
    page_icon="🎲",
    layout="wide"
)

# Rechte Sidebar per CSS
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    left: auto;
    right: 0;
}
</style>
""", unsafe_allow_html=True)

MAX_ZAHL = 10000000000000000000000000000000

st.title("🎲 Extremes Zahlen-Würfelspiel")

st.write("""
Klicke auf **Würfeln**.

- Zahlen von **1 bis 1000** gewinnen.
- Wenn alle Zahlen größer als **1000** sind, verlierst du.
- Bei jeder Niederlage kommt eine neue Zahl dazu.
- Alle vorhandenen Zahlen werden bei jedem Würfeln neu generiert.
- Die **kleinste Zahl** steht immer ganz oben.
- Das Spiel endet, wenn mindestens eine Zahl kleiner als **100** ist.
""")

# Session State vorbereiten
if "anzahl_zahlen" not in st.session_state:
    st.session_state.anzahl_zahlen = 1

if "spiel_beendet" not in st.session_state:
    st.session_state.spiel_beendet = False

if "aktuelle_zahlen" not in st.session_state:
    st.session_state.aktuelle_zahlen = []

if "alle_zahlen" not in st.session_state:
    st.session_state.alle_zahlen = []


def zufallszahl():
    return secrets.randbelow(MAX_ZAHL) + 1


def reset_game():
    st.session_state.anzahl_zahlen = 1
    st.session_state.spiel_beendet = False
    st.session_state.aktuelle_zahlen = []
    st.session_state.alle_zahlen = []


# Rechte Ranking-Leiste
with st.sidebar:
    st.header("🏆 Overall Ranking")

    if len(st.session_state.alle_zahlen) == 0:
        st.info("Noch keine Zahlen gewürfelt.")
    else:
        st.subheader("🔽 Kleinste Zahlen bisher")

        kleinste_zahlen = sorted(st.session_state.alle_zahlen)[:10]

        for platz, zahl in enumerate(kleinste_zahlen, start=1):
            st.write(f"**Platz {platz}:** {zahl}")

        st.divider()

        st.subheader("🎯 Am nächsten an 1000")

        nahe_an_1000 = sorted(
            st.session_state.alle_zahlen,
            key=lambda zahl: abs(zahl - 1000)
        )[:10]

        for platz, zahl in enumerate(nahe_an_1000, start=1):
            abstand = abs(zahl - 1000)
            st.write(f"**Platz {platz}:** {zahl}")
            st.caption(f"Abstand zu 1000: {abstand}")


if st.button("🔄 Spiel zurücksetzen"):
    reset_game()
    st.rerun()


if not st.session_state.spiel_beendet:
    if st.button("🎲 Würfeln"):
        neue_zahlen = []

        for i in range(st.session_state.anzahl_zahlen):
            zahl = zufallszahl()
            neue_zahlen.append(zahl)

        # Alle aktuellen Zahlen sortieren:
        # kleinste Zahl steht oben
        neue_zahlen.sort()

        st.session_state.aktuelle_zahlen = neue_zahlen
        st.session_state.alle_zahlen.extend(neue_zahlen)

        st.subheader("🎲 Aktuelle Zahlen")

        for index, zahl in enumerate(st.session_state.aktuelle_zahlen, start=1):
            if index == 1:
                st.success(f"🥇 Kleinste Zahl: **{zahl}**")
            else:
                st.write(f"Zahl {index}: **{zahl}**")

        # Spielende: mindestens eine Zahl kleiner als 100
        if any(zahl < 100 for zahl in st.session_state.aktuelle_zahlen):
            st.success("🏆 Eine Zahl ist kleiner als 100! Das Spiel ist beendet.")
            st.session_state.spiel_beendet = True

        # Gewinn: mindestens eine Zahl zwischen 1 und 1000
        elif any(1 <= zahl <= 1000 for zahl in st.session_state.aktuelle_zahlen):
            st.success("🎉 Gewonnen! Mindestens eine Zahl liegt zwischen 1 und 1000.")

        # Niederlage: alle Zahlen größer als 1000
        else:
            st.error("😢 Verloren! Alle Zahlen sind größer als 1000.")
            st.session_state.anzahl_zahlen += 1
            st.warning(
                f"In der nächsten Runde gibt es **{st.session_state.anzahl_zahlen} Zahlen**."
            )

else:
    st.info("Das Spiel ist beendet. Klicke auf **Spiel zurücksetzen**, um neu zu starten.")

# Falls schon Zahlen gewürfelt wurden, auch nach dem Neuladen anzeigen
if st.session_state.aktuelle_zahlen:
    st.divider()
    st.subheader("📌 Letzte gewürfelte Zahlen")

    for index, zahl in enumerate(st.session_state.aktuelle_zahlen, start=1):
        if index == 1:
            st.success(f"🥇 Kleinste Zahl: **{zahl}**")
        else:
            st.write(f"Zahl {index}: **{zahl}**")
