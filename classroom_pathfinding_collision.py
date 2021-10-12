import random

import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
from pathfinding import make_grid, find_path
from constants import world_size, pathfinding_range, proximity_infection_chance
from small_classroom_destinations import destinations

# world size, 300 for single class room view, 500/1000 for more building space
world = np.zeros((world_size, world_size, 3))
world_map = np.zeros((world_size, world_size))

# map that will contain the invisible paths that the agents will follow using vectors
hidden_map = np.zeros((world_size, world_size))

# creates the grid used by the pathfinding algorithm
grid = make_grid(world_size)


# world borders:

# left border
world_map[0:world_size+1, 0:2] = 20
# right border
world_map[0:world_size+1, world_size-1:world_size+1] = 20
# top border
world_map[0:2, 0:world_size+1] = 20
# bottom border
world_map[world_size-1:world_size+1, 0:world_size+1] = 20

# small classroom:

# left wall
world_map[47:254, 47:51] = 20
# right wall
world_map[47:254, 250:254] = 20
# top wall
world_map[47:51, 47:254] = 20
# bottom wall
world_map[250:254, 47:254] = 20

# desks

# teacher desk dimensions x = 30 y = 10
world_map[75:85, 135:165] = 20
# middle row
# short desk dimensions x = 30 y = 10
world_map[105:115, 135:165] = 20
# long desk dimensions x = 40 y = 10
world_map[130:140, 130:170] = 20
world_map[155:165, 130:170] = 20
world_map[190:200, 130:170] = 20
world_map[215:225, 130:170] = 20

# left side
# short desk dimensions x = 30 y = 10
world_map[105:115, 75:105] = 20
# long desk dimensions x = 40 y = 10
world_map[130:140, 70:110] = 20
world_map[155:165, 70:110] = 20
world_map[190:200, 70:110] = 20
world_map[215:225, 70:110] = 20


# right side
# short desk dimensions x = 30 y = 10
world_map[105:115, 195:225] = 20
# long desk dimensions x = 40 y = 10
world_map[130:140, 190:230] = 20
world_map[155:165, 190:230] = 20
world_map[190:200, 190:230] = 20
world_map[215:225, 190:230] = 20

# door
world_map[200:225, 250:254] = 0


D3_world_map = np.repeat(world_map[:, :, np.newaxis], 3, axis=2)


nr_of_agents = 25  # current max 42

agent_list_infected = np.random.rand(nr_of_agents) > 1
agent_list_infected[0] = 1
agent_list_susceptible = np.ones(nr_of_agents)


positions = np.random.rand(2, nr_of_agents)*world_size
#positions = np.array([[100.0], [30.0]])

# toggle random movement on or off. 1 for random movement, 0 for individual pathfinding.
agent_movement_mode = np.zeros(nr_of_agents)
agent_movement_mode[1] = 1

# toggle vector based pathfinding during random movement on or off.
agent_vector_pathfinding = np.ones(nr_of_agents)
# agent_vector_pathfinding[:] = 0

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


infected_positions = np.where(agent_list_infected == 1)

velocity = (np.random.rand(2, nr_of_agents)-0.5)*2
velocity_length = np.linalg.norm(velocity, ord=2, axis=0)

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
    # print(distances)
    # print()

    # print(infection_cases.shape)

    if infection_cases.shape[1] >= 1:
        infections = agent_list_infected[infection_cases[0, :]] == agent_list_susceptible[infection_cases[1, :]]
        infections_where = np.array(np.where(infections == 1))

        if random.random() < proximity_infection_chance:
            agent_list_infected[infection_cases[1, infections_where]] = 1
            agent_list_susceptible[infection_cases[1, infections_where]] = 0

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
        # wall interaction
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

            # Subtracting the sum of distances from velocity of agent i0
            velocity[:, i0] -= np.sum(wall_location, 1) * 10  # This is where a force multiplier can be added
            velocity[:, i0] -= np.sum(agent_location, 1) * 5  # This is where a force multiplier can be added

            velocity[:, i0] += np.sum(path_location, 1) * 30
            # print(velocity)

        velocity += (np.random.rand(2, nr_of_agents) - 0.5) *0.2 #Lower the number, smaller the direction change
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
