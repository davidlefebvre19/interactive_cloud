import os
import subprocess
import time


def play_sound_for_duration(subfolder, file_name, duration):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        audio_file = os.path.join(script_dir, subfolder, file_name)

        process = subprocess.Popen(['sudo', 'aplay', audio_file])

        time.sleep(duration)

        process.terminate()

    except Exception as e:
        print(f"Erreur lors de la lecture du fichier audio : {e}")


if __name__ == "__main__":
    # Nom du sous-dossier où se trouve le fichier audio
    subfolder = 'subdir'  # Sous-dossier "sounds"

    # Nom du fichier audio
    file_name = 'thunder_16bit.wav'

    play_duration = 5  # Durée en secondes

    # Appel de la fonction pour jouer le son pendant une durée spécifiée
    play_sound_for_duration(subfolder, file_name, play_duration)