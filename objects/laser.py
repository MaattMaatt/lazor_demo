
class Laser:

    def __init__(self,laserpos,laserdirection):
        # set the starting position and direction
        # position is 2-list of laser's coordinates
        # direction is a 2-list of laser's unit velocity (ex: (-1,1))
        self.position = laserpos
        self.direction = laserdirection

    def update(self,board_variation, all_points)
        # find potential new location of laser and decide how it will interact with that point

        # need to know which block the point is headed into (blocks are on even squares)

