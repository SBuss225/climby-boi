import numpy as np
class ClimbyBoi:
  def __init__(self, climber_stats, ):
    self.climber_stats = climber_stats
    self.handhold_distance_matrix = None

  def populate_handhold_distance_matrix(self, handhold_dict):
    num_handholds = len(handhold_dict)
    handholds = handhold_dict.values()
    self.handhold_distance_matrix = [[self.calc_distance_between_handholds(handholds[i], handholds[j]) for i in range(num_handholds)] for j in range(num_handholds)]

  def calc_distance_between_handholds(self, handhold_one, handhold_two):
    if handhold_one == handhold_two:
      return 0
  
    return np.sqrt((handhold_one.x - handhold_two.x) ** 2 + (handhold_one.y - handhold_two.y) ** 2)

class ClimberStats:
  def __init__(self, height, arm_length, leg_length, vertical_leg_reach, can_jump, can_foot_swap):
    self.height = height
    self.arm_length = arm_length
    self.leg_length = leg_length
    self.vertical_leg_reach = vertical_leg_reach
    self.can_jump = can_jump
    self.can_foot_swap = can_foot_swap