"""
T-DBSCAN
Author: Jaya
Source: Paper titled "T-DBSCAN: A Spatiotemporal Density Clustering for GPS Trajectory Segmentation"
"""

from geopy.distance import great_circle
"""
INPUTS:
    df={o1,o2,...,on} Set of objects
    CEps = Outer radius for density calculation
    Eps = Inner radius defining the density calculation 
    MinPts = Minimun number of points in neighborhood
OUTPUT:
    df = Updated dataframe with annotated clusters
"""

def T_DBSCAN(df, CEps,Eps, MinPts):
    
    C = 0
    Cp = {}
    UNMARKED = 777777
    
    
    df['cluster'] = UNMARKED
    df['visited'] = 'Not visited'
    MaxId = -1    
        
    for index, P in df.iterrows():        
        if index > MaxId:           
            
            df.set_value(index, 'visited', 'visited')            
            #search for continuous density-based neighbours N
            N = getNeighbors(P, CEps, Eps, df, index)
            MaxId = index            
            #create new cluster
            if len(N) > MinPts: 
                C = C + 1                
            #expand the cluster
            Ctemp, MaxId = expandCluster(P, N, CEps, Eps, MinPts, MaxId, df, index)            
            if C in Cp:
                Cp[C] = Cp[C] + Ctemp                             
            else:
                Cp[C] = Ctemp
                
    print("Clusters identified...")         
    Cp = mergeClusters(Cp) #merge clusters      
    df = updateClusters(df, Cp)  #update df     
       
    return df


# Retrieve neighbors
def getNeighbors(P, CEps, Eps, df, p_index):
    
    neighborhood = []
    center_point = P
    
    for index, point in df.iterrows():
        if index > p_index:
            distance = great_circle((center_point['latitude'], center_point['longitude']), (point['latitude'], point['longitude'])).meters
            if distance < Eps:
                neighborhood.append(index)
            elif distance > CEps:
                 break
             
    return neighborhood
        
 
    
#cluster expanding
def expandCluster(P, N, CEps, Eps, MinPts, MaxId, df, p_index):
    
    Cp = []
    N2 = []
    
    Cp.append(p_index)
    
    for index in N:
        point = df.loc[index]
        df.loc[index]['visited'] = 1
        if index > MaxId:
            MaxId = index     
        N2 = getNeighbors(point, CEps, Eps, df, index) #find neighbors of neighbors of core point P   
        if len(N2) >= MinPts: #classify the points into current cluster based on definitions 3,4,5            
            N = N + N2
        if index not in Cp:
            Cp.append(index)
            
    return Cp, MaxId
            
#merge clusters
def mergeClusters(Cp):
     
     Buffer = {}     
     
     print("Merging...")
     for idx, val in Cp.items():         
         
         if not Buffer: #if buffer is empty add first item by default
             Buffer[idx] = val
             
         else: #compare last item in the buffer with Cp             
             if max(Buffer[list(Buffer.keys())[-1]]) <= min(Cp[idx]): #new cluster = new Buffer entry
                 Buffer[(list(Buffer.keys())[-1])+1] = Cp[idx]
             else: #merge last item in the buffer with Cp
                 Buffer[list(Buffer.keys())[-1]] += Cp[idx]
                             
     return Buffer
                 
             
#update dataframe             
def updateClusters(df, Cp):
    
    for idx, val in Cp.items():
        for index in val:
            df.set_value(index, 'cluster', idx)
            
    return df
     
