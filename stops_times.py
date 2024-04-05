import xml.etree.ElementTree as ET

# Parser le fichier XML
def extaract_Stops_times(tree):
    myroot = tree.getroot()
    location_stop_codes = {}
    id_stop_codes = {}
    stop_times = [['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence','stop_headsign','pickup_type','drop_off_type', 'shape_dist_traveled']]
    L=list()
    idx=0
    # Parcourir toutes les balises dataItem
    for data_item in myroot.findall('.//dataItem'):
        # Extraire les informations de trainNumber
        train_number = data_item.find('trainNumber')
        route_data = data_item.find('run')
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
        # Extraire les attributs de trainrunning
        if z!=4:
            
            for train_running in myroot.findall('.//trainRunning'):
                location_element = train_running.find('location')
                if location_element is not None and location_element != 'V2Bis':
                    stop_code = location_element.text
                    if stop_code != 'V2Bis':  # Check if stop_code is not 'V2Bis'
                        if stop_code not in id_stop_codes :
                            idx += 1
                            id_stop_codes[stop_code] = idx


            
        
            k=0
            # Extraire les informations de trainRunning
            for train_running in data_item.findall('trainRunning'):
                if route_data.findtext('toLocation')==train_running.findtext('location') :
                    y=train_running.findtext('locationLname')
            for train_running in data_item.findall('trainRunning'):
                current_stop_code = train_running.findtext('location')
                if current_stop_code in id_stop_codes:
                    idxx = id_stop_codes[current_stop_code]
                else : idxx = ''
                departure_time = train_running.find('departureTime')
                departure_hour = departure_time.get('hour') if departure_time is not None else '00'
                departure_minutes = departure_time.get('minutes') if departure_time is not None else '00'
            
                arrival_time = train_running.find('arrivalTime')
                arrival_hour = arrival_time.get('hour') if arrival_time is not None else '00'
                arrival_minutes = arrival_time.get('minutes') if arrival_time is not None else '00'
                k=k+1
                running_data = [
                    train_number.findtext('id'),
                    '{}:{}:00'.format(arrival_hour , arrival_minutes ),
                    '{}:{}:00'.format(departure_hour, departure_minutes),            
                    idxx,
                    k,
                    y,
                    0,
                    0,
                    train_running.findtext('distance') or ''
                ]
                # Ajouter les données extraites au tableau stop_times
                stop_times.append(running_data)
    with open('GeneratedFiles/stops_times.txt', 'w') as stop_times_file:
        for row in stop_times:
            # Convert all elements in the row to strings
            row_as_strings = [str(item) for item in row]

            # Use the join method with the new list of strings
            stop_times_file.write(','.join(row_as_strings) + '\n')
