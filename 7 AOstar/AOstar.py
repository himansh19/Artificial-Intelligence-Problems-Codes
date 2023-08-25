def aoStar(graph, H, startNode):     # AO* algorithm with input data graph structure, heuristics and start node

    openList  = list()  # Openlist for nodes to be explored
    closeList = list()  # Closlist for nodes already processed 
    G = dict()          # F(X) = G(X) + H(X)
    S = dict()          # SOLVED status
    P = dict()          # PARENT of a node
    U = dict()          # UPDATED status for heuristic value
    
    openList.append([startNode])   # Initialization of openlist with startnode
    H[startNode] = 0               # Initialization for start node
    G[startNode] = 0               
    S[startNode] = False           
    P[startNode] = startNode      
    U[startNode] = False


    while S[startNode]==False:     # As long as startnode is not solved, loop!!
        print("--------------------------------------------------------------------------------------")
        print(openList)
        print(closeList)           # Printing status on each iteration
        print(H)
        print(S)
        print("---------------------------------------------------------------------------------------")
       
        bestNodeList=None                               # Compute node with lowest f(x) on AO Graph
        bestNodeCost=0
        for nodeList in openList:                       # Each element is a list
            currentNodeListHCost=0
            currentNodeListGCost=0
            for node in nodeList:                       # Compute G(X) and H(X) for each node in the list
                currentNodeListHCost = currentNodeListHCost + H[node]
                currentNodeListGCost = currentNodeListGCost + 1    # Weight between nodes is valued one, but can vary if weight matrix is supplied
            currentNodeListGCost=currentNodeListGCost + G[P[nodeList[0]]]      
            if bestNodeList==None or bestNodeCost>(currentNodeListGCost+currentNodeListHCost):
                bestNodeList=nodeList
                bestNodeCost=(currentNodeListGCost+currentNodeListHCost)
            print((currentNodeListGCost+currentNodeListHCost),":",nodeList)
        openList.remove(bestNodeList)                   # Move the best node(list) to close list of  
        closeList.append(bestNodeList)
                         
                                        
        for node in bestNodeList:                       # Process each node in the best node(list) for expansion
            if graph.get(node,None) == None:            # Expand each node with its child nodes
                S[node]=True                            # If node itself is child node, set the node as solved using S[X]
            elif S[node]==True:
                continue
            else:            
                for childNodeList in graph[node]:       # If child nodes lists are availabile, place each of them into openlist
                    if childNodeList not in openList and childNodeList not in closeList:
                        openList.append(childNodeList)
                        
                        for child in childNodeList:     # Initialize data of newly added node in the child node list
                            U[child] = False
                            S[child] = False
                            P[child] = node
                            G[child] = G[node] + 1      # Weight is set to 1, but can vary by weight matrix         
                    else:
                        for child in childNodeList:     # Update all the data of node already in closelist 
                            if G[child] > G[node] + 1:
                                U[child] = False
                                S[child] = False
                                G[child] = G[node] + 1
                                P[child] = node         

                    if childNodeList in closeList:      # If a node is updated, move back to open list  
                        closeList.remove(childNodeList)
                        openList.append(childNodeList)
    
        solved=True                                     # Checking all the node in the best node list are solved
        HeuristicCost=0
        for node in bestNodeList:
            solved=solved & S[node]
            HeuristicCost = HeuristicCost + H[node]

        if solved == True:                              # If all nodes in the best node list are solved, update its parent
            for node in bestNodeList:
                if U[P[node]] == False:                 # If parent's heuristic is not updated, updated it now and set the status
                    U[P[node]] = True
                    S[P[node]] = True
                    H[P[node]] = HeuristicCost + len(bestNodeList)
                    break
                    
                elif H[P[node]] > (HeuristicCost + len(bestNodeList)):  # If parent's heuristic is updated earlier
                    H[P[node]]  = (HeuristicCost + len(bestNodeList))   # update it with latest best value
                    S[P[node]]  = True
                    break
            
            for andedOrNodes in AOList:                                 # Check all parent nodes in a anded list are solved
                for node in bestNodeList:
                    if P[node] in andedOrNodes:
                        status  = True
                        for aoNode in andedOrNodes:                     # If all parent nodes in a anded list are solved
                            status = status & S[aoNode]
                        if status==True:                                # move back the parent node list back to openlist 
                            if andedOrNodes not in openList:            # for backtracking the revised heuristic values
                                openList.append(andedOrNodes)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")                            
    print("Final Heuristic values of nodes:",H)
    print("Final Solved status of nodes:",S)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
    
                                       
# Input data : heuristics, graph structure, anded/or list of nodes, start node    

h4 = {'S': 1, 'A': 7, 'B': 12, 'C': 13, 'D': 5, 'E': 6, 'F': 5, 'G': 7, 'H': 2}  # Heuristic values of Nodes 

graph4 = {                                        # Graph of Nodes and Edges 
    'S': [['A','B'], ['C']],                      # Neighbors of Node 'A', B, C & D with repective weights 
    'A': [['D'], ['E']],                          # Neighbors are included in a list of lists
    'C': [['F','G']],
    'D': [['H']]                              # Each sublist indicate a "OR" node or "AND" nodes
}
AOList=[['S'],['A','B'],['C'],['D'],['E'],['F','G'],['H']]
aoStar(graph4, h4, 'S')