from item import Item

# http://en.wikipedia.org/wiki/Knapsack_problem#0.2F1_knapsack_problem
def zero_one_knapsack(items, max_weight):

    max_values = [[0 for j in range(0, max_weight+1)] for i in range(0, len(items) + 1)]

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
            else: # we can't include this item at this weight
                max_values[max_values_index][weight] = max_values[max_values_index - 1][weight] # profit if this item is not included

    # max profit for all items given the maximum weight restriction
    return max_values[len(items)][max_weight]

def net_zero_knapsack(items, tolerance):

    negative_items = filter(lambda item: item.weight < 0, items)
    positive_items = filter(lambda item: item.weight > 0, items)

    negative_items_as_positive = map(lambda item: Item(item.profit, -item.weight), negative_items)
    
    total_positive = reduce(lambda total,item: total+item.weight, positive_items, 0)
    total_negative = reduce(lambda total,item: total+item.weight, negative_items_as_positive, 0)

    if total_positive < total_negative:
        optimal_profit = zero_one_knapsack(negative_items_as_positive, total_positive + tolerance)
    else:
        optimal_profit = zero_one_knapsack(positive_items, total_negative + tolerance)

    return optimal_profit
