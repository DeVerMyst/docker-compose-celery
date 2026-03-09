# Architecture IA Scalable avec Kubernetes & KEDA

Ce TP présente une architecture complète comprenant une API (FastAPI), un Front-end (Streamlit), un Worker (Celery) et un système d'autoscaling basé sur la charge de RabbitMQ.

## 🛠 1. Préparation de l'Image Docker

Nous utilisons une **"Fat Image"** : le même code est utilisé pour l'API, le Front et le Worker. Seule la commande de lancement change dans Kubernetes.

```bash
# Remplacer <votre-pseudo> par votre nom d'utilisateur Docker Hub
docker build -t <votre-pseudo>/ia-tp:latest .
docker login
docker push <votre-pseudo>/ia-tp:latest
```

## 2. Configuration de l'Environnement

1. **Activer Kubernetes** dans Docker Desktop (Settings > Kubernetes > Enable).
2. **Vérifier le contexte** :
```bash
kubectl config get-contexts
kubectl config use-context docker-desktop
```
3. **Installer KEDA** (L'autoscaler spécialisé pour les files de messages) :
```bash
kubectl apply --server-side -f https://github.com/kedacore/keda/releases/download/v2.13.0/keda-2.13.0.yaml
# Attendre que les pods soient "Running"
kubectl get pods -n keda
```
## 3. Déploiement de l'Infrastructure

Appliquez tous les fichiers de configuration dans l'ordre :

```bash
# Déployer la base (RabbitMQ, Redis, API, Worker, Front)
kubectl apply -f k8s/
```
Ou en appliquer d'un seul
```bash
# Activer l'Autoscaler KEDA
kubectl apply -f k8s/06_keda-autoscaler.yaml
```

## 4. Monitoring & Tests

Ouvrez 4 terminaux pour suivre le comportement du cluster :

* **T1 (Pods en direct) :** `kubectl get pods -w`
* **T2 (Interface Streamlit) :** `kubectl port-forward svc/streamlit-service 8501:8501`  
* **T3 (Dashboard Flower) :** `kubectl port-forward svc/flower-service 5555:5555` 
* **T4 (RabbitMQ Management) :** `kubectl port-forward svc/rabbitmq-service 15672:15672` 

---

## 5. Comprendre l'Autoscaling (KEDA)

### Pourquoi ça scale ?

Le fichier `06_keda-autoscaler.yaml` surveille la queue `celery` dans RabbitMQ.

* Si le nombre de messages en attente dépasse **3** (`value: "3"`), KEDA demande à Kubernetes de créer de nouveaux pods Workers.
* **CooldownPeriod (30s)** : C'est le temps que KEDA attend avant de décider de réduire le nombre de pods après que la file soit vide.
* **StabilizationWindow (300s)** : C'est une sécurité Kubernetes. Elle évite de supprimer des pods trop vite si une nouvelle vague de tâches arrive juste après la première (évite l'effet "yoyo").

### Point d'attention : La Concurrence

Dans le fichier `04_worker.yaml`, nous avons limité le worker :
`command: ["celery", "-A", "worker.app", "worker", "--concurrency=1"]`

**Pourquoi ?** Si un seul pod traite 10 tâches à la fois, KEDA ne verra jamais la file d'attente grandir et ne créera jamais de nouveaux pods. En limitant à 1 tâche par pod, on force la file à se remplir, ce qui déclenche l'autoscaling horizontal (plus de pods) au lieu de vertical (plus de threads).

---

## 🔍 Diagnostic Rapide

* **Vérifier l'autoscaler :** `kubectl get scaledobject`
* **Voir pourquoi ça ne scale pas :** `kubectl describe scaledobject worker-scaler`
* **Supprimer tout le projet :** `kubectl delete -f k8s/`

