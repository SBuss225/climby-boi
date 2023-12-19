class ClimbingWall:
  def __init__(self, height, width, handhold_dict):
    self.height = height # height in inches
    self.width = width # width in inches
    self.handhold_dict = handhold_dict # dictionary of coordinates (x, y) to Handhold objects
                                       # assume x and y are scaled based on wall width and height

class Handhold:
  def __init__(self, x, y, color="blue"):
    # x, y pair indicates the top middle of the handhold
    self.color = color
    self.x = x
    self.y = y
    self.occupied_by = None
