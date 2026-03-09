import os
import time

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://api:8000")
st.title("IA Monitor - Celery Training")

st.divider()
st.sidebar.header("Monitoring")
st.sidebar.write("[Ouvrir Flower (Dashboard)](http://localhost:5555)")
st.sidebar.info(
    "Utilisez `docker-compose up -d --scale worker=5` pour voir la vitesse augmenter !"
)

if "jobs" not in st.session_state:
    st.session_state.jobs = []

if st.button("Lancer une prédiction"):
    req = requests.post(f"{API_URL}/predict")
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
