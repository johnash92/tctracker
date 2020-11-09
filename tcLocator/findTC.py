def findTC(inputs):
    if inputs.stormName == None:
        if inputs.findAll:
            allStorms = findMultipleTCs(inputs)
        else:
            initLat, initLon = findSingleTC(inputs)
    else:
        bestLats, bestLon = findIBTrACSTC(inputs)

