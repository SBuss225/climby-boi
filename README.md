# climby-boi
My precious AI son who likes to climb colorful rocks.

# Assumptions
- flat climbing wall (only considering x and y axes)
- two hands can be on the same hold, but not two feet or a hand and foot
- the (x,y) pair of for a handhold is its top middle where you can actually hold
- general human torso shape is approximately a rectangle

# Tasks
## Phase 1 - base agent
- create data object for climbing wall 
- create initial measurements & limitations for agent (height, arm length, leg length)
- have agent calculate distance between handholds
- create algorithm for calculating shortest path (start with greedy)
- test with set walls
- maybe create feature to make it easier to create own walls?
- test with randomized walls 

## Phase 2 - display
- display wall and path
- show agent climbing the path

## Phase 3 - base interpreter
- have interpreter code translate image into data object
  - give height of wall as parameter 
  - distinguish between wall and handholds
  - determine start and end points (lowest reachable handholds -> bell or just top ledge of wall)

# Improvements 
## Agent
- add more measurements/limitations (leg flexibility, jump v no jump, foot swap v no foot swap)
- try different path finding algorithms (MCTS, backtracking search, deterministic search, markov decision process)
- take handhold color into account
- initialize position at the bottom of the wall better

## Interpreter
- have interpreter calc height of wall based on height of person in picture, enter person's height as param
- have interpreter compensate for angles/perspective distortion
- have interpreter recognize different colored handholds

## User interaction/ versatility
- allow measurements to be edited (will affect agent's reach and therefore potential paths)
- allow path color to be specified 
- use camera as input/output for AR

# Future work
- specify where exactly on the handholds you can actually get a grip rather than just having an (x,y) in the top middle assuming that's where the best hold is
- indicate what type each handhold is as well (jugs, pinches, slopers, crimps, edges, crack, etc.)
- give more advice for specific moves than just what holds to use
- allow agent to brace one foot against wall instead of putting it on a hold in places where that would be helpful
- add sloping walls (both negative and positive)
- have preset options for different levels (beginner = basic, intermediate = allow foot swaps, master = allow jumps, harder grips, etc.)
- allow for measurements in different metrics
- have hand/foot dominance influence which limbs move first
- only enter a few measurements and allow the rest to be estimated based on general proportions 
- make body proportions more accurate