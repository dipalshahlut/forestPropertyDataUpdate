###############################################################################################
#### PLEASE MAKE SURE YOUR GDAL SOFTWARE IS INSTALLED ON YOUR COMPUTER
##### WATCH BELOW LINK TO INSTALL gdal software

# https://www.youtube.com/watch?v=4viTd3n9C9g

########################    RUN THIS FILE WITH PYTHON 3 VERSION   #########################

###############################################################################################
# # """
# 28/09/2022 Author: Dipal Shah

# """
## RUN this for the first time only.
########################    REQUIRE LIBRARY INSTALLATION  #########################
##### and now run the below code to install 
# import sys
# import subprocess
# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# ###### python --version
# install('glob')
########################        load libraries          ##############################
import subprocess, glob, os
import geopandas
dir_name = r'C:\Users\dipal.shah\Documents\From old PC\xml_shp\Newfolder' # give a pathe to the directory folder
gdal_exe = r"C:\OSGeo4W\bin\ogr2ogr.exe"  # Path to the gdal exe file
out_file = r"C:\Users\dipal.shah\Documents\From old PC\xml_shp\Newfolder\merged.gpkg"  # Path to your output file
in_File = r"C:\Users\dipal.shah\Documents\From old PC\xml_shp\Newfolder"  # Path to your input file

# join .gpkg file name with the path
for ArchivesGpkg in glob.glob(os.path.join(dir_name,'*.gpkg')):
    if ArchivesGpkg != out_file:
    #print(ArchivesGpkg)
    # glad_exe converts gpkg to shape file for further modification ESRI Shapefile  
        subprocess.run(args=[gdal_exe,'-append', '-f', 'GPKG', f"{out_file}", f"{ArchivesGpkg}"], shell=True)
        os.remove(ArchivesGpkg)# remove converyed gpkg file


# ##### # read generated shape file
shp_gdf = geopandas.read_file(out_file)#, encoding='utf-8')

#rename column name according to ArboLiDAR input feature
shp_gdf1 = shp_gdf.rename(columns ={'treedatadate':'date_new','agepine':'T_MA','basalareapine':'G_MA','stemcountpine':'N_MA','meandiameterpine':'D_MA',
        'meanheightpine':'H_MA','volumepine':'V_MA','agespruce':"T_KU",'basalareaspruce':"G_KU",'stemcountspruce':"N_KU",
        'meandiameterspruce':"D_KU",'meanheightspruce':"H_KU",'volumespruce':"V_KU",'agedeciduous':"T_LP",'basalareadeciduous':"G_LP",
        'stemcountdeciduous':"N_LP",'meandiameterdeciduous':"D_LP",'meanheightdeciduous':"H_LP",'volumedeciduous':"V_LP",'age':"T",
        'basalarea':"G",'stemcount':"N",'meandiameter':"D",'meanheight':"H",'dominantheight':"H_DOM",'volume':"V"})

# further add MALLI_V and MALLI_Ycolumns and assign value of 2 and 0 respectively
shp_gdf_new= shp_gdf1.assign(MALLI_V = 2, MALLI_Y = 0)

#save changes to new shp file
shp_gdf_new.to_file(r'C:\Users\dipal.shah\Documents\From old PC\xml_shp\Newfolder\merged_rename.shp', encoding='utf-8')
# remove oupu shp file
os.remove(out_file)
print('Program run successfully!')


