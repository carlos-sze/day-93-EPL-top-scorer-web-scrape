import csv
import requests
from bs4 import BeautifulSoup

# Premier League player stats page
response = requests.get('https://www.premierleague.com/stats/top/players/goals')
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

# Create lists to store the data
players = soup.find_all(class_="playerName")
players_txt = [player.getText(strip=True) for player in players]

clubs = soup.find_all(name="a", class_="stats-table__cell-icon-align")
clubs_txt = [club.getText(strip=True) for club in clubs]

nationalities = soup.find_all(class_="stats__player-country")
nationalities_txt = [nationality.getText(strip=True) for nationality in nationalities]

goals = soup.find_all(class_="stats-table__main-stat")
goals_txt = [goal.getText(strip=True) for goal in goals]

# Find the maximum length among all data lists
max_length = max(len(players_txt), len(clubs_txt), len(nationalities_txt), len(goals_txt))

# Create a list of tuples with the data columns
data = list(zip(players_txt, clubs_txt, nationalities_txt, goals_txt))

# Fill missing values with empty strings
data += [('', '', '', '')] * (max_length - len(data))

# Save the data to a CSV file
filename = 'top_goalscorers.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Player', 'Club', 'Nationality', 'Goals'])  # Write the header row
    writer.writerows(data)  # Write the player data rows

print(f"Data saved to {filename}.")