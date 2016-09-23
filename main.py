# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:40:19 2016

@author: leo

>>>>>>>>>>>>>>>>>>>>>>>>>>>>
BRUTFORCE SOLVER FOR SOKOBAN
>>>>>>>>>>>>>>>>>>>>>>>>>>>


#==============================================================================
# WHY ?
#==============================================================================

I was blocked at level 11 on my phone. I needed closure...

#==============================================================================
# HOW TO PLAY THE GAME ?
#==============================================================================

https://en.wikipedia.org/wiki/Sokoban

#==============================================================================
# HOW TO USE THE SOLVER ?
#==============================================================================

Input: Set the Sokoban map in parameters

_map_example =  \
                '''
                XXXXXX
                X....X
                X.B.PX
                XXM..X
                X.M.XX
                X.M.XX
                X.M.XX
                X.O.XX
                XXXXXX
                '''

Lexique:

                X: wall
                .: trail
                O: objective
                P: player
                N: player on objective
                B: block
                M: block on objective
                
Constraints:
                - Surround your map with walls
                - Put as many blocks as objectives
  
Run the python script to solve.


#==============================================================================
# OUTPUTS           
#==============================================================================

Prints the steps to the solution if any is found


#==============================================================================
# HOW DOES IT WORK ?
#==============================================================================

Bruteforce !! A memory of block position and reachable states is kept, to avoid
cycles. Some pruning heuristics are added to avoid useless computations

"""

def print_map(_map):
    for x in _map.split('\n'):
        print ' '.join(list(x)).replace('.', ' ')

def build_map(map_lines):
    return '\n'.join(map_lines)

def make_id_map(map_lines):
    '''Returns dict mapping id to coordinate'''
    id_map = dict()
    counter = 0
    for (i, line) in enumerate(map_lines):
        for (j, char) in enumerate(line):
            if char != 'X':
                id_map[counter] = [i, j]
                counter += 1
    return id_map
            
def move_coord(coord, move):
    '''move can be up, right, down, left, static'''
    if move == 'up':
        return [coord[0]-1, coord[1]]
    if move == 'right':
        return [coord[0], coord[1] + 1]
    if move == 'down':
        return [coord[0] + 1, coord[1]]
    if move == 'left':
        return [coord[0], coord[1] - 1]
    if move == 'static':
        return [coord[0], coord[1]]
            
     
            
def make_adj_map(id_to_coords, coords_to_id):
    adj_map = dict()
    # For all non X
    for _id, coord in id_to_coords.iteritems():
        # Initiate adjascent tiles
        adj_map[_id] = []
        # For allpossible directions
        for move in ['up', 'down', 'left', 'right']:
            new_coord = move_coord(coord, move)
            # Check if the tile in this direction is not a wall
            if str(new_coord) in coords_to_id:
                adj_map[_id].append(coords_to_id[str(new_coord)])
    return adj_map

def make_move_map(id_to_coords, coords_to_id):
    """
    Returns dict
    id is block position
    Value is list of couples (id_pusher, new_block_id)
    """
    move_map = dict()
    for _id, coord in id_to_coords.iteritems():
        move_map[_id] = []
        for (m1, m2) in [('up', 'down'), ('left', 'right')]:
            new_coord_1 = move_coord(coord, m1)
            new_coord_2 = move_coord(coord, m2)
            if (str(new_coord_1) in coords_to_id) \
                    and (str(new_coord_2) in coords_to_id):
                move_map[_id].append((coords_to_id[str(new_coord_1)], coords_to_id[str(new_coord_2)]))        
                move_map[_id].append((coords_to_id[str(new_coord_2)], coords_to_id[str(new_coord_1)]))                 
    return move_map

          
def get_curr_coord(_map):
    for i, line in enumerate(_map.split('\n')):
        for j, char in enumerate(line):
            if char == 'P':
                return [i, j]




    #    def get_corners(self):
    #        corners = []
    #        for _id, info in self.super_map.iteritems():
    #            for (move_1, move_2) in [('up', 'left'), ('up', 'right'), ('down', 'left'), ('down', 'right')]:
    #                import pdb
    #                pdb.set_trace()
    #                move_id(_id, move, self.id_to_coords, self.coords_to_id)

def get_block_pos(super_map):
    '''Postion of blocks'''
    square_pos = []
    for _id, square in super_map.iteritems():
        if square in ['B', 'M']:
            square_pos.append(_id)
    return set(square_pos)
    
    

def get_hash(reachable, block_pos):
    return hash(str(set(reachable)) + str(block_pos))
    
def move_block(super_map, curr_id, P_id, B_id, B_new_id):
    """
    Modifies the super_map

    Will move P to B_id and B to B_new_id
    """
    assert super_map[B_id] in ['B', 'M']
    assert super_map[B_new_id] not in ['B', 'M']
    ini_block_count = sum(val in ['B', 'M'] for val in super_map.values())
    
    new_super_map = super_map.copy()

    if sum(val in ['N', 'P'] for val in new_super_map.values()) != 1:
        print 'here'

    # New empty space
    if super_map[curr_id] == 'P':
        new_super_map[curr_id] = '.'
    else:
        new_super_map[curr_id] = 'O'
    
    # New block position
    if super_map[B_new_id] in ['P', '.']:
        new_super_map[B_new_id] = 'B'
    else:
        new_super_map[B_new_id] = 'M' # Block on objective
    
    # New player position
    if super_map[B_id] == 'B':
        new_super_map[B_id] = 'P'
    else:
        new_super_map[B_id] = 'N' #  Player on objective
        

    
    # Make sure we still have as many blocks
    end_block_count = sum(val in ['B', 'M'] for val in super_map.values())    
    assert end_block_count == ini_block_count    
    
    assert sum(val in ['N', 'P'] for val in new_super_map.values()) == 1

    return (B_id, new_super_map)
            


class Sokoban():
    def __init__(self, _map):
        # Clean map
        _map = '\n'.join(_map.strip().split())
        # Check map is valid 
        assert _map.count('O') + _map.count('N') == _map.count('B')
        
        # Write map
        self.og_map = _map.strip()
        
        
        
        self.map_lines = _map.split('\n')
        assert all(len(x) == len(self.map_lines[0]) for x in self.map_lines)
        self.shape = [len(self.map_lines), (len(self.map_lines[0]))]        
        
        
        # Link id to coords
        self.id_to_coords = make_id_map(self.map_lines)
        self.coords_to_id = {str(val):key for key, val in self.id_to_coords.iteritems()}

        # Get possible transitions
        self.adj_map = make_adj_map(self.id_to_coords, self.coords_to_id)
        
        # Get possible moves (moving a block):
        self.move_map = make_move_map(self.id_to_coords, self.coords_to_id)
        
        # Get objectives        
        self.objective_pos = self.get_objective_pos()
        
        # Compute outer obejctives for efficient pruning
        self.get_outer_objectives()



    def get_reachable(self, super_map, curr_id):
        reachable = []
        tryable = list(self.adj_map[curr_id])
        done = [curr_id]
        
        while tryable:
            _id = tryable.pop()
            # If this id is not blocked
            if not super_map[_id] in ['B', 'M']:
                # Add all neighbours that were not visited
                reachable.append(_id)
                tryable.extend(filter(lambda x: x not in done, self.adj_map[_id]))
            done.append(_id)
        return reachable + [curr_id]
            
    def get_objective_pos(self):
        '''Position of objectives'''
        square_pos = []
        for _id, coords in self.id_to_coords.iteritems():    
            if self.map_lines[coords[0]][coords[1]] in ['O', 'M', 'N']:
                square_pos.append(_id)
        return set(square_pos)                
 

    def make_map(self, super_map):
        new_map_lines = list(self.map_lines)
        for _id, val in super_map.iteritems():
            coords = self.id_to_coords[_id]
            new_map_lines[coords[0]] = new_map_lines[coords[0]][:coords[1]] + val \
                                    + new_map_lines[coords[0]][coords[1]+1:]
        new_map = '\n'.join(new_map_lines)
        return new_map
    
    
    def get_outer_objectives(self):
        map_lines = self.map_lines
        left = len(map_lines[0])
        right = 0
        up = len(map_lines)
        down = 0
        
        for x, line in enumerate(map_lines):
            for y, char in enumerate(line):
                if char in ['M', 'N', 'O']:
                    left = min(left, y)
                    right = max(right, y)
                    up = min(up, x)
                    down = max(down, x)
        self.outer_objectives = {'left': left, 'right': right, 'up': up, 'down': down}


def solve_sokoban(sokoban, verbose=True):   
    ## Current info
    # Make the super map 
    super_map = {}    
    for _id, coords in sokoban.id_to_coords.iteritems():
        super_map[_id] = sokoban.map_lines[coords[0]][coords[1]]
    
    # Current player id
    curr_coord = get_curr_coord(sokoban.og_map)
    curr_id = sokoban.coords_to_id[str(curr_coord)]
    
    
    
    hashs_done = []
    positions_to_try = [(curr_id, super_map, None)]
    
    all_done = {0: (curr_id, super_map)}
    
    
    counter = 0
    while positions_to_try:
        
        # Print progress
        if verbose and (counter%400 == 0):
                print '***********'
                print 'Iteration', counter, '// Pos to still to try:', len(positions_to_try)
        counter += 1
        
          
        # Try new position
        (curr_id, super_map, parent) = positions_to_try.pop()
        
        # For each turn 
        reachable = sokoban.get_reachable(super_map, curr_id)
        block_pos = get_block_pos(super_map)
    
        # Check if we were already in this position
        _hash = get_hash(reachable, block_pos)   
        if _hash in hashs_done:
            continue
        else:
            hashs_done.append(_hash)
        
        # Check if we won
        if block_pos == sokoban.objective_pos:
            print "Solution found Whoohoo !!"
            break
    
    
        # For all blocks
        for bp in block_pos:
            # Prune if a block is in a corner and is not an objective
            if (super_map[bp] == 'B') and (not sokoban.move_map[bp]):
                #print 'Prunned 1'
                break
            # Prune if block is outer 
        
            if (sokoban.id_to_coords[bp][1] == 1) and (sokoban.outer_objectives['left'] > 1):
                #print 'Prunned 2'
                break
            if (sokoban.id_to_coords[bp][1] == sokoban.shape[1] - 2) and (sokoban.outer_objectives['right'] < sokoban.shape[1] - 2):
                #print 'Prunned 3'
                break        
            if (sokoban.id_to_coords[bp][0] == 1) and (sokoban.outer_objectives['up'] > 1):
                #print 'Prunned 4'
                break        
            if (sokoban.id_to_coords[bp][0] == sokoban.shape[0] - 2) and (sokoban.outer_objectives['down'] > sokoban.shape[0] - 2):
                #print 'Prunned 5'
                break            
            
            # For potential moves
            for mv in sokoban.move_map[bp]:
                if mv[0] in reachable:
                    if super_map[mv[1]] not in ['B', 'M']:
                        #print mv, curr_id
                        (new_curr_id, new_super_map) = move_block(super_map, curr_id, mv[0], bp, mv[1])           
                        positions_to_try.append((new_curr_id, new_super_map, counter))
                        
                        
        all_done[counter] = (curr_id, super_map, parent)
    else:
        print 'No solution found :('
        return (False, None, None)
    all_done[counter] = (curr_id, super_map, parent)
    
    return (True, counter, parent, all_done)

def print_solve_sol(sokoban, counter, parent, all_done):
    # Reconstruct path and print
    parent_chain = [counter, parent]
    while parent != 1:
        parent = all_done[parent_chain[-1]][2]
        parent_chain.append(parent)
    
    
    print '\n{stars}\nSOLVED YOUR SOKOBAN: SEE HOW in {val} steps...\n{stars}\n'.format(val=len(parent_chain)-1, stars='*'*50)
    for num in parent_chain[::-1]:
        raw_input("\nPress Enter to see the following steps...\n")
        print_map(sokoban.make_map(all_done[num][1]))
    print '*** DONE ***'    
  
  
KONROW_MAPS = {3:\
    """
    XXXXXX
    XX..XX
    X.PBXX
    XXB.XX
    XX.B.X
    XOB..X
    XOOMOX
    XXXXXX
    """, 
    11:\
    """
    XXXXXXXX
    XX.P.XXX
    XX.XB..X
    X.MO.O.X
    X..BB.XX
    XXX.XOXX
    XXX...XX
    XXXXXXXX
    """,
    12: \
    """
    XXXXXX
    X....X
    X.B.PX
    XXM..X
    X.M.XX
    X.M.XX
    X.M.XX
    X.O.XX
    XXXXXX
    """
    }
  
if __name__ == '__main__':
    
    # Parameters
    _map = KONROW_MAPS[11]    
    verbose = True
    
    # Initiate game
    sokoban = Sokoban(_map.strip())

    # Solve sokoban
    (has_sol, counter, parent, all_done) = solve_sokoban(sokoban, verbose)

    # Print solution
    print_solve_sol(sokoban, counter, parent, all_done)
    


    