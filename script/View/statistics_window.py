import tkinter as tk
from tkinter import Toplevel, messagebox
import os
import pandas as pd
from datetime import datetime, timedelta
import calendar

class StatisticsWindow:
    def __init__(self, root, csv_file):
        """Classe pour afficher les statistiques."""
        self.root = root
        self.csv_file = csv_file
        self.current_date = datetime.now()

        # Créer la fenêtre de statistiques
        self.window = Toplevel(root)
        self.window.title("Statistiques")
        self.window.geometry("900x700")  # Taille minimale augmentée à 600x600
        
        # ERRORS
        self.error_label = tk.Label(master=self.window, text="", font=("Arial", 14, "bold"))
        self.error_label.pack(pady=10)

        # Ajouter les flèches pour naviguer entre les mois
        self.previous_button = tk.Button(self.window, text="◄", command=self.show_previous_month)
        self.previous_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_button = tk.Button(self.window, text="►", command=self.show_next_month)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Afficher le nom du mois courant
        self.month_label = tk.Label(self.window, text=self.current_date.strftime("%B %Y"), font=("Arial", 16, "bold"))
        self.month_label.pack(pady=10)
      
        # Afficher un calendrier et les statistiques
        self.calendar_frame = tk.Frame(self.window)
        self.calendar_frame.pack(padx=10, pady=10)

        # Totaux en bas de la fenêtre
        self.total_month_label = tk.Label(self.window, text="", font=("Arial", 12, "bold"))
        self.total_month_label.pack(pady=10, padx=10)

        self.total_lifetime_label = tk.Label(self.window, text="", font=("Arial", 12, "bold"))
        self.total_lifetime_label.pack(pady=10)
        
        # Charger les statistiques depuis le fichier CSV et afficher les données
        self.load_statistics()

    def load_statistics(self):
        """Charger les statistiques depuis le fichier CSV et les afficher."""
        if not os.path.exists(self.csv_file):
            # messagebox.showerror("Erreur", "Fichier CSV introuvable")
            self.error_label.config(text="Please do a first session and come back here for your statistics", fg="red",)
        else:
            self.error_label.config(text="")

        # Lire le fichier CSV
        try:
            # Essayer de lire le fichier en UTF-8
            df = pd.read_csv(self.csv_file, encoding='utf-8')
        except UnicodeDecodeError:
            # Si une erreur survient, essayer de lire en ISO-8859-1 (latin-1)
            df = pd.read_csv(self.csv_file, encoding='ISO-8859-1')
        except:
            df = None

        # Transforming data
        if df is not None:
            df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
            df['Temps Passé sur Image'] = df['Temps Passé sur Image'].astype(float)

        # Extraire les données du mois courant
        month_start = self.current_date.replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        current_month_data = df[(df['Date'] >= month_start) & (df['Date'] < next_month)] if df is not None else None

        # Afficher le calendrier du mois
        self.show_calendar(current_month_data)

        # Calculer le total des heures du mois en cours
        total_seconds_month = current_month_data['Temps Passé sur Image'].sum() if df is not None else 0
        self.total_month_label.config(text=f"Total pour le mois : {self.format_time(total_seconds_month)}")

        # Calculer le total des heures pour toute la période de vie
        total_seconds_lifetime = df['Temps Passé sur Image'].sum() if df is not None else 0
        self.total_lifetime_label.config(text=f"Total pour toute la vie : {self.format_time(total_seconds_lifetime)}")

    def show_calendar(self, current_month_data):
        """Afficher le calendrier avec les heures passées par jour."""
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Créer un calendrier pour le mois courant (commençant par lundi)
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.current_date.year, self.current_date.month)

        # Ajouter les jours de la semaine en haut (commençant par lundi)
        days_of_week = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        for i, day in enumerate(days_of_week):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold"), width=10).grid(row=0, column=i)

        # Parcourir les semaines et jours dans le mois
        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day == 0:
                    continue  # Pas de jour (cases vides)

                # Créer un cadre pour chaque jour avec une bordure pour représenter la grille
                day_frame = tk.Frame(self.calendar_frame, highlightbackground="black", highlightthickness=1, width=80, height=80)
                day_frame.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

                # Afficher le numéro du jour dans le coin supérieur gauche
                day_label = tk.Label(day_frame, text=str(day), font=("Arial", 10), anchor="nw")
                day_label.place(x=5, y=5)

                # Extraire les données pour ce jour
                day_start = self.current_date.replace(day=day)
                day_end = day_start + timedelta(days=1)
                print(current_month_data)
                if current_month_data is None:
                    day_data = None
                else:
                    day_data = current_month_data[(current_month_data['Date'] >= day_start) &
                                              (current_month_data['Date'] < day_end)]

                # Calculer le total des heures pour ce jour
                total_seconds_day = day_data['Temps Passé sur Image'].sum() if day_data is not None else 0

                # Afficher le total des heures pour ce jour, ou rien s'il n'y a pas de données
                if total_seconds_day > 0:
                    formatted_time = self.format_time_compact(total_seconds_day)
                    hours_label = tk.Label(day_frame, text=formatted_time, font=("Arial", 12, "bold"), anchor="center")
                    hours_label.place(relx=0.5, rely=0.5, anchor="center")

    def show_previous_month(self):
        """Afficher le mois précédent dans le calendrier."""
        self.current_date = (self.current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        self.month_label.config(text=self.current_date.strftime("%B %Y"))
        self.load_statistics()

    def show_next_month(self):
        """Afficher le mois suivant dans le calendrier."""
        next_month = (self.current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        self.current_date = next_month
        self.month_label.config(text=self.current_date.strftime("%B %Y"))
        self.load_statistics()

    def format_time(self, seconds):
        """Convertit un temps en secondes en un format HH:MM:SS si supérieur à 1 heure, sinon MM:SS ou SS."""
        if seconds >= 3600:  # Plus de 1 heure
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            return f"{int(hours)}h {int(minutes)}min"
       
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{int(minutes)}min {int(seconds):02}sec"

    def format_time_compact(self, seconds):
        """Convertit un temps en secondes dans le format compact : "1h45"."""
        if seconds >= 3600:  # Plus d'une heure
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{int(hours)}h{int(minutes):02}"
        else:
            minutes = seconds // 60
            return f"{int(minutes)}min"


class StatisticsButton:
    def __init__(self, root, csv_file):
        self.root = root
        self.csv_file = csv_file

        # Créer le bouton avec l'icône de statistiques
        stats_button = tk.Button(root, text="📊 Statistiques", bg="gray", fg="white", command=self.open_stats_window)
        stats_button.pack(side=tk.RIGHT, pady=10, padx=10)

    def open_stats_window(self):
        """Ouvrir la fenêtre de statistiques."""
        StatisticsWindow(self.root, self.csv_file)
