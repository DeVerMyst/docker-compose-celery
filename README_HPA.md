# img docker

docker build -t ia-tp:latest .

oui on a tout le code (api, front et worker) dans la meme image 
C'est une pratique très courante en production (appelée "Fat Image" ou "Mono-repository image") car cela garantit que l'API et le Worker utilisent exactement les mêmes versions des dépendances et du code métier.

# install KEDA

kubectl apply --server-side -f https://github.com/kedacore/keda/releases/download/v2.13.0/keda-2.13.0.yaml

kubectl get pods -n keda

# HPA

Configuration de l'Environnement ⚙️
Il faut activer le cluster Kubernetes intégré à Docker Desktop.

Ouvrez Docker Desktop.
Allez dans les Settings (⚙️) > Kubernetes.
Cochez Enable Kubernetes.
Cliquez sur Apply & Restart (le redémarrage peut prendre quelques minutes).
💡 Vérification : Assurez-vous que votre contexte est bien réglé sur le cluster local : kubectl config use-context docker-desktop

verification
config get-contexts

deploiement
kubectl apply -f k8s/

kubectl apply -f k8s/06_keda-autoscaler.yaml

kubectl get scaledobject

T1 : kubectl get pods -w
T2 : kubectl port-forward svc/streamlit-service 8501:8501
T3 : kubectl port-forward svc/flower-service 5555:5555
T4 : kubectl port-forward svc/rabbitmq-service 15672:15672

kubectl get scaledobject
kubectl describe scaledobject worker-scaler

attention

Le diagnostic : Ton worker est "trop musclé"
Regarde bien les noms des workers dans tes logs : ForkPoolWorker-3, ForkPoolWorker-12...
Cela signifie qu'un seul pod worker a ouvert au moins 12 processus en parallèle.

command: ["celery", "-A", "worker.app", "worker", "--loglevel=info", "--concurrency=1"]