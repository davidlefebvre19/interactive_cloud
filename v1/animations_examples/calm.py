from rpi_ws281x import *
import time

# Configuration des LED
PIN = 12
NUM_LEDS = 50
BRIGHTNESS = 255
NOMBRE_HALO = 5
HALO_SIZE = 7
FADE_STEP = 5
DELAY = 0.001

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()


def fade_to_brightness(led_index, target_brightness, fade_step=FADE_STEP):
    # Récupérer la couleur actuelle et extraire la composante de luminosité
    current_color = strip.getPixelColor(led_index)
    current_brightness = (current_color & 0xff0000) >> 16  # Extrait la composante rouge comme luminosité

    while current_brightness != target_brightness:
        if current_brightness < target_brightness:
            current_brightness = min(current_brightness + fade_step, target_brightness)
        else:
            current_brightness = max(current_brightness - fade_step, target_brightness)

        strip.setPixelColor(led_index, Color(current_brightness, current_brightness, current_brightness))
        strip.show()
        time.sleep(0.01)


def move_halo():
    positions = [-HALO_SIZE] * NOMBRE_HALO  # Positions initiales des halos

    while True:
        # Parcourir chaque halo
        for i in range(NOMBRE_HALO):
            # Position actuelle du halo
            current_position = positions[i]

            # Éteindre les LEDs derrière le halo
            for j in range(HALO_SIZE):
                led_to_turn_off = (current_position + j - HALO_SIZE) % NUM_LEDS
                fade_to_brightness(led_to_turn_off, 0)

            # Mettre à jour la position du halo
            positions[i] = (positions[i] + 1) % NUM_LEDS

            # Allumer les LEDs pour le halo actuel
            for j in range(HALO_SIZE):
                led_to_light = (positions[i] + j) % NUM_LEDS
                fade_to_brightness(led_to_light, BRIGHTNESS)

        # Mettre à jour l'affichage de la bande LED
        strip.show()
        time.sleep(DELAY)


try:
    move_halo()
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()