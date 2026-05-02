# 🚀 Guide de lancement des services CV_EXPRESS

Pour faire fonctionner l'intégralité du backend (API, Notifications asynchrones, et Analytics), vous devez ouvrir plusieurs terminaux.

## Pre-requis
Assurez-vous que votre environnement virtuel est activé dans chaque nouveau terminal :
```bash
source venv/bin/activate
```

---

## 1. Terminal : Serveur d'API (Django)
Lance le serveur de développement principal.
```bash
python manage.py migrate
python manage.py runserver
```
**Accès :** [http://127.0.0.1:8000/api/schema/docs/](http://127.0.0.1:8000/api/schema/docs/)

## 2. Terminal : Broker de messages (Redis)
Indispensable pour Celery. Si vous avez Redis installé localement :
```bash
redis-server
```
*Si vous préférez Docker : `docker run -d -p 6379:6379 redis`*

## 3. Terminal : Worker Celery
Gère l'envoi des emails et des notifications en arrière-plan.
```bash
celery -A CV_EXPRESS worker --loglevel=info
```

## 4. Terminal : Monitoring Celery (Flower) - *Optionnel*
Interface web pour surveiller les tâches asynchrones.
```bash
celery -A CV_EXPRESS flower
```
**Accès :** http://localhost:5555

---
**Note :** Vérifiez bien que votre fichier `.env` contient les accès à la base de données et les clés API (OpenAI, Email SMTP) avant de commencer.