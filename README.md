# T-DBSCAN - Spatiotemporal Density Clustering for GPS Trajectory Segmentation

This is a pythonic implementation of the T-DBSCAN algorithm. Original paper: "T-DBSCAN: A Spatiotemporal Density Clustering for GPS Trajectory Segmentation".


## Steps
1. Download the **tdbscan.py** file and place it inside the Lib/site_packages folder
2. To call the algorithm use **df_clustered = tdbscan.T_DBSCAN(df, CEps, Eps, MinPts)**. Make sure the original data (df) is sorted based on timestamp. CEps is the outer serach radius, Eps is the inner serach radius and MinPts is the minimum number of points. 
