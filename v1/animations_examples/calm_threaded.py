from rpi_ws281x import *
import time
import threading

# Configuration des LED
HALO_SIZE = 3  # Taille de chaque halo
NUM_LEDS = 17
BRIGHTNESS = 255
FADE_STEP = 5  # Incrément pour le fondu
DELAY = 0.05   # Délai entre chaque mise à jour d'animation

# Initialisation de la bande de LEDs
#strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
#strip.begin()

# Luminosité actuelle de chaque LED
current_brightness = [0] * NUM_LEDS
lock = threading.Lock()

def fade_led(strip,led_index, target_brightness, fade_step):
    """ Fondu pour une LED spécifique. """
    #print("currently in fade led")
    global current_brightness
    start_brightness = current_brightness[led_index]
    step = fade_step if target_brightness > start_brightness else -fade_step

    for brightness in range(start_brightness, target_brightness, step):
        with lock:
            current_brightness[led_index] = brightness
            strip.setPixelColor(led_index, Color(brightness, brightness, brightness))
            strip.show()
        time.sleep(0.01)

def move_halo(strip,start_led, halo_size):
    """ Déplace le halo le long de la bande de LEDs. """
    end_led = start_led + halo_size
    for i in range(start_led, end_led):
        if 0 <= i < NUM_LEDS:
            target_brightness = BRIGHTNESS if i < end_led - 1 else 0
            threading.Thread(target=fade_led, args=(strip, i, target_brightness, FADE_STEP)).start()
            time.sleep(DELAY)

def run_calm_animation(stop_event, strip):
    print("CALM ANIMATION THREAD")
    current_led = 0
    while not stop_event.is_set():
        print("currently calm...")
        move_halo(strip,current_led, HALO_SIZE)
        current_led = (current_led + 1) % NUM_LEDS
        time.sleep(0.05)  # Vous pouvez ajuster cette valeur si nécessaire

    # Éteindre toutes les LEDs à l'arrêt
    with lock:
        print("calm animation end !")
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

if __name__ == "__main__":
    run_calm_animation()