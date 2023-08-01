import pandas as pd
import random
df = pd.read_csv("questions.csv")
m = min(df["Level"])
M = max(df["Level"])
level = 1
i = 1
while i < 10 :
    qID = random.choice(list(df[df['Level'] == level]['ID']))
    q = df[df['ID'] == qID]
    answer = input(q['Question'] + ' : ' + q['Possibility 1'] + ' / ' + q['Possibility 2'] + ' / ' + q['Possibility 3'] + ' / ' + q['Possibility 4'])
    if answer == q.loc[qID-1, 'Correct Answer'] :
        print("Correct, next question : ")
        level = min(level + 1, M)
    else : 
        print("Wrong, next question : ")
        level = max(level - 1, m)
    i = i+1
print('According to this assessment, you should take the Mastery Course Level ' + str(level+1))


    
