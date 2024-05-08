import arcpy
try:
    folder = "S:/2024_Spring/GEOG_3050/STUDENT/gklock/quiz 5/test"
    ### Rename to be the workspace with the airports.zip file ###
    arcpy.env.workspace = folder
        #This sets the workspace to be the chosen folder
    fcList = arcpy.ListFeatureClasses()
        #This creates a list of the feature classes in the workspace
    fcAirport = 'airports'
        #This sets fcAirport as the first item in the feature class list
    arcpy.management.AddField(fcAirport, "buffer", "LONG")
        #This creates a field named buffer with data type 'Long' for the airport feature class
    fields = ['FEATURE','TOT_ENP','buffer']
        #This makes a list of fields to be used in the cursor later
    with arcpy.da.UpdateCursor(fcAirport, fields) as cursor:
        for row in cursor:
            if row [0] != 'Airport' or 'Seaplane Base':
                row[2] = 0
                #if the Feature type is not airport or seaplane base, no buffer will be created
            if row[1] < 1000:
                row[2] = 0
                #if the total number of enplanments is less than 1000, no buffer will be created
            else:
                if row[0] == 'Airport' and row[1] > 10000:
                    row[2] = 15000
                    #Buffer of 15,000m for Airports with over 10,000 enplanements
                elif row[0] == 'Airport' and row[1] <= 10000:
                    row[2] = 10000
                    #Buffer of 10,000m for Airports with under or equal to 10,000 enplanements
                elif row[0] == 'Seaplane Base' and row[1] > 1000:
                    row[2] = 7500
                    #Buffer of 7500m for Seaplane Bases with over 1000 enplanements
            cursor.updateRow(row)
                #this updates the row
    arcpy.conversion.ExportFeatures(fcAirport, f"airport_buffer10")
    #this exports the feature class as a new feature class called "airport_buffer"
except arcpy.ExecuteError:
       print(arcpy.GetMessages(2))
    #this prints errors if the code fails

