import time

import requests
import streamlit as st

st.title("IA Monitor - Celery Training")

if "jobs" not in st.session_state:
    st.session_state.jobs = []

if st.button("Lancer une prédiction"):
    req = requests.post("http://api:8000/predict")
    task_id = req.json()["task_id"]
    st.session_state.jobs.append(task_id)

# Affichage du tableau
if st.session_state.jobs:
    st.subheader("État des tâches")
    for tid in st.session_state.jobs:
        status_req = requests.get(f"http://api:8000/status/{tid}").json()
        col1, col2, col3 = st.columns(3)
        col1.write(f"ID: {tid[:8]}...")
        col2.write(f"Statut: {status_req['status']}")
        col3.write(f"Résultat: {status_req['result'] or 'En attente...'}")

# Auto-refresh toutes les 2 secondes
time.sleep(2)
st.rerun()