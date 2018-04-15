from block import Block
from point import Point

class Laser:

    def __init__(self,laserpos,laserdirection):
        # set the starting position and direction
        # position is 2-list of laser's coordinates
        # direction is a 2-list of laser's unit velocity (ex: (-1,1))
        self.position = laserpos
        self.direction = laserdirection
        # marker for removal of laser if it is destroyed
        self.killed = 0

    def update(self,thisboard,all_points,boardlen,boardht):
        # find potential new location of laser and decide how it will interact with that point

        # need to know which block the point is headed into ("bpt")
        # we know where the block is based on which coordinate of laser position is even/odd
        if self.position[0] % 2 == 0:
            bpt = [self.position[0]+self.direction[0], self.position[1]]
        else:
            bpt = [self.position[0], self.position[1] + self.direction[1]] 
        # associate bpt with position in board
        boardx = (bpt[0]-1)/2
        boardy = (bpt[1]-1)/2
        new_laser = None
        newpt2 = None
        newdir = None
        if boardx < 0 or boardy < 0 or boardx > boardlen-1 or boardy > boardht-1:
            self.killed = 1
        else:
            # decide how we interact based on block properties, update laser with "newpt"
            thisblock = Block(thisboard[boardy][boardx]) # make block objects only as needed to save time
            if thisblock.kill == 1:
                self.killed = 1
            elif thisblock.thru == 1:
                self.position = [self.position[0] + self.direction[0], self.position[1] + self.direction[1]]
                # (direction unchanged if go through)
            else:
                if thisblock.refract == 1:
                    newpt2 = [self.position[0] + self.direction[0], self.position[1] + self.direction[1]]
                    newdir2 = [self.direction[0],self.direction[1]]
                    new_laser = newpt2,newdir2
                # reflect: change direction; again, handle even and odd x-coordinate cases differently
                if self.position[0] % 2 == 0:
                    self.direction[0] = -self.direction[0]
                else:
                    self.direction[1] = -self.direction[1]
                self.position = [self.position[0] + self.direction[0], self.position[1] + self.direction[1]]
        # update all_points if we hit a point
        for i in range(len(all_points)):
            all_points[i].check_intersection(self.position)
        return all_points,new_laser # return None if we dont refract

# # test stuff
# thisboard = [['O','O','O','O'],['O','O','O','O'],['O','O','O','O'],['A','O','O','O'],['O','O','O','C'],['O','O','A','O']]
# pthit = [Point([1,2]),Point([6,3])]
# l = Laser([8,7],[-1,1])
# l.update(thisboard,pthit,4,6)
# print 'stuff:'
# print l.position, l.direction
# print l.killed
# print ':stuff'

