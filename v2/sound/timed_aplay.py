import subprocess
import time


def play_sound_for_duration(file_path, duration):
    try:
        # Lancer aplay en arrière-plan
        process = subprocess.Popen(['sudo', 'aplay', file_path])

        # Attendre la durée spécifiée
        time.sleep(duration)

        # Arrêter aplay après la durée spécifiée
        process.terminate()

    except Exception as e:
        print(f"Erreur lors de la lecture du fichier audio : {e}")


if __name__ == "__main__":
    # Spécifie le fichier audio et la durée
    audio_file = 'wind_16bit.wav'  # Chemin vers ton fichier audio
    play_duration = 5  # Durée en secondes

    # Appel de la fonction pour jouer le son pendant une durée spécifiée
    play_sound_for_duration(audio_file, play_duration)