import flowaccumulator
import pandas as pd
import numpy as np


BASIN_DISTANCES = "basin_distances.csv"
BASIN_POP = "basin_pop.csv"
OUTCSV = "basin_weighted_downstream_001.csv"

def accumulate(ids, d_ids, values, distances, discount_rate=0.01):
    out = values.copy()
    computed = d_ids==0
    count = np.sum(computed)
    discount = 1-discount_rate
    while count < len(ids):
        print count
        compute = np.zeros(len(ids),dtype=bool)
        for i in ids[computed]:
            compute[np.asarray(d_ids==i)]=True
        for i in ids[compute]:
            out[i] = values[i]+values[d_ids[i]]*(discount**distances[i])
        computed = compute
        count += np.sum(compute)
    print count, "complete"
    return out


def main():
    df = pd.read_csv(BASIN_DISTANCES)
    df.set_index("BasinID", inplace=True)
    vdf = pd.read_csv(BASIN_POP)
    vdf.set_index("BASINID", inplace=True)
    df["pop"] = vdf["SUM"]
    df["pop"].fillna(0,inplace=True)

    df.sort(inplace=True)
    ids = df.index
    d_ids = df["dwnBasinID"]
    D = df["distance2downstream"]
    X = df["pop"]
    
    df["out"] = accumulate(ids,d_ids,X,D,0.001)
    df.to_csv(OUTCSV)

if __name__=="__main__":
    main()
