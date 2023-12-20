import unittest
from climby_boi import ClimbyBoi
import main
from climbing_wall import Handhold, ClimbingWall

class TestClimbyBoi(unittest.TestCase):
  def test_find_new_handhold(self):
    boi = main.create_climber()


    test_handholds = [[(x,y) for x in [24, 36]] for y in range(12, 120, 12)]
    handhold_dict = {}
    for row in test_handholds:
      for coord in row:
        handhold_dict[coord] = Handhold(*coord)
    test_wall = ClimbingWall(height=120, width=60, handhold_dict=handhold_dict)

    boi.initialize_body_locations(test_wall)
    boi.get_valid_x_handholds("left_hand", test_wall)
    boi.get_valid_y_handholds("left_hand", test_wall)

    boi.find_new_handhold("left_hand", test_wall)
    boi.run_greedy(test_wall)

if __name__=='__main__':
  unittest.main()
