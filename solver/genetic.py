# # solver/genetic.py
# import random
# import time
# from typing import List, Tuple
# from models import Location, Destination

# # --- GA PARAMETERS ---
# POPULATION_SIZE = 50
# ELITISM_COUNT = 5  # Keep top 5 best routes unchanged
# MUTATION_RATE = 0.2
# GENERATIONS = 200  # For Hackathon speed (can be 1000+)
# TIME_LIMIT_SEC = 3.0  # Force stop after 3 seconds for UI responsiveness

# # Penalty Weights (Must match report)
# LATENESS_WEIGHT = 2.0 
# PRIORITY_WEIGHT = 10.0 # High penalty for skipping priority order (soft preference)

# def solve_genetic(source: Location, destinations: List[Destination], 
#                   dist_matrix: List[List[float]], dur_matrix: List[List[float]], 
#                   locations_map: List[str], initial_route_ids: List[str] = None) -> Tuple[List[str], List[dict], float, float]:
    
#     start_time = time.time()
    
#     # 1. Map Data Setup
#     loc_to_index = {loc_id: i for i, loc_id in enumerate(locations_map)}
#     source_idx = loc_to_index[source.id]
    
#     # Identify destination indices (exclude source)
#     dest_indices = [loc_to_index[d.id] for d in destinations]
    
#     # 2. Population Initialization
#     population = []
    
#     # Seed 1: The Baseline Result (Smart Seeding)
#     # If baseline provided a route, we use it as the "Adam" chromosome
#     if initial_route_ids:
#         seed_route = [loc_to_index[rid] for rid in initial_route_ids if rid != source.id]
#         if len(seed_route) == len(dest_indices):
#             population.append(seed_route)
            
#     # Seed 2...N: Random Shuffles
#     while len(population) < POPULATION_SIZE:
#         individual = dest_indices[:]
#         random.shuffle(individual)
#         population.append(individual)

#     # 3. Evolution Loop
#     best_chromosome = None
#     best_fitness = float('inf')
    
#     for gen in range(GENERATIONS):
#         # Time Check
#         if time.time() - start_time > TIME_LIMIT_SEC:
#             break
            
#         # Evaluation
#         scored_pop = []
#         for chrom in population:
#             fitness = calculate_fitness(chrom, source_idx, destinations, dur_matrix, loc_to_index)
#             scored_pop.append((fitness, chrom))
            
#             if fitness < best_fitness:
#                 best_fitness = fitness
#                 best_chromosome = chrom[:]
        
#         # Selection (Sort by fitness - lower is better)
#         scored_pop.sort(key=lambda x: x[0])
        
#         # Elitism (Keep best)
#         next_gen = [x[1] for x in scored_pop[:ELITISM_COUNT]]
        
#         # Breeding (Crossover + Mutation)
#         while len(next_gen) < POPULATION_SIZE:
#             parent1 = tournament_selection(scored_pop)
#             parent2 = tournament_selection(scored_pop)
            
#             child = order_crossover(parent1, parent2)
            
#             if random.random() < MUTATION_RATE:
#                 mutate(child)
                
#             next_gen.append(child)
            
#         population = next_gen

#     # 4. Decode Best Solution
#     # Reconstruct full path: Source -> [Best Chromosome] -> Source
#     # SAFETY: if GA exits early (time limit) before finding best
#     if best_chromosome is None:
#         best_chromosome = population[0]
#     final_indices = [source_idx] + best_chromosome + [source_idx]
    
#     # Reuse the reporter from Baseline to generate schedule
#     # (We duplicate the logic slightly or import it if you refactored shared utils. 
#     # For speed, I will use a simple inline generator here matching baseline format)
#     return generate_report(final_indices, destinations, source, dist_matrix, dur_matrix, locations_map, loc_to_index)

# # --- CORE GA FUNCTIONS ---

# # def calculate_fitness(chromosome, source_idx, dests, dur_matrix, loc_map):
# #     """
# #     Fitness = Total Duration + (Lateness * Weight) + (Priority Inversion * Weight)
# #     """
# #     total_time = 0.0
# #     total_lateness = 0.0
# #     current_time = 0.0
    
# #     # Add travel from Source -> First Node
# #     first_node = chromosome[0]
# #     current_time += dur_matrix[source_idx][first_node]
# #     total_time += dur_matrix[source_idx][first_node]
    
# #     for i in range(len(chromosome)):
# #         curr_node = chromosome[i]
        
# #         # Find Destination Object
# #         dest_obj = next((d for d in dests if loc_map[d.id] == curr_node), None)
        
# #         if dest_obj:
# #             # Check Deadline
# #             if current_time > dest_obj.deadline_hours:
# #                 total_lateness += (current_time - dest_obj.deadline_hours)
            
# #             # Service Time
# #             service_hrs = dest_obj.service_time_minutes / 60.0
# #             current_time += service_hrs
# #             total_time += service_hrs
            
# #         # Travel to next node (or back to source if last)
# #         if i < len(chromosome) - 1:
# #             next_node = chromosome[i+1]
# #         else:
# #             next_node = source_idx
            
# #         travel = dur_matrix[curr_node][next_node]
# #         current_time += travel
# #         total_time += travel

# #     return total_time + (total_lateness * LATENESS_WEIGHT)
# def calculate_fitness(chromosome, source_idx, dests, dur_matrix, loc_map):
#     """
#     Fitness = Total Duration (hours) + (Lateness * Weight)
#     """
#     total_time = 0.0          # hours
#     total_lateness = 0.0      # hours
#     current_time = 0.0        # hours

#     # Source -> First node
#     first_node = chromosome[0]
#     # leg_time_hr = dur_matrix[source_idx][first_node] / 3600.0
#     leg_time_hr = (dur_matrix[source_idx][first_node] or 0.0) / 3600.0

#     current_time += leg_time_hr
#     total_time += leg_time_hr

#     for i in range(len(chromosome)):
#         curr_node = chromosome[i]

#         dest_obj = next((d for d in dests if loc_map[d.id] == curr_node), None)

#         if dest_obj:
#             if current_time > dest_obj.deadline_hours:
#                 total_lateness += (current_time - dest_obj.deadline_hours)

#             service_hrs = dest_obj.service_time_minutes / 60.0
#             current_time += service_hrs
#             total_time += service_hrs

#         # Next travel
#         next_node = chromosome[i + 1] if i < len(chromosome) - 1 else source_idx
#         # leg_time_hr = dur_matrix[curr_node][next_node] / 3600.0
#         leg_time_hr = (dur_matrix[curr_node][next_node] or 0.0) / 3600.0

#         current_time += leg_time_hr
#         total_time += leg_time_hr

#     return total_time + (total_lateness * LATENESS_WEIGHT)


# def tournament_selection(scored_population, k=3):
#     candidates = random.sample(scored_population, k)
#     candidates.sort(key=lambda x: x[0])
#     return candidates[0][1] # Return chromosome of best candidate

# def order_crossover(parent1, parent2):
#     """
#     OX1 Crossover: Preserves relative order of cities.
#     Critical for TSP/VRPTW to avoid invalid routes.
#     """
#     size = len(parent1)
#     start, end = sorted(random.sample(range(size), 2))
    
#     child = [-1] * size
#     child[start:end+1] = parent1[start:end+1]
    
#     # Fill remaining spots from Parent2
#     p2_index = 0
#     for i in range(size):
#         if child[i] == -1:
#             while parent2[p2_index] in child:
#                 p2_index += 1
#             child[i] = parent2[p2_index]
            
#     return child

# def mutate(chromosome):
#     """Swap Mutation"""
#     idx1, idx2 = random.sample(range(len(chromosome)), 2)
#     chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]

# # def generate_report(route_indices, dests, source, dist_m, dur_m, loc_names, loc_map):
# #     total_dist = 0
# #     total_time = 0
# #     schedule = []
# #     current_time = 0.0
    
# #     # Start
# #     schedule.append({
# #         "stop_id": source.id,
# #         "stop_name": source.name,
# #         "arrival_time": 0.0,
# #         "departure_time": 0.0,
# #         "lat": source.lat,
# #         "lon": source.lon,
# #         "status": "START"
# #     })

# #     for i in range(len(route_indices)-1):
# #         u, v = route_indices[i], route_indices[i+1]
# #         travel = dur_m[u][v]
# #         dist = dist_m[u][v]
# #         arrival = current_time + travel
        
# #         dest = next((d for d in dests if loc_map[d.id] == v), None)
        
# #         status = "OK"
# #         service = 0.0
# #         name = source.name
# #         lat, lon = source.lat, source.lon
        
# #         if dest:
# #             service = (dest.service_time_minutes / 60.0)
# #             name = dest.name
# #             lat, lon = dest.lat, dest.lon
# #             if arrival > dest.deadline_hours:
# #                 late_by = round(arrival - dest.deadline_hours, 1)
# #                 status = f"LATE (+{late_by}h)"
# #         else:
# #             status = "END"
            
# #         departure = arrival + service
        
# #         schedule.append({
# #             "stop_id": loc_names[v],
# #             "stop_name": name,
# #             "arrival_time": round(arrival, 2),
# #             "departure_time": round(departure, 2),
# #             "lat": lat,
# #             "lon": lon,
# #             "status": status
# #         })
        
# #         total_dist += dist
# #         total_time += (travel + service)
# #         current_time = departure
        
# #     return [loc_names[i] for i in route_indices], schedule, total_dist, total_time
# def generate_report(route_indices, dests, source, dist_m, dur_m, loc_names, loc_map):
#     total_dist = 0.0     # km
#     total_time = 0.0     # hours
#     schedule = []
#     current_time = 0.0   # hours

#     schedule.append({
#         "stop_id": source.id,
#         "stop_name": source.name,
#         "arrival_time": 0.0,
#         "departure_time": 0.0,
#         "lat": source.lat,
#         "lon": source.lon,
#         "status": "START"
#     })

#     for i in range(len(route_indices) - 1):
#         u, v = route_indices[i], route_indices[i + 1]

#         travel_hr = dur_m[u][v] / 3600.0
#         dist_km = dist_m[u][v]

#         arrival = current_time + travel_hr

#         dest = next((d for d in dests if loc_map[d.id] == v), None)

#         service = 0.0
#         status = "OK"
#         name = source.name
#         lat, lon = source.lat, source.lon

#         if dest:
#             service = dest.service_time_minutes / 60.0
#             name = dest.name
#             lat, lon = dest.lat, dest.lon

#             if arrival > dest.deadline_hours:
#                 late_by = round(arrival - dest.deadline_hours, 2)
#                 status = f"LATE (+{late_by}h)"
#         else:
#             status = "END"

#         departure = arrival + service

#         schedule.append({
#             "stop_id": loc_names[v],
#             "stop_name": name,
#             "arrival_time": round(arrival, 2),
#             "departure_time": round(departure, 2),
#             "lat": lat,
#             "lon": lon,
#             "status": status
#         })

#         total_dist += dist_km
#         total_time += (travel_hr + service)
#         current_time = departure

#     return [loc_names[i] for i in route_indices], schedule, total_dist, total_time
# solver/genetic.py
import random
import time
from typing import List, Tuple
from models import Location, Destination
from utils.index_map import IndexMap

# GA params (you can tune or expose)
POPULATION_SIZE = 30        # reduce a bit for stability
ELITISM_COUNT = 4
MUTATION_RATE = 0.2
GENERATIONS = 200
TIME_LIMIT_SEC = 3.0

# weights (kept but we use lexicographic tuple)
LATENESS_WEIGHT = 1.0   # not used to combine, but kept if you want scalar fallback
PRIORITY_WEIGHT = 1.0

def solve_genetic(source: Location, destinations: List[Destination],
                  dist_matrix: List[List[float]], dur_matrix: List[List[float]],
                  index_map: IndexMap, initial_route_ids: List[str] = None) -> Tuple[List[str], List[dict], float, float]:

    start_time = time.time()
    end_time = start_time + TIME_LIMIT_SEC

    # Build helper maps
    source_idx = index_map.idx(source.id)
    dest_indices = [index_map.idx(d.id) for d in destinations]
    dest_by_index = { index_map.idx(d.id): d for d in destinations }

    # population of permutations of destination indices
    population = []

    if initial_route_ids:
        seed_route = [index_map.idx(rid) for rid in initial_route_ids if rid != source.id]
        if len(seed_route) == len(dest_indices):
            population.append(seed_route)

    while len(population) < POPULATION_SIZE:
        indiv = dest_indices[:]
        random.shuffle(indiv)
        population.append(indiv)

    best_chrom = None
    best_fitness = (float('inf'), float('inf'), float('inf'))

    # Use time-limit primary. Also cap by generations as secondary safety.
    gen = 0
    while time.time() < end_time and gen < GENERATIONS:
        gen += 1

        scored_pop = []
        for chrom in population:
            fitness = calculate_fitness(chrom, source_idx, dest_by_index, dur_matrix, index_map)
            # fitness is a tuple: (lateness_hours, priority_penalty, total_time_hours)
            scored_pop.append((fitness, chrom))
            if fitness < best_fitness:
                best_fitness = fitness
                best_chrom = chrom[:]

        # sort lexicographically by tuple automatically
        scored_pop.sort(key=lambda x: x[0])

        # elitism
        next_gen = [x[1] for x in scored_pop[:ELITISM_COUNT]]

        # breeding
        while len(next_gen) < POPULATION_SIZE:
            parent1 = tournament_selection(scored_pop)
            parent2 = tournament_selection(scored_pop)
            child = order_crossover(parent1, parent2)
            if random.random() < MUTATION_RATE:
                mutate(child)
            next_gen.append(child)

        population = next_gen

    if best_chrom is None:
        best_chrom = population[0]

    final_indices = [source_idx] + best_chrom + [source_idx]

    # generate_report is same as before but expects index_map (see later)
    return generate_report(final_indices, list(dest_by_index.values()), source, dist_matrix, dur_matrix, index_map)

# --- fitness now returns a lexicographic tuple ---
def calculate_fitness(chromosome, source_idx, dest_by_index, dur_matrix, index_map):
    """
    Return (total_lateness_hours, priority_penalty, total_time_hours)
    - total_lateness_hours: sum of hours late at stops
    - priority_penalty: integer (inversion / ordering penalty)
    - total_time_hours: total route time (hours)
    """

    total_time = 0.0
    total_lateness = 0.0
    current_time = 0.0

    # travel source -> first
    if not chromosome:
        return (0.0, 0, 0.0)

    first = chromosome[0]
    travel_sec = dur_matrix[source_idx][first] if dur_matrix[source_idx][first] is not None else 0.0
    travel_hr = travel_sec / 3600.0
    current_time += travel_hr
    total_time += travel_hr

    # iterate stops
    for i, curr_idx in enumerate(chromosome):
        dest_obj = dest_by_index.get(curr_idx)
        if dest_obj:
            # lateness
            if current_time > dest_obj.deadline_hours:
                total_lateness += (current_time - dest_obj.deadline_hours)
            # service
            service_hr = dest_obj.service_time_minutes / 60.0
            current_time += service_hr
            total_time += service_hr
        # travel to next
        next_idx = chromosome[i+1] if i < len(chromosome)-1 else source_idx
        travel_sec = dur_matrix[curr_idx][next_idx] if dur_matrix[curr_idx][next_idx] is not None else 0.0
        travel_hr = travel_sec / 3600.0
        current_time += travel_hr
        total_time += travel_hr

    # priority penalty: count inversions in priority ordering
    # lower priority number == higher importance (1 is highest)
    priority_penalty = 0
    priorities = [dest_by_index[idx].priority for idx in chromosome]
    # count how many times a larger-numbered priority appears before a smaller-numbered one
    for i in range(len(priorities)):
        for j in range(i+1, len(priorities)):
            if priorities[i] > priorities[j]:
                priority_penalty += (priorities[i] - priorities[j])

    # Return lexicographic tuple
    return (round(total_lateness, 6), priority_penalty, round(total_time, 6))


def tournament_selection(scored_population, k=3):
    candidates = random.sample(scored_population, k)
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]

def order_crossover(parent1, parent2):
    size = len(parent1)
    if size < 2:
        return parent1[:]
    start, end = sorted(random.sample(range(size), 2))
    child = [-1]*size
    child[start:end+1] = parent1[start:end+1]
    p2i = 0
    for i in range(size):
        if child[i] == -1:
            while parent2[p2i] in child:
                p2i += 1
            child[i] = parent2[p2i]
    return child

def mutate(chromosome):
    if len(chromosome) < 2:
        return
    i, j = random.sample(range(len(chromosome)), 2)
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]

# generate_report adapted below (use index_map); keep as your existing generate_report but replace loc_names usage with index_map.ids
def generate_report(route_indices, dests, source, dist_m, dur_m, index_map):
    total_dist = 0.0
    total_time = 0.0
    schedule = []
    current_time = 0.0

    schedule.append({
        "stop_id": source.id,
        "stop_name": source.name,
        "arrival_time": 0.0,
        "departure_time": 0.0,
        "lat": source.lat,
        "lon": source.lon,
        "status": "START"
    })

    for i in range(len(route_indices)-1):
        u, v = route_indices[i], route_indices[i+1]
        travel_hr = (dur_m[u][v] or 0.0) / 3600.0
        dist_km = dist_m[u][v] if dist_m and dist_m[u][v] is not None else 0.0
        arrival = current_time + travel_hr

        # find dest if it's in dests using index_map.id(v)
        dest_obj = next((d for d in dests if d.id == index_map.id(v)), None)

        service_hr = 0.0
        status = "OK"
        name = source.name
        lat, lon = source.lat, source.lon

        if dest_obj:
            service_hr = dest_obj.service_time_minutes / 60.0
            name = dest_obj.name
            lat, lon = dest_obj.lat, dest_obj.lon
            if arrival > dest_obj.deadline_hours:
                status = f"LATE (+{round(arrival - dest_obj.deadline_hours,2)}h)"
        else:
            status = "END"

        departure = arrival + service_hr

        schedule.append({
            "stop_id": index_map.id(v),
            "stop_name": name,
            "arrival_time": round(arrival, 2),
            "departure_time": round(departure, 2),
            "lat": lat,
            "lon": lon,
            "status": status
        })

        total_dist += dist_km
        total_time += (travel_hr + service_hr)
        current_time = departure

    return [index_map.id(i) for i in route_indices], schedule, total_dist, total_time
