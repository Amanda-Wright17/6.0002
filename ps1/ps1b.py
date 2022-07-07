###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """

    
    if len(egg_weights) == 0:
        return sum(memo.values())
    else:
        max_weight = max(egg_weights)
        
    if max_weight == target_weight:
        memo[max_weight] = 1
        return sum(memo.values())
    
    # explore taking the egg
    elif max_weight < target_weight: 
        egg_count = target_weight // max_weight
        memo[max_weight] = egg_count
        eggs_left = egg_weights[:-1]
        updated_target_weight = target_weight - (max_weight * egg_count)
        return dp_make_weight(eggs_left, updated_target_weight, memo)
    
    # explore not taking the egg
    elif max_weight > target_weight:
        eggs_left = egg_weights[:-1]
        return dp_make_weight(eggs_left, target_weight, memo)
    
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    
    # egg_weights = (2, 3, 5, 10, 50)
    # n = 998
    # print("Egg weights = (2, 3, 5, 10, 50)")
    # print("n = 998")
    # print("Expected ouput: 25 (19 * 50 + 4 * 10 + 1 * 5 + 1 * 3 = 998)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    # print()
    
    
    # egg_weights = (3, 5, 10, 20)
    # n = 543
    # print("Egg weights = (3, 5, 10, 20)")
    # print("n = 543")
    # print("Expected ouput: 28 (27 * 20 + 1 * 5 = 28)")
    # print("Actual output:", dp_make_weight(egg_weights, n))
    # print()