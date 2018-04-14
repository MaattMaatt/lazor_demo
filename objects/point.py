
class Point:
    '''
    The Point.  This object desribes the points for which we want the laser
    light to intersect.
    '''
    def __init__(self, pointpos):
        # pointpos is a 2-list of point's coordinates

        # assign position that can be called outside class
        self.position = pointpos 
        # point is not intersected by laser until proven otherwise 
        self.intersect = 0

    def check_intersection(self, laserpos):
        # if at any time point is intersected by laser, stay that way for all time
        if self.intersect == 1:
            pass
        elif self.position != laserpos:
            pass
        else:
            self.intersect = 1
        return self.intersect

# test code
p = Point((1,2))
print p.position
print p.check_intersection((2,2))
print p.check_intersection((1,2))
print p.check_intersection((2,2))
