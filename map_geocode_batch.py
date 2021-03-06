import geopy
import mapbox
from mapbox import Geocoder
# from osgeo import ogr, osr
import csv

csv_file_with_address = '/home/ubuntu/PycharmProjects/Jasper_App/all_india_data_for_geocode_without_district.csv'
file_with_lat_long = 'lat_long.txt'
mapbox_access_token = 'pk.eyJ1IjoiZXJhYmhpbmF2IiwiYSI6ImNpcnMxZHVxeTBpaDBmbG04ZzAwaWJlemYifQ.QOJ5SoEcM8J0RwXC-cLl1w'

def csv_reader(csv_file):
    csvfile = open(csv_file, 'rb')
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    return reader


def get_row_from_address(csv_file):
    reader = csv_reader(csv_file)
    for row in reader:
        yield row


def file_writer(lat_lng_file, data):
    with open(lat_lng_file, 'a') as file:
        file.write(data)
        file.write('\n')
    return None


def geocode(address):
    g = Geocoder(access_token=mapbox_access_token)
    try:
        print address
        response = g.forward(address, country=['in'])
        collections = response.json()
    except:
        print 'Error Occurred'
        return "Not Found", 'Not Found'
    else:
        if response.status_code == 200 and len(collections['features']) >= 1:
            lat, lng = collections['features'][0]['geometry']['coordinates']
            return lat, lng
        else:
            return 'Not Found', 'Not Found'
'''
# method for creating a shapefile

def parse_file(filepath, output_shape):
    # create the shapefile
    drv = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(output_shape):
        drv.DeleteDataSource(output_shape)
    ds = drv.CreateDataSource(output_shape)
    # spatial reference
    sr = osr.SpatialReference()
    sr.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    lyr = ds.CreateLayer(output_shape, sr, ogr.wkbPoint)
    # fields
    featDefn = lyr.GetLayerDefn()
    fld_id = ogr.FieldDefn('id', ogr.OFTInteger)
    fld_address = ogr.FieldDefn('ADDRESS', ogr.OFTString)
    fld_address.SetWidth(255)
    lyr.CreateField(fld_id)
    lyr.CreateField(fld_address)
    print 'Shapefile %s created...' % ds.name
    # read text addresses file
    i = 0
    f = open(filepath, 'r')
    for address in f:
        try:
            print 'Geocoding %s' % address
            place, lat, lng = geocode(address)
            point = ogr.Geometry(ogr.wkbPoint)
            point.SetPoint(0, lng, lat)
            feat = ogr.Feature(lyr.GetLayerDefn())
            feat.SetGeometry(point)
            feat.SetField('id', i)
            feat.SetField('ADDRESS', address)
            lyr.CreateFeature(feat)
            feat.Destroy()
            i = i + 1
        except:
            print 'Error, skipping address...'
'''
# print geocode('bangalore')


def map_geocode_addresses(address_file, lat_long_file):
    global count
    temp = count
    for row in get_row_from_address(address_file):
        if temp > 0:
            temp -= 1
        else:
            lat, lng = geocode(','.join(row))
            # print ' '.join(row)
            address = '"' + ','.join(row) + '"'
            data = ','.join([address, str(lat), str(lng)])
            print data
            file_writer(lat_long_file, data)
            count += 1

    print 'Success'
count = 0
# try:
#     with open('data_processed.txt', 'r') as fobj:
#         count = int(fobj.readline().strip('\n'))
map_geocode_addresses(csv_file_with_address, file_with_lat_long)
# except:
#     with open('data_processed.txt', 'w') as fobj1:
#         fobj1.write(str(count))
