from numpy import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import random
import math

def transfer_cash(a, b, amount):
    a.cash -= amount
    b.cash -= amount

def add_resource(a, resource, amount):
    if resource not in a.stores:
        a.stores[resource] = 0
    a.stores[resource] += amount

def transfer_resource(a, b, resource, amount):
    add_resource(a, resource, -amount)
    add_resource(b, resource, amount)

class Recipe:
    def __init__(self):
        self.input = {}
        self.output = {}

# Market stuff
iron = 'iron'
alloys = 'alloys'
goods = [iron, alloys]
default_cost_prices = {iron: 50, alloys: 300}
alloy_making = Recipe()
alloy_making.input[iron] = 3
alloy_making.output[alloys] = 1
recipes = [alloy_making]

max_time = 1000

agents = []

bids = {}
offers = {}
prices = {}

class Bid:
    def __init__(self, agent, good, units, unit_price):
        self.agent = agent
        self.good = good
        self.units = units
        self.unit_price = unit_price

agent_counter = 0

def add_bid(bid):
    if bid.good not in bids:
        bids[bid.good] = []
    bids[bid.good].append(bid)

def add_offer(offer):
    if offer.good not in offers:
        offers[offer.good] = []
    offers[offer.good].append(offer)

class Agent:
    def __init__(self):
        global agent_counter
        self.cash = 100
        self.stores = {}
        self.id = agent_counter
        agent_counter += 1
        self.offers = dict(default_cost_prices)
        # If their bids succeed or not
        self.success = {}

    def simulate(self):
        pass

    def trade(self):
        self.success.clear()

MIN_PRICE = 0.5
class BasicBuyer(Agent):
    def __init__(self):
        super().__init__()
        # Add prices
        self.bid = 50
        self.cash += 1000

    def trade(self):
        super.trade()
        # Buy stuff for a certain price
        # Try to get a better price at a lower thing
        if iron in prices:
            pr = prices[iron]
            # Get middle
            # Adjust price by random
            self.bid = (pr + self.bid - random.randint(1, 5))/2
        add_bid(Bid(self, iron, 100, self.bid))

class BasicPopulation(Agent):
    def __init__(self):
        super().__init__()
        # Add prices
        self.cash += 1000

    def trade(self):
        super().trade()
        # Buy stuff for a certain price
        # Try to get a better price at a lower thing
        if alloys in prices:
            pr = prices[alloys]
            # Get middle
            # Adjust price by random
            self.offers[alloys] = (pr + self.offers[alloys] - random.randint(0, 5))/2
            # Actively seek to decrease price
            if alloys not in self.success:
                self.offers[alloys] *= 1.01
            else:
                self.offers[alloys] *= 0.99
        add_bid(Bid(self, alloys, random.randint(70, 120), self.offers[alloys]))

class BasicSeller(Agent):
    def __init__(self):
        super().__init__()
        # Add prices
        self.offer = 60
        add_resource(self, iron, 100)

    def simulate(self):
        add_resource(self, iron, 100)

    def trade(self):
        super().trade()
        # Re-adjust price
        if iron in prices:
            pr = prices[iron]
            # Get middle
            self.offer = (pr + self.offer + random.randint(1, 5))/2
            # Ensure price is above zero, so we don't give money with stuff
            if self.offer <= MIN_PRICE:
                self.offer = MIN_PRICE
        # Sell stuff for a certain price
        # Sell remaining iron
        add_offer(Bid(self, iron, self.stores[iron], self.offer))
        # ensure money is above a certain level

class BasicFactory(Agent):
    def __init__(self, recipe):
        super().__init__()
        self.offer = 60
        self.recipe = recipe
        self.alloy_offer = 300
        self.productivity = 100
        add_resource(self, iron, 100)

    def simulate(self):
        # Generate resources
        can_manufacture = True
        for k, v in self.recipe.input.items():
            # Check if it can manufacture by checking for enough resources
            # If it cannot manufacture, then cry, and make a lower amount
            if self.stores[k] > -v * self.productivity:
                add_resource(self, k, -v * self.productivity)
            else:
                can_manufacture = False
        if can_manufacture:
            for k, v in self.recipe.output.items():
                add_resource(self, k, v * self.productivity)

    def trade(self):
        super().trade()
        # Re-adjust price
        # Request everything in recipe
        for k, v in self.recipe.input.items():
            if k in prices:
                pr = prices[k]
                # Get middle
                self.offers[k] = (pr + self.offers[k] - random.randint(1, 5))/2
                # Ensure price is above zero, so we don't give money with stuff
            add_bid(Bid(self, k, v * self.productivity, self.offers[k]))

        # Sell alloys
        if alloys in prices:
            pr = prices[alloys]
            # Get middle
            self.alloy_offer = (pr + self.alloy_offer + random.randint(1, 5))/2
            # Ensure that they'll make a profit
            # If it's not sold, also decrease the price, if it is, increase the price
            # Actively seek to decrease price
            if alloys not in self.success:
                # Decrease price as a factor as amount of alloys
                self.alloy_offer *= (0.99 ** math.log10(self.stores[alloys]))
            else:
                self.alloy_offer *= 1.01
            min_price = (prices[iron] * self.recipe.input[iron])
            if self.alloy_offer <= min_price:
                self.alloy_offer = min_price
        add_offer(Bid(self, alloys, self.stores[alloys], self.alloy_offer))


buyer_count = 100
seller_count = 10

agents.append(BasicFactory(alloy_making))
agents.append(BasicPopulation())

agents.append(BasicSeller())
agents.append(BasicSeller())
agents.append(BasicSeller())

# Data collection
average_historic_prices = {}
highest_bids = {}
lowest_offers = {}
bid_count_history = {}
offer_count_history = {}
volume_history = {}

max_time = 1000
for age in range(max_time):
    # Create orders
    for agen in agents:
        agen.simulate()
        agen.trade()

    # Resolve orders
    # Resolve buy orders
    for good in goods:
        if good not in bids:
            # No bids, so infinite supply
            print("Not parsing {}, zero bids".format(good))
            continue
        if good not in offers:
            # no asks, so infinite demand
            print("Not parsing {}, zero offers".format(good))
            continue
        good_bid = bids[good]
        good_offer = offers[good]
        # Check for number of demands
        if len(good_bid) == 0:
            continue

        if len(good_offer) == 0:
            continue

        good_bid.sort(key=lambda x: x.unit_price, reverse=True)
        good_offer.sort(key=lambda x: x.unit_price, reverse=False)

        # Get number of bids and offers
        if good not in bid_count_history:
            bid_count_history[good] = {}
        bid_count_history[good][age] = sum(c.units for c in good_bid)

        if good not in offer_count_history:
            offer_count_history[good] = {}
        offer_count_history[good][age] = sum(c.units for c in good_offer)

        # Get highest bid
        highest_bid = good_bid[0]
        lowest_offer = good_offer[0]

        if good not in lowest_offers:
            lowest_offers[good] = {}
        lowest_offers[good][age] = lowest_offer.unit_price

        if good not in highest_bids:
            highest_bids[good] = {}
        highest_bids[good][age] = highest_bid.unit_price

        exit = 0
        tradeing_prices = []
        volume = 0
        while len(good_bid) > 0 and len(good_offer) > 0:
            current_buyer = good_bid[0]
            current_seller = good_offer[0]
            amount_traded = min(current_buyer.units, current_seller.units)
            trading_price = (current_seller.unit_price + current_buyer.unit_price) / 2
            # Check if the offer price is too low
            # Then reject if it's too low
            #if current_seller.unit_price < current_buyer.unit_price:
                # Remove it, it's too low
                #good_offer.pop(0)
                #good_bid.pop(0)
                #continue

            # The trade worked!
            if amount_traded > 0:
                current_buyer.units -= amount_traded
                current_seller.units -= amount_traded
                volume += amount_traded

                # Trade goods
                transfer_cash(current_buyer.agent, current_seller.agent, amount_traded * trading_price)
                transfer_resource(current_seller.agent, current_buyer.agent, good, amount_traded)

                # Data collection
                tradeing_prices.append(trading_price)

            # Check if it cannot be resolved
            # Remove all extra buy orders
            if current_buyer.units <= 0:
                current_buyer.agent.success[good] = True
                good_bid.pop(0)

            if current_seller.units <= 0:
                current_buyer.agent.success[good] = True
                good_offer.pop(0)

            exit += 1

        if good not in volume_history:
            volume_history[good] = {}
        volume_history[good][age] = volume

        # Clear bids
        good_bid.clear()
        good_offer.clear()

        if len(tradeing_prices) == 0:
            continue

        # Data collection
        if good not in average_historic_prices:
            average_historic_prices[good] = {}
        average_historic_prices[good][age] = sum(tradeing_prices)/len(tradeing_prices)
        prices[good] = average_historic_prices[good][age]

    # Compile stats

# Display plot
fig, axs = plt.subplots(1, 3)
# Make some space on the right side for the extra y-axis.

for k, v in highest_bids.items():
    offers = lowest_offers[k]
    axs[0].fill_between(v.keys(), v.values(), offers.values(), alpha=0.25, label="{}".format(k))

for k, v in average_historic_prices.items():
    axs[0].plot(v.keys(), v.values(), label="{}".format(k))

for k, v in offer_count_history.items():
    axs[1].plot(v.keys(), v.values(), label="{} offers".format(k))

for k, v in bid_count_history.items():
    axs[1].plot(v.keys(), v.values(), label="{} bids".format(k))

for k, v in volume_history.items():
    axs[2].plot(v.keys(), v.values(), label="{} volume".format(k), marker='o')

# Move the last y-axis spine over to the right by 20% of the width of the axes

# Get number of bids
axs[0].legend(loc="upper left")
axs[0].set_xlabel("Time")
axs[0].set_ylabel("Price")
axs[1].legend(loc="upper right")
axs[1].set_xlabel("Time")
axs[1].set_ylabel("Bids/offer amount (units)")
axs[2].set_ylabel("Volume (units)")
axs[2].set_xlabel("Time")
axs[2].legend(loc="lower left")

plt.show()
