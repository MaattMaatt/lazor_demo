

class Block:
    
    def __init__(self,blocktype):
        
        # block contains boolean info about the ways a laser will interact
        # laser can go go thru, be "killed", reflect, or reflect + refract

        if blocktype == 'O': # no block, go right through
            self.thru = 1
            self.kill = 0
            self.reflect = 0
            self.refract = 0
        elif blocktype == 'B': # opaque, kills laser
            self.thru = 0
            self.kill = 1
            self.reflect = 0
            self.refract = 0
        else: # reflect ('A') or refract ('C')
            self.thru = 0
            self.kill = 0
            self.reflect = 1
            if blocktype == 'C':
                self.refract = 1
            else:
                self.refract = 0