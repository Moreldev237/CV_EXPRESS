# 🚀 CV_EXPRESS

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/DRF-3.14-089106?style=for-the-badge&logo=drf&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-Custom-FF6B6B?style=for-the-badge)

*Une solution moderne de génération de CV et lettres de motivation avec assistance intelligente.*

</div>

---

## 📋 Table des matières

- [À propos](#à-propos)
- [ Fonctionnalités](#-fonctionnalités)
- [🛠️ Stack technique](#🛠️-stack-technique)
- [⚡ Démarrage rapide](#⚡-démarrage-rapide)
- [📂 Structure du projet](#📂-structure-du-projet)
- [🔗 API Endpoints](#🔗-api-endpoints)
- [🤝 Contribution](#🤝-contribution)
- [📄 Licence](#📄-licence)
- [👨‍💻 Auteur](#👨‍💻-auteur)

---

## 📖 À propos

**CV_EXPRESS** est une application Web Django permettant de créer et gérer des CV professionnels et des lettres de motivation. Le projet intègre une assistance IA pour la génération automatique de contenu, la correction grammaticale et les suggestions d'amélioration.

### Fonctionnalités principales

- Création et gestion de CV professionnels
- Génération de lettres de motivation
- Assistance intelligente par IA
- Export PDF et DOCX
- Gestion de templates visuels
- API REST complète

---

## 🎯 Fonctionnalités

### Modules principaux

| Module | Description |
|--------|-------------|
| **👤 Users** | Inscription / Connexion (JWT), Gestion du profil, Upload photo de profil |
| **📄 CV Builder** | Création de CV, Sections (expériences, formations, compétences, langues, projets) |
| **✉️ Cover Letter** | Création de lettres,Génération automatique, Modèles personalize |
| **🤖 AI Assistant** | Génération CV/Lettres, Correction grammaticale, Suggestions d'amélioration |
| **🎨 Templates** | Templates de CV (moderne, classique, professionnel), Gestion des thèmes |
| **📤 Export** | Génération PDF (WeasyPrint), Génération DOCX, Partage via lien public |

### Fonctionnalités avancées

| Module | Description |
|--------|-------------|
| **💳 Subscription** | Gestion des abonnements (gratuit / premium), Paiement en ligne |
| **📊 Analytics** | Statistiques d'utilisation, Activité des utilisateurs |
| **🔔 Notifications** | Envoi d'emails, Notifications push, Alertes |
| **🎯 Job Match** | Matching compétences / offres, Recommandations personnalisées |

---

## 🛠️ Stack technique

| Catégorie | Technologie |
|-----------|-------------|
| **Backend** | ![Django](https://img.shields.io/badge/Django-4.2+-092E20) Django REST Framework |
| **Base de données** | PostgreSQL 15 |
| **Authentification** | JWT (Simple JWT) |
| **IA** | OpenAI API |
| **Export PDF** | WeasyPrint, ReportLab |
| **Frontend** | Flutter / React *(en option)* |

### Outils recommandés

```bash
# Backend
Django + DRF
PostgreSQL
Redis (cache)

# IA
OpenAI API
LangChain
```

---

## ⚡ Démarrage rapide

### Prérequis

- Python 3.11+
- PostgreSQL 15+
- Virtualenv

### Installation

```bash
# Cloner le projet
git clone https://github.com/MORELDEV237/CV_EXPRESS.git
cd CV_EXPRESS

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Migrer la base de données
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

### Configuration

```bash
# Variables d'environnement recommandées
export SECRET_KEY=your_secret_key
export DEBUG=True
export DB_NAME=cv_express_db
export DB_USER=postgres
export DB_PASSWORD=your_password
export OPENAI_API_KEY=your_api_key
```

### Accès

- Serveur local: `http://127.0.0.1:8000`
- Admin Django: `http://127.0.0.1:8000/admin`
- API: `http://127.0.0.1:8000/api/`

---

## 📂 Structure du projet

```
CV_EXPRESS/
├── CV_EXPRESS/          # Configuration Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/               # Gestion des utilisateurs
├── cv_builder/          # Création de CV
├── cover_letter/        # Lettres de motivation
├── ai_assistant/        # Assistance IA
├── templates/           # Modèles visuels
├── export/              # Export PDF/DOCX
├── subscription/       # Abonnements (optionnel)
├── analytics/          # Statistiques
├── notifications/      # Notifications
└── job_match/         # Matching emploi (bonus)
```

---

## 🔗 API Endpoints

### Authentication

| Endpoint | Méthode | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Inscription |
| `/api/auth/login/` | POST | Connexion |
| `/api/auth/refresh/` | POST | Rafraîchir token |
| `/api/auth/logout/` | POST | Déconnexion |

### Utilisateurs

| Endpoint | Méthode | Description |
|----------|--------|-------------|
| `/api/users/profile/` | GET/PUT | Profil utilisateur |
| `/api/users/avatar/` | POST | Upload photo |

### CV

| Endpoint | Méthode | Description |
|----------|--------|-------------|
| `/api/cv/` | GET/POST | Liste/Créer CV |
| `/api/cv/{id}/` | GET/PUT/DELETE | Détails/Modifier/Supprimer |
| `/api/cv/{id}/export/` | GET | Exporter en PDF |

### Lettres de motivation

| Endpoint | Méthode | Description |
|----------|--------|-------------|
| `/api/letters/` | GET/POST | Liste/Créer lettre |
| `/api/letters/{id}/` | GET/PUT/DELETE | Détails/Modifier/Supprimer |

### IA

| Endpoint | Méthode | Description |
|----------|--------|-------------|
| `/api/ai/generate-cv/` | POST |Générer CV |
| `/api/ai/generate-letter/` | POST | Générer lettre |
| `/api/ai/improve/` | POST | Améliorer contenu |

### Templates

| Endpoint | Méthode | Description |
|----------|--------|-------------|
| `/api/templates/` | GET | Liste templates |
| `/api/templates/{id}/` | GET | Détails template |

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :

1. **Forker** le projet
2. **Créer** une branche (`git checkout -b feature/AmazingFeature`)
3. **Committer** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Pusher** sur la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### Bonnes pratiques

- Suivre le style de code PEP 8
- Écrire des tests unitaires
- Documenter les nouvelles fonctionnalités
- Vérifier que le code passe les tests

---

## 📄 Licence

Ce projet est sous licence personnalisée. Voir le fichier [license](license) pour plus de détails.

---

## 👨‍💻 Auteur

<div align="center">

**MORELDEV237**

*Développeur Full Stack & Créateur de solutions modernes*

[![GitHub](https://img.shields.io/badge/GitHub-MORELDEV237-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/MORELDEV237)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-MORELDEV237-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/moreldev237)
[![Email](https://img.shields.io/badge/Email-moreldev237@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:moreldev237@gmail.com)

</div>

---

<div align="center">

⭐⭐⭐ Merci pour votre intérêt ! N'hésitez pas à mettre une étoile si le projet vous plait.

</div>
