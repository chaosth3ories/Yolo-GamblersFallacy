import pandas as pd
import matplotlib.pyplot as plt

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

# Erstellen des Boxplots
plt.figure(figsize=(10, 6))
plt.boxplot(play_counts, vert=False)

# Skalierung der x-Achse, um nur bis zu 2000 Spiele anzuzeigen
plt.xlim(0, 150)

plt.title('Anzahl der Spiele von Spielern, die ihr erstes Spiel verloren haben (bis zu 150 Spiele)')
plt.xlabel('Anzahl der Spiele')
plt.show()
