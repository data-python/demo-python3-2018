import pandas as pd
import os

# data_folder=os.path.join( os.path.expanduser("~"),"data")
# data_filename=os.path.join( data_folder,"2013-2014-nba.csv")

# Don't read the first row, as it is blank, and parse the date column as a date
# results = pd.read_csv(data_filename,skiprows=[0,])
results = pd.read_csv("2013-2014-nba.csv", skiprows=[0,]) # 跳过第一行不读

# Fix the name of the columns
results.columns = ["Date", "Start (ET)",  "Visitor Team", "VisitorPts", "Home Team", "HomePts", "Score Type", "OT?", "Notes"]

results["HomeWin"] = results["VisitorPts"] < results["HomePts"]
# Our "class values"
y_true = results["HomeWin"].values
print("Home Win percentage: {0:.1f}%".format(100 * results["HomeWin"].sum() / results["HomeWin"].count()))


results["HomeLastWin"] = False
results["VisitorLastWin"] = False

# Now compute the actual values for these
# Did the home and visitor teams win their last game?
from collections import defaultdict
won_last = defaultdict(int)

for index, row in results.iterrows():  # Note that this is not efficient
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    row["HomeLastWin"] = won_last[home_team]
    row["VisitorLastWin"] = won_last[visitor_team]
    results.ix[index] = row
    # Set current win
    won_last[home_team] = row["HomeWin"]
    won_last[visitor_team] = not row["HomeWin"]

from sklearn.tree import DecisionTreeClassifier
import numpy as np

from sklearn.cross_validation import cross_val_score

# Create a dataset with just the necessary information
X_previouswins = results[["HomeLastWin", "VisitorLastWin"]].values
clf = DecisionTreeClassifier(random_state=14)
scores = cross_val_score(clf, X_previouswins, y_true, scoring='accuracy')
print("Using just the last result from the home and visitor teams")
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))


# Let's try see which team is better on the ladder. Using the previous year's ladder
# ladder_filename = os.path.join(data_folder, "leagues.csv")
# ladder = pd.read_csv(ladder_filename)

ladder = pd.read_csv("leagues.csv")

# We can create a new feature -- HomeTeamRanksHigher\
results["HomeTeamRanksHigher"] = 0
for index, row in results.iterrows():
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    if home_team == "New Orleans Pelicans":
        home_team = "New Orleans Hornets"
    elif visitor_team == "New Orleans Pelicans":
        visitor_team = "New Orleans Hornets"

    if not ladder[ladder["Team"] == home_team].empty:
        home_rank = ladder[ladder["Team"] == home_team]["Rk"].values[0]
    else:
        print("home_team:", home_team)
    if not ladder[ladder["Team"] == visitor_team].empty:
        visitor_rank = ladder[ladder["Team"] == visitor_team]["Rk"].values[0]
    else:
        print("visitor_team:", visitor_team)
    row["HomeTeamRanksHigher"] = int(home_rank > visitor_rank)
    results.ix[index] = row

X_homehigher =  results[["HomeLastWin", "VisitorLastWin", "HomeTeamRanksHigher"]].values
clf = DecisionTreeClassifier(random_state=14)
scores = cross_val_score(clf, X_homehigher, y_true, scoring='accuracy')

print("Using whether the home team is ranked higher")
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))

# Who won the last match? We ignore home/visitor for this bit
last_match_winner = defaultdict(int)
results["HomeTeamWonLast"] = 0

for index, row in results.iterrows():
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    teams = tuple(sorted([home_team, visitor_team]))  # Sort for a consistent ordering
    # Set in the row, who won the last encounter
    row["HomeTeamWonLast"] = 1 if last_match_winner[teams] == row["Home Team"] else 0
    results.ix[index] = row
    # Who won this one?
    winner = row["Home Team"] if row["HomeWin"] else row["Visitor Team"]
    last_match_winner[teams] = winner

X_home_higher =  results[["HomeLastWin", "VisitorLastWin","HomeTeamRanksHigher", "HomeTeamWonLast"]].values
clf = DecisionTreeClassifier(random_state=14)
scores = cross_val_score(clf, X_home_higher, y_true, scoring='accuracy')
print("Using whether the home team is ranked higher")
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))
