# Projet Nuage Interactif

Ce projet consiste à créer un nuage en coton accroché au plafond, équipé d'un Raspberry Pi, d'une bande LED WS2812, d'un microphone connecté en série et d'un haut-parleur. L'objectif est de lancer des animations lumineuses calmes et de déclencher une animation d'orage lorsque le microphone détecte une augmentation soudaine du volume sonore.

## Arborescence du projet 

├── animations_examples
│   ├── calm2.py
│   ├── calm3.py
│   ├── calm.py
│   ├── calm_threaded.py
│   ├── lightning.py
│   ├── raindrop.py
│   └── raindrop_threaded.py
├── bt_config_test
│   ├── autostartup.service
│   ├── bluetooth_setup.service
│   ├── bluetooth_setup.sh
│   ├── bt_conf.service
│   ├── client.py
│   └── cloudmain.service
├── leds_test
│   └── led_test.py
├── main
│   ├── animation_controller.py
│   ├── main.py
│   ├── rain.mp3
│   ├── sound_controller.py
│   ├── thunder.mp3
│   └── wind.mp3
├── mic_test
│   └── read_mic.py
├── sounds
│   ├── rain.mp3
│   ├── thunder.mp3
│   ├── wind.mp3
│   └── wind.wav
└── update.sh

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
