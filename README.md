# climby-boi
My precious AI son who likes to climb colorful rocks.

# Assumptions
- flat climbing wall (only considering x and y axes)
- two hands can be on the same hold, but not two feet or a hand and foot

# Tasks
## Phase 1 - base agent
- create data object for climbing wall 
- create initial measurements & limitations for agent (height, arm length, leg length)
- have agent calculate distance between handholds
- create algorithm for calculating shortest path (start with greedy)

## Phase 2 - display
- display wall and path
- show agent climbing the path

## Phase 3 - base interpreter
- have interpreter code translate image into data object
  - give height of wall as parameter 
  - distinguish between wall and handholds
  - determine start and end points (lowest reachable handholds -> bell)

# Improvements 
## Agent
- add more measurements/limitations (leg flexibility, jump v no jump, foot swap v no foot swap)
- try different path finding algorithms (MCTS, backtracking search, deterministic search, markov decision process)
- take handhold color into account

## Interpreter
- have interpreter calc height of wall based on height of person in picture, enter person's height as param
- have interpreter compensate for angles/perspective distortion
- have interpreter recognize different colored handholds

## User interaction/ versatility
- allow measurements to be edited (will affect agent's reach and therefore potential paths)
- allow path color to be specified 
- use camera as input/output for AR
