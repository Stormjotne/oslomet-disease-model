import random

import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
#import constants
from pathfinding import make_grid, find_path
from constants import world_size, pathfinding_range, proximity_infection_chance, surface_infection_chance,self_infection_chance,mask_protection_rate
from variables import wears_mask_percentage
from small_classroom_destinations import destinations
from hardcoded_classrooms import create_map

# world size, 300 for single class room view, 500/1000 for more building space
world = np.zeros((world_size, world_size, 3))

world_map = np.zeros((world_size, world_size))
world_map = create_map(world_map)

# map that will contain the invisible paths that the agents will follow using vectors
hidden_map = np.zeros((world_size, world_size))

# map that will contain the infectious surfaces.
infected_surfaces_map = np.full((world_size, world_size),-1)

#Surface - door classroom1
infected_surfaces_map[200:225, 250:251] = 0


# creates the grid used by the pathfinding algorithm
grid = make_grid(world_size)


D3_world_map = np.repeat(world_map[:, :, np.newaxis], 3, axis=2)


nr_of_agents = 25  # current max 42

agent_list_infected = np.random.rand(nr_of_agents) > 1
agent_list_infected[0] = 1
agent_list_susceptible = np.ones(nr_of_agents)

agent_list_infected_hands = np.zeros(nr_of_agents)

positions = np.random.rand(2, nr_of_agents)*world_size
#positions = np.array([[160.0,250.0], [255.0,260]])

positions[0][0] = 100.0
positions[1][0] = 30.0

positions[0][4] = 101.0
positions[1][4] = 31.0

positions[0][7] = 102.0
positions[1][7] = 29.0

# toggle random movement on or off. 1 for random movement, 0 for individual pathfinding.
agent_movement_mode = np.zeros(nr_of_agents)
#agent_movement_mode[1] = 1

# toggle vector based pathfinding during random movement on or off.
agent_vector_pathfinding = np.ones(nr_of_agents)
# agent_vector_pathfinding[:] = 0

# toggle if an agent has a facemask on or off
agent_face_mask = np.zeros(nr_of_agents)
# find the amount of agents that wear masks based on the % of the whole population
amount_wearing_masks = int(wears_mask_percentage * nr_of_agents)
# randomly choose the amount
agent_face_mask[np.random.choice(nr_of_agents,amount_wearing_masks,False)] = 1

#agent_face_mask[4] = 1

# the start and end node for the invisible path
hidden_start = np.array([[100], [30]])

# hidden_end = np.array([[270], [150]])
hidden_end = np.array([[120], [110]])


# creates the invisible path for vector path-following
hidden_path = []

if not hidden_path:
    hidden_path = find_path(grid, world_map, world_size, hidden_start[0][0], hidden_start[1][0], hidden_end[0][0], hidden_end[1][0])

#print(hidden_path)
#print(len(hidden_path))


for i in range(len(hidden_path)):

    x1 = hidden_path[i][1]
    y1 = hidden_path[i][0]
    hidden_map[y1][x1] = 1+i


infected_positions = np.array(np.where(agent_list_infected == 1))
infected_positions = np.array(positions[:, infected_positions])
#print(infected_positions)

velocity = (np.random.rand(2, nr_of_agents)-0.5)*2
velocity_length = np.linalg.norm(velocity, ord=2, axis=0)

#Adding agents to map for wall interaction
world[positions[0].astype(np.int32), positions[1].astype(np.int32), :] = 10


#Creating a map for collision avoidance
collision_map= np.zeros((world_size,world_size))

#Adding agents to this map
collision_map[positions[0].astype(np.int32), positions[1].astype(np.int32)] = 10



infection_range = 3
velocity_range = 10
attraction_range = 20
dispersion_range = 5

max_speed = 2

nr_of_infected = []

plt.title("Current positions")
plt.xlabel("x positions")
plt.ylabel("y positions")

path = []


# a function that calculates an individual path for each agent.
def calculate_path(nr_of_agents, grid, world_map, world_size, positions, destinations):

    p = []

    for i in range(nr_of_agents):
        p.append([])
        p[i] = find_path(grid, world_map, world_size, positions[0][i], positions[1][i], destinations[0][i], destinations[1][i])
    return p


random_movement = 1
count = 0
minute = 0
hour = 0
hand_infection_count = 0

while True:


    p_1 = np.repeat(positions[:, :, np.newaxis], positions.shape[1], axis=2)
    p_2 = np.rot90(p_1, axes=(1, 2))
    p_1 -= p_2


    distances = np.linalg.norm(p_1, axis=0)
    distances[np.arange(nr_of_agents), np.arange(nr_of_agents)] = infection_range + 20

    infection_cases = np.array(np.where(distances < infection_range))
    velocity_cases = np.array(np.where(distances < velocity_range))
    attraction_cases = np.array(np.where(distances < attraction_range))
    dispersion_cases = np.array(np.where(distances < dispersion_range))

    # looks for infectious surfaces
    infected_surfaces = np.array(np.where(infected_surfaces_map >= 0))


    #print(infected_positions)
    #print(infected_surfaces)
    # temporary for loop, need optimilization.
    # finding out if an infected agent has contact with a surface that he can infect.
    '''for i in range(len(infected_surfaces[0])):
        matches = [False]
        if infected_surfaces_map[infected_surfaces[0][i]][infected_surfaces[1][i]] > 0:
            y_component = np.equal(positions[0].astype(np.int32),infected_surfaces[0][i])
            x_component = np.equal(positions[1].astype(np.int32),infected_surfaces[1][i])
            matches = y_component & x_component

        y_component_infected = np.equal(infected_positions[0].astype(np.int32), infected_surfaces[0][i])
        x_component_infected = np.equal(infected_positions[1].astype(np.int32), infected_surfaces[1][i])
        matches_infected = y_component_infected & x_component_infected

        # if there is a match find out which agent/s it is
        if True in matches_infected:
            match_agent_location = np.array(np.where(matches_infected == True))
            # at each agent location increase the surface infection count
            for agent in match_agent_location:
                infected_surfaces_map[infected_positions[0][agent][0][0].astype(np.int32)][infected_positions[1][agent][0][0].astype(np.int32)] += 1


        if True in matches:
            match_agent_location = np.array(np.where(matches == True))
            # at each agent location increase the surface infection count
            for agent in match_agent_location:
                virus_amount = infected_surfaces_map[positions[0][agent][0].astype(np.int32)][positions[1][agent][0].astype(np.int32)]
                if random.random() <= (surface_infection_chance * virus_amount):
                    agent_list_infected_hands[agent] = virus_amount


    #surface_infected_contact = np.array(np.where(infected_surfaces[]))
    #if infected_positions
    #infected_surface_cases =
    # print(distances)
    # print()

    # print(infection_cases.shape)
    if np.any(agent_list_infected_hands > 0):
        infected_hands = np.array(np.where(agent_list_infected > 1))
        for agent in infected_hands:
            if random.random() <= self_infection_chance * agent_list_infected_hands[agent]:
                agent_list_infected[agent] = 1
                agent_list_susceptible[agent] = 0
    '''

    if infection_cases.shape[1] >= 1:
        print(infection_cases)
        print("")
        infections = agent_list_infected[infection_cases[0, :]] == agent_list_susceptible[infection_cases[1, :]]
        print(infections)
        print("")
        infections_where = np.array(np.where(infections == 1))
        print(infections_where)
        print("")
        print("Length: " + str(len(infections_where[0])))
        #print(len(infections_where[0]))
        for i in range(len(infections_where[0])):

            if agent_face_mask[infection_cases[1, infections_where[0][i]]] == 1:
                if random.random() <= proximity_infection_chance:
                    agent_list_infected[infection_cases[1,infections_where[0][i]]] = 1
                    agent_list_susceptible[infection_cases[1, infections_where[0][i]]] = 0

                #agent_list_infected[infection_cases[1, infections_where]] = 1
                #agent_list_susceptible[infection_cases[1, infections_where]] = 0

            if agent_face_mask[infection_cases[1, infections_where[0][i]]] == 0:
                if random.random() <= proximity_infection_chance * (1.0-mask_protection_rate):
                    agent_list_infected[infection_cases[1,infections_where[0][i]]] = 1
                    agent_list_susceptible[infection_cases[1, infections_where[0][i]]] = 0

    if dispersion_cases.shape[1] >= 1:
    # This would be where you implement social distancing as a force moving agent apart.
    # This is done in BOID simulations so look into that.
        pass
    if attraction_cases.shape[1] >= 1:
    # make agents cluster - again BOIDS
        pass
    if velocity_cases.shape[1] >= 1:
    # make agents align their movement - BOIDS
        pass

    # random movement:
    if random_movement == 1:
        # wall and agent interaction
        for i0 in range(nr_of_agents):
            wall_perception = world_map[
                              (positions[0, i0] - max_speed).astype(np.int32):(
                                      positions[0, i0] + max_speed + 1).astype(
                                  np.int32),
                              (positions[1, i0] - max_speed).astype(np.int32):(
                                      positions[1, i0] + max_speed + 1).astype(
                                  np.int32)]
            agent_percetion = collision_map[
                              (positions[0, i0] - dispersion_range).astype(np.int32):(
                                      positions[0, i0] + dispersion_range + 1).astype(
                                  np.int32),
                              (positions[1, i0] - dispersion_range).astype(np.int32):(
                                      positions[1, i0] + dispersion_range + 1).astype(
                                  np.int32)]

            # Looking for values of walls and agents
            wall_location = np.array(np.where(wall_perception == 20))
            agent_location = np.array(np.where(agent_percetion == 10))
            # subtract max speed to make the values relative to the center
            wall_location -= max_speed
            agent_location -= dispersion_range

            # hidden path interaction
            path_location = np.zeros((2, 1))

            if agent_vector_pathfinding[i0] == 1:
                hidden_path_perception = hidden_map[
                                  (positions[0, i0] - pathfinding_range).astype(np.int32):(
                                              positions[0, i0] + pathfinding_range+1).astype(
                                      np.int32),
                                  (positions[1, i0] - pathfinding_range).astype(np.int32):(
                                              positions[1, i0] + pathfinding_range+1).astype(
                                      np.int32)]
                # print(hidden_path_perception)
                # the intitial value should fix a rare error where the array was empty
                highest_value = np.amax(hidden_path_perception, initial=1)
                #path_location = np.zeros((2, 1))

                if highest_value != 0:
                    path_location = np.array(np.where(hidden_path_perception == highest_value))
                    path_location -= pathfinding_range

            #Subtracting velocity from agent i0 equals to sum of agent_location array
            velocity[:, i0] -= np.sum(agent_location, 1) * 5
            # Subtracting velocity from agent i0 equals to sum of wall_location array
            velocity[:, i0] -= np.sum(wall_location, 1) * 10

            velocity[:, i0] += np.sum(path_location, 1) * 30


        velocity += (np.random.rand(2, nr_of_agents) - 0.5) * 2
        velocity_length[:] = np.linalg.norm(velocity, ord=2, axis=0)
        velocity *= max_speed / velocity_length

        # cancel the velocity change for agents who are not supposed to move randomly
        cancel_velocity = np.array(np.where(agent_movement_mode == 1))
        for vel in cancel_velocity:
            velocity[:, vel] = 0

        # update all agent positions with velocity
        positions += velocity

        # change random movement to 0 after x turns
        count += 1
        if count == 200:
            random_movement = 1

    # if the agent is supposed to follow an individual direct path
    if random_movement == 0:
        if not path:
            path = calculate_path(nr_of_agents, grid, world_map, world_size, positions, destinations)
        for i in range(nr_of_agents):

            if path[i]:
                x1 = path[i][0][1]
                y1 = path[i][0][0]
                positions[0][i] = y1
                positions[1][i] = x1
                path[i].pop(0)



    # here dealing with agents moving outside the world
    above_world_size = np.array(np.where(positions > world_size))
    below_world_size = np.array(np.where(positions < 0))

    positions[above_world_size[0, :], above_world_size[1, :]] = 0
    positions[below_world_size[0, :], below_world_size[1, :]] = world_size - 1
    world[:, :, :] = D3_world_map

    world[positions[0].astype(np.int32), positions[1].astype(np.int32), :] = 10
    infected_positions = np.array(np.where(agent_list_infected == 1))
    infected_positions = np.array(positions[:, infected_positions])
    # print(infected_positions)
    world[infected_positions[0].astype(np.int32), infected_positions[1].astype(np.int32), 0:2] = 0
    nr_of_infected.append(np.sum(agent_list_infected))

    # Erasing old positions
    collision_map[:, :] = 0
    # Updating new positions
    collision_map[positions[0].astype(np.int32), positions[1].astype(np.int32)] = 10


    dim = (600, 600)

    world_resized = cv2.resize(world, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow('frame', world_resized)

    time.sleep(0.05)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
