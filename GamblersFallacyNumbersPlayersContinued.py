import pandas as pd

# Daten einlesen
data = pd.read_csv('DuneMaster.csv')

# Spieler, die ihr erstes Spiel verloren haben
players_lost_first_game = data.groupby('depositor').first()[data.groupby('depositor').first()['is_winner'] == 0]

# Gesamtzahl der Spiele für jeden Spieler
total_plays_per_player = data['depositor'].value_counts()

# Spieler, die weitergespielt haben
players_played_again = total_plays_per_player[total_plays_per_player.index.isin(players_lost_first_game.index) & (total_plays_per_player > 1)]

# Spieler, die aufgehört haben zu spielen
players_stopped_playing = total_plays_per_player[total_plays_per_player.index.isin(players_lost_first_game.index) & (total_plays_per_player == 1)]

# Anzahl der Spieler in beiden Kategorien
num_players_played_again = len(players_played_again)
num_players_stopped_playing = len(players_stopped_playing)

# Ausgabe der Ergebnisse
print(f"Anzahl der Spieler, die weitergespielt haben: {num_players_played_again}")
print(f"Anzahl der Spieler, die aufgehört haben zu spielen: {num_players_stopped_playing}")

