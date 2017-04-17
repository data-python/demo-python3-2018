import pandas as pd
import numpy as np

# data_folder = os.path.join( os.path.expanduser("~"),"PycharmProjects", "decisiontreeproject")
# data_filename=os.path.join( data_folder,"data.csv")
# results = pd.read_csv(data_filename,skiprows=[0,])
results = pd.read_csv("2013-2014-nba.csv", skiprows=[0,]) # 跳过第一行不读

# Fix the name of the columns 抽定义列字段
# Date,Start (ET),Visitor/Neutral,PTS,Home/Neutral,PTS,,,Notes
results.columns = ["Date", "Start (ET)",  "Visitor Team", "VisitorPts", "Home Team", "HomePts", "Score Type", "OT?", "Notes"]


# 提取新特征
results["HomeWin"] = results["VisitorPts"] < results["HomePts"] # 客队 < 主队
y_true = results["HomeWin"].values
print(results.ix[:5]) # 打印前五条?
print("Home Win percentage: {0:.1f}%".format(100 * results["HomeWin"].sum() / results["HomeWin"].count()))


# 两队最后输赢
results["HomeLastWin"] = False
results["VisitorLastWin"] = False

# Now compute the actual values for these
# Did the home and visitor teams win their last game?
from collections import defaultdict
won_last = defaultdict(int) # 最后获胜

for index, row in results.iterrows():  # Note that this is not efficient
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]
    row["HomeLastWin"] = won_last[home_team]
    row["VisitorLastWin"] = won_last[visitor_team]
    results.ix[index] = row

    # Set current win
    won_last[home_team] = row["HomeWin"]
    won_last[visitor_team] = not row["HomeWin"]
print(results.ix[20:25]) # 会自动打印
print()

# 使用决策树
# from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=14)

# from sklearn.cross_validation import cross_val_score
from sklearn.model_selection import cross_val_score


# Create a dataset with just the necessary information
X_previouswins = results[["HomeLastWin", "VisitorLastWin"]].values
clf = DecisionTreeClassifier(random_state=14)
scores = cross_val_score(clf, X_previouswins, y_true, scoring='accuracy')
print("Using just the last result from the home and visitor teams")
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))


# 第一个新特征
# Let's try see which team is better on the ladder. Using the previous year's ladder
# ladder_filename = os.path.join(data_folder, "")
ladder = pd.read_csv("leagues.csv")

# We can create a new feature -- HomeTeamRanksHigher
results["HomeTeamRanksHigher"] = 0
for index, row in results.iterrows():
    home_team = row["Home Team"]
    visitor_team = row["Visitor Team"]

    # 发生过改名的现象,需要处理
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
print(results[:5])


X_homehigher =  results[["HomeLastWin", "VisitorLastWin", "HomeTeamRanksHigher"]].values
clf = DecisionTreeClassifier(random_state=14)
scores = cross_val_score(clf, X_homehigher, y_true, scoring='accuracy')

print("Using whether the home team is ranked higher")
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))


# 第二个新特征
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
print(results.ix[:5])


X_home_higher =  results[["HomeTeamRanksHigher", "HomeTeamWonLast"]].values
clf = DecisionTreeClassifier(random_state=14)
scores = cross_val_score(clf, X_home_higher, y_true, scoring='accuracy')
print("Using whether the home team is ranked higher")
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))
