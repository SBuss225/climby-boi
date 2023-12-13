class ClimbingWall:
  def __init__(self, height, width, handhold_dict):
    self.height = height
    self.width = width
    self.handhold_dict = handhold_dict # dictionary of coordinates (x, y) to Handhold objects
                                       # assume x and y are scaled based on wall width and height

class Handhold:
  def __init__(self, color, x, y):
    self.color = color
    self.x = x
    self.y = y
