from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from datetime import datetime, timedelta
import random

app=Flask(__name__)
api=Api(app)

videoPostArgs=reqparse.RequestParser()
videoPostArgs.add_argument("Pizza(s)", action='append', help="What pizza are you ordering? (Give the ID)", required=True)
videoPostArgs.add_argument("Takeaway", type=bool, help="Add takeaway preference, True/False", required=True)
videoPostArgs.add_argument("Payment type", type=str, help="Add prefered method of payment", required=True)
videoPostArgs.add_argument("Customer ID", type=int, help="Add customer ID", required=True)
videoPostArgs.add_argument("Delivery Address", action='append', help="Add your delivery address", required=True)

pizzas=[{
			"Pizza ID" : 0,
			"Name" : "Margherita",
			"Vegetarian" : True,
			"Price" : 12.50,
			"Toppings" : [
							"Tomatoes",
							"Mozzarella",
							"Basil"
						 ]
		},
		{
			"Pizza ID" : 1,
			"Name" : "Meat Lovers Delight",
			"Vegetarian" : False,
			"Price" : 14.50,
			"Toppings" : [
							"Pepperoni",
							"Chicken",
							"Bacon"
						 ]
		},
		{
			"Pizza ID" : 2,
			"Name" : "Veggie Extravaganza",
			"Vegetarian" : True,
			"Price" : 13.50,
			"Toppings" : [
							"Peppers",
							"Onions",
							"Mushrooms"
						 ]
		}
	   ]

customers=[{
			"Pizza(s)" : [{
							"Pizza ID" : 1,
							"Note" : "Extra Bacon"
						  }
						 ],
			"Takeaway" : False,
			"Payment type" : "Card",
			"Customer ID" : 0,
			"Delivery Address" : {
									"Street" : "Angel Street",
									"City" : "New York",
									"Country" : "United States of America",
									"Zipcode" : "23AV423"
								 }
		},
		{
			"Pizza(s)" : [{
							"Pizza ID" : 2,
							"Note" : "No Mushrooms"
						  },
						  {
						  	"Pizza ID" : 0,
						  	"Note" : ""
						  }
						 ],
			"Takeaway" : True,
			"Payment type" : "Cash",
			"Customer ID" : 1,
			"Delivery Address" : {
									"Street" : "Willow Way",
									"City" : "London",
									"Country" : "United Kingdom",
									"Zipcode" : "QT76932"
								 }
		}
	   ]

orders=[{
			"Order" : {
						"Order ID" : 0,
						"Ordered at" : "15-05-21 17:59:33",
						"Status" : "In progress",
						"Delivery Time" : "15-05-21 21:40:00"
					  }
		}
	   ]

#---------------------------------------------------------------

def checkPizzaID(pizzaID):
	if(pizzaID >= len(pizzas)):
		abort(404, message="Pizza not found...")

def checkCustomerID(customerID):
	if(customerID >= len(customers)):
		abort(404, message="Customer not found...")

def checkOrderID(orderID):
	if(orderID >= len(orders)):
		abort(404, message="Order not found...")

def checkElapsedTime(orderID):

	#Get the minutes since order here
	
	if(minutesSinceOrder>=5):
		abort(412, message="Unable to cancel your order as more than 5 minutes have elapsed since it was placed.")

def checkOrderStatus(orderID):
	status=orders[orderID]["Order"]["Status"]
	if(status=="Cancelled" or status=="Delivered"):
		abort(422, message="Unable to cancel your order as it has either already been cancelled, or it has already been delivered.")


#---------------------------------------------------------------

class Pizzas(Resource):
	def get(self):
		return pizzas, 200

class Pizza(Resource):
	def get(self, pizzaID):
		checkPizzaID(pizzaID)
		return pizzas[pizzaID], 200

class Customer(Resource):
	def get(self, customerID):
		checkCustomerID(customerID)
		return customers[customerID], 200

class Order(Resource):
	def post(self):
		args=videoPostArgs.parse_args()
		#print(args) #Testing

		
		customers.append(args)
		#print(customers)

		#The rest is working
		orderID=len(orders)
		curDate=datetime.now()
		delTime=curDate+timedelta(minutes=15)
		newOrder={"Order" : {"Order ID" : orderID, "Ordered at" : curDate.strftime("%d-%m-%y %H:%M:%S"), "Status" : "In progress", "Delivery Time" : delTime.strftime("%d-%m-%y %H:%M:%S")}}
		orders.append(newOrder)
		return newOrder, 200

class CancelOrder(Resource):
	def put(self, orderID):
		checkOrderID(orderID)
		#checkElapsedTime(orderID)
		checkOrderStatus(orderID)

		#If code reaches here, then the order is cancel-able. :)
		orders[orderID]["Order"]["Status"]="Cancelled"
		return orders[orderID], 200

class DeliveryTime(Resource):
	def get(self, orderID):
		checkOrderID(orderID)
		deliveryTime=orders[orderID]["Order"]["Delivery Time"]

		deliveryTime=datetime.strptime(deliveryTime, "%d-%m-%y %H:%M:%S")
		curTime=datetime.now()
		timeLeft=deliveryTime-curTime
		totSec=timeLeft.total_seconds()
		minutes=int(totSec//60)
		seconds=round(totSec%60)
		if(minutes>=0):
			return {"Time until delivery: "+str(minutes)+" minute(s) and "+str(seconds)+" second(s)." : orders[orderID]}, 200
		else:
			return {"message" : "Your food should've arrived by now! Contact helpline 082-1328976 for more info."}


api.add_resource(Pizzas, "/api/pizza")
api.add_resource(Pizza, "/api/pizza/<int:pizzaID>")
api.add_resource(Customer, "/api/order/<int:customerID>")
api.add_resource(Order, "/api/order")
api.add_resource(CancelOrder, "/api/order/cancel/<int:orderID>")
api.add_resource(DeliveryTime, "/api/order/deliverytime/<int:orderID>")


#---------------------------------------------------------------
if(__name__=="__main__"):
	app.run(debug=True)

#12/05/2021
#Works when unchecked but breaks when it should work if checked :( - fixed :)

#13/05/2021
#Problem with sending body in post request, it can't deal with the double level of dictionaries! :( - quick fix atm is to just make the dictionary objects a string? - could be improved after bare minimum has been done!
