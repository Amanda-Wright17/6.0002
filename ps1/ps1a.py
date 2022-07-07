###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import copy

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cows = {}
    
    with open(filename) as file:
        for line in file:
            split = line.rstrip("\n").split(",")
            cows[split[0]] = split[1]
    return cows
                

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # sort cows by weight, returns list of cow names
    cows_sorted = sorted(cows, key=lambda x: cows[x], reverse=True)
    
    result = []
    cows_left = copy.copy(cows_sorted)
    
    
    while len(cows_left) > 0:
        ship = []
        total_weight = 0
        for name in cows_sorted:
            if name in cows_left:
                if total_weight + int(cows[name]) <= limit:
                    ship.append(name)
                    total_weight+= int(cows[name])
                    cows_left.remove(name)
                else:
                    continue
        result.append(ship)
            
    print("greedy", result)
    return result
                
    
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    
    current_best = None
    # enumerate all possible combinations, returns list of lists of cow names
    for partition in get_partitions(cows):
        isPossible = True
        
        # iterate through each list in the partition
        for ship in partition:
            total_weight = 0
            
            # iterate through each cow in the ship to sum weights
            for cow in ship:
                total_weight += int(cows[cow])
                
            # ensure ship meets weight limit, otherwise try new partition    
            if total_weight > limit:
                isPossible = False
                break
    
        
    
    # store the partition with fewest number of ships       
        if isPossible and (current_best is None or \
                           len(partition) < len(current_best)):
            current_best = partition
   
    print("brute", current_best)
    return current_best
                
            
            
        
    
        
            
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # load data 
    cows = load_cows("/Users/amanda/Desktop/cs/6.0002/psets/PS1/ps1_cow_data.txt")
    
    #time greedy method
    start_greedy = time.time()
    greedy = greedy_cow_transport(cows)
    end_greedy = time.time()
    print('Greedy algorithm takes ', len(greedy), 'trips')
    print('Greedy algorithm takes ', (end_greedy - start_greedy), 'seconds')
    
    # time brute method
    start_brute = time.time()
    brute = brute_force_cow_transport(cows)
    end_brute = time.time()
    print('Brute force algorithm takes ', len(brute), 'trips')
    print('Brute force algorithm takes ', (end_brute - start_brute), 'seconds')
    


compare_cow_transport_algorithms()

