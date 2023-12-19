from climbing_wall import ClimbingWall, Handhold
import random

test_handholds = [[Handhold(x, y) for x in [24, 36]] for y in range(12, 120)]
test_wall = ClimbingWall(height=120, width=60, handhold_dict=test_handholds)

def create_random_wall(width, height, num_handholds):
  handholds = []
  for i in range(num_handholds):
    rand_x = random.uniform(0, width)
    rand_y = random.uniform(12, height)

    while (rand_x, rand_y) in handholds:
      rand_x = random.uniform(0, width)
      rand_y = random.uniform(12, height)

    handholds.append((rand_x, rand_y))

  return ClimbingWall(height=height, width=width, handhold_dict=handholds)


