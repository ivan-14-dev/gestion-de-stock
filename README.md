# ERP Gestion de Stock

Une plateforme professionnelle tout-en-un pour gérer un magasin de vêtements, développée avec PySide6 pour le desktop.

## Fonctionnalités

### Modules Principaux
- Gestion de Stock (implémenté)
- Suivi des ventes quotidiennes
- Gestion de la clientèle
- Analyse des performances produits
- Système de promotion et remises
- Gestion des commandes fournisseurs
- Calculateur de commissions
- Surveillance des prix concurrents
- Système de réservation en magasin
- Tableau de bord des indicateurs clés (KPI)

### Module Gestion de Stock
- Ajout, modification, suppression de produits
- Gestion des variantes (taille, couleur, quantité)
- Upload de photos
- Recherche et filtres avancés
- Import/Export CSV et JSON
- Dashboard avec graphiques interactifs Plotly (pie, bar, line, heatmap, doughnut, horizontal bar, timeline) avec zoom, pan et sélection
- Table de produits avec colonnes personnalisables
- Cartes de résumé avec indicateurs clés
- Alertes de stock faible

## Installation

1. Cloner le repo:
   ```bash
   git clone https://github.com/ivan-14-dev/gestion-de-stock.git
   cd gestion-de-stock
   ```

2. Installer les dépendances:
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

Lancer l'application:
```bash
python src/main.py
```

- Utilisez la sidebar pour naviguer entre les modules.
- Dans "Gestion de Stock", utilisez l'onglet "Table" pour gérer les produits et "Dashboard" pour voir les analyses.

## Structure du Projet

- `src/`: Code source
  - `main.py`: Point d'entrée
  - `models.py`: Modèles de données
  - `storage.py`: Gestion du stockage CSV/JSON
  - `stock_widget.py`: Interface du module stock
  - `dashboard_widget.py`: Dashboard avec graphiques
  - `add_product_dialog.py`: Dialogue d'ajout de produit
- `data/`: Données persistées
- `images/`: Images des produits
- `docs/`: Documentation

## Interface Utilisateur

- Style moderne SaaS avec palette de couleurs professionnelle
- Sidebar avec effets de survol et accents bleus
- Boutons de toolbar avec apparence moderne
- Contrôles de formulaire avec coins arrondis et états de focus
- Tables, onglets et boîtes de groupe avec bordures propres
- Graphiques stylisés avec Seaborn pour visualisations de données modernes
- Tous types de graphiques (ligne, barre, camembert, donut) avec couleurs professionnelles
- Cartes de résumé avec apparence de carte
- Polices système optimisées pour la compatibilité PyQt

## Technologies

- PySide6 (Qt pour Python)
- Pandas (manipulation CSV)
- Plotly (graphiques interactifs)
- JSON pour stockage local

## Développement Futur

- Intégration Django REST Framework pour le backend
- Applications Web (Next.js) et Mobile (Flutter)
- Synchronisation Firebase
- Modules supplémentaires

## Licence

MIT