import iris

def boxConstraint(coords):
    if len(coords) != 4:
        raise Exception("Please provide coords as [minlat,maxlat,minlon,maxlon]")
    lon_constraint = iris.Constraint(longitude = lambda cell: \
                                     (cell < coords[3]) and (cell > coords[2]))
    lat_constraint = iris.Constraint(latitude = lambda cell: \
                                     (cell < coords[1]) and (cell > coords[0]))
    return lon_constraint&lat_constraint

