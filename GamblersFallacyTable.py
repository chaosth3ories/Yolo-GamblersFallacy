import pandas as pd

# Laden der Daten aus der hochgeladenen Datei
data = pd.read_csv('DuneMaster.csv')

# Schritt 1 & 2: Berechnen des durchschnittlichen Einsatzes vor dem ersten Verlust und Identifizieren von Spielern, die ihren Einsatz nach einem Verlust erhöht haben

# Filtern der Spieler, die mindestens einmal verloren haben
losers = data[data['is_winner'] == 0]

# Gruppieren nach Einzahler, um den ersten Verlust zu finden
first_losses = losers.groupby('depositor').first().reset_index()

# Zusammenführen, um alle Zeilen vor dem ersten Verlust für jeden Verlierer zu erhalten
merged_data = pd.merge(data, first_losses[['depositor', 'block_number']], on='depositor', how='left', suffixes=('', '_first_loss'))
before_first_loss = merged_data[merged_data['block_number'] < merged_data['block_number_first_loss']]

# Berechnung des durchschnittlichen Einsatzes vor dem ersten Verlust
avg_deposit_before_loss = before_first_loss.groupby('depositor')['deposit_eth'].mean().reset_index()
avg_deposit_before_loss.rename(columns={'deposit_eth': 'avg_deposit_before_loss'}, inplace=True)

# Zusammenführen des durchschnittlichen Einsatzes mit den Hauptdaten
data_with_avg_loss = pd.merge(data, avg_deposit_before_loss, on='depositor', how='left')

# Ermittlung des Einsatzes in der ersten Runde nach dem Verlust
data_with_avg_loss['next_round_deposit'] = data_with_avg_loss.groupby('depositor')['deposit_eth'].shift(-1)

# Identifizierung von Spielern, die ihren Einsatz nach einem Verlust erhöht haben
data_with_avg_loss['increased_bet_after_loss'] = (data_with_avg_loss['deposit_eth'] == data_with_avg_loss['next_round_deposit']) & \
                                                 (data_with_avg_loss['next_round_deposit'] > data_with_avg_loss['avg_deposit_before_loss']) & \
                                                 (data_with_avg_loss['is_winner'] == 0)

# Schritt 3: Hinzufügen einer Spalte 'Gamblers Fallacy', um diese Spieler zu markieren
data_with_avg_loss['gamblers_fallacy'] = data_with_avg_loss['increased_bet_after_loss'].apply(lambda x: 1 if x else 0)

# Schritt 4: Berechnung der Gesamtanzahl dieser Spieler
unique_gamblers_fallacy_players = data_with_avg_loss[data_with_avg_loss['increased_bet_after_loss']]['depositor'].nunique()

# Schritt 5: Berechnung des durchschnittlichen Einsatzes in ETH, des durchschnittlichen Gewinns/Verlusts und der durchschnittlich gespielten Runden für diese Spieler
selected_players_loss_data = data_with_avg_loss[data_with_avg_loss['increased_bet_after_loss']].copy()

# Durchschnittlicher Einsatz in ETH
average_deposit_loss = selected_players_loss_data['deposit_eth'].mean()

# Durchschnittlicher Gewinn/Verlust
selected_players_loss_data['win_loss_amount'] = selected_players_loss_data.apply(
    lambda row: -row['deposit_eth'] if row['is_winner'] == 0 else (selected_players_loss_data[selected_players_loss_data['roundid'] == row['roundid']]['deposit_eth'].sum() - row['deposit_eth']),
    axis=1
)
average_win_loss_loss = selected_players_loss_data['win_loss_amount'].mean()

# Durchschnittlich gespielte Runden
average_rounds_played_loss = selected_players_loss_data.groupby('depositor')['roundid'].nunique().mean()

# Ergebnisse
unique_gamblers_fallacy_players, average_deposit_loss, average_win_loss_loss, average_rounds_played_loss
