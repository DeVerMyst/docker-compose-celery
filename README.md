# Architecture Distribuée pour le MLOps : Celery, Redis et RabbitMQ

Ce projet démontre l'utilisation de files d'attente de tâches asynchrones pour gérer des calculs lourds (simulations de modèles IA) via différentes infrastructures.

## Structure du Projet

* `main.py` : API FastAPI (Producteur) qui reçoit les requêtes et délègue les tâches.
* `worker.py` : Instance Celery (Consommateur) qui exécute les calculs de manière asynchrone.
* `app.py` : Interface Streamlit (Client) pour visualiser l'état des jobs en temps réel.
* `Dockerfile` : Image unique utilisée pour tous les services Python.

---

## Configuration 1 : Full Redis (Niveau Débutant)

Dans cette configuration, Redis assure deux rôles : le transport des messages (Broker) et le stockage des résultats (Backend).

```bash
docker compose -f docker-compose.redis.yml up --build

```

### Accès aux services

* **Streamlit** : `http://localhost:8501`
* **FastAPI Docs** : `http://localhost:8000/docs` (Utilisez ce point pour envoyer des requêtes manuellement).
* **Flower** : `http://localhost:5555` (Visualisation des jobs Celery).

Jouez directement depuis la **FastAPI Docs** et regardez ce qui se passe du **Flower**.

---

## Configuration 2 : Full RabbitMQ (Niveau Intermédiaire)

Ici, RabbitMQ remplace Redis. Les résultats sont gérés via le protocole RPC (`rpc://`).

```bash
docker compose -f docker-compose.rabbitmq.yml up --build

```

### Observation Importante

Les jobs apparaissent en succès dans Flower mais restent en statut "PENDING" dans Streamlit.

**Pourquoi ?**
RabbitMQ est un pur "Message Broker". En mode RPC, il crée des files temporaires pour les résultats. Si le client n'est pas connecté à l'instant précis du résultat ou si la file est purgée, l'information est perdue. Contrairement à Redis, il ne stocke pas les données de manière persistante par défaut.

**L'intérêt de RabbitMQ malgré cela :**

1. **Performance** : RabbitMQ traite jusqu'à 100 000 messages par seconde, là où Redis atteint ses limites sur des flux massifs.
2. **Robustesse (ACK)** : Si un Worker tombe en plein calcul, RabbitMQ détecte la rupture de connexion et réassigne immédiatement la tâche à un autre Worker.
3. **Priorisation** : Gestion fine de la priorité des messages et routage complexe (Exchanges).

---

## Configuration 3 : L'Architecture Optimale (Niveau Expert)

Cette version hybride utilise les forces respectives de chaque outil : **RabbitMQ pour le transport** (vitesse et sécurité) et **Redis pour le stockage** (persistance des résultats).

```bash
docker compose -f docker-compose.final.yml up --build

```

### Avantages de l'architecture hybride

* **Fiabilité** : Les messages d'entrée sont sécurisés par RabbitMQ.
* **Disponibilité** : Les résultats sont stockés durablement dans Redis, permettant à Streamlit de les récupérer n'importe quand.
* **Scalabilité** : Cette architecture supporte parfaitement la montée en charge horizontale.

---

## Scaling Horizontal (Mise à l'échelle)

Pour simuler une charge importante et augmenter la puissance de calcul, vous pouvez multiplier le nombre de Workers sans modifier le code.

**Note** : Assurez-vous que le service `worker` dans le fichier YAML ne possède pas de `container_name` fixe pour éviter les conflits de nommage.

```bash
docker compose -f docker-compose.final.yml up --scale worker=3 -d

```

### Vérification du scaling

1. Consultez **Flower** (`localhost:5555`) : 3 workers actifs apparaîtront.
2. Envoyez 10 requêtes via FastAPI : vous observerez la répartition des tâches (Round-Robin) entre les différents containers workers dans les logs Docker.

--- 



