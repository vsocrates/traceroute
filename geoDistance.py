import geoip2.database
import csv
from math import radians, cos, sin, asin, sqrt

def main():
    reader = geoip2.database.Reader('./GeoLite2-City.mmdb') 
    f = open("output.csv", 'r+')
    data = readcsv2('output.csv')
    IPs = data['IP Address']
    f2 = open("geo_ouput.csv",'w+')
    writer = csv.writer(f2)
    writer.writerow( ('IP', '', '', 'Geo Distance') )
    for ip in IPs:
        response = reader.city(str(ip))
        latitude1  = response.location.latitude
        longitude1 = response.location.longitude
        
        print latitude1
        print longitude1

        response2 = reader.city('129.22.21.193')
        latitude2 = response2.location.latitude
        longitude2 = response2.location.longitude

        if latitude1 is not None and longitude1 is not None:
            distance = haversine(latitude1,longitude1,latitude2,longitude2)
            writer.writerow( (ip,'','',distance) )

    f.close()
    f2.close()
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def read_csv(file, columns, type_name="Row"):
  try:
    row_type = namedtuple(type_name, columns)
  except ValueError:
    row_type = tuple
  rows = iter(csv.reader(file))
  header = rows.next()
  mapping = [header.index(x) for x in columns]
  for row in rows:
    row = row_type(*[row[i] for i in mapping])
    yield row

def readcsv2(filename):
    with open(filename, 'rU') as infile:
  # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]
    return data

if __name__ == "__main__":
    main()
