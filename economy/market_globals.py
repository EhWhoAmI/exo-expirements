def initialize():
    # Incremental counter for unique Agent IDs
    global agent_counter
    agent_counter = 0
    
    # Measure of time in Game Ticks
    global gametime
    gametime = 0
    
    # List of Agents, index corresponds to Agent ID
    global Agents
    Agents = []

    # List of goods for trade
    global goods
    goods = ['iron', 'copper','plastic']