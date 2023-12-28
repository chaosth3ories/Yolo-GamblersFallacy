import pandas as pd
import matplotlib.pyplot as plt

# Daten einlesen
data = pd.read_csv('DuneMaster.csv')

# Ermittlung des ersten Spiels für jeden Spieler
first_games = data.groupby('depositor').first()

# Spieler, die ihr erstes Spiel verloren haben
players_lost_first_game = first_games[first_games['is_winner'] == 0].index

# Überprüfen, ob diese Spieler weitere Spiele gespielt haben
played_again = data[data['depositor'].isin(players_lost_first_game)].groupby('depositor').size() > 1

# Zählen, wie viele dieser Spieler weitergespielt haben und wie viele nicht
played_again_count = played_again.sum()
not_played_again_count = len(played_again) - played_again_count

# Daten für den Barchart
categories = ['Played Again', 'Not Played Again']
counts = [played_again_count, not_played_again_count]

# Erstellen des Barcharts
plt.figure(figsize=(8, 6))
plt.bar(categories, counts, color=['green', 'red'])
plt.title('Verhalten der Spieler nach dem Verlust des ersten Spiels')
plt.xlabel('Kategorie')
plt.ylabel('Anzahl der Spieler')
plt.show()
