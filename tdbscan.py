"""
T-DBSCAN
Author: Jaya
"""

import math
from datetime import timedelta
from geopy.distance import great_circle
"""
INPUTS:
    df={o1,o2,...,on} Set of objects
    spatial_threshold = Maximum geographical coordinate (spatial) distance value
    temporal_threshold = Maximum non-spatial distance value
    min_neighbors = Minimun number of points within Eps1 and Eps2 distance
OUTPUT:
    C = {c1,c2,...,ck} Set of clusters
"""
def T_DBSCAN(df, CEps,Eps, MinPts):
    
    C = 0
    Cp = {}
    UNMARKED = 777777
    VISITED = 1
    
    df['cluster'] = UNMARKED
    df['visited'] = UNMARKED
    MaxId = -1    
        
    for index, P in df.iterrows():
        if index > MaxId:
            df.set_value(index, 'visited', VISITED)
            
            #search for continuous density-based neighbours N
            N = getNeighbors(P, CEps, Eps, df, index)
            MaxId = index
            
            if len(N) > MinPts: #new cluster
                C = C + 1
                
            # assign a label to core point
            (Ctemp, MaxId) = expandCluster(P, N, CEps, Eps, MinPts, MaxId, df) #expand the cluster
            
            if C in Cp:
                Cp[C] = Cp[C] + Ctemp
            else:
                Cp[C] = Ctemp
            
            Cp = mergeClusters(Cp)  #merge clusters

                    
    return Cp


# Retrieve neighbors
def getNeighbors(P, CEps, Eps, df, p_index):
    
    neighborhood = []
    center_point = df.loc[p_index]
    
    for index, point in df.iterrows():
        if index > p_index:
            distance = great_circle((center_point['latitude'], center_point['longitude']), (point['latitude'], point['longitude'])).meters
            if distance < Eps:
                neighborhood.append(index)
            elif distance > CEps:
                 break
    return neighborhood
        
 
    
#cluster expanding
def expandCluster(P, N, CEps, Eps, MinPts, MaxId, df):
    
    Cp = []
    N2 = []
    
    Cp.append(P)
    
    for index, point in N:
        df.loc[index]['visited'] = 'visited'
        if index > MaxId:
            MaxId = index
        
        #find neighbors of neighbors of core point P
        N2 = getNeighbors(point, CEps, Eps, df, index)    
        if len(N2) >= MinPts:
            #classify the points into current cluster based on definitions 3,4,5
            N = N + N2
        
        if point not in Cp:
            Cp.append(point)
            
        return Cp, MaxId
            
#merge clusters
def mergeClusters(Cp):
     
     Buffer = {}
     
     
     for idx, val in enumerate(Cp):
         
         #add first item to buffer by default
         if not Buffer: #if buffer is empty
             Buffer[idx] = val
          
         else: #compare last item in the buffer with Cp
             if max(Buffer[list(Buffer.keys())[-1]]) <= min(Cp[idx]): #new cluster = new Buffer entry
                 Buffer[(list(Buffer.keys())[-1])+1] = Cp[idx]
             else: #merge last item in the buffer with Cp
                 Buffer[list(Buffer.keys())[-1]] += Cp[idx]
                 
     return Buffer
                 
             
             
        
     
# =============================================================================
#      for i, val in enumerate(keyList):
#          if max(Cp[val][0]) >= min(Cp[keyList[i+1]][0]):
#              if max(Cp[keyList[i]]) < min(Cp[keyList[i+1]]): #add the clusters to be merged in a new buffer. Python does not allow deletion of keys in loop
#                  Buffer[keyList[i]] = keyList[i+1]
#      
#      for key, val in sorted(list(Buffer.items()), key = lambda x:x[0].lower(), reverse=True):
#          Cp[key] = Cp[key]+Cp[val]
#          Cp.pop(val)
#      return Cp
# =============================================================================
# =============================================================================
#     # initialize each point with unmarked
#     df['cluster'] = UNMARKED
#     
#     # for each point in database
#     for index, point in df.iterrows():
#         if df.loc[index]['cluster'] == UNMARKED:
#             neighborhood = retrieve_neighbors(index, df, spatial_threshold, temporal_threshold)
#             
#             if len(neighborhood) < min_neighbors:
#                 df.set_value(index, 'cluster', NOISE)
# 
#             else: # found a core point
#                 cluster_label = cluster_label + 1
#                 df.set_value(index, 'cluster', cluster_label)# assign a label to core point
# 
#                 for neig_index in neighborhood: # assign core's label to its neighborhood
#                     df.set_value(neig_index, 'cluster', cluster_label)
#                     stack.append(neig_index) # append neighborhood to stack
#                 
#                 while len(stack) > 0: # find new neighbors from core point neighborhood
#                     current_point_index = stack.pop()
#                     new_neighborhood = retrieve_neighbors(current_point_index, df, spatial_threshold, temporal_threshold)
#                     
#                     if len(new_neighborhood) >= min_neighbors: # current_point is a new core
#                         for neig_index in new_neighborhood:
#                             neig_cluster = df.loc[neig_index]['cluster']
#                             if (neig_cluster != NOISE) & (neig_cluster == UNMARKED): 
#                                 # TODO: verify cluster average before add new point
#                                 df.set_value(neig_index, 'cluster', cluster_label)
#                                 stack.append(neig_index)
#     return df
# 
# 
# def retrieve_neighbors(index_center, df, spatial_threshold, temporal_threshold):
#     neigborhood = []
# 
#     center_point = df.loc[index_center]
# 
#     # filter by time 
#     min_time = center_point['date_time'] - timedelta(minutes = temporal_threshold)
#     max_time = center_point['date_time'] + timedelta(minutes = temporal_threshold)
#     df = df[(df['date_time'] >= min_time) & (df['date_time'] <= max_time)]
# 
#     # filter by distance
#     for index, point in df.iterrows():
#         if index != index_center:
#             distance = great_circle((center_point['latitude'], center_point['longitude']), (point['latitude'], point['longitude'])).meters
#             if distance <= spatial_threshold:
#                 neigborhood.append(index)
# 
#     return neigborhood
# =============================================================================
