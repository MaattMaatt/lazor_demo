# lazor_demo

Python project by Yingqing Chen and Matthew Schofield

Click on **'view project on Github'** above to view project files (**master**  branch contains final solution)

## Motivation

Lazor is an app-based puzzle game where laser beams are used to light up specific grid points.  Blocks reflect, refract, and absorb laser beams and some blocks are moveable by the user.  There are more block types but are not considered in the scope of this assignment.

## Files: 

* **boards** - file folder containing 9 example Lazor boards, in format specified by hherbol.  Boards and approximate execution times are listed below:
	* braid_5 - .4 sec
	* diagonal_8 - (>30 min with solver, not solver2)
	* diagonal_9 - 150 sec
	* mad_1 - 11 sec (with solver, not solver2)
	* mad_7 - 25 sec
	* showstopper_2 - .01 sec
	* tricky_1 - .1 sec
	* vertices_1 - .5 sec
	* vertices_2 - .15 sec
* **objects** - object files used in the game
	* **block.py** - stores block type and outputs T/F when asked how a laser will interact with it.
	* **game2.py** - the main file that contains most of hte code to run the game.  Reads in board file, prints output, generates permutations of boards and runs each permutation, updating laser positions until the game ends.
	* **game.py** - different version of game2, see explanation below in "unresolved issues".
	* **laser.py** - lasers move in discrete steps, interacting with block objects as they cross them and updating points crossed.  (laserobject).update is the main machinery for progressing the solver.
	* **point.py** - stores a solution point and tells whether or not it has been intersected.
* **solver2.py** - **RUN THIS FILE** and specify game board to time the run of the game, print solution to command window and append to file (if already solved, will append again).
* **solver.py** - different version of solver2, see explanation below in  "unresolved issues".

## Unresolved issues

We report 2 versions of the solver, “solver.py” and “solver2.py” , each with their corresponding game files (“game.py” and “game2.py”).  The solver2 file works for most of the boards, but has an issue in the permutations that causes boards with more than one type of user input block to fail.  This means solver2 fails to solve diagonal_8 and mad_1, and could have caused tricky_1 to fail.

The issue is that solver2, while going through all permutations of position, does not porperly go through all permutations of block type, which is only an issue if there is more than one block type.

Why not use use only solver then?  It is much slower than solver2 when given the same board (tricky_1 in 55 sec instead of .1 sec).  We never fully resolved the speed issue, and ran out of time.  It could be ans issue with deepcopy(), by using too much memory.  We know the issue is in the board generation not the solving, since the solving portion is unchanged between the two versions.  It does solve mad_1 but does not solve diagonal_8 after 30 minutes of waiting, though we believe it would eventually solve it.

## Optimization:

Some considerations were made.  We ran out of time for more advanced optimization but still considered some things.  We ended the game running loop early when all points were hit or we ran out of lasers, and we did this by deleting laser and point objects as we went.  

Once a correct board was found, we stopped the game loop.  We chose to diverge from the demo code and generate block objects only when needed.  There is a tradeoff here - we don't generate an entire board of block objects which saves time but if multiple lasers hit a block or a laser gets stuck in a loop the same block is then generated multiple times. The reasoning is that larger boards have less percentage of blocks covered by lasers.  It is unclear if this sped up the solutions or not.  

Lasers may be trapped in infinite loops when a refract block is encountered.  We stopped the game at 50 update iterations so it would not run forever.  


With more time, we could have run each board as generated (the suplied demo code was not set up for this, but would have been possible to implement).  This could cut off a fraction of the time if the number of permutations is large.

With more time, we could have added more conditions to end the game early.  For example, if a laser is destroyed before it hits a block, and if we add a property to the laser class that detects this, and the game iteration would immediately end (this is assuming a well-designed game board that requires all lasers hit points to complete levels, which is true for any default Lazor board).  We ran out of time to implement this and other considerations.

Another consideration is the fact that refract blocks can trap a laser in infinite loops.  A better way than stopping the game at 50 iterations would be to save all previous laser positions in a new list and check that if a laser has the same position and direction as a previous laser it would be automatically destroyed.
