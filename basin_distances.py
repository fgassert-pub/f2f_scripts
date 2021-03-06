import flowaccumulator
import pandas as pd
import numpy as np
from geopy.distance import great_circle


BASIN_CENTROIDS = "basin_centroids.csv"
OUTCSV = "basin_distances.csv"



def f0(i, X, Y, dIDs):
    if dIDs[i] > 0:
        p1 = Y[i],X[i]
        p2 = Y[dIDs[i]-1],X[dIDs[i]-1]
        return great_circle(p1,p2).kilometers
    return 0
def f(i, idx, values, X, Y, dIDs):
    if dIDs[i] > 0:
        p1 = Y[i],X[i]
        p2 = Y[dIDs[i]-1],X[dIDs[i]-1]
        return great_circle(p1,p2).kilometers
    return 0

def main():
    df = pd.read_csv(BASIN_CENTROIDS)
    ids = df["BasinID"]
    print np.sum(ids-np.arange(len(ids))-1)
    assert np.sum(ids-np.arange(len(ids))-1)==0
    d_ids = df["dwnBasinID"]
    args = [df["centroid_x"],df["centroid_y"],df["dwnBasinID"]]

    values = flowaccumulator.accumulate(ids, d_ids, f0, f, *args)
    df["distance2downstream"] = values
    df.to_csv(OUTCSV)

if __name__=="__main__":
    main()
