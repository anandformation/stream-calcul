import streamlit as st
import math

st.set_page_config(page_title="Simulateur Temps & Coûts – Analyse Lames", layout="centered")
st.title("Simulateur — Analyse et traitement de lames (Aerōtape)")

# --------------------------
# Entrées principales
# --------------------------
st.header("Configuration du projet")
nb_lames = st.number_input("Nombre de lames à traiter", min_value=1, max_value=20, step=1, value=10)
nb_pc = st.number_input("Nombre de PC disponibles (1 lame simultanée par PC)", min_value=1, step=1, value=1)

st.divider()

# --------------------------
# Étapes de traitement
# --------------------------
st.header("Durées machine (par lame)")

scan_min = st.number_input("Temps de scan (minutes / lame)", min_value=0, step=1, value=30)
segmentation_h = st.number_input("Temps de segmentation + pré-classification (heures / lame)", min_value=0.0, step=0.5, value=2.5)

st.header("Durées humaines (par lame)")
transfert_min = st.number_input("Temps d’envoi cloud (minutes / lame)", min_value=0, step=1, value=20)
annotation_min = st.number_input("Annotation humaine (minutes / lame)", min_value=0, step=1, value=20)

st.divider()

# --------------------------
# Coûts humains
# --------------------------
st.header("Coût humain")

mode_humain = st.radio("Mode de calcul du coût humain :", ["Rémunération horaire", "Salaire mensuel brut (converti)"])

if mode_humain == "Rémunération horaire":
    cout_humain_h = st.number_input("Coût humain (€ / heure)", min_value=0.0, step=1.0, value=35.0)
else:
    salaire_mensuel = st.number_input("Salaire brut chargé (€ / mois)", min_value=0, step=500, value=3000)
    cout_humain_h = (salaire_mensuel * 12) / 1607
    st.caption(f"Soit ~ {cout_humain_h:.2f} € / heure")

st.divider()

# --------------------------
# Coût machine (AFFICHÉ MAIS NON INCLUS)
# --------------------------
st.header("Coût machine")
cout_machine_unit = st.number_input("Coût par PC (€)", min_value=0, step=500, value=2000)
cout_machine_total = cout_machine_unit * nb_pc
st.caption(f"Investissement machine total (non inclus dans le coût projet) : {cout_machine_total} €")

st.divider()

# --------------------------
# Marges
# --------------------------
st.header("Marges sur les temps")
marge_humain = st.slider("Marge temps humain (+%)", 0, 200, 0)
marge_machine = st.slider("Marge temps machine (+%)", 0, 200, 0)

# --------------------------
# Calculs
# --------------------------

# Temps machine
scan_total_h = (scan_min / 60) * nb_lames
segmentation_total_h = segmentation_h * nb_lames
temps_machine_total = (scan_total_h + segmentation_total_h) * (1 + marge_machine / 100)

# Temps humain
transfert_total_h = (transfert_min / 60) * nb_lames
annotation_total_h = (annotation_min / 60) * nb_lames
temps_humain_total = (transfert_total_h + annotation_total_h) * (1 + marge_humain / 100)

# Temps total
temps_total = temps_machine_total + temps_humain_total

# Coût total
cout_total_humain = temps_humain_total * cout_humain_h
cout_total = cout_total_humain  # machine NON incluse

# --------------------------
# Affichage
# --------------------------

def hformat(h):
    return f"{int(h)} h {int((h%1)*60)} min"

st.header("Résultats")

st.write("### Temps")
st.write(f"- Temps machine total : **{hformat(temps_machine_total)}**")
st.write(f"- Temps humain total : **{hformat(temps_humain_total)}**")
st.write(f"➡ Temps total cumulé : **{hformat(temps_total)}**")

st.write("### Coûts (sans machine)")
st.write(f"- Coût humain total : **{cout_total_humain:,.2f} €**")
st.write(f"- Coût machine (investissement, non inclus) : {cout_machine_total:,.0f} €")
st.write(f"➡ **Coût total du projet (humain uniquement) : {cout_total:,.2f} €**")

st.divider()
st.info("Le coût machine est affiché à titre informatif mais n'entre pas dans le total projet.")
