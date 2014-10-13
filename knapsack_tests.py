from item import Item
import knapsack
from functools import reduce

def print_items_info(items):
    print("total profit {}".format(reduce(lambda total,item: total+item.profit, items, 0)))
    print("total weight {}".format(reduce(lambda total,item: total+item.weight, items, 0)))
    print("items")
    for item in items:
        print(item)

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

optimal_profit, selected_items = knapsack.zero_one_knapsack(random_positive_items, 800)
print(optimal_profit)
print_items_info(selected_items)

optimal_profit, selected_items = knapsack.net_zero_knapsack(random_items, 50)
print(optimal_profit)
print_items_info(selected_items)

#for item_index in range(0, len(items)):
#    for weight in range (0, max_weight+1):
#        print "item {} weight {} profit {}".format(item_index, weight, max_values[item_index][weight])
