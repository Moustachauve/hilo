[![Français][Françaisshield]][Français]
[![English][Englishshield]][English]

[![hacs][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![Project Maintenance][maintenance-shield]][user_profile]
[![License][license-shield]][license]
[![pre-commit][pre-commit-shield]][pre-commit]
[![black][black-shield]][black]
[![calver][calver-shield]][calver]
[![discord][discord-shield]][discord]


**BETA**

Ceci est une version Bêta. Il y aura probablement des bogues, irritants, etc. Merci pour votre patience et d'ouvrir des "Issues".

# Hilo - Home Assistant
Intégration pour Home Assistant d'[Hilo](https://www.hiloenergie.com/fr-ca/)

# ⚠️ Changement majeur à venir, merci de garder votre component à jour ⚠️

L'API sur laquelle nous comptons pour les défis Hilo sera fermée prochainement. Nous travaillons actuellement sur une
alternative utilisant Websocket/SignalR. **La mise à jour vers la version 2025.2.1 ou ultérieur est fortement recommandée**, car
les versions précédentes risquent de ne plus fonctionner en raison de la façon dont pip installe les dépendances.

Plusieurs utilisateurs et moi-même sommes en train de migrer nos communications avec l'API Hilo vers Websocket/SignalR
plutôt que des appels d'API. Le procéssus se fera graduellement et nous ferons tout ce qu l'on peut pour éviter de
briser des installations existantes.

Dans un premier temps, nous mettrons à jour la librairie `python-hilo` (https://github.com/dvd-dev/python-hilo),
ce changement devrait être transparent pour tous.

Ensuite, nous migrerons le capteur de défi (`sensor.defi_hilo`) vers Websocket/SignalR. La bonne nouvelle avec ça c'est
que les "glitchs" momentanés du capteur de défi sont complètement éliminés par cette méthode.

### Ce qui reste à faire de ce côté:
- Les attributs `allowed_kWh` et `used_kWh` sont **non-fonctionnels** actuellement, les information arrivent morcelées et tous
les cas ne sont pas traités encore.
- L'état "completed" ne fonctionne pas toujours, possiblement un race condition
- Certaines informations comme `total_devices`, `opt_out_devices` et `pre_heat_devices` ne persistent pas en mémoire.

Plus de détails disponibles dans [issue #486](https://github.com/dvd-dev/hilo/issues/486).

L'API servant à la lecture initial de la liste d'appareils sur votre compte Hilo subira également le même traitement.

Plus de détails disponibles dans [issue #564](https://github.com/dvd-dev/hilo/issues/564).

## 📌 Introduction
Cette intégration non-officielle HACS permet d'utiliser [Hilo](https://www.hiloenergie.com/fr-ca/) avec Home Assistant. **Elle n'est pas affiliée à Hilo ou Hydro-Québec.**  

**⚠️ Ne contactez pas Hilo ou Hydro-Québec pour les problèmes liés à cette intégration.**

🔗 [Configuration minimale recommandée](https://github.com/dvd-dev/hilo/wiki/FAQ-%E2%80%90-Français#avez-vous-une-configuration-recommandée)  
🔗 Blueprints : [NumerID](https://github.com/NumerID/blueprint_hilo) | [Arim215](https://github.com/arim215/ha-hilo-blueprints)  
🔗 Exemples d'automatisations YAML : [Automatisations](https://github.com/dvd-dev/hilo/tree/main/doc/automations)  
🔗 Exemples d'interfaces Lovelace : [Interfaces](https://github.com/dvd-dev/hilo/wiki/Utilisation)  

---

## 🔥 Fonctionnalités principales
✅ Supporte les interrupteurs et gradateurs comme lumières  
✅ Contrôle des thermostats et lecture des températures  
✅ Suivi de la consommation énergétique des appareils Hilo  
✅ Sensor pour les défis et la passerelle Hilo  
✅ Configuration via l'interface utilisateur  
✅ Authentification via le site web d'Hilo  
✅ Capteur météo extérieure avec icône changeante  

📌 **À faire** : Support d'autres appareils, amélioration des compteurs de consommation, documentation API

---

## 📥 Installation
### 1️⃣ Vérifier la compatibilité
- L'intégration nécessite le matériel Hilo installé et fonctionnel.
- Testée sous HA OS, Docker (ghcr.io), Podman. D'autres configurations peuvent poser problème.

### 2️⃣ Installation des fichiers
#### 🔹 Option 1 : Via HACS
[![Installer via HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dvd-dev&repository=hilo&category=integration)

1. Assurez-vous d'avoir [HACS](https://hacs.xyz/docs/setup/download/) installé.
2. Dans HACS, cliquez sur `+ EXPLORE & DOWNLOAD REPOSITORIES`, recherchez "Hilo" et téléchargez-le.
3. Redémarrer Home Assistant

#### 🔹 Option 2 : Manuellement
1. Téléchargez la dernière version depuis [GitHub](https://github.com/dvd-dev/hilo/releases/latest).
2. Copiez `custom_components/hilo` dans le dossier `custom_components` de Home Assistant.
3. Redémarrer Home Assistant

### 3️⃣ Ajouter l'intégration à Home Assistant
[![Ajouter l'intégration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=hilo)

1. Allez à **Paramètres > Appareils et services > Intégrations**.
2. Cliquez sur `+ AJOUTER UNE INTÉGRATION` et recherchez "Hilo".
3. Authentifiez-vous sur le site web d'Hilo et liez votre compte.

---

## 📌 Suivis de la consommation électrique
Si vous souhaitez utiliser la génération automatique des capteurs de consommation électrique, suivez ces étapes :

1. **Ajouter la plateforme `utility_meter`**  
   Ajoutez la ligne suivante dans votre fichier `configuration.yaml` :
   ```yaml
   utility_meter:
   ```

2. **Activer la génération automatique**  
   - Dans l'interface utilisateur de l'intégration, cliquez sur `Configurer`.
   - Cochez **Générer compteurs de consommation électrique**.

3. *(Optionnel)* **Redémarrer Home Assistant**  
   - Attendez environ 5 minutes. L'entité `sensor.hilo_energy_total_low` sera créée et contiendra des données.
   - **Le `status`** devrait être `collecting`.
   - **L'état `state`** devrait être un nombre supérieur à 0.
   - Toutes les entités et capteurs créés seront préfixés ou suffixés par `hilo_energy_` ou `hilo_rate_`.

4. **Erreur connue (à ignorer)**  
   Si vous voyez cette erreur dans le journal de Home Assistant, elle peut être ignorée :
   ```
   2021-11-29 22:03:46 ERROR (MainThread) [homeassistant] Error doing job: Task exception was never retrieved
   Traceback (most recent call last):
   [...]
   ValueError: could not convert string to float: 'None'
   ```

5. **Ajout manuel au tableau de bord "Énergie"**  
   Une fois créés, les compteurs devront être ajoutés manuellement.

---

## ⚠️ Avertissement
Lorsque l'on active les compteurs, il est recommandé de **retirer les anciens capteurs manuels** afin d'éviter des données en double.

Si vous rencontrez un problème et souhaitez collaborer, activez la journalisation **debug** et fournissez un extrait du fichier `home-assistant.log`. La méthode est expliquée ci-dessous.

---

## ⚙️ Autres options de configuration
Vous pouvez configurer des options supplémentaires en cliquant sur `Configurer` dans Home Assistant :
![alt text](image.png)
### ✅ **Générer compteurs de consommation électrique**
- Génère automatiquement les compteurs de consommation électrique.
- **Nécessite** la ligne suivante dans `configuration.yaml` :
  ```yaml
  utility_meter:
  ```

### ✅ **Générer seulement les compteurs totaux pour chaque appareil**
- Calcule uniquement le total d'énergie **sans division** entre coût faible et coût élevé.

### ✅ **Enregistrer les données de demande et les messages Websocket**
- Nécessite un **niveau de journalisation `debug`** sur l'intégration et `pyhilo`.
- Permet un suivi détaillé pour le développement et le débogage.

### ✅ **Verrouiller les entités `climate` lors des défis Hilo**
- Empêche toute modification des consignes de température **pendant un défi** Hilo.

### ✅ **Suivre des sources de consommation inconnues dans un compteur séparé**
- Toutes les sources **non Hilo** sont regroupées dans un capteur dédié.
- Utilise la lecture du **compteur intelligent** de la maison.

### 📌 **Nom du tarif Hydro-Québec** (`rate d` ou `flex d`)
- Définissez le **nom du plan tarifaire**.
- **Valeurs supportées** :
  - `'rate d'`
  - `'flex d'`

### ⏳ **Intervalle de mise à jour (min : 60s)**
- Définit le **nombre de secondes** entre chaque mise à jour.
- **Valeur par défaut** : `60s`.
- **Ne pas descendre sous 30s** pour éviter une suspension de Hilo.
- Depuis **2023.11.1**, le minimum est passé de **15s à 60s**.


## 📌 FAQ et support
🔗 [FAQ complète](https://github.com/dvd-dev/hilo/wiki/FAQ)  
💬 Rejoignez la communauté sur [Discord](https://discord.gg/MD5ydRJxpc)

**Problèmes ?** Ouvrez une "Issue" avec les logs `debug` activés dans `configuration.yaml` :
```yaml
logger:
  default: info
  logs:
     custom_components.hilo: debug
     pyhilo: debug
```

---

# 🤝 Contribuer  

Rapporter tout problème est une excellente manière pour tous de contribuer au projet.  

Si vous rencontrez des problèmes ou observez des comportements étranges, veuillez soumettre une "Issue" en y joignant vos journaux.  

## 📜 Activer la journalisation de débogage  
Pour activer la journalisation de débogage, ajoutez ceci dans votre fichier `configuration.yaml` :  

```yaml
logger:
  default: info
  logs:
    custom_components.hilo: debug
    pyhilo: debug
```

Si vous avez de l'expérience en Python ou avec Home Assistant et souhaitez contribuer au code, n'hésitez pas à soumettre une pull request.  

---

# 🛠️ Préparer un environnement de développement via VSCode DevContainer  

Pour faciliter le développement, un environnement est disponible via DevContainer de VSCode. Assurez-vous d'avoir **VSCode** et **Docker** installés sur votre ordinateur.  

1. Ouvrez le dossier du projet dans VSCode.  
2. Installez l'extension **Remote - Containers**.  
3. Ouvrez la palette de commandes (**Ctrl+Shift+P** ou **Cmd+Shift+P**) et recherchez :  
   ```
   Remote-Containers: Reopen in Container
   ```
4. Attendez que l'environnement soit prêt.  
5. Ouvrez un terminal dans VSCode et exécutez :  
   ```bash
   scripts/develop
   ```
   pour installer les dépendances et lancer Home Assistant.  
6. VSCode devrait vous proposer d'ouvrir un navigateur pour accéder à Home Assistant. Sinon, ouvrez manuellement :  
   ```
   http://localhost:8123
   ```
7. Effectuez la configuration initiale de Home Assistant.  
8. Ajoutez l'intégration **Hilo** via l'interface utilisateur.  
9. Modifiez les fichiers dans le dossier `custom_components/hilo` et observez les changements en temps réel dans Home Assistant.  

Dans le terminal où vous avez lancé `scripts/develop`, les journaux de Home Assistant et de l'intégration Hilo devraient défiler.  

---

# ✅ Avant de soumettre une Pull Request  

Il est essentiel de tester vos modifications sur une installation locale. Vous pouvez modifier les fichiers `.py` de l'intégration directement dans votre dossier `custom_components/hilo`.  

⚠ **N'oubliez pas votre copie de sauvegarde!**  

Si vous devez modifier `python-hilo` pour vos tests, installez votre fork avec la commande suivante dans votre CLI :  

```bash
pip install -e git+https://github.com/VOTRE_FORK_ICI/python-hilo.git#egg=python-hilo
```

Redémarrez ensuite Home Assistant pour que l'installation prenne effet. Pour revenir en arrière :  

```bash
pip install python-hilo
```

Puis redémarrez Home Assistant.  

---

# 🚀 Soumettre une Pull Request  

1. **Créez un fork** du dépôt dans votre espace utilisateur.  
2. **Clonez-le** sur votre ordinateur.  
3. Pour maintenir une certaine standardisation du code, nous utilisons des **linters** et des **validateurs** exécutés via des hooks `pre-commit` :  

   ```bash
   pre-commit install --install-hooks
   ```

4. Apportez vos modifications au code.  
5. Une fois terminé, ajoutez les fichiers modifiés :  

   ```bash
   git add path/to/file
   ```

6. Créez un commit :  

   ```bash
   git commit -m "J'ai changé ceci parce que ..."
   ```

7. Poussez les changements vers votre dépôt distant :  

   ```bash
   git push
   ```

8. Sur le dépôt d'origine, **GitHub** devrait vous proposer de créer une **Pull Request** (PR). Suivez les instructions.  

---

# 👥 Collaborateurs initiaux  

- **[Francis Poisson](https://github.com/francispoisson/)**  
- **[David Vallee Delisle](https://github.com/valleedelisle/)**  

## 🎖️ Mentions très honorables  

- **[Ian Couture](https://github.com/ic-dev21/)** : Il maintient cet addon depuis un certain temps.  
- **[Hilo](https://www.hiloenergie.com)** : Merci à Hilo pour son soutien et ses contributions.  

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[commits-shield]: https://img.shields.io/github/commit-activity/y/dvd-dev/hilo.svg?style=for-the-badge
[commits]: https://github.com/dvd-dev/hilo/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[license]: https://github.com/dvd-dev/hilo/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/dvd-dev/hilo.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40dvd--dev-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/dvd-dev/hilo.svg?style=for-the-badge
[releases]: https://github.com/dvd-dev/hilo/releases
[user_profile]: https://github.com/dvd-dev
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[calver-shield]: https://img.shields.io/badge/calver-YYYY.MM.Micro-22bfda.svg?style=for-the-badge
[calver]: http://calver.org/
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[black]: https://github.com/psf/black
[discord-shield]: https://img.shields.io/badge/discord-Chat-green?logo=discord&style=for-the-badge
[discord]: https://discord.gg/MD5ydRJxpc
[Englishshield]: https://img.shields.io/badge/en-English-red?style=for-the-badge
[English]: https://github.com/dvd-dev/hilo/blob/main/README.en.md
[Françaisshield]: https://img.shields.io/badge/fr-Français-blue?style=for-the-badge
[Français]: https://github.com/dvd-dev/hilo/blob/main/README.md
