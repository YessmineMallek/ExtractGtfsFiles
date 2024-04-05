import xml.etree.ElementTree as ET
import pandas as pd  # type: ignore
from sqlalchemy import create_engine # type: ignore

def findShape(shortName):
    dfTrips2=pd.read_csv("trips2.txt")
    for index, row in dfTrips2.iterrows():
        if(shortName==row['trip_short_name']):
            return(row['shape_id'])

def parse_gtfs_file(file_content: str):
    parser = ET.XMLParser()
    tree = ET.ElementTree(ET.fromstring(file_content, parser=parser)) 
    return tree



def extract_Trips_Routes_CSV(tree):
    myroot=tree.getroot()
    colsRoutes=['route_id','agency_id','route_short_name','route_long_name','route_desc','route_type','route_url']
    rowsRoutes=[]
    
    colsTrips=['route_id','service_id','trip_id','trip_headsign','trip_short_name','direction_id','block_id','shape_id']
    rowsTrips=[]
    
    route_id_counter=1
    routesList=[]
    idLists={}
    departure=""
    arrival=""
    agency=0
    for data_item in myroot.findall('.//dataItem'):
        #extraire les informations de run
        data_route= data_item.find("run")
        train_number=data_item.find("trainNumber")
        sname=train_number.findtext('sname')
        daySymbolText=0
        days=train_number.findtext('daySymbolText')
        if(days=="Q" or days=="FAC:Q"):
            daySymbolText=427
        elif(days=="Q DF" ):
            daySymbolText=428
        elif (days=="LU-VE SFDF" or days=="Q SFDF"):
            daySymbolText=429
        elif(days=="SA" or days=="SA,DI DF"):
            daySymbolText=430
        elif(days=="VE"):
            daySymbolText=432
        elif(days=="LU-JE"):
            daySymbolText=433
        

        #extraire les informations du trainRunning
        for train_running in data_item.findall('trainRunning'):
            if(data_route.findtext('fromLocation')==train_running.findtext('location')):
                departure=train_running.findtext('locationLname')
            if(data_route.findtext('toLocation')==train_running.findtext('location')):
                arrival=train_running.findtext('locationLname')
            
        if(train_number.findtext("trainClass")=="GL-OCLIM" or 
        train_number.findtext("trainClass")=="GL-OMN" or
        train_number.findtext("trainClass")=="GL-DCLIM" or 
        train_number.findtext("trainClass")=="GL-AuEX"):
            agency=3
        elif (train_number.findtext("trainClass")=="BL" and sname.isdigit() ) :
            if(int(sname)>=100 and int(sname)< 300):
                agency=2
            else :
                agency=1
        elif (train_number.findtext("trainClass")=="BL"):
            agency=1
        else :
            agency=0
        
        
        fromLocation=data_route.findtext('fromLocation')
        toLocation=data_route.findtext('toLocation')    
    
        longName=fromLocation+"-"+toLocation
        longName2=toLocation+"-"+fromLocation
    
        if(agency!=0):
            if(not(longName in routesList) and not(longName2 in routesList)):
                rowsRoutes.append({
                    "route_id":route_id_counter,
                    "agency_id":agency,
                    "route_short_name":longName,
                    "route_long_name":departure+"-"+arrival,
                    "route_desc":"",
                    "route_type":2,
                    "route_url":""
                }) 
                routesList.append(longName)
                routesList.append(longName2)
                idLists[longName2] = route_id_counter
                idLists[longName] = route_id_counter

                route_id_counter+=1
            rowsTrips.append(
                {
                    "route_id":idLists[longName2],           
                    'service_id':daySymbolText,
                    'trip_id':train_number.findtext('id'),
                    'trip_headsign':arrival,
                    'block_id':'',
                    'trip_short_name':sname,
                    'shape_id':findShape(sname)

                })
        
    #DataFrames
    dfRoutes = pd.DataFrame(rowsRoutes, columns=colsRoutes) 
    dfTrips=pd.DataFrame(rowsTrips,columns=colsTrips)
    print(dfRoutes)
    print(dfTrips)
    dfRoutes.to_csv('GeneratedFiles/routes.txt',index=False)
    dfTrips.to_csv('GeneratedFiles/trips.txt',index=False)
    return "routes.txt","trips.txt"




#Base de Données Extract
def extract_Db(dfRoutes,dfTrips):
    username = 'postgres'
    password = 'mallek12'
    hostname = 'localhost'
    database_name = 'GTFS_Base'
    port = '5432'
    # Create SQLAlchemy engine
    engine = create_engine(f'postgresql://{username}:{password}@{hostname}:{port}/{database_name}')
    try:
        dfRoutes.to_sql('routes',engine,if_exists='replace',index=False)

        dfTrips.to_sql('trips',engine,if_exists='replace',index=False)



    except Exception as e:
        print("Error connecting to PostgreSQL:", e)

    finally:
        # Dispose the engine
        engine.dispose()


    
    
        


        


