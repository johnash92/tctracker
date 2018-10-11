def box_constraint(minlat,maxlat,minlon,maxlon):
    import iris
    # Create constraint to extract data from cube over a certain region
    longitude_constraint1=iris.Constraint(longitude = lambda cell:cell>minlon)
    longitude_constraint2=iris.Constraint(longitude = lambda cell:cell<maxlon)
    latitude_constraint1=iris.Constraint(latitude = lambda cell:cell>minlat)
    latitude_constraint2=iris.Constraint(latitude = lambda cell:cell<maxlat)
    box_constraint=longitude_constraint1&longitude_constraint2&latitude_constraint1&latitude_constraint2
    return box_constraint
