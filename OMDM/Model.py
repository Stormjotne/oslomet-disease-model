"""

"""


class Model:
    """
    Implement the Agent-based Model in this class.
    """
    def __init__(self, parameters, normalized=True):
        """
        Put any declarations of object fields/variables in this method.
        """
        #   Parameters that are static to the model
        self.base_transmission_probability = 0.128
        self.one_meter_transmission_probability = 0.026
        #   Half-assed inferred values
        self.two_meter_transmission_probability = 0.002
        self.four_meter_transmission_probability = 0.0007
        #   Virus time-to-live on surfaces in days
        virus_ttl_surface = range(6, 9)
        #   virus time-to-live on agent in hours
        virus_ttl_agent = range(1, 9)
        #   Parameters controlled by the Evolutionary Algorithm
        self.social_distancing = None
        self.hand_hygiene = None
        self.respiratory_hygiene = None
        self.face_masks = None
        self.face_shields = None
        self.key_object_disinfection = None
        self.surface_disinfection = None
        self.ventilation_of_indoor_spaces = None
        #   These parameters are medium priority.
        self.face_touching_avoidance = None
        #   These parameters are low priority.
        self.test_based_screening = None
        self.vaccination = None
        self.cohort_size = None
        self.electives = None
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
        #   Parameters controlled by the Evolutionary Algorithm
        #   Range:  0.1 - 4.1 meters
        self.social_distancing = 0.1 + round(parameters["social_distancing"] * 4, 2)
        #   Range:  1% - 100%   Decimal rounded to hundreds.
        self.hand_hygiene = 0.01 + round(parameters["hand_hygiene"] * 0.99, 2)
        #   Range:  1% - 100%   Decimal rounded to hundreds.
        self.respiratory_hygiene = 0.01 + round(parameters["respiratory_hygiene"] * 0.99, 2)
        #   Range:  1% - 100%   Decimal rounded to hundreds.
        self.face_masks = 0.01 + round(parameters["face_masks"] * 0.99, 2)
        #   Range:  1% - 100%   Decimal rounded to hundreds.
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
    
        
        
#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
