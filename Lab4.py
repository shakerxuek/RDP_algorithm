from typing import SupportsFloat
import shapefile

# part A
def shapefile_info(x:str):
    print('shapetype:')
    with shapefile.Reader(x) as shp:
        print(shp)
    sf=shapefile.Reader(x)    
    shapess=sf.shapes()
    print('Bounding box of shapefile:')
    print(sf.bbox)
    pointnum=[]
    print('Bounding box of each shape:')
    for i in shapess:
        temp2=len(i.points)
        pointnum.append(temp2)
        print(i.bbox)
    print('the list containing the numbers of points in each shape:')
    print(pointnum)
    
shapefile_info("Shapefile/CALGIS_CITYBOUND_LIMIT.shp")



