import streamlit as st
import secrets

st.title("🎲 Extremes Zahlen-Würfelspiel")

MAX_ZAHL = 10000000000000000000000000000000

st.write("""
Klicke auf **Würfeln**.

- Zahlen von **1 bis 1000** gewinnen.
- Wenn alle Zahlen größer als **1000** sind, verlierst du.
- Bei jeder Niederlage kommt eine neue Zahl dazu.
- Alle Zahlen werden bei jedem Würfeln neu generiert.
- Das Spiel endet, wenn eine Zahl kleiner als **100** ist.
""")

# Startwerte speichern
if "anzahl_zahlen" not in st.session_state:
    st.session_state.anzahl_zahlen = 1

if "spiel_beendet" not in st.session_state:
    st.session_state.spiel_beendet = False


def zufallszahl():
    return secrets.randbelow(MAX_ZAHL) + 1


if st.button("🔄 Spiel zurücksetzen"):
    st.session_state.anzahl_zahlen = 1
    st.session_state.spiel_beendet = False
    st.rerun()


if not st.session_state.spiel_beendet:
    if st.button("🎲 Würfeln"):
        zahlen = []

        for i in range(st.session_state.anzahl_zahlen):
            zahlen.append(zufallszahl())

        st.subheader("Deine Zahlen:")

        for index, zahl in enumerate(zahlen, start=1):
            st.write(f"Zahl {index}: **{zahl}**")

        # Prüfen, ob eine Zahl kleiner als 100 ist
        if any(zahl < 100 for zahl in zahlen):
            st.success("🏆 Eine Zahl ist kleiner als 100! Das Spiel ist beendet.")
            st.session_state.spiel_beendet = True

        # Prüfen, ob man gewonnen hat
        elif any(1 <= zahl <= 1000 for zahl in zahlen):
            st.success("🎉 Gewonnen! Mindestens eine Zahl liegt zwischen 1 und 1000.")

        # Wenn alle Zahlen größer als 1000 sind, verliert man
        else:
            st.error("😢 Verloren! Alle Zahlen sind größer als 1000.")
            st.session_state.anzahl_zahlen += 1
            st.warning(
                f"In der nächsten Runde gibt es {st.session_state.anzahl_zahlen} Zahlen."
            )

else:
    st.info("Das Spiel ist beendet. Klicke auf **Spiel zurücksetzen**, um neu zu starten.")
