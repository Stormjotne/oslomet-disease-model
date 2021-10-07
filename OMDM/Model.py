"""

"""
from random import random

class Model:
    """
    Implement the Agent-based Model in this class.
    """
    def __init__(self, parameters, normalized=True, static_population=1000):
        """
        Put any declarations of object fields/variables in this method.
        :param parameters:
        :type parameters:
        :param normalized:
        :type normalized:
        :param static_population:
        :type static_population:
        """
        #   Model outputs
        self.number_currently_infected = 0
        self.infected_history = []
        self.number_total_infected = 0
        #   Parameters that are static to the model
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
        #   Population (Number of Agents)
        #   Can be static for early testing
        #   Should be controlled by the Evolutionary Algorithm later
        self.number_of_agents = static_population
        #   Parameters controlled by the Evolutionary Algorithm
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
        if normalized:
            self.interpret_normalized_genome(parameters)
        else:
            self.interpret_genome(parameters)
        
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
        self.respiratory_hygiene = 0.01 + round(parameters["respiratory_hygiene"] * 0.99, 2)
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        self.face_masks = 0.01 + round(parameters["face_masks"] * 0.99, 2)
        #   Range:  1% - 100%   Decimal rounded to hundredths.
        self.face_shields = 0.01 + round(parameters["face_shields"] * 0.99, 2)
        #   Range:  1/8 - 8/8 hour/school day
        self.key_object_disinfection = (1 + round(parameters["key_object_disinfection"] * 7)) / 8
        #   Range:  1/16 - 8/16 hour/school day
        self.surface_disinfection = (1 + round(parameters["surface_disinfection"] * 7)) / 16
        #   Range:  1 - 3600 seconds
        self.ventilation_of_indoor_spaces = 1 + round(parameters["ventilation_of_indoor_spaces"] * 3599)
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
        
    def interpret_genome(self, parameters):
        if not self.number_of_agents:
            self.number_of_agents = parameters["number_of_agents"]
        #   Parameters controlled by the Evolutionary Algorithm
        self.social_distancing = parameters["social_distancing"]
        self.hand_hygiene = parameters["hand_hygiene"]
        self.respiratory_hygiene = parameters["respiratory_hygiene"]
        self.face_masks = parameters["face_masks"]
        self.face_shields = parameters["face_shields"]
        self.key_object_disinfection = parameters["key_object_disinfection"]
        self.surface_disinfection = parameters["surface_disinfection"]
        self.ventilation_of_indoor_spaces = parameters["ventilation_of_indoor_spaces"]
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
        step = 0
        while step < self.simulation_time:
            self.number_currently_infected = 0
            for agent in range(self.number_of_agents):
                if random() < self.base_transmission_probability:
                    self.number_currently_infected += 1
            self.infected_history.append(self.number_currently_infected)
            self.number_total_infected += self.number_currently_infected
            step += 1
        return self.number_currently_infected, self.infected_history, self.number_total_infected, self.number_of_agents
        
    
#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
