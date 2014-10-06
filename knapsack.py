from item import Item
from functools import reduce

# http://en.wikipedia.org/wiki/Knapsack_problem#0.2F1_knapsack_problem
def zero_one_knapsack(items, max_weight):

    max_values = [[0 for j in range(0, max_weight+1)] for i in range(0, len(items) + 1)]
    selected_items = [[False for j in range(0, max_weight+1)] for i in range(0, len(items))]

    # max profit with zero items is 0
    for weight in range(0, max_weight + 1):
        max_values[0][weight] = 0
    
    # compute max profit for all possible scenarios
    for item_index in range(0, len(items)):
        item = items[item_index]
        max_values_index = item_index + 1
        for weight in range(0, max_weight + 1):
            if(item.weight <= weight): # we can include this item at this weight
                exclude_profit = max_values[max_values_index - 1][weight] # profit if this item is not included
                include_profit = max_values[max_values_index - 1][weight - item.weight] + item.profit # profit if this item is included
                max_values[max_values_index][weight] = max(exclude_profit, include_profit)
                if include_profit > exclude_profit:
                    selected_items[item_index][weight] = True # we are using this item at this weight
            else: # we can't include this item at this weight
                max_values[max_values_index][weight] = max_values[max_values_index - 1][weight] # profit if this item is not included

    # iterate over items in reverse to figure out which ones were selected
    # because of the way we construct the set of items, if we are keeping item k, we store it and then look at what we would keep in a knapsack of weight remaining_weight - k.weight
    included_items = []
    remaining_weight = max_weight
    for item_index in reversed(range(0, len(items))):
        if selected_items[item_index][remaining_weight]:
            included_items.append(items[item_index]) 
            remaining_weight -= items[item_index].weight

    # max profit for all items given the maximum weight restriction
    return (max_values[len(items)][max_weight], included_items)

def net_zero_knapsack(items, tolerance):

    # divide the items between positive and negative weights
    negative_items = [item for item in items if item.weight < 0]
    positive_items = [item for item in items if item.weight > 0]

    # convert the negative weight items to positive weights
    negative_items_as_positive = map(lambda item: Item(item.profit, -item.weight), negative_items)
    
    total_positive = reduce(lambda total,item: total+item.weight, positive_items, 0)
    total_negative = reduce(lambda total,item: total+item.weight, negative_items_as_positive, 0)

    # pack the heavier of the two sets of items into a weight capacity of the smaller set (+ threshold)
    if total_positive < total_negative:
        optimal_profit, included_items = zero_one_knapsack(negative_items_as_positive, total_positive + tolerance)
        included_items = map(lambda item: Item(item.profit, -item.weight), included_items) # convert back to negative weights
        included_items += positive_items
    else:
        optimal_profit, included_items = zero_one_knapsack(positive_items, total_negative + tolerance)
        included_items += negative_items

    return optimal_profit, included_items
