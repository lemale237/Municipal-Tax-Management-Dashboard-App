# Municipal-Tax-Management-Dashboard-App
Interactive dashboard for real-time monitoring of municipal tax payments. Built with Flask (API), Dash (GUI) and Plotly (charts). Displays key metrics like paid/unpaid amounts, trends, campaign efficiency. Fetches data from Flask API connected to MySQL. Includes fake data generator. Auto-refreshes every 10 sec. Responsive design. 


# Tableau de bord de gestion des taxes municipales

Ce projet consiste en un tableau de bord pour la visualisation en temps réel des données de gestion des taxes municipales de la mairie de Douala 3ème.

## Aperçu du tableau de bord

Le tableau de bord affiche plusieurs graphiques et métriques pour suivre en temps réel :

- Montant total des taxes payées et impayées
- Nombre de taxes payées et impayées  
- Répartition des moyens de paiement
- Défauts de paiement par mois
- Taux de paiement par type de taxe
- Efficacité des campagnes de recouvrement
- Tendances des paiements et recouvrements
- Historique des paiements
- Localisation géographique des défauts de paiement

![Aperçu du tableau de bord](1.png)

## Fonctionnalités

Les principales fonctionnalités du tableau de bord sont :

- **Mise à jour en temps réel** : Les données sont récupérées en temps réel depuis l'API Flask pour fournir des métriques à jour.
- **Visualisations interactives** : Les graphiques sont construits avec Plotly et Dash pour permettre une expérience interactive (survol, zoom etc).
- **Design responsive** : Le tableau de bord s'adapte aux écrans desktop et mobile. 
- **Thème sombre** : L'interface utilise une palette de couleurs sombres pour un meilleur confort visuel.

## Technologies utilisées

- **Python** : Pour le script de génération de données factices, l'API Flask et le tableau de bord Dash.
- **MySQL** : Pour le stockage des données.
- **Flask** : Framework Python pour construire l'API REST.
- **Dash** : Bibliothèque Python pour créer des tableaux de bord web interactifs.
- **Plotly** : Bibliothèque JavaScript de graphiques pour la visualisation.
- **Bootstrap** : Framework CSS pour le style et la mise en page responsive.

## Installation

**Étape 1** : Cloner le dépôt GitHub

```bash
https://github.com/lemale237/Municipal-Tax-Management-Dashboard-App.git


**Étape 2** : Créer un environnement virtuel et installer les dépendances

```bash
cd tableau-bord-taxes-municipales
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt

**Étape 4** : Exécuter le script de génération de données factices

```bash
python script.py

