import numpy as np
import pylab as plt
import networkx as nx

# map cell to cell, add circular cell to goal point
points_list = [(0,4), (0,6), (1,5), (1,7), (2,4), (2,6), (3,5), (3,7), (4,8), (4,10), (5,9), (5,11), (6,8), (6,10), (7,9), (7,11)]

goal = [8, 11]

#G=nx.Graph()
#G.add_edges_from(points_list)
#pos = nx.spring_layout(G)
#nx.draw_networkx_nodes(G,pos)
#nx.draw_networkx_edges(G,pos)
#nx.draw_networkx_labels(G,pos)
#plt.show()

# how many points in graph? x points
MATRIX_SIZE = len(points_list)

# create matrix x*y
R = np.matrix(np.ones(shape=(MATRIX_SIZE, MATRIX_SIZE)))
R *= -1


#print(np.matrix(R))

# assign zeros to paths and 100 to goal-reaching point
for point in points_list:
    #print(point)
    if point[1] in goal:
        R[point] = 100
    else:
        R[point] = 0

#    if point[0] in goal:
#        R[point[::-1]] = 100
#    else:
#        # reverse of point
#        R[point[::-1]]= 0

# add goal point round trip
R[goal,goal]= 100

print(np.matrix(R), end=' ')


Q = np.matrix(np.zeros([MATRIX_SIZE,MATRIX_SIZE]))
print(Q)

# learning parameter
gamma = 0.8

initial_state = 1

def available_actions(state):
    current_state_row = R[state,]
    av_act = np.where(current_state_row >= 0)[1]
    return av_act


#current_state = np.random.randint(0, 8)
#available_act = available_actions(current_state)
#print('current_state')
#print(current_state)
#print('available_act')
#print(available_act)

def sample_next_action(available_actions_range):
    next_action = int(np.random.choice(available_act,1))
    return next_action

#action = sample_next_action(available_act)
#print('action')
#print(action)

def update(current_state, action, gamma):
  max_index = np.where(Q[action,] == np.max(Q[action,]))[1]

  if max_index.shape[0] > 1:
      max_index = int(np.random.choice(max_index, size = 1))
  else:
      max_index = int(max_index)
  max_value = Q[action, max_index]
  
  Q[current_state, action] = R[current_state, action] + gamma * max_value
  print('max_value', R[current_state, action] + gamma * max_value)
  
  if (np.max(Q) > 0):
    return(np.sum(Q/np.max(Q)*100))
  else:
    return (0)

#score = update(current_state,action,gamma)
#print('score')
#print(score)

# Training
scores = []
for i in range(700):
    current_state = np.random.randint(0, 8)
    available_act = available_actions(current_state)
    action = sample_next_action(available_act)
    score = update(current_state,action,gamma)
    scores.append(score)
    #print ('Score:', str(score))
    
print("Trained Q matrix:")
print(Q/np.max(Q)*100)

# Testing
current_state = 0
steps = [current_state]

while current_state not in goal:

    next_step_index = np.where(Q[current_state,] == np.max(Q[current_state,]))[1]
    
    if next_step_index.shape[0] > 1:
        next_step_index = int(np.random.choice(next_step_index, size = 1))
    else:
        next_step_index = int(next_step_index)
    
    steps.append(next_step_index)
    current_state = next_step_index

print("Most efficient path:")
print(steps)

plt.plot(scores)
plt.show()
