from climby_boi import ClimbyBoi, ClimberStats

# for now, just returns a default climber
def create_climber():
  # measurements in inches
  stats = ClimberStats(height=67, arm_length=28, leg_length=32.5, shoulder_distance=14.5, 
                       vertical_leg_reach=24, vertical_arm_reach=87, horizontal_leg_reach=58)
  return ClimbyBoi(stats)

# main functionality

climber = create_climber()