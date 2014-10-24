from item import Item
from functools import reduce
from fractions import gcd

# http://en.wikipedia.org/wiki/Knapsack_problem#0.2F1_knapsack_problem
def zero_one_knapsack(items, max_weight):

    greatest_common_divisor = reduce(lambda current_gcd,item: gcd(current_gcd, item.weight), items, max_weight)
    items = [Item(item.profit, int(item.weight / greatest_common_divisor)) for item in items]
    max_weight = int(max_weight / greatest_common_divisor)

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

    # iterate over items in reverse to figure out which ones were selected for each possible knapsack weight capacity
    # because of the way we construct the set of items, if we are keeping item k, we store it and then look at what we would keep in a knapsack of weight remaining_weight - k.weight
    remaining_weights = range(0, max_weight + 1) # each possible max weight
    included_items_by_capacity = [[] for i in range(0, max_weight + 1)] # for each possible max weight store the included items

    for item_index in reversed(range(0, len(items))):
        for index, weight in enumerate(remaining_weights):
            if selected_items[item_index][weight]:
                included_items_by_capacity[index].append(items[item_index])
                remaining_weights[index] -= items[item_index].weight

    scaled_included_items_by_capacity = [[] for i in range(0, max_weight*greatest_common_divisor + 1)]
    for capacity_index in range(0, max_weight*greatest_common_divisor + 1):
        for item in included_items_by_capacity[capacity_index//greatest_common_divisor]:
            scaled_included_items_by_capacity[capacity_index].append(Item(item.profit, int(item.weight * greatest_common_divisor)))

    weight_of_included_items = reduce(lambda weight, item: weight+item.weight, scaled_included_items_by_capacity[max_weight*greatest_common_divisor], 0)

    # max profit for all items given the maximum weight restriction
    return (max_values[len(items)][max_weight], weight_of_included_items, scaled_included_items_by_capacity[max_weight*greatest_common_divisor], scaled_included_items_by_capacity)



# nets negative and positive weight items to zero within the given tolerance while maximizing profit
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
        optimal_profit, weight_of_included_items, included_items, included_items_by_capacity = zero_one_knapsack(negative_items_as_positive, total_positive + tolerance)
        smaller_weight_items = positive_items
    else:
        optimal_profit, weight_of_included_items, included_items, included_items_by_capacity = zero_one_knapsack(positive_items, total_negative + tolerance)
        smaller_weight_items = negative_items_as_positive

    weight_of_smaller_weight_items = reduce(lambda weight, item: weight+item.weight, smaller_weight_items, 0)
    profit_of_smaller_weight_items = reduce(lambda profit, item: profit+item.profit, smaller_weight_items, 0)

    if abs(weight_of_included_items - weight_of_smaller_weight_items) <= tolerance:
        if total_positive < total_negative:
            included_items = map(lambda item: Item(item.profit, -item.weight), included_items) # convert back to negative weights
        else:
            smaller_weight_items = map(lambda item: Item(item.profit, -item.weight), smaller_weight_items) # convert back to negative weights
        return optimal_profit + profit_of_smaller_weight_items, weight_of_included_items + weight_of_smaller_weight_items, included_items + smaller_weight_items

    p, w, i, smaller_items_by_capacity = zero_one_knapsack(smaller_weight_items, weight_of_smaller_weight_items)

    smaller_items_capacity_index = weight_of_smaller_weight_items
    larger_items_capacity_index = weight_of_included_items
    
    while smaller_items_capacity_index >= 0 and larger_items_capacity_index >= 0:

        smaller_items_weight_at_current_capacity = reduce(lambda weight, item: weight+item.weight, smaller_items_by_capacity[smaller_items_capacity_index], 0)
        larger_items_weight_at_current_capacity = reduce(lambda weight, item: weight+item.weight, included_items_by_capacity[larger_items_capacity_index], 0)

        if(abs(smaller_items_weight_at_current_capacity - larger_items_weight_at_current_capacity) <= tolerance):
            smaller_items = smaller_items_by_capacity[smaller_items_capacity_index]
            larger_items = included_items_by_capacity[larger_items_capacity_index]
            smaller_items_profit = reduce(lambda profit, item: profit+item.profit, smaller_items, 0)
            larger_items_profit = reduce(lambda profit, item: profit+item.profit, larger_items, 0)
            return smaller_items_profit + larger_items_profit, smaller_items_weight_at_current_capacity + larger_items_weight_at_current_capacity, smaller_items + larger_items

        if(smaller_items_weight_at_current_capacity > larger_items_weight_at_current_capacity):
            smaller_items_capacity_index -= 1
        else:
            larger_items_capacity_index -= 1

    raise IndexError('Net zero knapsack should have returned at zero weight knapsack indices')








