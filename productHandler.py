import math

# productMap = {
#    1: Product1,
#    2: Product2,
# ...n: ProductN
#   P1: ProductPackage1
# ...Pn: ProductPackageN
# }
productMap = {}


class Product:
    def __init__(self, identifier, productType, name, price, currency, numOfBought, numOfSold, numInInventory):
        self.identifier = identifier
        self.productType = productType
        self.name = name
        self.price = price
        self.currency = currency
        self.numOfBought = numOfBought
        self.numOfSold = numOfSold
        self.numInInventory = numInInventory


class ProductPackage:
    def __init__(self, identifier, productType, name, products, price, currency, numInInventory):
        self.identifier = identifier
        self.productType = productType
        self.name = name
        # products = [{product1, quantity}, {product2, quantity}]
        self.products = products
        self.price = price
        self.currency = currency
        self.numInInventory = numInInventory


def initProducts(productData, productPackageData):
    for product in productData['products']:
        productMap[product['id']] = Product(
            product['id'], product['type'], product['name'], product['price'], product['currency'], 0, 0, 0)

    for package in productPackageData['productPackages']:
        productList = []
        price = 0
        if 'price' in package:
            price = package['price']

        else:
            for product in package['products']:
                price += getProductCost(product['id'],
                                        product['numberOfProducts'], None)

        for product in package['products']:
            productList.append(
                (productMap[product['id']], product['numberOfProducts']))

        productMap[package['id']] = ProductPackage(
            package['id'], package['type'], package['name'], productList, price, package['currency'], 0)


def getProducts():
    return productMap


def getProductName(productID):
    return productMap[productID].name


def getProductInventory(productID):
    return productMap[productID].numInInventory


def getProductCost(productID, quantity, discount):
    if discount == None:
        cost = productMap[productID].price * quantity
    else:
        itemsToPay = quantity - math.floor(quantity / discount)
        cost = productMap[productID].price * itemsToPay
    return cost


def getCurrency(productID):
    return productMap[productID].currency


def getNumberOfPackages(products):
    quantitiesList = []
    for product in products:
        neededItemsPerPackage = product[1]
        availableItems = getProductInventory(product[0].identifier)
        itemsForPackage = math.floor(availableItems / neededItemsPerPackage)
        quantitiesList.append(itemsForPackage)
    return min(quantitiesList)


def checkInventory(productID, quantityRequested):
    flag = True
    if(productMap[productID].numInInventory - quantityRequested < 0):
        flag = False
    return flag


def sellProducts(productID, itemsToSell, autoPurchase):
    res = True
    if(productMap[productID].numInInventory - itemsToSell >= 0):
        productMap[productID].numInInventory -= itemsToSell
        if autoPurchase:
            buyProducts(productID, itemsToSell * 2)
    else:
        res = False
    return res


def sellProductPackage(packageID, itemsToSell, autoPurchase):
    res = True
    if(productMap[packageID].numInInventory - itemsToSell >= 0):
        for product in productMap[packageID].products:
            res = sellProducts(product[0].identifier, product[1]
                               * itemsToSell, autoPurchase)

        # Update available packages in inventory
        productMap[packageID].numInInventory -= itemsToSell
    else:
        res = False
    return res


def buyProducts(productID, numOfItems):
    if productID in getProducts():
        if productMap[productID].productType == "item":
            productMap[productID].numInInventory += numOfItems

        # Update available packages in inventory
        for product in productMap:
            if(productMap[product].productType == "package"):
                numOfPackages = getNumberOfPackages(
                    productMap[product].products)
                productMap[product].numInInventory = numOfPackages


def toggleAutoPurchase(autoPurchase):
    autoPurchase = not autoPurchase
    return autoPurchase
