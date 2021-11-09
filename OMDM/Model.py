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

#   Genome Interpretation Constants
minimum_population = 100
minimum_distancing = 0.1
maximum_distancing = 4.1
minimum_percentage = 0.01
maximum_percentage = 1.00
frequency_counter = 1
frequency_denominator = 8


class Model:
    """
    Implement the Agent-based Model in this class.
    """
    def __init__(self, parameters, maximum_population, normalized=True, static_population=36, visualize=False):
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
        #   Desired size of agent population
        self.maximum_population = maximum_population
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
        self.iteration_counter = 0
        self.world_size = 600
        self.pathfinding_range = 3
        self.proximity_infection_chance = 0.12
        self.surface_infection_chance = 0.01
        self.self_infection_chance = 0.01
        self.mask_protection_rate = 0.5
        #   Taken from classroom_pathfinding and what already existed in this module
        self.max_speed = 2
        #self.dispersion_range = 5
        self.dispersion_range = int(round(self.social_distancing * 5))

        self.agent_room_counter1 = 0
        self.agent_room_counter2 = 0
        self.agent_room_counter3 = 0
        self.agent_room_counter4 = 0
        self.agent_room_counter5 = 0
        
        if self.dispersion_range == 0:
            self.dispersion_range = 1
        elif self.dispersion_range > 20:
            self.dispersion_range = 20

        self.attraction_range = 20
        self.velocity_range = 10
        self.infection_range = 3
        self.world = np.zeros((self.world_size, self.world_size, 3))
        self.world_map = np.zeros((self.world_size, self.world_size))
        #   Map that will contain the infectious surfaces.
        self.infected_surfaces_map = np.full((self.world_size, self.world_size), -1)
        #self.world_map = create_map(self.world_map, self.world_size)
        if not os.path.isfile("imported_map_information"):

            self.world_map,self.infected_surfaces_map,self.classroom_locations,self.start_location_x,self.start_location_y = create_map_from_img(self.world_map, self.infected_surfaces_map)
            with open("imported_map_information", 'wb') as f:
                Campus.start_point_y = self.start_location_y
                Campus.start_point_x = self.start_location_x
                pickle.dump(self.world_map, f)
                pickle.dump(self.infected_surfaces_map,f)
                pickle.dump(self.classroom_locations,f)
                pickle.dump(self.start_location_x,f)
                pickle.dump(self.start_location_y,f)
        else:
            with open("imported_map_information", 'rb') as f:
                self.world_map = pickle.load(f)
                self.infected_surfaces_map = pickle.load(f)
                self.classroom_locations = pickle.load(f)
                self.start_location_x = pickle.load(f)
                self.start_location_y = pickle.load(f)
                Campus.start_point_y = self.start_location_y
                Campus.start_point_x = self.start_location_x

        #   Map that will contain the invisible paths that the agents will follow using vectors
        self.hidden_map = np.zeros((self.world_size, self.world_size))
        self.hidden_map_list = []

        #self.group_schedule = [[2,1,3],[3,2,1],[1,3,2]]
        self.group_schedule = [[1,4,2],[2,3,0],[4,0,3],[3,2,1],[0,1,4]]



        for i in range(len(self.group_schedule)):
            self.hidden_map_list.append([])
            for j in range(len(self.group_schedule[0])+1):
                self.hidden_map_list[i].append(np.copy(self.hidden_map))


        #for i in range(len(self.classroom_locations)):
         #   self.hidden_map_list.append(np.copy(self.hidden_map))

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
        self.simulation_length = 9
        #   Simulation length in time step  (3600/1 seconds per hour)
        self.simulation_time = self.simulation_length * self.day_length * 3600 / self.time_step_length
        #   Virus time-to-live on surfaces in days
        self.virus_ttl_surface = range(6, 9)
        #   virus time-to-live on agent in hours
        self.virus_ttl_agent = range(1, 9)
        #   agent recovery rate
        self.agent_recovery_rate = range(7, 14)

        # Counting variable for disinfecting surfaces
        self.disinfect_surface_counter = 0
        # Counting the iteration since last self infection check
        self.self_infection_counter = 0
        self.self_infection_check_rate = 100
        
        self.agent_list_infected = np.random.rand(self.number_of_agents) > 1
        self.agent_list_infected[5] = 1
        self.agent_list_susceptible = np.zeros(self.number_of_agents,dtype=bool)
        self.agent_list_infected_hands = np.zeros(self.number_of_agents)

        # sets a percentage of agents to be mindfull of touching their face
        self.agent_face_touching_avoidance = np.zeros(self.number_of_agents)
        self.amount_avoiding = int(self.number_of_agents * self.face_touching_avoidance)
        self.agent_face_touching_avoidance[np.random.choice(self.number_of_agents, self.amount_avoiding, False)] = 1

        # sets a percentage of agents to be periodically washing their hands.
        self.agent_hand_hygine = np.zeros(self.number_of_agents)
        self.amount_hand_hygine = int(self.number_of_agents * self.hand_hygiene)
        self.agent_hand_hygine[np.random.choice(self.number_of_agents, self.amount_hand_hygine, False)] = 1
        self.hand_wash_counter = 0
        # the amount of iterations before handwash
        self.hand_wash_interval = 500
        self.schedule_iteration_counter = 0
        self.next_class_interval = 1200
        self.counter_varible =0


        # assign agents into different groups
        self.agent_list_groups = np.zeros(self.number_of_agents, dtype=np.int32)
        #   contains the amount of students in groups 1,2,3. The ramainder will end up in the default group 0.
        self.agent_ratio_per_group = [0.2,0.3,0.2,0.1]
        self.members_per_group = []

        for i in range(len(self.group_schedule)-1):
            self.members_per_group.append(int(self.agent_ratio_per_group[i]*self.number_of_agents))


        print(self.members_per_group)
        for i in range(len(self.members_per_group)):
            self.agent_list_groups[np.random.choice(self.number_of_agents, self.members_per_group[i], False)] = i+1

        print(self.agent_list_groups)
        #self.group_schedule = [[2,1,3],[3,2,1],[1,3,2]]
        #self.group_path_list =
        #for i in range(len(self.group_schedule)):

        #   2*nr_of_agents array for positioning
        self.positions = np.zeros((2, self.number_of_agents))
        #   Initialize start point in y(0) and x(1) coordinates for all agents
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
        print(self.classroom_locations)
        for i in range(len(self.classroom_locations)):

            self.hidden_start[0].append(Campus.start_point_y)
            self.hidden_start[1].append(Campus.start_point_x)
            self.hidden_end[0].append(self.classroom_locations[i][1][1])
            self.hidden_end[1].append(self.classroom_locations[i][1][0])
        '''print(self.hidden_start)
        print(self.hidden_end)'''
        # creates the invisible path for vector path-following
        self.hidden_path_list = []
        self.hidden_path = []
        self.group_path_list = []
        if not os.path.isfile("path_list"):


            for i in range(len(self.group_schedule)):
                self.hidden_path_list = []

                for j in range(len(self.group_schedule[i])):
                    if j == 0:
                        self.hidden_path = find_path(self.grid, self.world_map, self.world_size,
                                                 Campus.start_point_y,Campus.start_point_x,
                                                 self.classroom_locations[self.group_schedule[i][j]][1][1],
                                                 self.classroom_locations[self.group_schedule[i][j]][1][0],
                                                 )

                        self.hidden_path_list.append(self.hidden_path)

                    print(self.group_schedule[i])
                    if not j+1 >= len(self.group_schedule[i]):
                        print("j:" + str(j))
                        self.hidden_path = find_path(self.grid, self.world_map, self.world_size,
                                             self.classroom_locations[self.group_schedule[i][j]][1][1],
                                             self.classroom_locations[self.group_schedule[i][j]][1][0],
                                             self.classroom_locations[self.group_schedule[i][j+1]][1][1],
                                             self.classroom_locations[self.group_schedule[i][j+1]][1][0]
                                                 )

                        self.hidden_path_list.append(self.hidden_path)
                        print(Campus.start_point_y,Campus.start_point_x)
                    if j+1 == len(self.group_schedule[i]):
                        self.hidden_path = find_path(self.grid, self.world_map, self.world_size,
                                                 self.classroom_locations[self.group_schedule[i][j]][1][1],
                                                 self.classroom_locations[self.group_schedule[i][j]][1][0],
                                                 Campus.start_point_y,Campus.start_point_x
                                                 )

                        self.hidden_path_list.append(self.hidden_path)


                for k in range(len(self.hidden_path_list)):
                    for l in range(len(self.hidden_path_list[k])):
                        x1 = self.hidden_path_list[k][l][1]
                        y1 = self.hidden_path_list[k][l][0]
                        self.hidden_map_list[i][k][y1][x1] = 1 + l

            with open("path_list", 'wb') as f:
                pickle.dump(self.hidden_map_list,f)
        else:
            with open("path_list", 'rb') as f:
                self.hidden_map_list = pickle.load(f)



        #   Variable for storing positions of infected agents

        self.schedule_progress = 0

        self.infected_positions = np.array(np.where(self.agent_list_infected == 1))
        self.infected_positions = np.array(self.positions[:, self.infected_positions])

        self.velocity = np.zeros((2, self.number_of_agents))
        self.velocity_length = np.linalg.norm(self.velocity, ord=2, axis=0)
        # Creating a map for collision avoidance
        self.collision_map = np.zeros((self.world_size, self.world_size))
        # Adding agents to this map
        self.collision_map[self.positions[0].astype(np.int32), self.positions[1].astype(np.int32)] = 10

        self.susceptibility_map = np.zeros((self.world_size, self.world_size))
        self.susceptibility_map[Campus.start_point_y][Campus.start_point_x] = 1
        for i in range(len(self.classroom_locations)):
            self.susceptibility_map[self.classroom_locations[i][1][1]][self.classroom_locations[i][1][0]] = 1

        self.path = []
        self.random_movement = 1
        self.count = 0
        #   Creating an array of values to use for spawning agents at every given iteration
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
            self.number_of_agents = minimum_population + \
                round(parameters["number_of_agents"] * (self.maximum_population - minimum_population))
        #   Parameters controlled by the Evolutionary Algorithm
        #   Range:  0.1 - 4.1 meters
        self.social_distancing = minimum_distancing + \
            round(parameters["social_distancing"] * (maximum_distancing - minimum_distancing), 2)
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        self.hand_hygiene = minimum_percentage + \
            round(parameters["hand_hygiene"] * (maximum_percentage - minimum_percentage), 2)
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        self.face_masks = minimum_percentage + \
            round(parameters["face_masks"] * (maximum_percentage - minimum_percentage), 2)
        #   Range:  1/8 - 8/8 hour/school day
        self.key_object_disinfection = (frequency_counter +
                                        round(parameters["key_object_disinfection"] *
                                        (frequency_denominator - frequency_counter))) / frequency_denominator
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        self.face_touching_avoidance = minimum_percentage + \
            round(parameters["face_touching_avoidance"] * (maximum_percentage - minimum_percentage), 2)
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        #   self.face_shields = 0.01 + round(parameters["face_shields"] * 0.99, 2)
        #   Range:  1 - 3600 seconds
        #   self.ventilation_of_indoor_spaces = 1 + round(parameters["ventilation_of_indoor_spaces"] * 3599)
        #   These parameters are medium priority.
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        #   self.respiratory_hygiene = 0.01 + round(parameters["respiratory_hygiene"] * 0.99, 2)
        #   Range:  1/16 - 8/16 hour/school day
        #   self.surface_disinfection = (1 + round(parameters["surface_disinfection"] * 7)) / 16
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
        self.face_touching_avoidance = parameters["face_touching_avoidance"]
        '''
        self.respiratory_hygiene = parameters["respiratory_hygiene"]
        self.surface_disinfection = parameters["surface_disinfection"]
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
        return {
            "number_currently_infected": self.number_currently_infected,
            "infected_history": self.infected_history,
            "number_total_infected": self.number_total_infected,
            "parameters": {
                "number_of_agents": self.number_of_agents,
                "social_distancing": self.social_distancing,
                "hand_hygiene": self.hand_hygiene,
                "face_masks": self.face_masks,
                "key_object_disinfection": self.key_object_disinfection,
                "face_touching_avoidance": self.face_touching_avoidance
            }
        }

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

    def disinfect_surfaces(self):
        """
        A functions that removes infection from all surfaces.
        @return:
        @rtype:
        """
        surfaces = np.array(np.where(self.infected_surfaces_map>0))

        for i in range(len(surfaces[0])):
            y = surfaces[0][i]
            x = surfaces[1][i]
            self.infected_surfaces_map[y][x] = 0
        return
        #return self.infected_surfaces_map
        
    def simulate(self):
        """
        Run the model simulation with input parameters.
        @return:
        @rtype:
        """

        

        # Counting variable for initiating agent spawning at defined position
        spawning_counter = 0

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
                #   Detect if distance between agents <= social_distansing
                #
                pass
            if attraction_cases.shape[1] >= 1:
                #   Make agents cluster - again BOIDS-Not used!
                pass
            if velocity_cases.shape[1] >= 1:
                #   Make agents align their movement - BOIDS-Not used!
                pass

            #   Random Movement
            if self.random_movement == 1:
                #   Wall and agent interaction
                #   Init infected_surface_perception outside loop scope
                infected_surface_perception = None
                infected_surfaces_location = None

                for i0 in range(self.number_of_agents):
                    wall_perception = self.world_map[                                               #Give agents a percetion equal to max_spedd +1, used to deect walls
                                      (self.positions[0, i0] - self.max_speed).astype(np.int32):(
                                        self.positions[0, i0] + self.max_speed + 1).astype(
                                          np.int32),
                                      (self.positions[1, i0] - self.max_speed).astype(np.int32):(
                                        self.positions[1, i0] + self.max_speed + 1).astype(
                                          np.int32)]
                    agent_percetion = self.collision_map[                                           #Give agents a perception equal to dispersion_range +1, used to detect other agents
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
                    infected_sus_perception = self.susceptibility_map[
                                                  (self.positions[0, i0] - 100).astype(np.int32):(
                                                          self.positions[0, i0] + 101).astype(
                                                      np.int32),
                                                  (self.positions[1, i0] - 100).astype(np.int32):(
                                                          self.positions[1, i0] + 101).astype(
                                                      np.int32)]
                    #   Looking for values of walls and agents and storing corresponding coordinates
                    wall_location = np.array(np.where(wall_perception == 20))
                    agent_location = np.array(np.where(agent_percetion == 10))
                    infected_sus_location = np.array(np.where(infected_sus_perception > 0))
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
                            virus_amount = int(np.amax(infected_surface_perception, initial=0))
                            if random() <= (self.surface_infection_chance * virus_amount):
                                self.agent_list_infected_hands[i0] += 1

                    if len(infected_sus_location) > 0:
                        self.agent_list_susceptible[i0]=False
                    elif infected_sus_location == 0 and self.agent_list_susceptible[i0]==False:
                        self.agent_list_susceptible[i0]=True
                    #   Hidden path interaction
                    path_location = np.zeros((2, 1))
    
                    if self.agent_vector_pathfinding[i0] == 1:
                        hidden_path_perception = self.hidden_map_list[self.agent_list_groups[i0]][self.schedule_progress][
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
                    #   This is where a we assign a new path for agent i0
                    #   Decreasing the x and y velocity of agent i0 equal to sum of agent_location array
                    self.velocity[:, i0] -= np.sum(agent_location, 1) * 8
                    #   Decreasing the x and y velocity of agent i0 equal to sum of wall_location array
                    self.velocity[:, i0] -= np.sum(wall_location, 1) * 4
                    #   Increasing  the x and y velocity of agent i0 equal to sum of path_location array
                    self.velocity[:, i0] += np.sum(path_location, 1) * 2

                # Add randomness to to movement, higher multiplicator results in greater change of direction per iteration
                self.velocity += (np.random.rand(2, self.number_of_agents) - 0.5) * 0.5
                # Calculating the magnitude of the velocity vector-Using L2 method. square root of sum of the squared abs values.
                self.velocity_length[:] = np.linalg.norm(self.velocity, ord=2, axis=0)
                # Setting the velocity relative to max_speed
                self.velocity *= self.max_speed / self.velocity_length

                #   Cancel the velocity change for agents who are not supposed to move randomly
                cancel_velocity = np.array(np.where(self.agent_movement_mode == 1))
                for vel in cancel_velocity:
                    self.velocity[:, vel] = 0

                #Check if agent is at start position
                check_y = np.array(np.where(self.positions[0].astype(np.int32) == Campus.start_point_y))
                check_x = np.array(np.where(self.positions[1].astype(np.int32) == Campus.start_point_x))
                stay = []
                for i in check_y[0]:
                    if i in check_x[0]:
                        stay += [i]
                #Check classroom 1
                check_y_cl_1 = np.array(np.where(self.positions[0].astype(np.int32) == self.classroom_locations[0][1][1]))
                check_x_cl_1 = np.array(np.where(self.positions[1].astype(np.int32) == self.classroom_locations[0][1][0]))
                stay_cl_1 = []
                for i in check_y_cl_1[0]:
                    if i in check_x_cl_1[0]:
                        stay_cl_1 += [i]

                # Check classroom 2
                check_y_cl_2 = np.array(np.where(self.positions[0].astype(np.int32) == self.classroom_locations[1][1][1]))
                check_x_cl_2 = np.array(np.where(self.positions[1].astype(np.int32) == self.classroom_locations[1][1][0]))
                stay_cl_2 = []
                for i in check_y_cl_2[0]:
                    if i in check_x_cl_2[0]:
                        stay_cl_2 += [i]

                # Check classroom 3
                check_y_cl_3 = np.array(np.where(self.positions[0].astype(np.int32) == self.classroom_locations[2][1][1]))
                check_x_cl_3 = np.array(np.where(self.positions[1].astype(np.int32) == self.classroom_locations[2][1][0]))
                stay_cl_3 = []
                for i in check_y_cl_3[0]:
                    if i in check_x_cl_3[0]:
                        stay_cl_3 += [i]
                # Check classroom 4
                check_y_cl_4 = np.array(np.where(self.positions[0].astype(np.int32) == self.classroom_locations[3][1][1]))
                check_x_cl_4 = np.array(np.where(self.positions[1].astype(np.int32) == self.classroom_locations[3][1][0]))
                stay_cl_4 = []
                for i in check_y_cl_4[0]:
                    if i in check_x_cl_4[0]:
                        stay_cl_4 += [i]
                # Check classroom 5
                check_y_cl_5 = np.array(np.where(self.positions[0].astype(np.int32) == self.classroom_locations[4][1][1]))
                check_x_cl_5 = np.array(np.where(self.positions[1].astype(np.int32) == self.classroom_locations[4][1][0]))
                stay_cl_5 = []
                for i in check_y_cl_5[0]:
                    if i in check_x_cl_5[0]:
                        stay_cl_5 += [i]
                #print(stay_cl_3)
                #Cancel velocity when agents reach destination
                self.velocity[:, stay] = 0
                self.velocity[:, stay_cl_1] = 0
                self.velocity[:, stay_cl_2] = 0
                self.velocity[:, stay_cl_3] = 0
                self.velocity[:, stay_cl_4] = 0
                self.velocity[:, stay_cl_5] = 0
                # Use the same arrays so that agents cannot be infected when located at spawning/classroom positions
                '''self.agent_list_susceptible[:] = True
                self.agent_list_susceptible[stay] = False
                self.agent_list_susceptible[stay_cl_1] = False
                self.agent_list_susceptible[stay_cl_2] = False
                self.agent_list_susceptible[stay_cl_3] = False
                self.agent_list_susceptible[stay_cl_4] = False
                self.agent_list_susceptible[stay_cl_5] = False
                '''
                #Making sure agents are spawing with an interval equal to ite_between
                if np.any(self.spawn_array[:] == self.iteration_counter):
                    self.velocity[0, spawning_counter] = 0
                    self.velocity[1, spawning_counter] = -1
                    spawning_counter = spawning_counter + 1

                if np.all(self.velocity[:,:] == 0) == True and spawning_counter > 0:
                    print("herer vi nå")
                    self.agent_room_counter1 = len(stay_cl_1)-1
                    self.agent_room_counter2 = len(stay_cl_2)-1
                    self.agent_room_counter3 = len(stay_cl_3)-1
                    self.agent_room_counter4 = len(stay_cl_4)-1
                    self.agent_room_counter5 = len(stay_cl_5)-1
                    if self.schedule_progress < len(self.group_schedule[0]):
                        self.schedule_progress = self.schedule_progress+1
                        self.counter_varible=200

                if (self.schedule_progress == 1 or self.schedule_progress ==  2 or self.schedule_progress ==  3) and self.counter_varible > 20:
                    self.counter_varible=0
                    if self.agent_room_counter1 >= 0:
                        #print(self.agent_room_counter1,"her")
                        self.velocity[0, stay_cl_1[self.agent_room_counter1]] = 0
                        self.velocity[1, stay_cl_1[self.agent_room_counter1]] = self.max_speed
                        self.agent_room_counter1 = self.agent_room_counter1 - 1

                    if self.agent_room_counter2 >= 0:
                        #print(self.agent_room_counter2, "her")
                        self.velocity[0, stay_cl_2[self.agent_room_counter2]] = 0
                        self.velocity[1, stay_cl_2[self.agent_room_counter2]] = self.max_speed
                        self.agent_room_counter2 = self.agent_room_counter2 - 1

                    if self.agent_room_counter3 >= 0:
                        #print(self.agent_room_counter3, "her")
                        self.velocity[0, stay_cl_3[self.agent_room_counter3]] = 0
                        self.velocity[1, stay_cl_3[self.agent_room_counter3]] = self.max_speed
                        self.agent_room_counter3 = self.agent_room_counter3 - 1

                    if self.agent_room_counter4 >= 0:
                        #print(self.agent_room_counter4, "her")
                        self.velocity[0, stay_cl_4[self.agent_room_counter4]] = 0
                        self.velocity[1, stay_cl_4[self.agent_room_counter4]] = -self.max_speed
                        self.agent_room_counter4 = self.agent_room_counter4 - 1

                    if self.agent_room_counter5 >= 0:
                        print(self.agent_room_counter5, "her")
                        self.velocity[0, stay_cl_5[self.agent_room_counter5]] = 0
                        self.velocity[1, stay_cl_5[self.agent_room_counter5]] = -self.max_speed
                        self.agent_room_counter5 = self.agent_room_counter5 - 1

                # update all agent positions with velocity
                self.positions += self.velocity
                self.counter_varible +=1
                print(self.counter_varible)
                # Self infection check:
                if self.self_infection_counter == self.self_infection_check_rate:
                    if np.any(self.agent_list_infected_hands > 0):
                        infected_hands = np.array(np.where(self.agent_list_infected_hands > 0))
                        for agent in infected_hands[0]:
                            if self.agent_face_touching_avoidance[agent] and self.agent_list_susceptible[agent]:
                                if random() <= (self.self_infection_chance * self.agent_list_infected_hands[agent] * 0.5):
                                    self.agent_list_infected[agent] = 1
                                    self.agent_list_susceptible[agent] = 0

                            elif not self.agent_face_touching_avoidance[agent] and self.agent_list_susceptible[agent]:
                                if random() <= self.self_infection_chance * self.agent_list_infected_hands[agent]:
                                    self.agent_list_infected[agent] = 1
                                    self.agent_list_susceptible[agent] = 0

                            self.self_infection_counter = 0
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
            #Setting RGB value equal to white for visualization of healthy agents
            self.world[self.positions[0].astype(np.int32), self.positions[1].astype(np.int32), :] = 10
            infected_positions = np.array(np.where(self.agent_list_infected == 1))
            infected_positions = np.array(self.positions[:, infected_positions])
            # Setting RGB value equal to red for visualization of infected agents
            self.world[infected_positions[0].astype(np.int32), infected_positions[1].astype(np.int32), 0:2] = 0

            #Updates currently infected
            self.number_currently_infected = np.sum(self.agent_list_infected)
            #Adds up to count total number of infected
            self.infected_history.append(self.number_currently_infected)
            #   Needs attention
            self.number_total_infected += (self.number_currently_infected - self.infected_history[self.iteration_counter - 1])

            #   Erasing old positions for collision detection
            self.collision_map[:, :] = 0
            # Updating new positions for collision detection
            self.collision_map[self.positions[0].astype(np.int32), self.positions[1].astype(np.int32)] = 1

            # iterete the surface disinfect counter and if it is time, disinfect all surfaces.
            self.disinfect_surface_counter += 1
            if self.disinfect_surface_counter == int(self.key_object_disinfection * 1000):

                self.disinfect_surfaces()
                self.disinfect_surface_counter = 0


            self.hand_wash_counter += 1
            if self.hand_wash_counter == self.hand_wash_interval:
                washes_hands = np.array(np.where(self.agent_hand_hygine))
                for agent in washes_hands:
                    self.agent_list_infected_hands[agent] = 0
                self.hand_wash_counter = 0

            #   Plus operation for while loop was moved from the top
            self.iteration_counter = self.iteration_counter + 1

            self.schedule_iteration_counter += 1
            if self.schedule_iteration_counter == self.next_class_interval:
                if self.schedule_progress < len(self.group_schedule[0]):
                    #self.schedule_progress += 1
                    self.schedule_iteration_counter = 0
            self.self_infection_counter += 1

            # if statement true-> finish simulation
            if self.iteration_counter == self.simulation_time:
                break
            #   OpenCV Visualization
            if self.visualize:
                dim = (600, 600)
                world_resized = cv2.resize(self.world, dim, interpolation=cv2.INTER_AREA)
                cv2.imshow('frame', world_resized)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        if self.visualize:
            cv2.destroyAllWindows()

        return {
                "number_currently_infected": self.number_currently_infected,
                "infected_history": self.infected_history,
                "number_total_infected": self.number_total_infected,
                "parameters": {
                    "number_of_agents": self.number_of_agents,
                    "social_distancing": self.social_distancing,
                    "hand_hygiene": self.hand_hygiene,
                    "face_masks": self.face_masks,
                    "key_object_disinfection": self.key_object_disinfection,
                    "face_touching_avoidance": self.face_touching_avoidance
                }
        }


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    from OMDM.Individual import Individual
    from OMDM.Fitness import population_spread_fitness
    new_individual = Individual(0.2, genome_length=6)
    new_model = Model(new_individual.genome.genome, visualize=True)
    new_individual.phenotype = new_model.simulate()
    print(new_individual.phenotype)
    new_individual.fitness = population_spread_fitness(new_individual.phenotype, 500, 1, 1)
    print(new_individual.fitness)
    