###############################################################################################

#### PLEASE MAKE SURE YOUR ARCMAP IS 10.2 OR HIGHER VERSION

########################    RUN THIS FILE WITH ARCMAP PYTHON 2.7 VERSION   #########################

###############################################################################################
# # """
# 28/09/2022 Author: Dipal Shah

# """

##### and now run the below code to install 
## RUN this for the first time only.
########################    REQUIRE LIBRARY INSTALLATION  #########################
# import sys
# import subprocess
# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# ###### python --version
# install('simpledbf')
# install('urllib3')
##########################      load libraries      ########################################
import arcpy
from arcpy import env
import os
from simpledbf import Dbf5
import urllib


# set the workspace to avoid having to type in the full path to the data every time
env.workspace = r"C:\Users\dipal.shah\Documents\From old PC\xml_shp"
arcpy.env.overwriteOutput = True 


GridData = 'utm10.shp'   # define grid data shp file
standData =  'forestpropertydata_output.shp' #define stand data shp file

# # # First, make a layer from the feature class
arcpy.MakeFeatureLayer_management(GridData, 'grid')
# # # First, make a layer from the feature class
arcpy.MakeFeatureLayer_management(standData, 'stand_lyr')
#########  DO NOT EDIT /MADE CHANGES TO CODE BELOW
outfc = 'Test_new.shp' # write output file name

def unique_values(table, field):
    with arcpy.da.SearchCursor(table,[field]) as cursor:
        return sorted({row[0] for row in cursor})

# intersect grid shp with stand shp
#intersection = ([GridData,standData],outfc,join_attributes="ALL", output_type="INPUT") #NO_FID
#intersection = arcpy.analysis.Intersect([GridData,standData],outfc,join_attributes="NO_FID", output_type="INPUT")
# # Make a layer and select cities that overlap the chihuahua polygon
arcpy.SelectLayerByLocation_management('grid', 'INTERSECT', 'stand_lyr',1, 'NEW_SELECTION', 'NOT_INVERT')

uniqLehtitunnu = unique_values('grid','LEHTITUNNU')
print uniqLehtitunnu
# ##arcpy.FeatureClassToFeatureClass_conversion(intersection,outfc)
arcpy.CopyFeatures_management('grid', outfc) 

#define Metsahaletus HILA data link for the data download
webUrl = urllib.urlopen('https://aineistot.metsaan.fi/avoinmetsatieto/Hila/Karttalehti/').readlines()

for ID in uniqLehtitunnu: ## loop through all the unique HILA file
    Num = str(ID) # convert unique HILA file number to string 
    for line in webUrl: ## loop through all the lines in WEBURL
        if ID in line:  # if number is present is the weburl line      
            # merge the number with the Hila to download data   
            Down= 'https://aineistot.metsaan.fi/avoinmetsatieto/Hila/Karttalehti/Hila_{}.zip'.format(Num) 
            #print Down
            #define where the path where folder to be stored            
            folder_path = r'C:\Users\dipal.shah\Documents\From old PC\xml_shp\Hila_{}.zip'.format(Num)
            urllib.urlretrieve(Down,folder_path)  # download the data to the given path

###### delete xml2shp output shape file
#arcpy.Delete_management(standData)

del intersection
del uniqLehtitunnu

###### delete stand data shape file
arcpy.Delete_management(outfc)

print 'Program run successfully!'