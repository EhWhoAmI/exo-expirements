from market_agent import Agent
from OrderClass import BuyOrder
from OrderClass import SellOrder

import market_globals as globals
import matplotlib.pyplot as plt
import json

from random import randint

#####################################
#           Function Defs
####################################

def record_data(Agents_Data):
    Agents_Data['Time'].append(globals.gametime)
    for i, agent_ in enumerate(globals.Agents):
        Agents_Data['AgentsList'][i]['Cash'].append(agent_.cash)
        Agents_Data['AgentsList'][i]['Store'].append(agent_.stores[test_good])
    return Agents_Data

####################################
#               Main
####################################
globals.initialize()

# Initialize Orders
Orders = {}
for good in globals.goods:
    Orders[good]= {}
    Orders[good]['Buy'] = []
    Orders[good]['Sell'] = []

# 
test_good   = globals.goods[0]
test_good_stock = 20
test_amount = 10
test_buy_price = 2
test_sell_price = 1

# Create a buyer and seller
for i in range(2):
    globals.Agents.append(Agent())
    globals.Agents[i].add_resource(test_good,test_good_stock)

# Create a 3rd Agent who will buy and sell
globals.Agents.append(Agent())

# Initialize the store of the test good for the 3rd Agent
globals.Agents[2].add_resource(test_good,0)

# Create buy and sell orders for the 3rd Agent to work with
Orders[test_good]['Buy'].append(BuyOrder(test_good,test_amount,test_buy_price,0))
    
Orders[test_good]['Sell'].append(SellOrder(test_good,test_amount,test_sell_price,1))

# Initialize Data Gathering
Agents_Data = {}
Agents_Data['Time'] = []
Agents_Data['Time'].append(globals.gametime)
Agents_Data['AgentsList'] = []


for i, agent_ in enumerate(globals.Agents):
    tempStruct = {}
    tempStruct['Cash'] = []
    tempStruct['Cash'].append(agent_.cash)
    tempStruct['Store'] = []
    tempStruct['Store'].append(agent_.stores[test_good])

    Agents_Data['AgentsList'].append(tempStruct)

for i in range(test_amount*2):
    # Increment game time
    globals.gametime += 1

    # Grab temp variables for easy reading
    current_stock = globals.Agents[2].stores[test_good]
    Agent_ID = globals.Agents[2].id

    # Buy if they have 0, sell if they have 1
    if current_stock == 0:
        Orders[test_good]['Sell'][0].Sell(1,Agent_ID)
    else:
        Orders[test_good]['Buy'][0].Purchase(1,Agent_ID)
    
    Agents_Data = record_data(Agents_Data)

fid = open('Agents_Data.json','w')
fid.write(json.dumps(Agents_Data, indent = 2))
fid.close()