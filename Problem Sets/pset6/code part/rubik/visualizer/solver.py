import rubik

l = [value for _, value in rubik.quarter_twists_names.items()]
counter_twist_names = dict()
names_to_moves = {val: key for key, val in rubik.quarter_twists_names.items()}

for i in range(len(l)):
    if i%2 == 0:
        counter_twist_names[l[i]] = l[i + 1]
    else:
        counter_twist_names[l[i]] = l[i - 1]

def neighbors(v):
    """
    Returns neighbors of the given vertex
    
    """
    applied_twists = []
    
    for twist in rubik.quarter_twists:
        applied_twists.append((rubik.quarter_twists_names[twist] ,rubik.perm_apply(twist, v)))
            
    return applied_twists

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    level_forward = {start: 0}
    level_backward = {end: 0}
    parent_forward = {start: None}
    parent_backward = {end: None}
    i_forward = 1
    i_backward = 1
    frontier_forward = [start]
    frontier_backward = [end]
    
    while set(frontier_forward).intersection(set(frontier_backward)) == set():
        
        if i_forward > 8 or i_backward > 8:
            return None
        
        next_forward = []
        next_backward = []
        
        #From start to end
        for u_forward in frontier_forward:
            for v_label, v_forward in neighbors(u_forward):
                
                if v_forward not in level_forward:
                    level_forward[v_forward] = i_forward
                    parent_forward[v_forward] = counter_twist_names[v_label]
                    #parent_forward[v_forward] = v_label
                    next_forward.append(v_forward)
                    
        frontier_forward = next_forward
        i_forward += 1
        
        #From end to start
        for u_backward in frontier_backward:
            for v_label, v_backward in neighbors(u_backward):
                
                if v_backward not in level_backward:
                    level_backward[v_backward] = i_backward
                    parent_backward[v_backward] = counter_twist_names[v_label]
                    #parent_backward[v_backward] = v_label
                    next_backward.append(v_backward)
                    
        frontier_backward = next_backward
        i_backward += 1
        
    soln = set(frontier_forward).intersection(set(frontier_backward)).pop()
    soln_forward = soln
    soln_backward = soln
    path_forward = []
    parent_move = parent_forward[soln_forward]
    parent = rubik.perm_apply(names_to_moves[parent_move], soln_forward)
    while parent != start:
        path_forward.append(counter_twist_names[parent_move])
        soln_forward = parent
        parent_move = parent_forward[soln_forward]
        parent = rubik.perm_apply(names_to_moves[parent_move], soln_forward)
        
    path_forward.append(counter_twist_names[parent_move])
    path_forward.reverse()
    
    path_backward = []
    parent_move = parent_backward[soln_backward]
    parent = rubik.perm_apply(names_to_moves[parent_move], soln_backward)
    # print('parent move is: ', parent_move, type(parent_move))
    # print(soln_backward)
    while parent != end:
        path_backward.append(parent_move)
        soln_backward = parent
        parent_move = parent_backward[soln_backward]
        # print('In the loop: ', parent_move)
        parent = rubik.perm_apply(names_to_moves[parent_move], soln_backward)
    
    path_backward.append(parent_move)
        
    return [names_to_moves[move] for move in path_forward + path_backward]
    #return i_forward, len(set(frontier_forward).intersection(set(frontier_backward))), set(frontier_forward).intersection(set(frontier_backward))
                    
        
                
    
