#cropyield api collection file
#Note: make sure to handle if crop data isnt given for a county
#Note: hay measured in tons / acre, cotton in lbs / acre
#Note: some "commodity:null" data is sandwitched between county data, look for this in next analysis
import requests
import json

def reqError(state, commodity, input, file, fd):
    f2 = open("invalid_states.txt", "a")
    f2.write("\"STATE\":\""+state+"\",\"commodity\":\""+commodity+"\"\n")
    f2.close()
    if (commodity == "CORN"):
        input.update({"CORN":"null"})
    if (commodity == "WHEAT"):
        input.update({"WHEAT":"null"})
    else:
        sobj = {commodity:"null"}
        input.update(sobj)
    file.seek(0)
    json.dump(fd, file)

def writeCom(data,curstate,input, file, fd):
    x = 0
    #try:
    #    jsonfile = json.load(f)
    #except:
    #    a = 0
    for i in data["data"]:
        cn = data["data"][x]["county_name"]
        crop = data["data"][x]["commodity_desc"]
        val = data["data"][x]["Value"]
        try:
            cv = crop+"_value"
            param = {cv:val}
            input[cn][0].update(param)
            file.seek(0)
            json.dump(fd, file)
        except:
            param1 = {cn:[{}]}
            cv = crop+"_value"
            param2 = {cv:val}

            input.update(param1)
            file.seek(0)
            json.dump(fd, file)

            input[cn][0].update(param2)
            file.seek(0)
            json.dump(fd, file)
        x += 1
    
    #f.seek(0)
    #try:
    #    f[curstate][cn].append(",\""+crop+"_value\":\""+val+"\"")
    #except:
    #    f.write("{\""+data["data"][x]["county_name"]+"\":[")
    #    f.write("{\""+data["data"][x]["commodity_desc"]+"_value\":\""+data["data"][x]["Value"]+"\"}]")


states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
            'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

#this builds the default json file for the data
def buildJson(f):
    f.write("{\"states\":[")
    for x in range(49):
        f.write("{\""+states[x]+"\":[{}]},")
    f.write("{\""+"WY"+"\":[{}]}]}")
    f.seek(0)

commodity = ['COTTON','HAY','SOYBEANS']
desc = ["CORN, GRAIN - YIELD, MEASURED IN BU / ACRE","COTTON, PIMA - YIELD, MEASURED IN LB / ACRE","HAY - YIELD, MEASURED IN TONS / ACRE","SOYBEANS - YIELD, MEASURED IN BU / ACRE","WHEAT - YIELD, MEASURED IN BU / ACRE"]

#this code opens a text file with an API key and saves it
k = open("QSAPIkey.txt")
key = k.read()
k.close()

#note: code will not work unless API key is present; I removed mine for security
#API key can be generated at https://quickstats.nass.usda.gov/api
def pullData(commodity, curstate, int):
        webadd = "http://quickstats.nass.usda.gov/api/api_GET/?key="+key+"&commodity_desc="+commodity+"&short_desc="+desc[int]+"&agg_level_desc=COUNTY&year__GE=2021&state_alpha="+curstate+"&format=JSON"
        response = requests.get(webadd)
        #print(response.text)
        return response.json()


f = open("cydata.json", "w")
buildJson(f)
f.close()
f = open("cydata.json", "r+")
file_data = json.loads(f.read())
#f.seek(0)
#f.write("{\"states\":[")
#pulls county data for each state from quick stats api
for s in range(50):
    #these are the current state, and a messy data type needed for the json functions to work in the helpers
    curstate = states[s]
    input = file_data["states"][s][curstate][0]
    #f.write("{\""+curstate+"\":[")

    data = pullData("CORN", curstate, 0)
    str = json.dumps(data)
    if str == "{\"error\": [\"bad request - invalid query\"]}":
        #print(json.dumps(data))
        reqError(curstate,"CORN",input,f,file_data)
    else:
        writeCom(data,curstate,input,f,file_data)
    f.seek(0)

    for i in range(3):
        curcom = commodity[i]
        data = pullData(curcom, curstate, i+1)
    
        x = 0
        if json.dumps(data) == "{\"error\": [\"bad request - invalid query\"]}":
            reqError(curstate,curcom,input,f,file_data)
        else:
            writeCom(data,curstate,input,f,file_data)
    f.seek(0)


    data = pullData("WHEAT", curstate, 4)
    if json.dumps(data) == "{\"error\": [\"bad request - invalid query\"]}":
        reqError(curstate,"WHEAT",input,f,file_data)
    else:
        writeCom(data,curstate,input,f,file_data)
    f.seek(0)
