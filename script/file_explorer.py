import subprocess

def open_csv_in_explorer(file_path):
    """Ouvre le fichier CSV dans l'explorateur de fichiers ou Finder."""
    if os.name == 'nt':  # Windows
        os.startfile(file_path)
    elif os.name == 'posix':  
        subprocess.call(['open', file_path])  # Pour macOS
        subprocess.call(['xdg-open', file_path]) # Pour Linux