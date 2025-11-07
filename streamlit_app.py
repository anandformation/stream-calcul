import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Simulateur traitement lames — Ōberon", layout="centered")
st.title("Simulateur — traitement & coût par site (Aerōtape)")

# ---- Configuration par site ----
st.header("Configuration principale")
nb_sites = st.number_input("Nombre de SITES", min_value=1, step=1, value=1)
nb_lames = st.number_input("Nombre de LAMES (modifiable à la main)", min_value=1, max_value=100, step=1, value=nb_sites * 7)

st.markdown("---")

# ---- Machine ----
st.header("Paramètres machine")
temps_lame_h = st.number_input("Temps de processing par lame (heures)", min_value=0.0, step=0.5, value=2.0)
nb_pc = st.number_input("Nombre de PC (1 lame en parallèle par PC)", min_value=1, step=1, value=1)

st.markdown("---")

# ---- Paramètres opérationnels manuels ----
st.header("Paramètres opérationnels (REMPLISSAGE MANUEL)")

pickup_min = st.number_input("Aller chercher le tambour (minutes / site)", min_value=0, step=1, value=30)
prep_fuschine_min = st.number_input("Préparation Fuschine (minutes / site)", min_value=0, step=1, value=30)
load_unload_min = st.number_input("Chargement / déchargement lames (minutes / site)", min_value=0, step=1, value=15)
transfer_cloud_h = st.number_input("Transfert cloud vers les PC (heures / site)", min_value=0.0, step=0.1, value=2.0)
annotation_min_per_lame = st.number_input("Annotation humaine (minutes / lame)", min_value=0, step=1, value=15)

st.markdown("---")

# ---- Coûts ----
st.header("Coûts")
human_operators = st.number_input("Nombre d'opérateurs humains", min_value=1, step=1, value=1)
human_cost_h = st.number_input("Coût humain (€ / heure)", min_value=0.0, step=1.0, value=35.0)
machine_cost_h = st.number_input("Coût machine (€ / heure)", min_value=0.0, step=1.0, value=2.0)

st.markdown("---")

# ================= CALCULS ==================

# Machine
batches = math.ceil(nb_lames / nb_pc)
machine_process_h = batches * temps_lame_h
machine_transfer_h = nb_sites * transfer_cloud_h
machine_total_h = machine_process_h + machine_transfer_h

# Humain
human_pickup_h = (pickup_min/60) * nb_sites
human_prep_h = (prep_fuschine_min/60) * nb_sites
human_load_h = (load_unload_min/60) * nb_sites
human_annot_h = (annotation_min_per_lame/60) * nb_lames
human_total_h = human_pickup_h + human_prep_h + human_load_h + human_annot_h

# Coûts
cost_human = human_total_h * human_cost_h
cost_machine = machine_total_h * machine_cost_h
cost_total = cost_human + cost_machine

# Temps mur (approximation)
machine_wall_h = machine_total_h
human_wall_h = human_total_h / human_operators
wall_clock_h = max(machine_wall_h, human_wall_h)

def hformat(h):
    return f"{int(h)}h {int((h%1)*60)}min"

# ================= AFFICHAGE ==================

st.header("Résultats")

st.subheader("Temps machine")
st.write(f"Temps total machine : **{machine_total_h:.2f} h** (~{hformat(machine_total_h)})")

st.subheader("Temps humain")
st.write(f"Temps total humain : **{human_total_h:.2f} h** (~{hformat(human_total_h)})")

st.subheader("Estimation durée projet (temps mur)")
st.write(f"Durée estimée : **{hformat(wall_clock_h)}**")

st.subheader("Coûts estimés")
st.write(f"Coût humain : **{cost_human:.2f} €**")
st.write(f"Coût machine : **{cost_machine:.2f} €**")
st.write(f"Coût total : **{cost_total:.2f} €**")

st.markdown("---")

# Tableau résumé
df = pd.DataFrame({
    "Variable": [
        "Sites", "Lames", "PC",
        "Temps/lame (h)", "Batches", "Machine total (h)",
        "Humain total (h)", "Coût humain (€)",
        "Coût machine (€)", "Coût total (€)"
    ],
    "Valeur": [
        nb_sites, nb_lames, nb_pc,
        temps_lame_h, batches, round(machine_total_h,2),
        round(human_total_h,2), round(cost_human,2),
        round(cost_machine,2), round(cost_total,2)
    ]
})

st.dataframe(df, use_container_width=True)

st.info("""
Hypothèses :
- 1 PC traite 1 lame simultanément max.
- Transferts et traitements machines sont sommés de manière linéaire.
- Temps humain estimé parallélisable selon le nombre d'opérateurs.
- Temps mur ≈ max(temps machine, temps humain parallèle).
""")
