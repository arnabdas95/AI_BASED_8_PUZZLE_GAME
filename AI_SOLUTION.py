import copy
class Node():
    def __init__(self,state,parent,move,heuristic_cost,depth):
        self.state=state
        self.parent=parent
        self.move=move
        self.heuristic_cost=heuristic_cost
        self.depth=depth
        self.list_of_child_huristic_cost = []
        # get the position of blank tiles
        self.blank_index = self.state.index(9)
        self.blank_tile_row = self.blank_index // 3
        self.blank_tile_col = self.blank_index % 3

    #manhattan distance or huristic function 1
    def manhattan_distance(self, new_state, GOAL_STATE):
        sum_manhuttan_distance = 0
        for item in GOAL_STATE:
            # find row and col of GOAL STATE
            goal_row = (item - 1) // 3
            goal_col = (item - 1) % 3

            # find the index of item is in the new state
            state_index = new_state.index(item)

            # find row and col of NEW STATE
            new_row = state_index // 3
            new_col = state_index % 3
            sum_manhuttan_distance += (abs(goal_row - new_row) + abs(goal_col - new_col))
        return sum_manhuttan_distance

    #g(n) function / cost of misplaced tiles /heuristic function 2
    def heuristic_fn2(self,new_state, GOAL_STATE):
        #as discard the blank tile cost so -1
        g_of_n =-1
        for item in range(len(GOAL_STATE)):
            if GOAL_STATE[item]!=new_state[item]:
                g_of_n +=1
        return g_of_n

    #f(n) = g(n)+h(n)
    # def total_huristic_f_of_n(self):
    #     return self.manhattan_distance(self.new_state, GOAL_STATE)+self.heuristic_fn2(self.new_state, GOAL_STATE)

    #check already visited state or not if not then add it to the set
    #as list is mutable so convert it to tuple then add it to set or error occured
    def check_visited_or_not(self,new_state):
        if tuple(new_state)  in visited_state_set:
            return False
        visited_state_set.add(tuple(new_state))
        return True

    #choose /sort the best heuristic among all child node
    def get_best_huristic_among_all_child(self):
        self.list_of_child_huristic_cost.sort(key=lambda x: x[1])
        return self.list_of_child_huristic_cost[0]

#move function - up, down ,left ,right
    def left_move(self):
        if self.blank_tile_col>0:
            blank_index = self.state.index(9)
            left_child_state=copy.deepcopy(self.state)
            #interchanging blank and left tile
            left_child_state[blank_index], left_child_state[blank_index-1]=left_child_state[self.blank_index-1], left_child_state[self.blank_index]
            return left_child_state
    def right_move(self):
        if self.blank_tile_col < 2:
            blank_index = self.state.index(9)
            right_child_state = copy.deepcopy(self.state)
            # interchanging blank and right tile
            right_child_state[blank_index], right_child_state[blank_index +1] = right_child_state[self.blank_index + 1], \
                                                                          right_child_state[self.blank_index]
            return right_child_state
    def up_move(self):
        if self.blank_tile_row > 0:
            blank_index = self.state.index(9)
            up_child_state = copy.deepcopy(self.state)
            # interchanging blank and up tile
            up_child_state[blank_index], up_child_state[blank_index - 3] = up_child_state[self.blank_index - 3], \
                                                                               up_child_state[self.blank_index]
            return up_child_state

    def down_move(self):
        if self.blank_tile_row < 2:
            blank_index = self.state.index(9)
            down_child_state = copy.deepcopy(self.state)
            # interchanging blank and down tile
            down_child_state[blank_index], down_child_state[blank_index +3] = down_child_state[self.blank_index +3], \
                                                                               down_child_state[self.blank_index]
            return down_child_state



# Global variable declare
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#INITIAL_STATE = [2,7,3,5,9,4,1,6,8]
#INITIAL_STATE= [1,3,4,8,6,2,7,9,5] #easy
INITIAL_STATE = [1, 2, 5, 4, 3, 6, 7, 9, 8]

initial_to_goal_path = []
visited_state_set = set()
vs =[]
node = Node(INITIAL_STATE,None,None,0,0)
node_queue =[]

#before start check if initial state is also goal state then don't run while
if GOAL_STATE== INITIAL_STATE:
    print("win")
    exit(0)

while(True):
    left_move_child =node.left_move()
    right_move_child =node.right_move()
    up_move_child = node.up_move()
    down_move_child = node.down_move()
    print(f"new state created-parent ={node.state}")
    print(f"left_move_child={left_move_child},right_move_child= {right_move_child},up_move_child= {up_move_child},down_move_child= {down_move_child}")

    if left_move_child !=None:
       # if node.check_visited_or_not(left_move_child):
       if left_move_child not in vs:
            vs.append(left_move_child)
            if left_move_child != GOAL_STATE:
              left_child_total_huristic_cost =node.heuristic_fn2(left_move_child,GOAL_STATE)+node.manhattan_distance(left_move_child, GOAL_STATE)
              node.list_of_child_huristic_cost.append(['LEFT_MOVE',left_child_total_huristic_cost])
              print(f"left-child heuristic value{left_child_total_huristic_cost}")
            else:
                print("win")
                initial_to_goal_path.append("LEFT_MOVE")
                break

    if right_move_child != None:
        # if node.check_visited_or_not(right_move_child):
        if right_move_child not in vs:
            vs.append(right_move_child)
            if right_move_child != GOAL_STATE:
                right_child_total_huristic_cost = node.heuristic_fn2(right_move_child, GOAL_STATE) + node.manhattan_distance(
                    right_move_child, GOAL_STATE)
                node.list_of_child_huristic_cost.append(['RIGHT_MOVE', right_child_total_huristic_cost])
                print(f"rightt-child heuristic value{right_child_total_huristic_cost}")
            else:
                print("win")
                initial_to_goal_path.append("RIGHT_MOVE")
                break

    if up_move_child != None:
        #if node.check_visited_or_not(up_move_child):
        if up_move_child not in vs:
            vs.append(up_move_child)
            if up_move_child != GOAL_STATE:
                up_child_total_huristic_cost = node.heuristic_fn2(up_move_child, GOAL_STATE) + node.manhattan_distance(
                    up_move_child, GOAL_STATE)
                node.list_of_child_huristic_cost.append(['UP_MOVE', up_child_total_huristic_cost])
                print(f"up-child heuristic value{up_child_total_huristic_cost}")
            else:
                print("win")
                initial_to_goal_path.append("UP_MOVE")
                break

    if down_move_child != None:
        #if node.check_visited_or_not(down_move_child):
        if down_move_child not in vs:
            vs.append(down_move_child)
            if down_move_child != GOAL_STATE:
                down_child_total_huristic_cost = node.heuristic_fn2(down_move_child, GOAL_STATE) + node.manhattan_distance(
                    down_move_child, GOAL_STATE)
                node.list_of_child_huristic_cost.append(['DOWN_MOVE', down_child_total_huristic_cost])
                print(f"down-child heuristic value{down_child_total_huristic_cost}")
            else:
                print("win")
                initial_to_goal_path.append("DOWN_MOVE")
                break
    print("huristic function calculated")
    #add best path and huristic value
    desired_move =( node.get_best_huristic_among_all_child())
    initial_to_goal_path.append(desired_move[0])
    print(desired_move)
    #print(f"set{visited_state_set}")
    #set new parent node among the child node
    if desired_move[0]=='LEFT_MOVE':
        node = Node(left_move_child, node.state, 'LEFT',desired_move[1],node.depth+1)

    if desired_move[0] == 'RIGHT_MOVE':
        node = Node(right_move_child, node.state, 'RIGHT', desired_move[1], node.depth + 1)

    if desired_move[0] == 'UP_MOVE':
        node = Node(up_move_child, node.state, 'UP', desired_move[1], node.depth + 1)

    if desired_move[0] == 'DOWN_MOVE':
        node = Node(down_move_child, node.state, 'DOWN', desired_move[1], node.depth + 1)

    print(f"depth={node.depth},state={node.state},move={node.move}")

print(initial_to_goal_path)