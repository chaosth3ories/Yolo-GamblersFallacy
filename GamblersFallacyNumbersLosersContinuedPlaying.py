import pandas as pd

# Daten einlesen
data = pd.read_csv('DuneMaster.csv')

# Ermittlung des ersten Spiels für jeden Spieler
first_games = data.groupby('depositor').first()

# Spieler, die ihr erstes Spiel verloren haben
players_lost_first_game = first_games[first_games['is_winner'] == 0].index

# Daten der Spieler filtern, die ihr erstes Spiel verloren haben
lost_first_game_data = data[data['depositor'].isin(players_lost_first_game)]

# Zählen, wie oft diese Spieler insgesamt gespielt haben
play_counts = lost_first_game_data.groupby('depositor').size()

# Berechnung von Quartilen, Minimum, Maximum, Median und Standardabweichung
quartiles = play_counts.quantile([0.25, 0.5, 0.75])
minimum = play_counts.min()
maximum = play_counts.max()
median = play_counts.median()
std_dev = play_counts.std()

# Ausgabe der Ergebnisse
print(f"Quartile: \n{quartiles}")
print(f"Minimum: {minimum}")
print(f"Maximum: {maximum}")
print(f"Median: {median}")
print(f"Standardabweichung: {std_dev}")
