def calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygonA, fcPolygonB, idFieldPolygonB):
    try:
        import arcpy
        arcpy.env.workspace = input_geodatabase
            #sets the workspace as the gien gdb
        fcA = fcPolygonA
        fcB = fcPolygonB
            #these define variables for the input feature classes
        arcpy.management.AddField(fcA, "fcAArea","double")
        arcpy.management.AddField(fcB, "fcBArea","double")
            #these create area fields for the input feature classes
        arcpy.management.CalculateField(fcA, "fcAArea", "!shape.area!","PYTHON3", "", "DOUBLE")    
        arcpy.management.CalculateField(fcB, "fcBArea", "!shape.area!","PYTHON3", "", "DOUBLE")
            #these two lines calculate the area of the input feature classes
        arcpy.analysis.SummarizeWithin(fcB, fcA, "sumWithin", "", [['fcAArea', 'SUM']], "", "FEET")
            #this creates a feature class that adds up the area of fcA within fcB in feet
        pctA = "sumWithin"
            #this creates a variable for the summarized output feature class
        arcpy.management.AddField(pctA, "pctA","double")
            #this adds a field to the output feature class
        arcpy.management.CalculateField(pctA, "pctA", "!sum_fcAArea! / !fcBArea!","PYTHON3", "", "Double")
            #this calculates the percentage of fcA within fcB
        arcpy.management.AddJoin(fcB, "FIPS", pctA, "FIPS")
            #this joins the created feature class to the fcB input with FIPS as the key
    except arcpy.ExecuteError:
       print(arcpy.GetMessages(2))
            #this displays any error messages

