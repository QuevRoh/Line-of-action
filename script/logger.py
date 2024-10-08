import os
import csv
from datetime import datetime

def log_to_csv(file_path, image_time_spent, session_initial_time, session_mode):
    """Enregistre les données de la session dans un fichier CSV."""
    # En-têtes du fichier CSV
    headers = ['Date', 'Temps Passé sur Image', 'Temps Initial de la Session', 'Mode de la Session']

    # Vérifier si le fichier existe déjà
    file_exists = os.path.exists(file_path)

    # Créer le fichier ou vérifier les en-têtes s'il existe
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            # Si le fichier n'existe pas, écrire les en-têtes
            writer.writerow(headers)
        else:
            # Si le fichier existe, vérifier les en-têtes
            with open(file_path, mode='r') as read_file:
                reader = csv.reader(read_file)
                first_line = next(reader, None)
                if first_line != headers:
                    # Écraser le fichier avec les bonnes en-têtes
                    file.truncate(0)  # Effacer le fichier existant
                    writer.writerow(headers)

        # Enregistrer la ligne
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         f"{image_time_spent:.2f}",
                         f"{session_initial_time / 60:.2f} minutes",
                         session_mode])