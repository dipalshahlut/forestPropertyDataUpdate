###############################################################################################

#### PLEASE MAKE SURE YOUR ARCMAP IS 10.2 OR HIGHER VERSION

########################    RUN THIS FILE WITH ARCMAP PYTHON 2.7 VERSION   #########################

###############################################################################################
# # """
# 28/09/2022 Author: Dipal Shah

# """

###############################     load libraries              #############################3
import arcpy
from arcpy import env
import os
# set the workspace to avoid having to type in the full path to the data every time
env.workspace = r'C:\Users\dipal.shah\Documents\From old PC\xml_shp\Newfolder'


#########  DO NOT EDIT /MADE CHANGES TO CODE BELOW 
in_shp = r'C:\Users\dipal.shah\Documents\From old PC\xml_shp\Newfolder\merged_rename.shp' # name of the input shape file
# Set local variables
inputTimeField = "date_new"
inputTimeFormat = "yyyy-MM-dd;1033;;"
outputDateField = "inv_date"

# Execute CalculateEndDate
arcpy.ConvertTimeField_management(in_shp, inputTimeField,inputTimeFormat , outputDateField, output_time_type="DATE")
#, output_time_format="'Not Used'")


out_gdb = r'C:\Users\dipal.shah\Documents\From old PC\xml_shp\Newfolder\merged_gdb.gdb'   # name of the output gdb database file
gdb_path = os.path.dirname(out_gdb)  #DEFINE  directory path and name
gdb_name = os.path.basename(out_gdb) #define the base name of the path
# if the folder name already exist at the defined path the shpt to dbf conversion 
# function will not work hence,
if arcpy.Exists(gdb_name):  
    print '\n folder {} already exist \n'.format(gdb_name)
    arcpy.Delete_management(gdb_name)   # delete the gdb folder if it exist
    arcpy.CreateFileGDB_management(gdb_path, gdb_name) # now create new gdb folder
    arcpy.FeatureClassToGeodatabase_conversion(in_shp,out_gdb)  # convert shp to gdb
else:
    arcpy.CreateFileGDB_management(gdb_path, gdb_name) # now create new gdb folder
    arcpy.FeatureClassToGeodatabase_conversion(in_shp,out_gdb)  # convert shp to gdb


# ###### delete merged stands data shape file
# arcpy.Delete_management(in_shp)


print 'Program run successfully!'
print 'Finished!!'
