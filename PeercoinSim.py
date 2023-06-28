import numpy as np
import matplotlib.pyplot as plt

dayyear=(365*33+8)/33
secday=60*60*24
MaxSimDays=365*2
NumSim=1000

#Simulation Variables
diff=20.43
StaticReward=1.34

# Precomputed probability for 31-90 days to be adjusted by value/diff
probsecs = [2**224 * (x+1) / (2**256) for x in range(60)]

#Model
def RandomDaysToMint(outValue,difficulty,rng):

    adj = outValue / difficulty
    probs = [1 - (1 - probsecs[x]*adj)**secday for x in range(60)]

    DaysToMint=31
    for x in range(60):

        rnd = rng.random()
        probday = probs[x]

        if rnd<probday: break

        DaysToMint+=1

    else: DaysToMint=DaysToMint+rng.geometric(probs[59])

    return DaysToMint

rng = np.random.default_rng()

#Reward Wrapper
def MintRewards(outValue,difficulty):

    totalreward=0

    for _ in range(NumSim):

        MintDays=RandomDaysToMint(outValue,difficulty,rng)

        #Coinage Limit
        if MintDays < MaxSimDays:
            CoinageReward=0.03*outValue*min(365, MintDays)/dayyear
            normreward=(CoinageReward+StaticReward)/MintDays
            totalreward+=normreward

    # Return annualised percentage
    return totalreward/NumSim/outValue*36500

OutArray=[2**(x/2) for x in range(24)]
print(OutArray)

def OutputWrapper():
    RewardArray=[MintRewards(x, diff) for x in OutArray]
    PlotArray=[OutArray,RewardArray]
    return PlotArray

fig, ax = plt.subplots()
for w in range(100):
    RandPlot=OutputWrapper()
    ax.scatter(RandPlot[0],RandPlot[1])
    print(w)
ax.set_xlabel("UTXO Size")
ax.set_ylabel("% Reward / Yr")
plt.xscale("log")
plt.grid()
plt.show()

