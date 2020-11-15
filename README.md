# Case & Code comments

## Run the application

To run the program you need to install:

- Python
- pip (downloads)
- tabulate (formatted printing)

## Adjustments from the case description

Adjustments made:

- SP1 -> S1 P1
  <br>
  (Sell 1 of package 1). The change was made to avoid confusion between quantity wanted and package requested.
- "Buy X" is the same as "Deliver X to warehouse"
- Packages can either have a predetermined (discounted) price set in the database, or be a sum of the products it contains.

## Comments about the program

- Automatic purchase is currently ON when starting the program.
- The program is made for "expert" users, but wouldn't be recommended as a program for "normal" users as it's easy to enter the wrong numbers.
- The unit tests should be expanded to include more tests.
- The discounts can be handled better, e.g. giving discounts for specific products instead of all. I just did not implement this, but it could be handled partly by making a package with a lesser price.

**Product ID op1 (chosen):**

First product has ID 1, second has ID 2 ... n has ID n. The operations "S"/"L", product ID and number are separated by a blank to make itr easier for the user to specify what he/she wants. This does not follow the guidelines exactly, but I believe it's a better choice comparing to cmd/git bash commands.

If the application had an interface besides the console, I would select option number 2, but I think it's cumbersome and too easy for the user to make mistakes entering information if the ID is 8 chars long.

**Product ID op2:**

Have an 8 digits string as identifier for each object. The number of products possible to have with a 8-digit product ID is **40,320**. This could be improved by accepting additional characters (A-Z).

The current command line is not be the most usable, as the product ID could be mixed with the number of items requested (as both are numbers). This could be mitigated by asking for several inputs (type of product + actions&amount of items), by separating the values with e.g."," or " ", or by providing a form to enter the data.
