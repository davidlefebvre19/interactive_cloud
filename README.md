# Projet Nuage Interactif

Ce projet consiste à créer un nuage en coton accroché au plafond, équipé d'un Raspberry Pi, d'une bande LED WS2812, d'un microphone connecté en série et d'un haut-parleur. L'objectif est de lancer des animations lumineuses calmes et de déclencher une animation d'orage lorsque le microphone détecte une augmentation soudaine du volume sonore.

## Dépendances

Ce projet nécessite les bibliothèques Python suivantes :

- `threading`
- `pygame`
- `pydub`
- `socket`
- `time`
- `random`
- `numpy`
- `usb.core`
- `art`

## Installation et Configuration

1. **Cloner le dépôt :**
    ```sh
    git clone https://github.com/votre-utilisateur/projet-nuage-interactif.git
    cd projet-nuage-interactif
    ```

2. **Créer et activer un environnement virtuel :**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Installer les dépendances :**
    ```sh
    pip install pygame pydub numpy pyusb art
    ```

4. **Configurer les services systemd :**
    ```sh
    sudo cp bt_config_test/*.service /etc/systemd/system/
    sudo systemctl enable autostartup.service
    sudo systemctl enable bluetooth_setup.service
    sudo systemctl enable bt_conf.service
    sudo systemctl enable cloudmain.service
    ```

5. **Configurer et tester la bande LED :**
    ```sh
    sudo python leds_test/led_test.py
    ```

6. **Configurer et tester le microphone :**
    ```sh
    sudo python mic_test/read_mic.py
    ```

7. **Lancer le script principal :**
    ```sh
    sudo python main/main.py
    ```

## Utilisation

Le projet nuage interactif déclenchera des animations calmes par défaut. Lorsque le microphone détecte une augmentation soudaine du volume sonore, l'animation d'orage sera lancée avec des effets de lumière et de son correspondants.
