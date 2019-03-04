import requests
import json
import arcpy
import os

# SPIRE AIS ENDPOINT
ENDPOINT = 'https://ais.spire.com/vessels'

FORMAT = 'json'

# YOUR TOKEN
AUTH_TOKEN = 'eyJhbGciOiJIU***exampledoenstwork***pYXQiOjE1MDkxNTEzMzZ9.hrDU77IOkPt6VwYIvdM0UVcQ-rLETLewDfDwuEw111M' # arcpy.GetParameterAsText(0) # token as first param

HEADERS = {
    "Authorization": "Bearer {}".format(AUTH_TOKEN),
    'Accept': 'application/%s' % FORMAT
    }


class ShipPoint:
    """Model to ship points."""

    def __init__(self, ship_id, name, mmsi, ship_type, ship_class, flag, las_k_pos, updated_at, gen_class, ind_class):  # noqa: E501
        """Docstring."""
        self.id = ship_id
        self.name = name
        self.mmsi = mmsi
        self.ship_type = ship_type
        self.ship_class = ship_class
        self.flag = flag
        self.las_k_pos = las_k_pos
        self.updated_at = updated_at
        self.gen_class = gen_class
        self.ind_class = ind_class

# gets input drawn parameter (polygon)
gj = arcpy.GetParameter(0)
fcname = "Returned_ships"

def build_feature_class(ships):
    # arcpy.env.workspace = wk = arcpy.GetParameterAsText(1)
    arcpy.env.workspace = wk = arcpy.env.scratchGDB
    arcpy.AddMessage(arcpy.env.scratchGDB)
    arcpy.AddMessage(wk)

    #r"C:\Users\heat3463\Documents\ArcGIS\Projects\Spire_API_Test\Spire_API_Test.gdb"
    sr = arcpy.SpatialReference(4326)

    
    if arcpy.Exists(fcname) is False:
        arcpy.CreateFeatureclass_management(wk, fcname, "POINT", spatial_reference=sr)  # NOQA

    arcpy.management.AddFields(fcname, [["ID", "TEXT", "ID", 50],  # NOQA
                                        ["NAME", 'TEXT', "NAME", 50],  # NOQA
                                        ["MMSI", 'TEXT', "MMSI", 20],  # NOQA
                                        ['SHIP_TYPE', 'TEXT', 'SHIP_TYPE', 50],
                                        ["SHIP_CLASS", 'TEXT', "SHIP_CLASS", 50],
                                        ["FLAG", 'TEXT', "FLAG", 10],
                                        ["UPDATED_AT", 'TEXT', "UPDATED_AT", 100], # NOQA
                                        ["GEN_CLASS", 'TEXT', "GEN_CLASS", 50],
                                        ["IND_CLASS", 'TEXT', "IND_CLASS", 50],
                                        ["COURSE", "TEXT", "COURSE", 10]])

    entslist = ["ID", "NAME", "MMSI", "SHIP_TYPE", "SHIP_CLASS", "FLAG", "UPDATED_AT", "GEN_CLASS", "IND_CLASS", "COURSE", "SHAPE@XY"]   # noqa: E501

    iCur = arcpy.da.InsertCursor(fcname, entslist)

    # arcpy.AddMessage("getting here")
    for ship in ships:
        adds = []
        adds.append(ship.id)
        adds.append(ship.name)
        adds.append(ship.mmsi)
        adds.append(ship.ship_type)
        adds.append(ship.ship_class)
        adds.append(ship.flag)
        adds.append(ship.updated_at)
        adds.append(ship.gen_class)
        adds.append(ship.ind_class)
        course = ship.las_k_pos['course']
        adds.append(course)
        lx = ship.las_k_pos['geometry']['coordinates'][1]
        ly = ship.las_k_pos['geometry']['coordinates'][0]
        adds.append((ly, lx))

        iCur.insertRow(adds)

    fs=arcpy.FeatureSet()
    fs.load(os.path.join(arcpy.env.scratchGDB, fcname))
    arcpy.SetParameter(1, fs)   

    del iCur


if __name__ == '__main__':

    for row in arcpy.da.SearchCursor(gj, ["SHAPE@"]):
        extent = row[0].extent      
        sr = arcpy.SpatialReference(4326)
        e = extent.projectAs(sr)
        break     

    mypolyjson = {"type": "Polygon", "coordinates": [[[e.XMax, e.YMax], [e.XMax, e.YMin], [e.XMin, e.YMin],[e.XMin, e.YMax], [e.XMax, e.YMax]]]}
    strTest = "last_known_or_predicted_position_within=" + json.dumps(mypolyjson);
    svrReq = ENDPOINT + "?" + strTest

    # arcpy.AddMessage(svrReq)

    response = requests.get(svrReq, headers = HEADERS)
    datajson = json.loads(response.text)
     
    ships = []

    # 1. get total
    if 'paging' in datajson:
        p = datajson['paging']
        if 'total' in p:
            total = p['total']
            arcpy.AddMessage("Number of ships detected in area: {}".format(total))
        # if 'next' in p:
        #     next_page = p['next']
        # else:
        #     next_page = ""

    # for every page:

    # session = requests.Session()

# def get_jobs():
#     url = "https://api.angel.co/1/tags/1664/jobs" 
#     first_page = session.get(url).json()
#     yield first_page
#     num_pages = first_page['last_page']

#     for page in range(2, num_pages + 1):
#         next_page = session.get(url, params={'page': page}).json()
#         yield next_page['page']

# for page in get_jobs():
# https://stackoverflow.com/questions/17777845/python-requests-arguments-dealing-with-api-pagination

# since = data['paging']['next']
#                 #if request already has a next, strip it out
#                 if request.find("next=") != -1:
#                     t = request.find("next=") + len("next=")
#                     request=request[:t] #strip out
#                     request = request + since
#                 else:
#                     request = request + "&next=%s" % since
               

    if 'data' in datajson:
        for d in datajson['data']:
            ship_id = d['id']
            name = d['name']
            mmsi = d['mmsi']
            if 'ship_type' in d: 
                ship_type = d['ship_type'] 
            else:
                ship_type = ""
            if 'class' in d:
                ship_class = d['class']
            else:
                ship_class = ""
            if 'flag' in d:
                flag = d['flag']
            else:
                flag = ""
            if 'last_known_position' in d:
                las_k_pos = d['last_known_position']
                # if 'course' in las_k_pos:
            else:
                las_k_pos = ""
                course = ""
            if 'updated_at' in d:
                updated_at = d['updated_at']
            else:
                updated_at = ""
            if 'general_classification' in d:
                gen_class = d['general_classification']
            else:
                gen_class = ""
            if 'individual_classification' in d:
                ind_class = d['individual_classification']
            else:
                ind_class = ""
            ship = ShipPoint(ship_id, name, mmsi, ship_type, ship_class, flag, las_k_pos, updated_at, gen_class, ind_class)
            ships.append(ship)

    
    # if next_page != "":  # go to next page
    #     arcpy.AddMessage("Paging...")

    # Now we have a ships array with attributes. Write to feature class.
    build_feature_class(ships)

