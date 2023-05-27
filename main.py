from random import randint
import pandas as pd
import plotly.graph_objects as go

dfList = []
gainLossList = []

#   Number of runs
runs = 100

totalWin = 0
totalLoss = 0

for count4 in range(runs):
    gainLoss = []
    countList = []

    #   Variables

    #  Percentage of balance used in a single trade. | Default: 25
    balPerc = 30
    #   Expected reward per trade. | Default: 4.0
    reward = 4.5
    #   Expected risk per trade. | Default: 1.5
    risk = 2
    #   Starting balance. | Default: 1000
    bal = 1000
    #   Average win rate of strategy. | Default: 30
    odds = 30
    #   Number of trades in a day. | Default: 10
    trades = 5
    #   Number of trading days. | Default: 252
    days = 252
    #   Target balance to achieve. | Default: bal * 2 (100% increase)
    tarBal = bal * 2
    ogBal = bal
    win = 0
    lose = 0

    for count in range(days):
        for count2 in range(trades):
            rand = randint(0, 100)

            perOfBal = bal * (balPerc / 100)
            gain = (reward / 100) * perOfBal
            loss = (risk / 100) * perOfBal

            if rand > odds:
                lose += 1
                bal -= loss
                totalLoss += 1

            if rand < odds:
                win += 1
                totalWin += 1
                bal += gain

        gainLoss.append(round(bal, 2))
        countList.append(int(count))
        result = 0
    gainLossList.append(round(bal, 2))
    d = {'GainLoss': gainLoss, 'Days': countList}
    df = pd.DataFrame(d)
    dfList.append(df)

traces = []

titleString = f"Risk: {risk}% Reward: {reward}% Win Rate: {odds}% Starting Capital: ${ogBal} Percent Of Capital/Trade: {balPerc}% Trades/Day: {trades} Days: {days}"

layout = go.Layout(title=str(titleString))

fig1 = go.Figure(layout=layout)

for i, df in enumerate(dfList):
    dfList[i] = dfList[i].set_index('GainLoss')
    fig1.add_trace(go.Scatter(x=df['Days'], y=df['GainLoss'], mode='lines', name=f'Run #{str(i)}'))

avgValue = 0
tempVal = 0
for i in gainLossList:
    tempVal += i
    avgValue = tempVal / len(gainLossList)

above = 0
below = 0

for g in gainLossList:
    if g >= avgValue:
        above += 1
    if g < avgValue:
        below += 1

avgPerc = round(above / len(gainLossList), 2) * 100

above1 = 0
below1 = 0

for t in gainLossList:
    if t >= tarBal:
        above1 += 1
    if t < tarBal:
        below1 += 1

avgPercAbo = 0

try:
    avgPercAbo = round(above1 / len(gainLossList), 2) * 100
except:
    pass

print("Average End Capital: ", round(avgValue, 2))
print("Above End Capital: ", avgPerc)
print(f"Above Target Capital ({str(tarBal)}): {avgPercAbo}")
print("Win/Loss: ", totalWin / totalLoss)
print("Total Win Rate: ", totalWin / (runs * (trades * days)))

fig1.show()
