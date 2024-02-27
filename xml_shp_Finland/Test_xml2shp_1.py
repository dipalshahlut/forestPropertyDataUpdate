###############################################################################################

########################    RUN THIS FILE WITH PYTHON 3 VERSION   #########################

###############################################################################################
# -*- coding: utf-8 -*-
# # """
# 28/09/2022 Author: Dipal Shah

# """
###### please check python version in your computer by changing directory to python folder in cmd
## and paste below command in cmd to check python version
#python --version

###### For python27 instruction
## python compatible wheels for GDAL, FIONA, SHAPELY, PYPROJ
## paste suggested wheel (whl_file folder unzip and paste them in) to the python folder
## and now run the below code to install 

##############################   OR      ##############################################
###### please download python compatible wheels for GDAL, FIONA, SHAPELY, PYPROJ from below link
## https://www.lfd.uci.edu/~gohlke/pythonlibs/
## for instance if you have python 38 version then download GDAL win32 wheel 
## compatible to python version would be 'GDAL‑3.3.3‑cp38‑cp38‑win32.whl'
## locate all wheels in downloads and
## paste suggested wheel to the python folder
## and now run the below code to install 
## RUN this for the first time only.
########################    REQUIRE LIBRARY INSTALLATION  #########################

# # import sys
# # import subprocess

# # def install(package):
# #     subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# # ###### python --version
# # install('pandas')
# # install('numpy')
# # install('descartes')
# # install('GDAL')
# # install('Fiona')
# # install('Shapely')
# # install('pyproj')
# # install('minidom-ext')
# # install('lxml')


########################## load libraries ##################################

from xml.dom import minidom
import os
import sys

########## PASTE the xml file folder here ##############
path = r'C:\Users\dipal.shah\Documents\From old PC\xml_shp'
File = "forestpropertydata.xml"  # define the xml file name here

###########################################################
os.chdir(path)
import geopandas
import geopandas as gpd
from shapely.geometry import Point,Polygon,MultiPolygon
import numpy as np
import pandas as pd
from shapely import wkt
from shapely import wkb
import lxml.etree
import xml.etree.ElementTree as et 
from xml.dom.minidom import parseString
from operator import itemgetter
from osgeo import ogr
import fiona
import re


#following function will convert xml to python dataframe
def Xml2DataFrame(FileName): 
    # import xml data by reading from a file
    xtree = et.parse(FileName)  # define the xml file name here 
    xroot = xtree.getroot() 

    Comp = [] #define empty list to collect data

    for RealEstates in xroot[0]: # each for loop goes through xml file nodes
        for rID in RealEstates:
            for feat in rID:
                for st in feat[1]:
                    standid = st.attrib# collect standid information            
                    for gml in st[0]:
                        for coor in gml:
                            for PolyGeo in coor[0]:                           
                                for polyFi in PolyGeo:                   
                                    for Fipoly in polyFi:
                                        Poly = Fipoly.text # collect polygon coordinates
                                        PolygonCoord = str(st.attrib), Poly
                                        Comp.append(PolygonCoord) 
    #convert list to python dataframe with column name standid and polygon geometry
    df_ = pd.DataFrame(Comp,columns = ["Standid","geom"]) #
    # convert standid object datatype to numerical datatype
    df_['Standid'] = df_['Standid'].str.strip('{}').str.split(': ').str[1] 
    df_['Standid'] = df_['Standid'].str.lstrip("'").str.rstrip("'").astype('int32')
    return df_

#following function will take python dataframe and convert polygon coord string
# to point coordf tuple(python datatype)  
def List2Tuple(df_):
    list_pol = []
    for j in range(0,len(df_)):
        ress = df_[j].split(' ')
        Pol=[]
        for i in range(0,len(ress)):   
            splitCoordinate_xy = ress[i]
            Tup = eval(splitCoordinate_xy)
            Tup_new =Tup 
            Pol.append(Tup_new)
        list_pol.append(Pol)
    return list_pol

#following function will convert polygon geometry to shp file polygon geometry format
def Geometry2Polygon(list_pol):
    df['geometry'] = [Polygon(x) for x in list_pol]
    return df['geometry']

#following function will convert python dataframe to geopanda dataframe
#to write shp file 
def df2Geodf(df_):
    # convert to geodataframe using the latitude and logitude columns
    settlements_gdf = geopandas.GeoDataFrame(df_[['Standid','geometry']])
    # make sure the coordinate system is set
    settlements_gdf.crs="EPSG:3067"
    settlements_gdf.head()
    return settlements_gdf

# following function will print warning if there are duplicate standid
def CheckDuplicateStandID(df_):
    df2 = df_['Standid'][df['Standid'].duplicated()]
    if df2.empty == False:
        print('There is/are duplicate standid')
    return
# #following function will will group polygons with same standid to multipolygon 
# and will avoid duplication of standid data
def groupby_multipoly(df, by, aggfunc="first"):
    data = df.drop(labels=df.geometry.name, axis=1)
    aggregated_data = data.groupby(by=by).agg(aggfunc)
    # Process spatial component
    def merge_geometries(block):
        return MultiPolygon(block.values)

    g = df.groupby(by=by, group_keys=False)[df.geometry.name].agg(
        merge_geometries
    )
    # Aggregate
    aggregated_geometry = gpd.GeoDataFrame(g, geometry=df.geometry.name, crs=df.crs)
    # Recombine
    aggregated = aggregated_geometry.join(aggregated_data)
    return aggregated
# following function will convert geodataframe to shp file
def Geodf2shp(grouped,File):
    grouped.set_geometry(col='geometry', inplace=True)
    name = File.split('.')   
    grouped.to_file(driver = 'ESRI Shapefile', filename= "%s_output.shp" %name[0])
    return 


#############################################################################################
#run xml to shp code

df = Xml2DataFrame(File)
polygonGeom = List2Tuple(df['geom'])
geospatialPoly = Geometry2Polygon(polygonGeom)
checkStandid = CheckDuplicateStandID(df)
gdf = df2Geodf(df) 
grouped = groupby_multipoly(gdf, by='Standid')
Shapefile = Geodf2shp(grouped,File)   

print('Program run successfully!')
print('Finished!')
