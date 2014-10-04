# http://en.wikipedia.org/wiki/Knapsack_problem#0.2F1_knapsack_problem
def zero_one_knapsack(items, max_weight):
    
    max_values = [[0 for j in range(0, max_weight+1)] for i in range(0, len(items))]

    # max profit with zero items is 0
    for weight in range(0, max_weight+1):
        max_values[0][weight] = 0
    
    # compute max profit for all possible scenarios
    for item_index in range(1, len(items)):
        item = items[item_index]
        for weight in range(0, max_weight+1):
            if(item.weight <= weight): # we can include this item at this weight
                exclude_profit = max_values[item_index - 1][weight] # profit if this item is not included
                include_profit = max_values[item_index - 1][weight - item.weight] + item.profit # profit if this item is included
                max_values[item_index][weight] = max(exclude_profit, include_profit)
            else: # we can't include this item at this weight
                max_values[item_index][weight] = max_values[item_index - 1][weight] # profit if this item is not included

    # max profit for all items given the maximum weight restriction
    return max_values[len(items) - 1][max_weight]
