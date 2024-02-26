""" The first line consists of a single integer 
, the transaction fee on Monnei. The second line consists of a single integer 
, the transaction fee on Fjee. The third line consists of a single integer 
, the transaction fee on Dolladollabilljoll."""

# establish order
services = {0: "Monnei", 1: "Fjee", 2: "Dolladollabilljoll"}

# track fees
fees = []
for _ in range(3):
    fees.append(int(input("")))

# find cheapest service
cheapest_service_fee = None
cheapest_service = None
for service in services:
    # check each cost
    if cheapest_service_fee == None or fees[service] < cheapest_service_fee:
        cheapest_service_fee = fees[service]
        cheapest_service = services[service]

# notify cheapest service
print(cheapest_service)
