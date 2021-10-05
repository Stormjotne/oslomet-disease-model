import numpy as np
import matplotlib.pyplot as plt
import cv2



world_size = 1000
world = np.zeros((world_size,world_size,3))
world_map = np.zeros((world_size,world_size))



#Small ClassRoom
world_map[200:500,300:303] = 20 #Left Wall
world_map[200:500,600:603] = 20 #Right Wall

world_map[197:201,300:603] = 20 #Top Wall
world_map[500:503,300:603] = 20 #Bottom Wall

#Desks

#Teacher Desk and Middle Row
world_map[250:265,415:486] = 20

world_map[325:340,415:486] = 20
world_map[375:390,415:486] = 20
world_map[425:440,415:486] = 20

#Left side

world_map[325:340,335:386] = 20
world_map[375:390,335:386] = 20
world_map[425:440,335:386] = 20

#Right Side

world_map[325:340,515:566] = 20
world_map[375:390,515:566] = 20
world_map[425:440,515:566] = 20

#Door
world_map[450:475,600:603] = 0



world_map[world_size-1,:] = 20
world_map[world_size-2,:] = 20
world_map[world_size-3,:] = 20


world_map[0,:] = 20
world_map[1,:] = 20
world_map[2,:] = 20

world_map[world_size-1,:] = 20
world_map[world_size-2:,:] = 20
world_map[world_size-3:,:] = 20





D3_world_map = np.repeat(world_map[:,:,np.newaxis],3,axis = 2)

nr_of_agents = 1000
agent_list_infected = np.random.rand(nr_of_agents)>1
agent_list_infected[0] = 1
agent_list_susceptible = np.ones(nr_of_agents)


positions = np.random.rand(2,nr_of_agents)*world_size
infected_positions = np.where(agent_list_infected == 1)

velocity = (np.random.rand(2,nr_of_agents)-0.5)*2
velocity_length = np.linalg.norm(velocity, ord = 2, axis = 0)

world[positions[0].astype(np.int32), positions[1].astype(np.int32),:] = 10

infection_range = 3
velocity_range = 10
attraction_range = 20
dispersion_range = 5

max_speed = 3

nr_of_infected = []

plt.title("Current positions")
plt.xlabel("x positions")
plt.ylabel("y positions")
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

        agent_list_infected[infection_cases[1, infections_where]] = 1
        agent_list_susceptible[infection_cases[1, infections_where]] = 0
    if dispersion_cases.shape[1] >= 1:
        # This would be where you implement social distancing as a force moving agent apart.
        # This is done in BOID similations so look into that.

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

    #im = cv2.imread()
    #cv2.imshow('frame', im)

    scale = 0
    dim = (720,720)

    #cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    world_resized = cv2.resize(world, dim, interpolation=cv2.INTER_AREA)


    cv2.imshow('frame', world_resized)

    #cv2.resizeWindow("frame", 1280, 720)

    #plt.pause(0.05)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

