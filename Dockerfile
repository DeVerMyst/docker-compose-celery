FROM python:3.11-slim

# Empêche la création de fichiers .pyc et force l'affichage des logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Récupération de l'exécutable 'uv' depuis l'image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Étape de cache pour les dépendances
COPY pyproject.toml .
# On installe les dépendances listées dans le pyproject.toml
RUN uv pip install --system .

# Copie du code source (API, Worker, Front)
COPY . .