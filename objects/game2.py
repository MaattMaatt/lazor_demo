from __future__ import print_function
import sys
import copy
import itertools

# import the Point, Block, and Laser objects
from block import Block
from point import Point
from laser import Laser

class Game:

    def __init__(self, fptr):
        '''
        Initialize our game.
        **Parameters**
            fptr: *str*
                The file name of the input board to solve.
        **Returns**
            game: *Game*
                This game object.
        '''
 
        self.fname = fptr
        self.available_space = 0
        self.blocks = []
        self.blocks_per = []
        self.read(fptr)

    # make initial board to print
    def __str__(self):
        '''
        print the initial board
        '''

        print('-'* (2 *len(self.board_set1[0])+1))
        for i in range(len(self.board_set1)):
            for j in range(len(self.board_set1[0])):
                print('|'+ str(self.board_set1[i][j]), end = '')
            print ('|')
            print('-'* (2 *len(self.board_set1[0])+1))
        return ''

    def read(self, fptr):
        '''
        reads in a file, and generates the internal board list, lazor list, point list and block list. 
        Also generate the permutation of the block list

        **Parameters**
            fptr: *str*
                The file name of the input board to solve.
        **Returns**
            None
        '''


        self.fptr1 = open(fptr, 'r')
        self.fptr = self.fptr1.read()

        self.board_set1 = []
        data = [line for line in self.fptr.strip().split('\n') if not '#' in line]
        for i in range(len(data)):
            if i < len(data) and data[i]== '':
                del data[i]

        # generate the original board set list as 'board_set1'
        board_set = data[data.index('GRID START')+1:data.index('GRID STOP')]
        for i in range(len(board_set)):
            board_set[i]= board_set[i].replace(' ','')
        for i in range(len(board_set)):
            self.board_set1.append(list(itertools.chain(board_set[i])))

        # Define the length and height of our original board. 
        self.length = len(self.board_set1[0])
        self.height = len(self.board_set1)

        # Genarate and reformat the block set, lazor set and point set from the files we read in/
        data = data[data.index('GRID STOP')+1:]

        for i in range(len(data)):
            if data[i].find('A') == 0:
                a = i
                break
        for i in range(len(data)):
            if data[i].find('L') == 0 :
                b = i
                break
        for i in range(len(data)):
            if data[i].find('P')==0:
                c = i
                break
        self.block_set = data[a:b]
        self.block_set = [self.block_set[i].split(' ') for i in range(len(self.block_set))]
        self.lazor_set = data[b:c]
        self.lazor_set = [self.lazor_set[i].split(' ') for i in range(len(self.lazor_set))]
        self.point_set = data[c:] 
        self.point_set = [self.point_set[i].split(' ') for i in range(len(self.point_set))]

        # Assign the point and lazor objects to the list separately.
        for p in range(len(self.point_set)):
            self.point_set[p] = Point([int(self.point_set[p][1]),int(self.point_set[p][2])])
        for l in range(len(self.lazor_set)):
            self.lazor_set[l] = Laser([int(self.lazor_set[l][1]),int(self.lazor_set[l][2])],[int(self.lazor_set[l][3]),int(self.lazor_set[l][4])])

        #figure out the number of available space
        for i in range(len(self.board_set1)):
            for j in range(len(self.board_set1[0])):
                if self.board_set1[i][j] == 'o':
                    self.available_space += 1
        
        # make the list of original block set
        for i in range(len(self.block_set)):
            for j in range(int(self.block_set[i][1])):
                self.blocks.append(self.block_set[i][0])

        # make the list of all permutations of blocks
        self.blocks_per = list(set(itertools.permutations(self.blocks)))

        # close the file
        self.fptr1.close()


    def generate_boards(self): 
        '''
        A function to generate all possible board combinations with the
        available blocks.

        **Parameters**
            None
    
        **Returns**
            board: *list*
                a list of all possible boards containing blocks that could happen in the original board
        '''

        def get_partitions(n, k):
            # generating permutations

            for c in itertools.combinations(range(n + k - 1), k - 1):
                yield [b - a - 1 for a, b in zip((-1,) + c, c + (n + k - 1,))]

        # Get the a list of different possible block positions. 
        partitions = [
            p for p in get_partitions(len(self.blocks), self.available_space) if max(p) == 1
        ]



        # add the permutated blocks into the available_space partitions

        for n in range(len(self.blocks_per)):
            for i in range(len(partitions)):
                k = 0
                for j in range(len(partitions[0])):
                    if partitions[i][j] == 1:
                        partitions[i][j] = self.blocks_per[n][k]
                        k += 1
                    elif partitions[i][j] == 0:
                        partitions[i][j] = 'o'
        
        
        # Now we have the partitions, we just need to make our boards
        boards = []
        # add the block partitions into the boards
        for n in range(len(partitions)):
            k = 0
            self.board_set2 = copy.deepcopy(self.board_set1)
            for i in range(len(self.board_set1)):
                for j in range(len(self.board_set1[0])):
                    if self.board_set1[i][j] == 'o':
                        self.board_set2[i][j] = partitions[n][k]    # could change to the Block object with the input of partitions[n][k]
                        k += 1
            boards.append(self.board_set2)

        return boards

    #def set_board(self, board):
    # we choose not to use this function and instead generate block objects only when called by laser
    # (attempt at optimizing, but not sure if it improved speed)

    def save_board(self,board): 
        '''
        A function to save potential boards to file.  This is to be used when
        the solution is found, but can also be used for debugging.
        **Parameters**
            board: *list*
                The board list we want to write to the original file
        
        **Returns**
            None
        '''
        fptr2 = open(self.fname, 'a')
        fptr2.write('# Here is the solve:')

        for i in range(len(board)):
            fptr2.write(str(board[i]))
            
        fptr2.close()

    def run(self): # main code to test variuos permutations

        # initialize as unsolved
        self.solvenum = -1
        self.goodboard = None

        # Get all boards
        print("Generating all the boards..."),
        sys.stdout.flush()
        boards = self.generate_boards()
        print("Done")
        sys.stdout.flush()

        print("Playing boards...")
        sys.stdout.flush()

        # Loop through the boards, and "play" them
        for b_index, board in enumerate(boards):

            # reset lasers and points
            all_points = copy.deepcopy(self.point_set)
            all_lasers = copy.deepcopy(self.lazor_set)

            solved = 0
            done = 0
            iters = 0
            while not done and iters < 50:
                # maximum 50 iterations to deal with infinite looping lasers
                # (only possible if refract block involved)
                iters += 1

                # loop through and update lasers and points
                for l in range(len(all_lasers)):
                    all_points,new_laser = all_lasers[l].update(board, all_points,self.length,self.height)
                    # add new laser to list if refracted
                    if new_laser is not None:
                        all_lasers.append(Laser(new_laser[0],new_laser[1]))

                # get rid of points that we already hit and lasers that were destroyed   
                for l in range(len(all_lasers)):
                    if l < len(all_lasers) and all_lasers[l].killed:
                        del(all_lasers[l])
                for p in range(len(all_points)):
                    if p < len(all_points) and all_points[p].intersect:
                        del(all_points[p])

                # stop conditions:  
                # if we hit all points, were done and solved
                if all_points == []:
                    done = 1
                    solved = 1
                # if no lasers left but points not hit, then we failed
                elif all_lasers == []:
                    done = 1
                else:
                    pass

            # break out of loop if we solved it (no need to go through other permutations) and retain winning board      
            if solved:
                self.solvenum = b_index
                self.goodboard = board
                break

        # print correct board 
        if self.goodboard != None:
            print('Solution:')
            print('-'* (2 *len(self.goodboard[0])+1))
            for i in range(len(self.goodboard)):
                for j in range(len(self.goodboard[0])):
                    print('|'+ str(self.goodboard[i][j]), end = '')
                print ('|')
                print('-'* (2 *len(self.goodboard[0])+1))

            self.save_board(self.goodboard)
        else: 
            print('No solution found...')
