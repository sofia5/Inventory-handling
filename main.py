
from tabulate import tabulate
import time
import productHandler
import json

choice = ""
autoPurchase = True
# Every forth is for free
discount = 4

with open('products.json') as productData:
    with open('productPackages.json') as productPackageData:
        productHandler.initProducts(
            json.load(productData), json.load(productPackageData))

while choice != "Q":
    print("\n" + tabulate([['S[quantity] [product ID]', 'To sell products, enter S + number of items to sell + SPACE + product ID'], ['I[quantity] [product ID]', 'To buy, enter I + number of items to buy + SPACE + product ID.'], ['L', 'Enter L to show the current product status.'], ['C', 'Enter C to show the product catalogue.'], ['T', 'Toggle automatic purchasing. Current status is ' + ('On' if autoPurchase else 'Off') +
                                                                                                                                                                                                                                                                                                                                             '. \nThis means that when X number of items are sold 2X are bought.'], ['Q', 'Enter Q to quit.']], colalign=("center",), headers=['Operation', 'Description']))
    choice = input("\nWhat would you like to do? ")

    if len(choice) == 0:
        print("You need to provide an input.")

    else:
        operation = choice[0].upper()

        # Quit program
        if operation == "Q":
            print("Closing application")
            break

        # Show inventory
        elif operation == "L":
            res = productHandler.getProducts()
            ids = []
            names = []
            fruits = []
            inventory = []

            for product in res:
                fruitList = []
                ids.append(res[product].identifier)
                inventory.append(res[product].numInInventory)

                # Evaluate if package
                if res[product].identifier[0] == 'P':
                    names.append(res[product].name)
                    for packageItem in res[product].products:
                        fruitList.append(
                            packageItem[0].name + " x" + str(packageItem[1]))
                    fruits.append(', '.join(fruitList))
                else:
                    names.append("-")
                    fruits.append(res[product].name)

            table = zip(ids, names, fruits, inventory)

            print("\n" + tabulate(table, colalign=("right", "left", "left",
                                                   "right"), headers=['ID', 'Package Name', 'Fruits', 'Number of items in inventory']))

        # Show product catalogue
        elif operation == "C":
            res = productHandler.getProducts()
            ids = []
            names = []
            fruits = []
            prices = []

            for product in res:
                fruitList = []
                ids.append(res[product].identifier)
                prices.append(str(res[product].price) +
                              ' ' + res[product].currency)

                # Evaluate if package
                if res[product].identifier[0] == 'P':
                    for packageItem in res[product].products:
                        fruitList.append(
                            packageItem[0].name + " x" + str(packageItem[1]))

                    names.append(res[product].name)
                    fruits.append(', '.join(fruitList))
                else:
                    names.append("-")
                    fruits.append(res[product].name)

            table = zip(ids, names, fruits, prices)

            print("\n" + tabulate(table, colalign=("right", "left", "left",
                                                   "right"), headers=['ID', 'Package Name', 'Fruits', 'Price']))

        # Change automatic purchase toggle
        elif operation == "T":
            autoPurchase = productHandler.toggleAutoPurchase(autoPurchase)
            print("Changing automatic purchasing to " +
                  ('On' if autoPurchase else 'Off'))

        # Check productID and number of items as both are required to sell and buy
        elif(" " not in choice):
            print(
                "Sorry, you are missing the product ID (or have forgotten to separate it with a SPACE)")
        else:
            productID = choice.split(' ')[1].upper()

            try:
                numOfItems = int(choice[1:].split(' ')[0])

            except ValueError:
                print("Sorry, the number of items is not a number.")

            if numOfItems < 0:
                print("Sorry, the number of items requested cannot be negative.")

            if productID in productHandler.getProducts():

                # Sell products
                if operation == "S":
                    if(productID[0] == 'P'):
                        res = productHandler.sellProductPackage(
                            productID, numOfItems, autoPurchase)
                    else:
                        res = productHandler.sellProducts(
                            productID, numOfItems, autoPurchase)

                    productInventory = productHandler.getProductInventory(
                        productID)
                    productName = productHandler.getProductName(productID)
                    totalCost = productHandler.getProductCost(
                        productID, numOfItems, discount)
                    totalDiscounted = productHandler.getProductCost(
                        productID, numOfItems, None) - totalCost
                    currency = productHandler.getCurrency(
                        productID)

                    if(totalDiscounted == 0 and res):
                        print(str(numOfItems) + " " + productName +
                              "/s sold: " + str(totalCost) + " " + currency)
                    elif(totalDiscounted > 0 and res):
                        print(str(numOfItems) + " " + productName + "/s sold: " +
                              str(totalCost) + " " + currency + ". Discount earned: " + str(totalDiscounted) + " " + currency)
                    elif(not res):
                        print(
                            "You are trying to sell more items than you currently have in stock. Try again")

                    if(autoPurchase and res):
                        print(str(2 * numOfItems) + " " + productName +
                              "/s added to the inventory as automatic purchasing is ON. Automatic purchasing can be turned off using (T).")
                    print("Current " + productName +
                          " inventory: " + str(productInventory))

                # Buy products (request delivery)
                elif operation == "I":
                    productHandler.buyProducts(productID, numOfItems)
                    productName = productHandler.getProductName(productID)
                    productInventory = productHandler.getProductInventory(
                        productID)

                    print(str(numOfItems) + " " + productName +
                          "/s added to the inventory")
                    print("Current \u001b[1m" + productName +
                          "\u001b[0m inventory: " + str(productInventory))
                else:
                    print("The command " + operation +
                          " is not a valid input.")
            else:
                print(
                    "Sorry, the product ID provided does not match any existing products. Check the product catalogue (C) to get some help.")

    # Timer could be used to make the response appear longer before the next input
    # time.sleep(1.8)
