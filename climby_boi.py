import numpy as np

GREEDY_ALGORITHM = "greedy"
LEFT_HAND = "left_hand"
RIGHT_HAND = "right_hand"
LEFT_FOOT = "left_foot"
RIGHT_FOOT = "right_foot"
LEFT_SHOULDER = "left_shoulder"
RIGHT_SHOULDER = "right_shoulder"
LEFT_HIP = "left_hip"
RIGHT_HIP = "right_hip"

FOOT = "foot"
HAND = "hand"

class ClimbyBoi:
  def __init__(self, climber_stats):
    self.climber_stats = climber_stats
    self.handhold_distance_matrix = None
    self.limb_locations = {LEFT_HAND: (0, 0), RIGHT_HAND: (0, 0), LEFT_FOOT: (0, 0), RIGHT_FOOT: (0, 0)}
    self.torso_vertices = {LEFT_SHOULDER: (0, 0), RIGHT_SHOULDER: (0, 0), LEFT_HIP: (0, 0), RIGHT_HIP: (0, 0)}
    self.limb_to_torso_connections = {LEFT_HAND: LEFT_SHOULDER, RIGHT_HAND: RIGHT_SHOULDER, LEFT_FOOT: LEFT_HIP, RIGHT_FOOT: RIGHT_HIP}

  def populate_handhold_distance_matrix(self, handhold_dict):
    num_handholds = len(handhold_dict)
    handholds = handhold_dict.values()
    self.handhold_distance_matrix = [[self.calc_distance_between_handholds(handholds[i], handholds[j]) for i in range(num_handholds)] for j in range(num_handholds)]

  def calc_distance_between_handholds(self, handhold_one, handhold_two):
    if handhold_one == handhold_two:
      return 0
  
    return np.sqrt((handhold_one.x - handhold_two.x) ** 2 + (handhold_one.y - handhold_two.y) ** 2)
  
  def calc_shortest_path(self, wall, algorithm=GREEDY_ALGORITHM):
    if (algorithm == GREEDY_ALGORITHM):
      return self.run_greedy(wall)

  def run_greedy(self, wall):
    # initialize limb and torso locations to standing bottom-center of the wall
    self.initialize_body_locations(wall)
    self.find_first_handholds()

    # find a valid next handhold for each limb, repeat until top is within reach
    # add each handhold to the full path along with which limb is on it
    top_reached = False
    while (not top_reached):
      for limb in self.limb_locations:
        self.find_new_handhold(limb, wall)

        self.reorient_torso()

    # when a limb is moved, drag the attached torso point along with it so that 
    # that limb is valid, but then check to see if that drags any of the other limbs
    # out of line

  def find_new_handhold(self, limb, wall):
    # if hand is already on a handhold
    limb_loc = self.limb_locations[limb]
    curr_handhold = self.wall.handhold_dict[limb_loc]
    if (curr_handhold != -1):
      curr_handhold.occupied_by = self.get_limb_type(limb)

    # find area of potential handholds
    valid_x_handholds = self.get_valid_x_handholds(limb, wall)
    valid_y_handholds = self.get_valid_y_handholds(limb, wall)
    all_valid_handholds = [handhold for handhold in valid_x_handholds if handhold in valid_y_handholds]  
      
    self.handhold_distance_matrix[limb]

  def get_valid_x_handholds(self, limb, wall):
    curr_loc = self.limb_locations[limb]
    all_handhold_coords = wall.handhold_dict.keys()
    x_sorted_coords = sorted(all_handhold_coords, key=lambda x:int(x[0]))
    valid_coords = []

    def is_in_hand_x_range():
      return True

    def is_in_foot_x_range():
      return True

    if (self.get_limb_type(limb) == HAND):
      valid_coords = [coord for coord in x_sorted_coords if (is_in_hand_x_range(coord[0]))]

    


  def get_valid_y_handholds(self, limb, wall):
    all_handhold_coords = wall.handhold_dict.keys()
    y_sorted_coords = sorted(all_handhold_coords, key=lambda x:int(x[1]))
    valid_coords = []

  def get_limb_type(self, limb):
    if (limb == RIGHT_FOOT or limb == LEFT_FOOT):
      return FOOT
    else:
      return HAND
    
  def reorient_torso():
    pass
      
  def initialize_body_locations(self, wall):
    wall_x_center = wall.width / 2
    body_left_x = wall_x_center - (self.climber_stats.shoulder_distance / 2)
    body_right_x = wall_x_center + (self.climber_stats.shoulder_distance / 2)
    shoulder_y = self.climber_stats.vertical_arm_reach - self.climber_stats.arm_length
    hip_y = self.climber_stats.leg_length
    hand_y = shoulder_y - self.climber_stats.arm_length

    self.torso_vertices[LEFT_SHOULDER] = (body_left_x, shoulder_y)
    self.torso_vertices[RIGHT_SHOULDER] = (body_right_x, shoulder_y)
    self.torso_vertices[LEFT_HIP] = (body_left_x, hip_y)
    self.torso_vertices[RIGHT_HIP] = (body_right_x, hip_y)
    
    self.limb_locations[LEFT_HAND] = (body_left_x, hand_y)
    self.limb_locations[RIGHT_HAND] = (body_right_x, hand_y)
    self.limb_locations[LEFT_FOOT] = (body_left_x, 0)
    self.limb_locations[RIGHT_FOOT] = (body_right_x, 0)
    

  def is_valid_orientation(self):
    # are limbs allowed distance from torso points
    if (self.limb_locations[LEFT_HAND] - self.torso_vertices[LEFT_SHOULDER] > self.arm_length):
      return False
    if (self.limb_locations[RIGHT_HAND] - self.torso_vertices[RIGHT_SHOULDER] > self.arm_length):
      return False
    if (self.limb_locations[LEFT_FOOT] - self.torso_vertices[LEFT_HIP] > self.leg_length):
      return False
    if (self.limb_locations[RIGHT_FOOT] - self.torso_vertices[RIGHT_HIP] > self.leg_length):
      return False

    # are hands above feet
    # are hands within allowed distance from feet 
    # are feet within allowed distance from each other 
    # are feet within vertical_leg_reach
    # center point between hands and center point between feet cannot form more than 45 degree angle either way (not too sideways)


class ClimberStats:
  def __init__(self, height, arm_length, leg_length, shoulder_distance,
               vertical_leg_reach, vertical_arm_reach, horizontal_leg_reach, 
               can_jump=False, can_foot_swap=False):
    # all measurements in inches
    self.height = height
    self.arm_length = arm_length # armpit to longest finger
    self.leg_length = leg_length # inseam
    self.shoulder_distance = shoulder_distance # center of one shoulder to the other
    self.vertical_leg_reach = vertical_leg_reach # how high the bottom of your foot can reach from the ground when you 
                                                 # bring it up directly in front of you, foot flat
    self.vertical_arm_reach = vertical_arm_reach # how high up you can reach with your arm when standing flat
                                                 # on the ground. Measured from ground to longest finger
    self.horizontal_leg_reach = horizontal_leg_reach # max distance between feet when standing flat, measured from the inside
                                                     # of one foot to the inside of the other

    self.can_jump = can_jump
    self.can_foot_swap = can_foot_swap