#xLim = (20, 30)
#yLim = (-10, -5)
xLim = (241, 273)
yLim = (-97, -63)

### Question 1 done analytically
#maxYspeed, maxIter = 9, 20
maxYspeed, maxIter = 96, 194

possibleStarts = []
# From paper analysis on yLim<0, the "time" of crossing the bucket can't be larger than -2*yLim[0]
for xSpeedStart in range(1, xLim[1] + 1) :
    for ySpeedStart in range(yLim[0], maxYspeed + 1) : # second term comes from question 1
        x, y = 0, 0
        xSpeed, ySpeed = xSpeedStart, ySpeedStart
        for _ in range(maxIter) :
            x, y = x + xSpeed, y + ySpeed
            xSpeed = max(0, xSpeed - 1)
            ySpeed = ySpeed - 1
            if x > xLim[1] or y < yLim[0] : # can't come back in
                break
            if x >= xLim[0] and y <= yLim[1] :
                possibleStarts.append((xSpeedStart, ySpeedStart))
                break


### Question 2
print(len(possibleStarts))
