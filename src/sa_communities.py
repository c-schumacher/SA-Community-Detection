import numpy as np
import random
import math

def sa_communities(G, runs=1, temp=100, cooling_rate=0.01, min_steps=100, reset=5, constant=1, updates=False):
    def modularity(G, C):
        delta = np.equal.outer(C, C)
        Q_val = (G - mod_Si*mod_Sj/W) * delta/W
        return Q_val.sum()

    def delta_modularity(G, C, i, newC=None):  
        if C[i] == newC:
            return 0
        w = float(G.sum())
        sigma_out = G.sum(axis=1)    
        sigma_in = G.sum(axis=0)     
    
        I = C==newC
        Si = float(sum(G[i,:])) + float(sum(G[:,i]))                 
        Si_in = float(sum(G[i, I])) + float(sum(G[I, i]))           
        Sj_s = float(sum(sigma_out[I])) + float(sum(sigma_in[I]))               
        deltaQ = Si_in/w - (Si*Sj_s)/w**2
        return deltaQ
    
    def random_node(node_list):
        return random.choice(node_list)
     
    def flip_node_random(G, C, n):
        n_comm = C[n]
        connections = np.unique(np.append(np.nonzero(G[:,n])[0], np.nonzero(G[n,:])[0]))
        connected = [i for i in connections if C[i] != n_comm] 
        if len(connected) == 0: 
            return C
        new_c = None
        mx_Q = None
        deltaRemove = delta_modularity(G, C, n)
        for i in connected:
            deltaQ = delta_modularity(G, C, n, C[i]) - deltaRemove 
            if deltaQ > mx_Q:
                new_c = C[i]
                mx_Q = deltaQ 
        tmp_comms = np.copy(C)
        np.place(tmp_comms, tmp_comms==n, new_c)
        return tmp_comms
    
    res = []
    best_comms = None
    best_Q = 0.0
    
    W = float(G.sum()) 
    mod_Si = G.sum(axis=1)[:, None] - np.zeros(len(G))
    mod_Sj = G.sum(axis=0)[None, :] - np.zeros(len(G))
  
    node_idx = np.arange(0, len(G))
    communities = np.arange(0, len(G))
    for i in range(runs):
        n = random_node(node_idx)
        c = flip_node_random(G, communities, n)
        Q = modularity(G, c)

        min_steps = min_steps 
        step=0
        max_c = c
        max_Q = Q
        T = temp
       
        if updates:
            print "Starting temperature:", T
        while T > 1:
            u = random.uniform(0,1)
            n1 = random_node(node_idx)
            c1 = flip_node_random(G, c, n1)
            Q1 = modularity(G, c1)

            alpha = math.exp(1.0/T * constant * (Q1-Q))
            if u <= alpha:
                step += 1
                c = c1
                Q = Q1
            if step > min_steps:
                if Q > max_Q:
                    max_c = c
                    max_Q = Q
                if step%reset == 0:
                    Q = max_Q
                    c = max_c
            T *= 1 - cooling_rate 
            if updates:
                print "Temperature={0:.3f} and Q={1:.5f}".format(T, Q)     
        tmp = modularity(G, max_c)
        if tmp > best_Q:
            best_comms = max_c
            best_Q = tmp
        res.append(tmp)
    return (res, best_comms, best_Q)
