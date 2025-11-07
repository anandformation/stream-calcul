import streamlit as st
import math

st.title("Simulateur de temps de processing des lames")

# Entrées utilisateur (avec limites 1 à 100 lames)
nb_lames = st.number_input("Nombre de lames à analyser", min_value=1, max_value=100, step=1, value=10)
saison = st.selectbox("Période", ["Basse saison (2h par lame)", "Haute saison (3h par lame)"])
nb_pc = st.number_input("Nombre de PC disponibles", min_value=1, step=1, value=1)

# Détermination du temps par lame
temps_par_lame = 2 if "Basse" in saison else 3

# Calcul du nombre de lots (batchs) à exécuter
batchs = math.ceil(nb_lames / nb_pc)

# Temps total
temps_total_h = batchs * temps_par_lame
jours = temps_total_h // 24
heures_restantes = temps_total_h % 24

# Résultats
st.divider()
st.subheader("Estimation du temps de traitement")

st.write(f"- Temps par lame : **{temps_par_lame} heure(s)**")
st.write(f"- Nombre de lames : **{nb_lames}**")
st.write(f"- Machines utilisées en parallèle : **{nb_pc} PC**")
st.write(f"- Nombre de cycles de calcul (batchs) : **{batchs}**")

if jours > 0:
    st.success(f"Temps total estimé : **{jours} jour(s) et {heures_restantes} heure(s)**")
else:
    st.success(f"Temps total estimé : **{temps_total_h} heures**")
