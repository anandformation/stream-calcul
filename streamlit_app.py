import streamlit as st
import math

st.set_page_config(page_title="Simulateur Temps & Coûts – Aerōtape", layout="centered")
st.title("Simulateur — Analyse complète par site (scan + PC + annotation)")

# --------------------------
# Entrées principales
# --------------------------
st.header("Configuration par site")
nb_sites = st.number_input("Nombre de sites", min_value=1, step=1, value=1)

# 1 site = 7 lames, mais override possible
default_lames = nb_sites * 7
nb_lames = st.number_input("Nombre total de lames (override possible)", min_value=1, max_value=500, step=1, value=default_lames)
st.caption(f"Par défaut : {nb_sites} sites = {default_lames} lames")

st.divider()

# --------------------------
# Paramètres machine
# --------------------------
st.header("Temps machine")

scan_min = st.number_input("Temps de scan (min / lame)", min_value=0, step=1, value=30)
max_scan_batch = 20  # CONSTANTE imposée

segmentation_h = st.number_input("Temps de processing (segmentation + préclass) (heures / lame)", min_value=0.0, step=0.25, value=2.5)

nb_pc = st.number_input("Nombre de PC disponibles (1 lame simultanée / PC)", min_value=1, step=1, value=1)

marge_machine = st.slider("Marge temps machine (+%)", 0, 200, 0)

st.divider()

# --------------------------
# Paramètres humains
# --------------------------
st.header("Temps humain")

transfert_min = st.number_input("Envoi dans le cloud (min / lame)", min_value=0, step=1, value=20)
annotation_min = st.number_input("Annotation humaine (min / lame)", min_value=0, step=1, value=20)

marge_humain = st.slider("Marge temps humain (+%)", 0, 200, 0)

# --------------------------
# Coût humain
# --------------------------
st.header("Coût humain")

mode_humain = st.radio("Mode de calcul", ["Rémunération horaire", "Salaire mensuel brut (converti)"])

if mode_humain == "Rémunération horaire":
    cout_humain_h = st.number_input("Coût humain (€ / heure)", min_value=0.0, step=1.0, value=35.0)
else:
    salaire_mensuel = st.number_input("Salaire brut chargé (€ / mois)", min_value=0, step=500, value=3000)
    cout_humain_h = (salaire_mensuel * 12) / 1607
    st.caption(f"Équivalent : {cout_humain_h:.2f} € / heure")

st.divider()

# --------------------------
# Coût machine (non inclus)
# --------------------------
st.header("Coût machine (NON inclus dans le total projet)")

cout_machine_unit = st.number_input("Coût d'un PC (€)", min_value=0, step=500, value=2000)
cout_machine_total = cout_machine_unit * nb_pc
st.caption(f"Investissement machine total : {cout_machine_total} €")

st.divider()

# --------------------------
# CALCULS
# --------------------------

# --- Temps scan ---
scan_time_per_lame_h = scan_min / 60
total_scan_batches = math.ceil(nb_lames / max_scan_batch)
scan_total_h = total_scan_batches * (max_scan_batch * scan_time_per_lame_h)

# Exemple : 35 lames → batches (20, 15)

# --- Temps processing ---
processing_total_h = (segmentation_h * nb_lames) / nb_pc  # distribué sur PC

# --- marge machine ---
scan_total_h *= (1 + marge_machine/100)
processing_total_h *= (1 + marge_machine/100)

# --- Temps machine TOTAL ---
temps_machine_total = max(scan_total_h, processing_total_h)

# --------------------------
# TEMPS HUMAIN
# --------------------------
transfert_total_h = (transfert_min/60) * nb_lames
annotation_total_h = (annotation_min/60) * nb_lames
temps_humain_total = (transfert_total_h + annotation_total_h) * (1 + marge_humain/100)

# --------------------------
# TEMPS TOTAL
# --------------------------
temps_total = temps_machine_total + temps_humain_total

# --------------------------
# COÛT TOTAL
# --------------------------
cout_total_humain = temps_humain_total * cout_humain_h
cout_total_projet = cout_total_humain  # machine EXCLUE

# --------------------------
# AFFICHAGE
# --------------------------

def hformat(h):
    return f"{int(h)} h {int((h % 1)*60)} min"

st.header("Résultats")

st.write("### Temps")
st.write(f"- Temps scan total : **{hformat(scan_total_h)}**")
st.write(f"- Temps processing PC total : **{hformat(processing_total_h)}**")
st.write(f"- Temps machine total (scan vs processing) : **{hformat(temps_machine_total)}**")
st.write(f"- Temps humain total : **{hformat(temps_humain_total)}**")
st.write(f"➡ Temps **total cumulé** = **{hformat(temps_total)}**")

st.write("### Coûts (humain uniquement)")
st.write(f"- Coût humain total : **{cout_total_humain:,.2f} €**")
st.write(f"- Coût machine (non inclus) : **{cout_machine_total:,.0f} €**")
st.write(f"➡ **Coût total projet = {cout_total_projet:,.2f} €** (humain uniquement)")

st.divider()
st.info("Logique complète : scan par batch de 20, processing distribué sur PC, humain après traitement, marges appliquées.")
