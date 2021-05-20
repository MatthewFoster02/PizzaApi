import requests
import random
from datetime import datetime, timedelta

BASE="http://127.0.0.1:5000/api/"

print("The pizzas: ")
checkPizzas=requests.get(BASE+"pizza")
print(checkPizzas.json())

print("\n-------------------------------------------------------------------\n")

print("View specific pizza: ")
viewPizza=requests.get(BASE+"pizza/1")
print(viewPizza.json())

print("\n-------------------------------------------------------------------\n")

print("Check customer history: ")
viewCustomer=requests.get(BASE+"order/2")
print(viewCustomer.json())

print("\n-------------------------------------------------------------------\n")

print("Make an order: ")
#makeOrder=requests.post(BASE+"order", {"Pizza(s)" : [{"Pizza ID : 2", "Note : No onions!"}], "Takeaway" : True, "Payment type" : "Apple pay", "Customer ID" : 2, "Delivery Address" : {"Street : Mozart Street", "City : Vienna", "Country : Austria", "Zipcode : 65433IY"}})
#print(makeOrder.json())

print("\n-------------------------------------------------------------------\n")

print("Cancel an order: ")
cancelOrder=requests.put(BASE+"order/cancel/0")
print(cancelOrder.json())

print("\n-------------------------------------------------------------------\n")

print("Get delivery time: ")
timeRemaining=requests.get(BASE+"order/deliverytime/1")
print(timeRemaining.json())