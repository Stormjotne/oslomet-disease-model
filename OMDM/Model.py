"""

"""
import pickle
from random import random, choice
import numpy as np
import cv2
import time
import os.path

from OMDM.Maps import create_map, create_map_from_img
from OMDM.Path import make_grid, find_path
from OMDM.Campus import Campus


class Model:
    """
    Implement the Agent-based Model in this class.
    """
    def __init__(self, parameters, normalized=True, static_population=36, visualize=False):
        """
        Put any declarations of object fields/variables in this method.
        :param parameters:
        :type parameters:
        :param normalized:
        :type normalized:
        :param static_population:
        :type static_population:
        """
        #   OpenCV Visualization for testing.
        self.visualize = visualize
        
        #   Model outputs
        self.number_currently_infected = 0
        self.infected_history = []
        self.number_total_infected = 0
        #   Model outputs end here.
        
        #   Parameters controlled by the Evolutionary Algorithm
        #   Population (Number of Agents) (Can be static for testing)
        self.number_of_agents = static_population
        self.social_distancing = 0
        self.hand_hygiene = 0
        self.respiratory_hygiene = 0
        self.face_masks = 0
        self.face_shields = 0
        self.key_object_disinfection = 0
        self.surface_disinfection = 0
        self.ventilation_of_indoor_spaces = 0
        #   These parameters are medium priority.
        self.face_touching_avoidance = 0
        #   These parameters are low priority.
        self.test_based_screening = 0
        self.vaccination = 0
        self.cohort_size = 0
        self.electives = 0
        #   Interpret input genome
        if normalized:
            self.interpret_normalized_genome(parameters)
        else:
            self.interpret_genome(parameters)
        #   The genome interpretation ends here.
        
        #   Parameters that are static to the model
        #   Taken from constants
        self.world_size = 600
        self.pathfinding_range = 3
        self.proximity_infection_chance = 0.7
        self.surface_infection_chance = 0.05
        self.self_infection_chance = 0.05
        self.mask_protection_rate = 0.5
        #   Taken from classroom_pathfinding and what already existed in this module
        self.max_speed = 2
        self.dispersion_range = 5
        self.attraction_range = 20
        self.velocity_range = 10
        self.infection_range = 3
        self.world = np.zeros((self.world_size, self.world_size, 3))
        self.world_map = np.zeros((self.world_size, self.world_size))
        #   Map that will contain the infectious surfaces.
        self.infected_surfaces_map = np.full((self.world_size, self.world_size), -1)
        #self.world_map = create_map(self.world_map, self.world_size)

        self.world_map,self.infected_surfaces_map,self.classroom_locations = create_map_from_img(self.world_map, self.infected_surfaces_map)

        #   Map that will contain the invisible paths that the agents will follow using vectors
        self.hidden_map = np.zeros((self.world_size, self.world_size))
        self.hidden_map_list = []

        for i in range(len(self.classroom_locations)):
            self.hidden_map_list.append(np.copy(self.hidden_map))

        '''self.hidden_map = np.zeros((self.world_size, self.world_size))
        self.hidden_map_list = []
        
        for i in range(len(self.agent_list_groups)):
            self.hidden_map_list.append([]) 
            for j in range(len(self.group_schedule[i]+1)):
                self.hidden_map_list[i].append(np.copy(self.hidden_map))
        '''


        #   Map that will contain the infectious surfaces.
        #   Surface - door classroom1
        #self.infected_surfaces_map[200:225, 250:251] = 0
        #   Creates the grid used by the pathfinding algorithm
        self.grid = make_grid(self.world_size)
        self.D3_world_map = np.repeat(self.world_map[:, :, np.newaxis], 3, axis=2)
        #   Taken from parameters doc
        self.base_transmission_probability = 0.128
        self.one_meter_transmission_probability = 0.026
        #   Half-assed inferred values
        self.two_meter_transmission_probability = 0.002
        self.four_meter_transmission_probability = 0.0007
        #   Simulation time variables
        #   Time step length in seconds
        self.time_step_length = 60
        #   School day length in hours
        self.day_length = 8
        #   Simulation length in days
        self.simulation_length = 3
        #   Simulation length in time step  (3600/1 seconds per hour)
        self.simulation_time = self.simulation_length * self.day_length * 3600 / self.time_step_length
        #   Virus time-to-live on surfaces in days
        self.virus_ttl_surface = range(6, 9)
        #   virus time-to-live on agent in hours
        self.virus_ttl_agent = range(1, 9)
        #   agent recovery rate
        self.agent_recovery_rate = range(7, 14)
        
        self.agent_list_infected = np.random.rand(self.number_of_agents) > 1
        self.agent_list_infected[5] = 1
        self.agent_list_susceptible = np.zeros(self.number_of_agents,dtype=bool)
        self.agent_list_infected_hands = np.zeros(self.number_of_agents)
        # assign agents into different groups
        self.agent_list_groups = np.zeros(self.number_of_agents, dtype=np.int32)
        # contains the amount of students in groups 1,2,3. The ramainder will end up in the default group 0.
        self.members_per_group = [12,10]
        for i in range(len(self.members_per_group)):
            self.agent_list_groups[np.random.choice(self.number_of_agents, self.members_per_group[i], False)] = i+1

        self.group_schedule = [[2,1,3],[3,2,1],[1,3,2]]
        #self.group_path_list =
        #for i in range(len(self.group_schedule)):


        self.positions = np.zeros((2, self.number_of_agents))
        self.positions[0,:] = Campus.start_point_y
        self.positions[1,:] = Campus.start_point_x
        #   Toggle random movement on or off. 1 for random movement, 0 for individual pathfinding.
        self.agent_movement_mode = np.zeros(self.number_of_agents)
        #   Toggle vector based pathfinding during random movement on or off.
        self.agent_vector_pathfinding = np.ones(self.number_of_agents)
        #   Toggle if an agent has a facemask on or off
        self.agent_face_mask = np.zeros(self.number_of_agents)
        #   Find the amount of agents that wear masks based on the % of the whole population
        self.amount_wearing_masks = int(self.face_masks * self.number_of_agents)
        #   Randomly choose the number of agents
        self.agent_face_mask[np.random.choice(self.number_of_agents, self.amount_wearing_masks, False)] = 1
        #   The start and end node for the invisible path
        #self.hidden_start = np.array([[350,350,150,140], [300,300,100,450]])
        #self.hidden_end = np.array([[150,140,300,300], [100,450,450,100]])
        self.hidden_start = [[],[]]
        self.hidden_end = [[],[]]
        for i in range(len(self.classroom_locations)):

            self.hidden_start[0].append(Campus.start_point_y)
            self.hidden_start[1].append(Campus.start_point_x)
            self.hidden_end[0].append(self.classroom_locations[i][1][1])
            self.hidden_end[1].append(self.classroom_locations[i][1][0])
        print(self.hidden_start)
        print(self.hidden_end)
        # creates the invisible path for vector path-following
        self.hidden_path_list = []
        self.hidden_path = []
        if not os.path.isfile("path_list"):

        #if not self.hidden_path:
            for i in range(len(self.hidden_start[0])):
                self.hidden_path = find_path(self.grid, self.world_map, self.world_size, self.hidden_start[0][i], self.hidden_start[1][i],
                                        self.hidden_end[0][i], self.hidden_end[1][i])
                print(self.hidden_path)
                self.hidden_path_list.append(self.hidden_path)
                # hidden_path_list.append(find_path(grid, world_map, world_size, hidden_start[0][i], hidden_start[1][i], hidden_end[0][i], hidden_end[1][i]))
                print("List: ")
                print(self.hidden_path_list)

            for i in range(len(self.hidden_path_list)):
                for j in range(len(self.hidden_path_list[i])):
                    x1 = self.hidden_path_list[i][j][1]
                    y1 = self.hidden_path_list[i][j][0]
                    self.hidden_map_list[i][y1][x1] = 1 + j

            with open("path_list", 'wb') as f:
                pickle.dump(self.hidden_map_list,f)
        else:
            with open("path_list", 'rb') as f:
                self.hidden_map_list = pickle.load(f)

        self.infected_positions = np.array(np.where(self.agent_list_infected == 1))
        self.infected_positions = np.array(self.positions[:, self.infected_positions])

        self.velocity = np.zeros((2, self.number_of_agents))
        self.velocity_length = np.linalg.norm(self.velocity, ord=2, axis=0)
        # Creating a map for collision avoidance
        self.collision_map = np.zeros((self.world_size, self.world_size))
        # Adding agents to this map
        self.collision_map[self.positions[0].astype(np.int32), self.positions[1].astype(np.int32)] = 10
        #   Unsure if this is current or total
        nr_of_infected = []
        self.path = []
        self.random_movement = 1
        self.count = 0
        #   Creating an array of values to use for spawning agents at every hundred iteration
        ite_between = 20
        self.spawn_array = np.full(self.number_of_agents, None)
        for i in range(self.number_of_agents):
            self.spawn_array[i] = i * ite_between

    def interpret_normalized_genome(self, parameters):
        """
        Interpret values between 0 and 1 to parameters usable in the model.
        :param parameters:
        :type parameters:
        :return:
        :rtype:
        """
        #   Population (Number of Agents)
        #   Can be static for early testing
        #   Should be controlled by the Evolutionary Algorithm later
        #   Checks if the variable was assigned in __init__ already.
        if not self.number_of_agents:
            #   Range 100 - 5000 agents
            self.number_of_agents = 100 + round(parameters["number_of_agents"] * 4900)
        #   Parameters controlled by the Evolutionary Algorithm
        #   Range:  0.1 - 4.1 meters
        self.social_distancing = 0.1 + round(parameters["social_distancing"] * 4, 2)
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        self.hand_hygiene = 0.01 + round(parameters["hand_hygiene"] * 0.99, 2)
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        self.face_masks = 0.01 + round(parameters["face_masks"] * 0.99, 2)
        #   Range:  1/8 - 8/8 hour/school day
        self.key_object_disinfection = (1 + round(parameters["key_object_disinfection"] * 7)) / 8
        #   Range:  1/16 - 8/16 hour/school day
        self.surface_disinfection = (1 + round(parameters["surface_disinfection"] * 7)) / 16
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        self.face_touching_avoidance = 0.01 + round(parameters["face_touching_avoidance"] * 0.99, 2)
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        #   self.face_shields = 0.01 + round(parameters["face_shields"] * 0.99, 2)
        #   Range:  1 - 3600 seconds
        #   self.ventilation_of_indoor_spaces = 1 + round(parameters["ventilation_of_indoor_spaces"] * 3599)
        #   These parameters are medium priority.
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        #   self.respiratory_hygiene = 0.01 + round(parameters["respiratory_hygiene"] * 0.99, 2)
        '''
        self.face_touching_avoidance = parameters["face_touching_avoidance"]
        '''
        #   These parameters are low priority.
        '''
        self.test_based_screening = parameters["test_based_screening"]
        self.vaccination = parameters["vaccination"]
        self.cohort_size = parameters["cohort_size"]
        self.electives = parameters["electives"]
        '''
        
    def interpret_genome(self, parameters):
        """
        @deprecated
        @param parameters:
        @type parameters:
        @return:
        @rtype:
        """
        if not self.number_of_agents:
            self.number_of_agents = parameters["number_of_agents"]
        #   Parameters controlled by the Evolutionary Algorithm
        self.social_distancing = parameters["social_distancing"]
        self.hand_hygiene = parameters["hand_hygiene"]
        self.face_masks = parameters["face_masks"]
        self.key_object_disinfection = parameters["key_object_disinfection"]
        self.surface_disinfection = parameters["surface_disinfection"]
        self.face_touching_avoidance = parameters["face_touching_avoidance"]
        '''
        self.respiratory_hygiene = parameters["respiratory_hygiene"]
        self.face_shields = parameters["face_shields"]
        self.ventilation_of_indoor_spaces = parameters["ventilation_of_indoor_spaces"]
        '''
        #   These parameters are medium priority.
        '''
        self.face_touching_avoidance = parameters["face_touching_avoidance"]
        '''
        #   These parameters are low priority.
        '''
        self.test_based_screening = parameters["test_based_screening"]
        self.vaccination = parameters["vaccination"]
        self.cohort_size = parameters["cohort_size"]
        self.electives = parameters["electives"]
        '''
    
    def placeholder_simulate(self):
        """
        @deprecated
        Just a mathematical model of the disease transmission with evolved parameters.
        :return:
        :rtype:
        """
        step = 0
        while step < self.simulation_time:
            self.number_currently_infected = 0
            current_recovery_rate = choice(self.agent_recovery_rate)
            for agent in range(self.number_of_agents):
                if 0 <= self.social_distancing < 1:
                    if random() < self.base_transmission_probability:
                        self.number_currently_infected += 1
                elif 1 <= self.social_distancing < 2:
                    if random() < self.one_meter_transmission_probability:
                        self.number_currently_infected += 1
                elif 2 <= self.social_distancing < 3:
                    if random() < self.two_meter_transmission_probability:
                        self.number_currently_infected += 1
                elif 3 <= self.social_distancing < 4.1:
                    if random() < self.four_meter_transmission_probability:
                        self.number_currently_infected += 1
                if step % current_recovery_rate == 0:
                    self.number_currently_infected = round(self.number_currently_infected * 0.5)
            self.infected_history.append(self.number_currently_infected)
            self.number_total_infected += (self.number_currently_infected - self.infected_history[step - 1])
            step += 1
        return {"number_currently_infected": self.number_currently_infected,
                    "infected_history": self.infected_history,
                    "number_total_infected": self.number_total_infected,
                    "number_of_agents": self.number_of_agents}

    def calculate_path(self, destinations):
        """
        A function that calculates an individual path for each agent.
        @return:
        @rtype:
        """
        new_path = []
        for i in range(self.number_of_agents):
            new_path.append([])
            new_path[i] = find_path(self.grid, self.world_map, self.world_size, self.positions[0][i],
                self.positions[1][i], destinations[0][i], destinations[1][i])
        return new_path


    def disinfect_surfaces(self, surfaces):
        """
        A functions that removes infection from all surfaces.
        @return:
        @rtype:
        """
        for i in range(len(surfaces[0])):
            y = surfaces[0][i]
            x = surfaces[1][i]
            self.infected_surfaces_map[y][x] = 0
    
        return self.infected_surfaces_map
        
    def simulate(self):
        """
        Run the model simulation with input parameters.
        @return:
        @rtype:
        """
        #   Creating an array of values to use for spawning agents at every hundred iteration
        self.iteration_counter = 0

        # Counting variable for initiating agent spawning at defined position
        spawning_counter = 0
        minute = 0
        hour = 0
        hand_infection_count = 0
        nr_of_infected = []
        while True:

            # Matrices to calculate distances between agents by using positions at each iteration
            p_1 = np.repeat(self.positions[:, :, np.newaxis], self.positions.shape[1], axis=2)
            p_2 = np.rot90(p_1, axes=(1, 2))
            p_1 -= p_2
    
            distances = np.linalg.norm(p_1, axis=0)
            distances[np.arange(self.number_of_agents), np.arange(self.number_of_agents)] = self.infection_range + 20
    
            infection_cases = np.array(np.where(distances < self.infection_range))
            velocity_cases = np.array(np.where(distances < self.velocity_range))
            attraction_cases = np.array(np.where(distances < self.attraction_range))
            dispersion_cases = np.array(np.where(distances < self.dispersion_range))
    
            # looks for infectious surfaces
            infected_surfaces = np.array(np.where(self.infected_surfaces_map >= 0))

            if infection_cases.shape[1] >= 1:
                infections = self.agent_list_infected[infection_cases[0, :]] & \
                    self.agent_list_susceptible[infection_cases[1, :]]
                infections_where = np.array(np.where(infections == True))
    
                if random() <= self.proximity_infection_chance:
                    self.agent_list_infected[infection_cases[1, infections_where]] = 1
                    self.agent_list_susceptible[infection_cases[1, infections_where]] = 0
    
                for i in range(len(infections_where[0])):
        
                    if self.agent_face_mask[infection_cases[1, infections_where[0][i]]] == 1:
                        if random() <= self.proximity_infection_chance:
                            self.agent_list_infected[infection_cases[1, infections_where[0][i]]] = 1
                            self.agent_list_susceptible[infection_cases[1, infections_where[0][i]]] = 0

                        # agent_list_infected[infection_cases[1, infections_where]] = 1
                        # agent_list_susceptible[infection_cases[1, infections_where]] = 0
        
                    if self.agent_face_mask[infection_cases[1, infections_where[0][i]]] == 0:
                        if random() <= self.proximity_infection_chance * (1.0 - self.mask_protection_rate):
                            self.agent_list_infected[infection_cases[1, infections_where[0][i]]] = 1
                            self.agent_list_susceptible[infection_cases[1, infections_where[0][i]]] = 0
            
            if dispersion_cases.shape[1] >= 1:
                #   This would be where you implement social distancing as a force moving agent apart.
                #   This is done in BOID simulations so look into that.
                pass
            if attraction_cases.shape[1] >= 1:
                #   Make agents cluster - again BOIDS
                pass
            if velocity_cases.shape[1] >= 1:
                #   Make agents align their movement - BOIDS
                pass

            #   Random Movement
            if self.random_movement == 1:
                #   Wall and agent interaction
                #   Init infected_surface_perception outside loop scope
                infected_surface_perception = None
                infected_surfaces_location = None
                #   Try to replace nr_of_agents with spawning counter-1
                for i0 in range(self.number_of_agents):
                    wall_perception = self.world_map[
                                      (self.positions[0, i0] - self.max_speed).astype(np.int32):(
                                        self.positions[0, i0] + self.max_speed + 1).astype(
                                          np.int32),
                                      (self.positions[1, i0] - self.max_speed).astype(np.int32):(
                                        self.positions[1, i0] + self.max_speed + 1).astype(
                                          np.int32)]
                    agent_percetion = self.collision_map[
                                      (self.positions[0, i0] - self.dispersion_range).astype(np.int32):(
                                        self.positions[0, i0] + self.dispersion_range + 1).astype(
                                          np.int32),
                                      (self.positions[1, i0] - self.dispersion_range).astype(np.int32):(
                                        self.positions[1, i0] + self.dispersion_range + 1).astype(
                                          np.int32)]
                    infected_surface_perception = self.infected_surfaces_map[
                                                  (self.positions[0, i0] - 1).astype(np.int32):(
                                                          self.positions[0, i0] + 2).astype(
                                                      np.int32),
                                                  (self.positions[1, i0] - 1).astype(np.int32):(
                                                          self.positions[1, i0] + 2).astype(
                                                      np.int32)]
                    #   Looking for values of walls and agents
                    wall_location = np.array(np.where(wall_perception == 20))
                    agent_location = np.array(np.where(agent_percetion == 10))

                    infected_surfaces_location = np.array(np.where(infected_surface_perception >= 0))
                    #   Subtract max speed to make the values relative to the center
                    wall_location -= self.max_speed
                    agent_location -= self.dispersion_range
                    infected_surfaces_location -= 1

                    if len(infected_surfaces_location[0]) > 0:
                        if self.agent_list_infected[i0] == 1:
                            for i in range(len(infected_surfaces_location[0])):
                                y = self.positions[0][i0].astype(np.int32) + infected_surfaces_location[0][i]
                                x = self.positions[1][i0].astype(np.int32) + infected_surfaces_location[1][i]
                                self.infected_surfaces_map[y][x] += 1
                        if self.agent_list_infected[i0] == 0:
                            virus_amount = int(np.amax(infected_surface_perception, initial=0) / 2)
                            if random() <= (self.surface_infection_chance * virus_amount):
                                self.agent_list_infected_hands[i0] = virus_amount
                    if np.any(self.agent_list_infected_hands > 0):
                        infected_hands = np.array(np.where(self.agent_list_infected_hands > 0))
                        for agent in infected_hands[0]:
                            if random() <= self.self_infection_chance * self.agent_list_infected_hands[agent]:
                                self.agent_list_infected[agent] = 1
                                self.agent_list_susceptible[agent] = 0
                    
                    #   Hidden path interaction
                    path_location = np.zeros((2, 1))
    
                    if self.agent_vector_pathfinding[i0] == 1:
                        hidden_path_perception = self.hidden_map_list[self.agent_list_groups[i0]][
                                          (self.positions[0, i0] - self.pathfinding_range).astype(np.int32):(
                                                      self.positions[0, i0] + self.pathfinding_range + 1).astype(
                                              np.int32),
                                          (self.positions[1, i0] - self.pathfinding_range).astype(np.int32):(
                                                      self.positions[1, i0] + self.pathfinding_range + 1).astype(
                                              np.int32)]
                        #   Print(hidden_path_perception)
                        #   The initial value should fix a rare error where the array was empty
                        highest_value = np.amax(hidden_path_perception, initial=1)
                        if highest_value != 0:
                            path_location = np.array(np.where(hidden_path_perception == highest_value))
                            path_location -= self.pathfinding_range

                    if self.count == 300:
                        '''self.hidden_path_list[0].reverse()
                        self.hidden_path_list[1].reverse()
                        #print("Hellllo")
                        # np.where(agent_list_groups==0,agent_list_groups,2)
                        # np.where(agent_list_groups==1,agent_list_groups,3)

                        for i in range(len(self.hidden_path_list)):
                            for j in range(len(self.hidden_path_list[i])):
                                x1 = self.hidden_path_list[i][j][1]
                                y1 = self.hidden_path_list[i][j][0]
                                self.hidden_map_list[i][y1][x1] = 1 + j'''
                    #   Needs attention
                    #   Subtracting velocity from agent i0 equals to sum of agent_location array
                    self.velocity[:, i0] -= np.sum(agent_location, 1) * 8
                    #   Subtracting velocity from agent i0 equals to sum of wall_location array
                    self.velocity[:, i0] -= np.sum(wall_location, 1) * 4
                    self.velocity[:, i0] += np.sum(path_location, 1) * 30

                self.velocity += (np.random.rand(2, self.number_of_agents) - 0.5) * 0.5
                self.velocity_length[:] = np.linalg.norm(self.velocity, ord=2, axis=0)
                self.velocity *= self.max_speed / self.velocity_length

                #   Cancel the velocity change for agents who are not supposed to move randomly
                cancel_velocity = np.array(np.where(self.agent_movement_mode == 1))
                for vel in cancel_velocity:
                    self.velocity[:, vel] = 0

                # Cancel velocity when located at start position
                check_y = np.array(np.where(self.positions[0] == Campus.start_point_y))
                check_x = np.array(np.where(self.positions[1] == Campus.start_point_x))
                stay = []
                for i in check_y[0]:
                    if i in check_x[0]:
                        # print(i)
                        stay += [i]
                self.velocity[:, stay] = 0
                # Use the same array so that agents cannot be infected when located at start/finish
                self.agent_list_susceptible[:] = True
                self.agent_list_susceptible[stay] = False

                #
                if np.any(self.spawn_array[:] == self.iteration_counter):
                    self.velocity[0, spawning_counter] = 0
                    self.velocity[1, spawning_counter] = -1
                    spawning_counter = spawning_counter + 1
                    #print(spawning_counter)

                # update all agent positions with velocity
                self.positions += self.velocity

                #   Change random movement to 0 after x turns
                #print(self.count)
                self.count += 1
                if self.count == 200:
                    self.random_movement = 1



            # if the agent is supposed to follow an individual direct path
            if self.random_movement == 0:
                if not self.path:
                    #   Update for new maps
                    self.path = self.calculate_path(Campus.small_classroom_destinations)
                for i in range(self.number_of_agents):
                    if self.path[i]:
                        x1 = self.path[i][0][1]
                        y1 = self.path[i][0][0]
                        self.positions[0][i] = y1
                        self.positions[1][i] = x1
                        self.path[i].pop(0)
            # here dealing with agents moving outside the world
            above_world_size = np.array(np.where(self.positions > self.world_size))
            below_world_size = np.array(np.where(self.positions < 0))

            self.positions[above_world_size[0, :], above_world_size[1, :]] = 0
            self.positions[below_world_size[0, :], below_world_size[1, :]] = self.world_size - 1
            self.world[:, :, :] = self.D3_world_map

            self.world[self.positions[0].astype(np.int32), self.positions[1].astype(np.int32), :] = 10
            infected_positions = np.array(np.where(self.agent_list_infected == 1))
            infected_positions = np.array(self.positions[:, infected_positions])
            # print(infected_positions)
            self.world[infected_positions[0].astype(np.int32), infected_positions[1].astype(np.int32), 0:2] = 0

            #   Replaced old infection summary
            #   nr_of_infected.append(np.sum(self.agent_list_infected))
            self.number_currently_infected = np.sum(self.agent_list_infected)
            self.infected_history.append(self.number_currently_infected)
            #   Needs attention
            self.number_total_infected += (self.number_currently_infected - self.infected_history[self.iteration_counter - 1])

            #   Erasing old positions
            self.collision_map[:, :] = 0
            # Updating new positions
            self.collision_map[self.positions[0].astype(np.int32), self.positions[1].astype(np.int32)] = 1
            
            #   Plus operation for while loop was moved from the top
            self.iteration_counter = self.iteration_counter + 1
            # if statement true-> finish simulation
            if self.iteration_counter == self.simulation_time:
                print(self.iteration_counter)
                break;
            #   OpenCV Visualization
            if self.visualize:
                dim = (600, 600)
                world_resized = cv2.resize(self.world, dim, interpolation=cv2.INTER_AREA)
                cv2.imshow('frame', world_resized)
    
                #   time.sleep(0.05)
                #   print(time.time() - beginning_time)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        if self.visualize:
            cv2.destroyAllWindows()


        return {"number_currently_infected": self.number_currently_infected,
                "infected_history": self.infected_history,
                "number_total_infected": self.number_total_infected,
                "number_of_agents": self.number_of_agents}

#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    from OMDM.Individual import Individual
    from OMDM.Fitness import population_spread_fitness
    new_individual = Individual(0.2, genome_length=7)
    new_model = Model(new_individual.genome.genome, visualize=True)
    new_individual.phenotype = new_model.simulate()
    print(new_individual.phenotype)
    new_individual.fitness = population_spread_fitness(new_individual.phenotype, 5000, 1, 1)
    print(new_individual.fitness)
    