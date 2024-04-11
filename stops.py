
import csv
def update_location(location_element):
        if location_element == '192D':
            location_element = '193E'
        else:
            location_element = {
                'Riadh': '160P',
                'SiMES': '271Y',
                'SMAR': '192D',
                'TebZI': '270X',
                'LyZa': '152F',
                'STADE': '155J',
                'GDFH': '125Z'
            }.get(location_element, location_element)
        return location_element

def extract_stops_files(tree):
    lat_lon = {'lat': 0, 'lon': 0}
    location_stop_codes = {}
    id_stop_codes = {}
    idx=0
    with open("Ressources/stops.txt", 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)
        
        for row in csv_reader:
            code = row[1]  
            lat = row[4] 
            lon = row[5] 
            lat_lon[code] = {'lat': lat, 'lon': lon}
    myroot = tree.getroot()
    # Parcourir toutes les balises dataItem
    for data_item in myroot.findall('.//dataItem'):
        # Extraire les informations de trainNumber
        train_number = data_item.find('trainNumber') 

        if (
        (train_number.findtext('trainClass') == 'GL-OCLIM') or
        (train_number.findtext('trainClass') == 'GL-OMN') or
        (train_number.findtext('trainClass') == 'GL-DCLIM') or
        (train_number.findtext('trainClass') == 'GL-AuEX')
        ):
            z=3
        else :
            if ((train_number.findtext('trainClass')=='BL') and (train_number.findtext('sname').isdigit())) :
                if ((int(train_number.findtext('sname'))>=100) and (int(train_number.findtext('sname'))<300)) :
                    z=2
                else :
                    z=1
            else :
                if (train_number.findtext('trainClass')=='BL') :
                    z=1
                else :
                    z=4
        if z!=4 :
            for  train_running in (myroot.findall('.//trainRunning')):
            # Trouver les balises locationLname et location dans chaque trainRunning
                location_name_element = train_running.find('locationLname')
                location_element = train_running.find('location')
                if location_name_element is not None and location_element is not None and location_element != 'V2Bis':
                    # Extraire le nom de la station et son code d'arrêt
                    
                    location_name = location_name_element.text
                    stop_code = update_location(location_element.text)
                    if stop_code != 'V2Bis':  # Check if stop_code is not 'V2Bis'
                        if stop_code not in id_stop_codes :
                            idx += 1
                            # Ajouter le nom de la station et son code d'arrêt au dictionnaire
                            location_stop_codes[location_name] = stop_code
                            id_stop_codes[stop_code] = idx
    with open('GeneratedFiles/stops.txt', 'w') as file:
        file.write("stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station\n")
        for idx, (location_name, stop_code) in enumerate(location_stop_codes.items(), start=1):
            latt = 0.0
            lonn = 0.0
            if stop_code in lat_lon:
                latt = lat_lon[stop_code]['lat']
                lonn = lat_lon[stop_code]['lon']
            file.write(f"{idx},{stop_code},{location_name},,{latt},{lonn},,,0,\n")
    
        