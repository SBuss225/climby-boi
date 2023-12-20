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
RIGHT = "right"
LEFT = "left"

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

    # find a valid next handhold for each limb, repeat until top is within reach
    # add each handhold to the full path along with which limb is on it
    top_reached = False
    while (not top_reached):
      for limb in self.limb_locations:
        valid_handholds = self.find_new_handhold(limb, wall)
        best_handhold = self.limb_locations[limb]

        for handhold in valid_handholds:
          if wall.handhold_dict[handhold].occupied_by != None:
            continue
          if self.move_to_handhold(limb, wall, handhold):
            best_handhold = handhold
            break
      if self.torso_vertices[LEFT_SHOULDER][1] + self.climber_stats.arm_length > wall.height:
        top_reached = True
        print("You reached the top! Congrats!")
        

    # when a limb is moved, drag the attached torso point along with it so that 
    # that limb is valid, but then check to see if that drags any of the other limbs
    # out of line

  def move_to_handhold(self, limb, wall, handhold):
    limb_loc = self.limb_locations[limb]
    
    if limb_loc in wall.handhold_dict:
      wall.handhold_dict[limb_loc].occupied_by = None
    
    new_limb_locations = self.limb_locations.copy()
    new_limb_locations[limb] = handhold

    new_torso_verticies, new_limb_locations = self.reorient_torso(new_limb_locations)
    if self.is_valid_orientation(new_limb_locations, new_torso_verticies, wall):
      self.limb_locations = new_limb_locations
      self.torso_vertices = new_torso_verticies
      wall.handhold_dict[handhold].occupied_by = self.get_limb_type(limb)
      return True
    elif limb_loc in wall.handhold_dict:
      wall.handhold_dict[limb_loc].occupied_by = self.get_limb_type(limb)
      return False
    else:
      return False
    
  def find_new_handhold(self, limb, wall):
    # if hand is already on a handhold
    limb_loc = self.limb_locations[limb]
    if limb_loc in wall.handhold_dict:
      wall.handhold_dict[limb_loc].occupied_by = self.get_limb_type(limb)

    # find area of potential handholds
    valid_x_handholds = self.get_valid_x_handholds(limb, wall)
    valid_y_handholds = self.get_valid_y_handholds(limb, wall)
    all_valid_handholds = [handhold for handhold in valid_y_handholds if handhold in valid_x_handholds]  
    return all_valid_handholds

    #self.handhold_distance_matrix[limb]

  def get_valid_x_handholds(self, limb, wall):
    all_handhold_coords = wall.handhold_dict.keys()
    x_sorted_coords = sorted(all_handhold_coords, key=lambda x:int(x[0]))
    valid_coords = []

    # currently there is no risk of reaching past current torso loc
    # this may cause an issue as if we can't reach past torse, torso can't adjust
    def is_in_hand_x_range(target_x_coord):
      joint_socket = self.torso_vertices[self.limb_to_torso_connections[limb]]
      left_reach = joint_socket[0] - self.climber_stats.arm_length
      right_reach = joint_socket[0] + self.climber_stats.arm_length
      return target_x_coord >= left_reach and target_x_coord <= right_reach

    def is_in_foot_x_range(target_x_coord):
      joint_socket = self.torso_vertices[self.limb_to_torso_connections[limb]]
      left_reach = joint_socket[0] - self.climber_stats.horizontal_leg_reach
      right_reach = joint_socket[0] + self.climber_stats.horizontal_leg_reach

      # it's harder to reach with legs crossed over
      if (self.get_limb_side(limb) == RIGHT):
        left_reach = joint_socket[0] - self.climber_stats.horizontal_leg_reach / 2
      else:
        right_reach = joint_socket[0] + self.climber_stats.horizontal_leg_reach / 2

      return target_x_coord >= left_reach and target_x_coord <= right_reach

    if (self.get_limb_type(limb) == HAND):
      valid_coords = [coord for coord in x_sorted_coords if (is_in_hand_x_range(coord[0]))]
    else:
      valid_coords = [coord for coord in x_sorted_coords if (is_in_foot_x_range(coord[0]))]
    return valid_coords


  def get_valid_y_handholds(self, limb, wall):
    all_handhold_coords = wall.handhold_dict.keys()
    y_sorted_coords = sorted(all_handhold_coords, key=lambda x:int(x[1]), reverse=True)
    valid_coords = []

    def is_in_hand_y_range(target_y_coord):
      joint_socket = self.torso_vertices[self.limb_to_torso_connections[limb]]
      # we want to encourage vertical movement
      upper_reach = joint_socket[1] + self.climber_stats.arm_length
      lower_reach = joint_socket[1] - self.climber_stats.arm_length / 2
      return target_y_coord <= upper_reach and target_y_coord >= lower_reach
    
    def is_in_foot_y_range(target_y_coord):
      joint_socket = self.torso_vertices[self.limb_to_torso_connections[limb]]
      # may need to adjust the vertical_leg_reach when the torso is tilted
      upper_reach = joint_socket[1] + self.climber_stats.vertical_leg_reach
      lower_reach = joint_socket[1] - self.climber_stats.leg_length
      return target_y_coord <= upper_reach and target_y_coord >= lower_reach
    
    if (self.get_limb_type(limb) == HAND):
      valid_coords = [coord for coord in y_sorted_coords if (is_in_hand_y_range(coord[1]))]
    else:
      valid_coords = [coord for coord in y_sorted_coords if (is_in_foot_y_range(coord[1]))]
    return valid_coords

  def get_limb_type(self, limb):
    if (limb == RIGHT_FOOT or limb == LEFT_FOOT):
      return FOOT
    else:
      return HAND
    
  def get_limb_side(self, limb):
    if (limb == RIGHT_FOOT or limb == RIGHT_HAND):
      return RIGHT
    else:
      return LEFT
    
  def reorient_torso(self, new_limb_locs):
    new_torso_verticies = {}
    higher_foot, other_foot = (LEFT_FOOT, RIGHT_FOOT) if new_limb_locs[LEFT_FOOT][1] > new_limb_locs[RIGHT_FOOT][1] else (RIGHT_FOOT, LEFT_FOOT)
    
    # straighten the leg of the higher foot
    higher_hip_loc = self.tupleAdder(new_limb_locs[higher_foot], (0, self.climber_stats.leg_length))
    new_torso_verticies[self.limb_to_torso_connections[higher_foot]] = higher_hip_loc
    other_hip_offset = self.climber_stats.shoulder_distance if self.get_limb_side(other_foot) == RIGHT else -self.climber_stats.shoulder_distance
    other_hip_loc = self.tupleAdder(new_torso_verticies[self.limb_to_torso_connections[higher_foot]], (other_hip_offset, 0))
    new_torso_verticies[self.limb_to_torso_connections[other_foot]] = other_hip_loc
    
    new_limb_locs[other_foot] = self.tupleAdder(new_limb_locs[higher_foot], (other_hip_offset, 0))
    
    y_torso_increase = higher_hip_loc[1] - self.torso_vertices[self.limb_to_torso_connections[higher_foot]][1]
    # increase shoulders by same amount to keep torso consistent
    new_torso_verticies[LEFT_SHOULDER] = self.tupleAdder(self.torso_vertices[LEFT_SHOULDER], (0, y_torso_increase))
    new_torso_verticies[RIGHT_SHOULDER] = self.tupleAdder(self.torso_vertices[RIGHT_SHOULDER], (0, y_torso_increase))
    
    return new_torso_verticies, new_limb_locs
  
  def tupleAdder(self, tuple1, tuple2, isSub=False):
    res = tuple(map(lambda i, j: i + j if not isSub else i - j, tuple1, tuple2))
    return res
  
  def euclidCalc(self, tuple1, tuple2):
    return np.sqrt((tuple1[0] - tuple2[0]) ** 2 + (tuple1[1] - tuple2[1]) ** 2)

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
  
  def still_on_floor(self):
    return self.limb_locations[LEFT_FOOT][1] == 0 or self.limb_locations[RIGHT_FOOT][1] == 0

  def is_valid_orientation(self, new_limb_locs, new_torso_verticies, wall):
    # are limbs allowed distance from torso points
    if (self.euclidCalc(new_limb_locs[LEFT_HAND], new_torso_verticies[LEFT_SHOULDER]) > self.climber_stats.arm_length):
      return False
    if (self.euclidCalc(new_limb_locs[RIGHT_HAND], new_torso_verticies[RIGHT_SHOULDER]) > self.climber_stats.arm_length):
      return False
    if (self.euclidCalc(new_limb_locs[LEFT_FOOT], new_torso_verticies[LEFT_HIP]) > self.climber_stats.leg_length):
      return False
    if (self.euclidCalc(new_limb_locs[RIGHT_FOOT], new_torso_verticies[RIGHT_HIP]) > self.climber_stats.leg_length):
      return False

    # are at least 3 limbs on handholds
    num_limbs_on_handholds = 0
    for limb in new_limb_locs:
      limb_loc = new_limb_locs[limb]
      if limb_loc in wall.handhold_dict:
        num_limbs_on_handholds += 1

    if num_limbs_on_handholds < 3 and not self.still_on_floor():
      return False
    
    return True

    # are hands above feet by at least a foot
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