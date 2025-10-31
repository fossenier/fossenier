gas = 50
light = 50
heavy = 50
lubricant = 50
fuel = 50

def gasToFuel():
    pass
def lightToRocket():
    pass
def lightToFuel():
    pass
def lightToGas():
    pass
def heavyToLubricant():
    pass
def heavyToLight():
    pass

if gas > 75:
    gasToFuel()
elif gas <= 75:
    pass

if light > 75:
    if gas < 25:
        lightToGas()
    elif gas >= 25:
        if fuel > 75:
            lightToRocket()
        elif fuel <= 75:
            lightToFuel()
elif light <= 75:
    pass

if heavy > 75:
    if lubricant < 75:
        heavyToLubricant()
    elif lubricant <=75:
        heavyToLight()
elif heavy <= 75:
    pass

