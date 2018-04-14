from __future__ import print_function
import sys
import copy
import itertools

# import the Point, Block, and Laser objects


class Game:
    '''
    The game grid.  Here we read in some user input, assign all our blocks,
    lasers, and points, determine all the possible different combinations
    of boards we could make, and then run through them all to try and find
    the winning one.
    '''

    def __init__(self, fptr):
        '''
        Difficulty 1

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


    # DO SOMETHING HERE SO WE CAN PRINT A REPRESENTATION OF GAME!
    def __str__(self):
        print('-'* (2 *len(self.board_set1[0])+1))
        for i in range(len(self.board_set1[0])):
            for j in range(len(self.board_set1[0])):
                print('|'+ str(self.board_set1[i][j]), end = '')
            print ('|')
            print('-'* (2 *len(self.board_set1[0])+1))

    def read(self, fptr):
        '''
        Difficulty 3

        Some function that reads in a file, and generates the internal board.

        **Parameters**

            fptr: *str*
                The file name of the input board to solve.

        **Returns**

            None
        '''
        self.fptr1 = open(fptr, 'r')
        self.fptr = self.fptr1.read()

        # self.block_set = []
        # self.lazor_set = []
        # self.point_set = []
        self.board_set1 = []
        data = [line for line in self.fptr.strip().split('\n') if not '#' in line]
        for i in range(len(data)):
            if i < len(data) and data[i]== '':
                del data[i]

        #create the list of board, block, lazor, point separately
        board_set = data[data.index('GRID START')+1:data.index('GRID STOP')]
        for i in range(len(board_set)):
            board_set[i]= board_set[i].replace(' ','')
        for i in range(len(board_set)):
    		self.board_set1.append(list(itertools.chain(board_set[i]))) 
    	self.length = len(self.board_set1[0])
		self.height = len(self.board_set1)

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

        #figure out the number of available space
        for i in range(len(self.board_set1)):
            for j in range(len(self.board_set1[0])):
                if self.board_set1[i][j] == 'o':
                    self.available_space += 1
        
        # make the list of original block set
        for i in range(len(self.block_set1)):
            for j in range(int(self.block_set[i][1])):
                self.blocks.append(self.block_set[i][0])

        # make the list of all permutations of blocks
        self.blocks_per = list(set(itertools.permutations(self.blocks)))


        self.fptr1.close()


    def generate_boards(self):
        '''
        Difficulty 3

        A function to generate all possible board combinations with the
        available blocks.

        First get all possible combinations of blocks on the board (we'll call these boards)
          We know we have self.blocks, and N_blocks = len(self.blocks)
          We also know we have self.available_space
          So, essentially we have to find all the possible ways to put N_blocks into
          self.available_space
        This becomes the "stars and bars" problem; however, we have distinguishable "stars",
        and further we restrict our system so that only one thing can be put in each bin.

        **Returns**

            None
        '''

        def get_partitions(n, k):
            '''
            A robust way of getting all permutations.  Note, this is clearly not the fastest
            way about doing this though.

            **Reference**

             - http://stackoverflow.com/a/34690583
            '''
            for c in itertools.combinations(range(n + k - 1), k - 1):
                yield [b - a - 1 for a, b in zip((-1,) + c, c + (n + k - 1,))]

        # Get the different possible block positions.  Note, due to the function we're using, we
        # skip any instance of multiple "stars in bins".
        partitions = [
            p for p in get_partitions(len(self.blocks), self.available_space) if max(p) == 1
        ]

        # Now we have the partitions, we just need to make our boards
        boards = []

        # add the permutationed blocks into the available_space partitions
        for n in range(len(self.blocks_per)):
            for i in range(len(partitions)):
                k = 0
                for j in range(len(partitions[0])):
                    if partitions[i][j] == 1:
                        partitions[i][j] = self.blocks_per[n][k]
                        k += 1
                    elif partitions[i][j] == 0:
                		partitions[i][j] = 'o'
        
        # add the block partitions into the boards
        for n in range(len(partitions)):
    		k = 0
    		for i in range(len(self.board_set1)):
        		for j in range(len(self.board_set1[0])):
            		if self.board_set1[i][j] == 'o':
                		self.board_set1[i][j] = partitions[n][k]    # could change to the Block object with the input of partitions[n][k]
                		k += 1
    		boards.append(self.board_set1)

    	return boards

    def set_board(self, board):
        '''
        Difficulty 2

        A function to assign a potential board so that it can be checked.

        **Parameters**

            board: *list, Block*
                A list of block positions.  Note, this list is filled with
                None, unless a block is at said position, then it is a
                Block object.

        **Returns**

            None
        '''
        # YOUR CODE HERE
        pass

    def save_board(self,board): # need more testing.
        '''
        Difficulty 2

        A function to save potential boards to file.  This is to be used when
        the solution is found, but can also be used for debugging.

        **Returns**

            None
        '''
        # YOUR CODE HERE
        fptr2 = open("showstopper_2.input", 'a')
		fptr2.write('Here is the solving board')

		for i in range(len(board)):
			for j in range(len(board[0])):
				if board[i][j]!= None:
					board[i][j] = board[i][j].btype()


		fptr2.write(board) 
		fptr2.close()

    def run(self):
        '''
        Difficulty 3

        The main code is here.  We call the generate_boards function, then we
        loop through, using set_board to assign a board, "play" the game,
        check if the board is the solution, if so save_board, if not then
        we loop.

        **Returns**

            None
        '''

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
            # Set board
            self.set_board(board)

            # MAYBE MORE CODE HERE?

            # LOOP THROUGH LASERS
            for j, laser in enumerate(current_lasers):
              child_laser = None
              child_laser = laser.update(self.board, self.points)

            # MAYBE MORE CODE HERE?

            # CHECKS HERE
