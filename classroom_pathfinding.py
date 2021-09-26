import random

import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
from pathfinding import make_grid, find_path
from constants import world_size

# world size, 300 for single class room view, 500/1000 for more building space
world = np.zeros((world_size, world_size, 3))
world_map = np.zeros((world_size, world_size))
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


nr_of_agents = 12  # current max 42

agent_list_infected = np.random.rand(nr_of_agents) > 1
agent_list_infected[0] = 1
agent_list_susceptible = np.ones(nr_of_agents)


positions = np.random.rand(2, nr_of_agents)*world_size




infected_positions = np.where(agent_list_infected == 1)

velocity = (np.random.rand(2, nr_of_agents)-0.5)*2
velocity_length = np.linalg.norm(velocity, ord=2, axis=0)

world[positions[0].astype(np.int32), positions[1].astype(np.int32), :] = 10

infection_range = 3
velocity_range = 10
attraction_range = 20
dispersion_range = 5

max_speed = 2

nr_of_infected = []

plt.title("Current positions")
plt.xlabel("x positions")
plt.ylabel("y positions")

destinations = [[120, 120, 120, 120, 120, 120, 145, 145, 145, 145, 145, 145, 145, 145, 145, 170, 170, 170, 170, 170, 170
                    , 170, 170, 170, 205, 205, 205, 205, 205, 205, 205, 205, 205, 230, 230, 230, 230, 230, 230, 230, 230, 230],
                [85, 95, 145, 155, 205, 215, 80, 90, 100, 140, 150, 160, 200, 210, 220, 80, 90, 100, 140, 150, 160, 200,
                 210, 220, 80, 90, 100, 140, 150, 160, 200, 210, 220, 80, 90, 100, 140, 150, 160, 200, 210, 220]]

path = []

def calculate_path(nr_of_agents,grid,world_map,world_size,positions,destinations):
    p = []

    for i in range(nr_of_agents):
        p.append([])
        p[i] = find_path(grid, world_map, world_size, positions[0][i], positions[1][i], destinations[0][i], destinations[1][i])
    return p

random_movement = 1
count = 0
while True:
    #random movement:
    if random_movement == 1:


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

        # wall interaction
            for i0 in range(nr_of_agents):
                wall_perception = world_map[
                      (positions[0, i0] - max_speed).astype(np.int32):(positions[0, i0] + max_speed + 1).astype(
                          np.int32),
                      (positions[1, i0] - max_speed).astype(np.int32):(positions[1, i0] + max_speed + 1).astype(
                          np.int32)]
                wall_location = np.array(np.where(wall_perception > 0))
    # subtract max speed to make the values relative to the center
                wall_location -= max_speed

                velocity[:, i0] -= np.sum(wall_location, 1) * 10

            velocity += (np.random.rand(2, nr_of_agents) - 0.5) * 2
            velocity_length[:] = np.linalg.norm(velocity, ord=2, axis=0)
            velocity *= max_speed / velocity_length

            positions += velocity
            count += 1
            if count == 80:
                random_movement = 0

    if random_movement == 0:
        if not path:
            path = calculate_path(nr_of_agents,grid,world_map,world_size,positions,destinations)
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

    dim = (600, 600)

    world_resized = cv2.resize(world, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow('frame', world_resized)

    time.sleep(0.05)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
