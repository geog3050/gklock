#GEOG3050
#Gretchen Klock and Grace Shipley
#Final Project: Optimal Path - Bus Function Code

#Set up environment and parameters
destinations = r"S:\2024_Spring\GEOG_3050\STUDENT\gklock\final\landmarks_revised\landmarks_revised.shp"
busRoutes = r"S:\2024_Spring\GEOG_3050\STUDENT\gklock\final\bus_routes\CTA_BusRoutes.shp"
busStops = r"S:\2024_Spring\GEOG_3050\STUDENT\gklock\final\bus_stops\CTA_BusStops.shp"
project_gdb = r"S:\2024_Spring\GEOG_3050\STUDENT\gklock\final\final.gdb"
def TravelBus(destinations, busRoutes, busStops, project_gdb):
    #Set up paramters and environment
    import arcpy
    arcpy.env.workspace = project_gdb
    arcpy.CheckOutExtension("network")
    arcpy.env.overwriteOutput = True

    #Spatial_Reference--its assumed that all data will be in the same spatial reference to begin with.
    desc = arcpy.Describe(busStops)

    #Create Feature Dataset and Copy Features
    arcpy.CreateFeatureDataset_management(project_gdb, "bus_FD", desc.spatialReference)
    routes = busRoutes
    stops = busStops
    landmarks = destinations
    arcpy.CopyFeatures_management(routes, project_gdb + "/bus_FD/routes")
    arcpy.CopyFeatures_management(stops, project_gdb + "/bus_FD/stops")
    arcpy.CopyFeatures_management(landmarks, project_gdb + "/bus_FD/landmarks")
    bus_feat_set = r"S:\2024_Spring\GEOG_3050\STUDENT\gklock\final_proj\final_proj.gdb\bus_FD"
    #routes_FD = r"S:\2024_Spring\GEOG_3050\STUDENT\gklock\final\final.gdb\bus_fd\routes"
    #stops_FD = r"S:\2024_Spring\GEOG_3050\STUDENT\gklock\final\final.gdb\bus_fd\stops"

    #Create Network Dataset
    arcpy.na.CreateNetworkDataset("bus_FD", "bus_ND", ["routes", "stops"])

    #Buildnetwork based off Dataset
    bus_ND = "bus_ND"
    arcpy.BuildNetwork_na(bus_ND)

    #Create Route Analysis Layer (where the optimal path will eventually be found)

    bestRoute = arcpy.na.MakeRouteAnalysisLayer(bus_ND, "myRoute", "Length", "FIND_BEST_ORDER")
    bestRoute = bestRoute.getOutput(0)

    #Associate network analysis class names with the route analysis layer
    naClasses = arcpy.na.GetNAClassNames(bestRoute15, "INPUT")
    
    #Gets field mappings for the destination class in the network analysis layer
    fieldMappings = arcpy.na.NAClassFieldMappings(bestRoute15, naClasses["Stops"])

    #Sets the default value for the length attribute to 0
    fieldMappings["Attr_Length"].defaultValue = 0

    #Adds the destination locations to the route analysis layer using the field mappings
    arcpy.na.AddLocations(bestRoute, "Stops", "/bus_FD/landmarks", fieldMappings)

    #This finds the most optimal route
    arcpy.na.Solve(bestRoute)

TravelBus(destinations, busRoutes, busStops, project_gdb)
