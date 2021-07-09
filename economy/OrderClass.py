from market_agent import Agent

gametime = 0 # In-Game Ticks
agent_counter = 0 # Running ticker of Agent Unique IDs
Agents   = []

goods = ['iron', 'copper','plastic']
Orders = {}
for good in goods:
    Orders[good]= {}
    Orders[good]['Buy'] = []
    Orders[good]['Sell'] = []

class Order:
    Amount    = 0       # Units of resource
    Price     = 0       # Price Per unit
    TotalCost = 0       # Price for whole order
    Completed = False   # Order is completed, can be removed

    # A particular exchange order, either buy or sell, for a resource
    # at a set price and amount available
    def __init__(self, resource_ID, Amount, Price, Agent_ID):
        global gametime
        self.Amount = Amount
        self.Price  = Price
        self.TotalCost = self.Amount*self.Price
        self.resource_ID    = resource_ID  # Unique ID of the resource
        self.OrderOwner_ID  = Agent_ID   # Unique ID of Owner
        self.TimeOfCreation = gametime  # Time the Order was made

class BuyOrder(Order):
    global Agents
    def __init__(self, resource_ID, Amount, Price, Agent_ID):
        super().__init__(resource_ID, Amount, Price, Agent_ID)
        # The Agent will convert their cash into an Amount of resource at a set Price
        # This stored cash will be transfered to the seller upon a Purchase transaction
        Agents[self.OrderOwner_ID].cash -= self.TotalCost        

    def add_resources(self, Amount):
        # Calculate the cost of adding the Amount desired
        Cost = Amount*self.Price

        # Initialize check for completed transaction
        Check = False               
        if Agents[self.OrderOwner_ID].cash >= Cost:
            Agents[self.OrderOwner_ID].cash -= Cost
            self.Amount += Amount
            Check = True
        
        return Check
    
    def Purchase(self, Amount, Agent_ID):
        # Check if Amount desired is more than the Order's Amount
        if Amount > self.Amount:
            # Calculate the cost of purchasing the Order's Full Amount
            Cost = self.Amount*self.Price
        else:
            # Calculate the cost of purchasing the desired Amount
            Cost = Amount*self.Price

        # Initialize check for completed transaction
        Check = False

        if Agents[Agent_ID].cash >= Cost:
            Agents[Agent_ID].cash -= Cost
            Agents[self.OrderOwner_ID].stores[self.resource_ID] += Amount
            self.Amount -= Amount
            if self.Amount == 0:
                self.Completed = True
            Check = True
        
        return Check

class SellOrder(Order):
    global Agents
    def __init__(self, resource_ID, Amount, Price, Agent_ID):
        super().__init__(resource_ID, Amount, Price, Agent_ID)
        # The Agent will store the Amount into the Sell Order
        # This stored Amount will be transfered to the buyer upon a Sell transaction
        Agents[self.OrderOwner_ID].stores[self.resource_ID] -= Amount

    def subtract_resources(self, Amount):
        if Amount > self.Amount:
            deltaAmount = self.Amount
        else:
            deltaAmount = Amount
        
        Agents[self.OrderOwner_ID].stores[self.resource_ID] += deltaAmount
        if self.Amount == 0:
            self.Completed = True

    
    def Sell(self, Amount, Agent_ID):
        # Check if Amount desired is more than the Order's Amount
        if Amount > self.Amount:
            # Calculate the cost of purchasing the Order's Full Amount
            Cost = self.Amount*self.Price
        else:
            # Calculate the cost of purchasing the desired Amount
            Cost = Amount*self.Price

        # Initialize check for completed transaction
        Check = False

        if Agents[Agent_ID].cash >= Cost:
            Agents[Agent_ID].cash -= Cost
            Agents[Agent_ID].stores[self.resource_ID] += Amount
            Agents[self.OrderOwner_ID].cash += Cost
            self.Amount -= Amount
            if self.Amount == 0:
                self.Completed = True
            Check = True
        
        return Check

test_good = goods[0]

for i in range(2):
    Agents.append(Agent())
    Agents[i].add_resource(test_good,1000)


for j, agent_var in enumerate(Agents):
    if j == 0:
        Orders[test_good]['Buy'].append(BuyOrder(test_good,10,1,j))
    else:
        Orders[test_good]['Sell'].append(SellOrder(test_good,10,1,j))
