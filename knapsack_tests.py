from item import Item
import knapsack

def print_items_info(items):
    print "total profit {}".format(reduce(lambda total,item: total+item.profit, items))
    print "total weight {}".format(reduce(lambda total,item: total+item.weight, items))
    print "items"
    for item in items:
        print item,

random_items = [
    Item(100, 100),
    Item(50, 50),
    Item(300, -300),
    Item(250, 250),
    Item(100, -100),
    Item(150, -150),
    Item(200, 200)
    ]

random_positive_items = [
    Item(100, 100),
    Item(50, 50),
    Item(300, 300),
    Item(250, 250),
    Item(100, 100),
    Item(150, 150),
    Item(200, 200)
    ]

print(knapsack.zero_one_knapsack(random_positive_items, 800))
