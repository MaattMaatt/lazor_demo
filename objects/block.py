 
class block:
    
    def __init__(self,blocktype):
        
        # block contains boolean info about the ways a laser will interact
        # laser can go go thru, be "killed", reflect, or reflect + refract

        # save block type in block so we can print it later
        self.btype = blocktype

        if blocktype == 'x' or blocktype == 'o':
            self.thru = 1
            self.kill = 0
            self.reflect = 0
            self.refract = 0
        elif blocktype == 'b' or blocktype == 'B':
            self.thru = 0
            self.kill = 1
            self.reflect = 0
            self.refract = 0
        else: # reflect or refract
            self.thru = 0
            self.kill = 0
            self.reflect = 1
            if blocktype == 'c' or blocktype == 'C':
                self.refract = 1
            else:
                self.refract = 0

# opaq = block('o')
# print opaq.thru 
# print opaq.kill 
# print opaq.reflect 
# print opaq.refract 
# print opaq.btype