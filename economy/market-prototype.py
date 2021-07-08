import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

factory_index = 0
# Recipes:
# Demand
class Factory:
    def __init__(self):
        global factory_index
        self.resources = {}
        self.production = {}
        self.history_resources = {}
        self.index = factory_index
        self.money = 100000
        factory_index += 1

    def __str__(self):
        return str(self.index)

class Recipe:
    def __init__(self):
        self.input = {}
        self.output = {}

class Market():
    def __init__(self):
        self.demand = {}
        self.supply = {}
        self.supply_history = {}
        self.demand_history = {}
        self.sd = {}
        self.sd_history = {}
        self.prices = {}
        self.price_history = {}
        self.resources = {}

market = Market()
iron = 'iron'
alloys = 'alloys'

alloymaking = Recipe()
alloymaking.input[iron] = 30
alloymaking.output[alloys] = 10

city_a = Factory()
city_b = Factory()

city_b.recipe = alloymaking

city_a.production[iron] = 100

cities = [city_a, city_b]
plt.xkcd()
fig, axs = plt.subplots(1, 4)

money_history = {}
for i in range(100):
    # Generate resources
    for city in cities:
        for resource, amount in city.production.items():
            if resource not in city.resources:
                city.resources[resource] = 0
            city.resources[resource] += amount

    # Do recipes
    for city in cities:
        if hasattr(city, 'recipe'):
            # Add resources
            for resource, amount in city.recipe.input.items():
                if resource not in city.resources:
                    city.resources[resource] = 0
                city.resources[resource] -= amount

            for resource, amount in city.recipe.output.items():
                if resource not in city.resources:
                    city.resources[resource] = 0
                city.resources[resource] += amount

    # Add people to buy
    # Attempt to sell them
    market.supply = {}
    for city in cities:
        for resource, v in city.resources.items():
            if resource not in market.supply:
                market.supply[resource] = 0
            market.supply[resource] += v

    # Add demand
    for city in cities:
        if hasattr(city, 'recipe'):
            # Add resources
            for resource, amount in city.recipe.input.items():
                if resource not in market.demand:
                    market.demand[resource] = 0
                market.demand[resource] += amount

    for city in cities:
        for resource, v in city.resources.items():
            if resource not in market.resources:
                market.resources[resource] = 0
            market.resources[resource] += v
            city.resources[resource] = 0
    # Calculate s/d ratio
    for resource, amount in market.demand.items():
        if resource in market.supply:
            market.sd[resource] = market.supply[resource]/amount

    # Calculate price
    for resource, amount in market.sd.items():
        if resource not in market.prices:
            market.prices[resource] = 1
        if amount > 1:
            # Higher supply
            # So calculate things
            market.prices[resource] *= amount
        elif amount < 1:
            # Higher demand
            market.prices[resource] *= amount

    # Buy and sell stuff
    for city in cities:
        # Sell stuff
        # Dump everything in store to market?
        '''if hasattr(city, 'recipe'):
            # Add resources
            for resource, amount in city.recipe.input.items():
                # Buy that amount of resources or something
                # Get the resources you want to get
                amount_to_buy = city.money / market.prices[resource]
                city.money -= amount_to_buy * market.prices[resource]
                #market.prices[resource] * amount
                # Lower demand or something'''


    # History of supply
    for resource, amount in market.supply.items():
        if resource not in market.supply_history:
            market.supply_history[resource] = {}
        market.supply_history[resource][i] = amount

    for resource, amount in market.demand.items():
        if resource not in market.demand_history:
            market.demand_history[resource] = {}
        market.demand_history[resource][i] = amount

    for resource, amount in market.sd.items():
        if resource not in market.sd_history:
            market.sd_history[resource] = {}
        market.sd_history[resource][i] = amount

    for resource, amount in market.prices.items():
        if resource not in market.price_history:
            market.price_history[resource] = {}
        market.price_history[resource][i] = amount

    # history of resources
    for city in cities:
        for resource, amount in city.resources.items():
            if resource not in city.history_resources:
                city.history_resources[resource] = {}
            city.history_resources[resource][i] = amount
        if str(city) not in money_history:
            money_history[str(city)] = {}
        money_history[str(city)][i] = (city.money)

for city in cities:
    for resource, amount in city.history_resources.items():
        axs[0].plot(city.history_resources[resource].keys(), city.history_resources[resource].values(), label="{} {}".format(resource, str(city)))
axs[0].legend()
for resource, v in market.supply_history.items():
    axs[1].plot(market.supply_history[resource].keys(), market.supply_history[resource].values(), label="{} supply".format(resource))

for resource, v in market.demand_history.items():
    axs[1].plot(market.demand_history[resource].keys(), market.demand_history[resource].values(), label="{} demand".format(resource))

for resource, v in market.sd_history.items():
    axs[2].plot(market.sd_history[resource].keys(), market.sd_history[resource].values(), label="{} supply/demand".format(resource))

for resource, v in market.price_history.items():
    axs[3].plot(market.price_history[resource].keys(), market.price_history[resource].values(), label="{} price".format(resource))

ax = axs[3].twinx()
for city in cities:
    ax.plot(money_history[str(city)].keys(), money_history[str(city)].values(), label="{}".format(city))

plt.xlabel("time")
plt.ylabel("units")
axs[1].legend()
axs[2].legend()
axs[3].legend()
plt.show()
