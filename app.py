import streamlit as st
import secrets

st.title("🎲 Zufallszahlen-Würfel")

st.write("Klicke auf den Button, um eine Zahl zwischen 1 und 10000000000000000000000000000000 zu würfeln.")

MAX_ZAHL = 10000000000000000000000000000000

if st.button("🎲 Würfeln"):
    zahl = secrets.randbelow(MAX_ZAHL) + 1

    st.subheader("Deine Zahl:")
    st.write(zahl)

    if zahl > 1000:
        st.success("🎉 Gewonnen!")
    else:
        st.error("😢 Leider nicht gewonnen.")
