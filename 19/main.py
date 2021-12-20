import numpy as np

f = open("input.txt", "r")
L = f.read().split("\n\n")
f.close()

L[-1] = L[-1][:-2] # remove last linebreak

scanners = []
for elt in L :
    elt = elt.split("\n")[1:]
    scan = np.zeros((3, len(elt)), np.int32)
    for i,pos in enumerate(elt) :
        scan[:,i] = [int(e) for e in pos.split(",")]
    scanners.append(scan)

perm1 = [0, 0, 1, 1, 2, 2]
perm2 = [1, 2, 0, 2, 0, 1]
perm3 = [2, 1, 2, 0, 1, 0]
sign1 = [ 1,  1,  1,  1, -1, -1, -1, -1]
sign2 = [ 1,  1, -1, -1,  1,  1, -1, -1]
sign3 = [ 1, -1,  1, -1,  1, -1,  1, -1]
rotations = []
for p1, p2, p3 in zip(perm1, perm2, perm3) :
    for s1, s2, s3 in zip(sign1, sign2, sign3) :
        newR = np.zeros((3,3), np.int32)
        newR[0, p1] = s1
        newR[1, p2] = s2
        newR[2, p3] = s3
        rotations.append(newR)



def fitScanner(scanner, scanRef) :
    for rot in rotations : #48
        scan = np.matmul(rot, scanner)
        for jRef in range(scanRef.shape[1]) : #~25+
            for jScan in range(scan.shape[1]) : #~25
                vecShift = scan[:, jScan] - scanRef[:, jRef]
                alignsToRef = np.zeros(scan.shape[1], bool)
                for jBeacon in range(scan.shape[1]) : #~25
                    for jBeaconRef in range(scanRef.shape[1]) : #~25+
                        if all(scan[:, jBeacon] == scanRef[:, jBeaconRef] + vecShift) :
                            alignsToRef[jBeacon] = True
                            break #Won't align with 2 reference beacons
                if np.sum(alignsToRef) >= 12 :
                    notAligned = np.logical_not(alignsToRef)
                    newBeacons = scan[:, notAligned] - np.tile(vecShift[:, np.newaxis], (1, np.sum(notAligned)))
                    return np.concatenate((scanRef, newBeacons), 1), True
    return scanRef, False

scanRef = scanners[0]
scanAdded = [False for _ in range(len(scanners))]
scanAdded[0] = True
while True :
    for i in range(1, len(scanners)) :
        if not scanAdded[i] :
            scanRef, added = fitScanner(scanners[i], scanRef)
            scanAdded[i] = added
            if added :
                print(f"Added scanner: {i}, total beacons: {scanRef.shape[1]}")
            else :
                print(f"Failed to add scanner: {i}")
    if all(scanAdded) :
        break
