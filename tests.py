import unittest
import productHandler
import json

productData = json.load(open('products.json'))
productPackageData = json.load(open('productPackages.json'))


class TestProductHandlerMethods(unittest.TestCase):

    def test_buyItem(self):
        productHandler.initProducts(productData, productPackageData)
        productHandler.buyProducts('1', 15)
        self.assertEqual(productHandler.getProductInventory('1'), 15)

    def test_buyPackage(self):
        productHandler.initProducts(productData, productPackageData)
        state1 = productHandler.getProducts()
        productHandler.buyProducts('P1', 1)
        state2 = productHandler.getProducts()
        self.assertDictEqual(state1, state2)

    def test_buyItemThatDoesNotExist(self):
        productHandler.initProducts(productData, productPackageData)
        state1 = productHandler.getProducts()
        productHandler.buyProducts('A', 15)
        state2 = productHandler.getProducts()
        self.assertEqual(state1, state2)

    def test_sellItemWithAutoPurchase(self):
        productHandler.initProducts(productData, productPackageData)
        productHandler.buyProducts('2', 15)
        productHandler.sellProducts('2', 5, True)
        self.assertEqual(productHandler.getProductInventory('2'), 20)

    def test_sellItemPackageWithAutoPurchase(self):
        productHandler.initProducts(productData, productPackageData)
        productHandler.buyProducts('1', 8)
        productHandler.buyProducts('4', 5)
        productHandler.sellProductPackage('P1', 2, True)
        self.assertEqual(productHandler.getProductInventory('P1'), 2)
        self.assertEqual(productHandler.getProductInventory('1'), 16)
        self.assertEqual(productHandler.getProductInventory('4'), 9)

    def test_sellItemsWithoutAutoPurchase(self):
        productHandler.initProducts(productData, productPackageData)
        productHandler.buyProducts('2', 15)
        productHandler.sellProducts('2', 5, False)
        self.assertEqual(productHandler.getProductInventory('2'), 10)

    def test_sellItemPackageWithoutAutoPurchase(self):
        productHandler.initProducts(productData, productPackageData)
        productHandler.buyProducts('1', 8)
        productHandler.buyProducts('4', 5)
        productHandler.sellProductPackage('P1', 2, False)
        self.assertEqual(productHandler.getProductInventory('P1'), 0)
        self.assertEqual(productHandler.getProductInventory('1'), 0)
        self.assertEqual(productHandler.getProductInventory('4'), 1)

    def test_autoPurchaseToggle(self):
        self.assertTrue(productHandler.toggleAutoPurchase(False))


if __name__ == '__main__':
    unittest.main()
