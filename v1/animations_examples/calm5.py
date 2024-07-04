from rpi_ws281x import Adafruit_NeoPixel, Color
import random
import time

# Configuration des LED
PIN = 12
NUM_LEDS = 50
BRIGHTNESS = 255
DELAY = 0.02
NUM_SECTIONS = 5

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

def random_brightness():
    """Génère une luminosité aléatoire pour une section."""
    return random.randint(0, BRIGHTNESS)

def fade_in_out(section_index):
    """Fait un effet fade-in ou fade-out pour une section donnée."""
    start_brightness = random_brightness()
    end_brightness = random_brightness()
    steps = random.randint(10, 50)  # Nombre aléatoire d'étapes pour l'effet fade

    # Fade-in
    for i in range(steps):
        brightness = int(start_brightness + (end_brightness - start_brightness) * (i / steps))
        set_section_brightness(section_index, brightness)
        strip.show()
        time.sleep(DELAY)

    # Fade-out
    for i in range(steps):
        brightness = int(end_brightness + (start_brightness - end_brightness) * (i / steps))
        set_section_brightness(section_index, brightness)
        strip.show()
        time.sleep(DELAY)

def set_section_brightness(section_index, brightness):
    """Allume une section avec une luminosité spécifiée."""
    section_size = NUM_LEDS // NUM_SECTIONS
    start_led = section_index * section_size
    end_led = min(start_led + section_size, NUM_LEDS)

    for i in range(start_led, end_led):
        strip.setPixelColor(i, Color(brightness, brightness, brightness))

def animate():
    while True:
        # Choisir une section aléatoire
        section_index = random.randint(0, NUM_SECTIONS - 1)

        # Choisir aléatoirement entre fade-in et fade-out
        fade_type = random.choice(["in", "out"])

        if fade_type == "in":
            fade_in_out(section_index)
        else:
            fade_in_out(section_index)

try:
    animate()
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()