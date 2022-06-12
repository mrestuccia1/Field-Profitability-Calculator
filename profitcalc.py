#!/usr/bin/env python3
import json

f1 = open("./QSAPIDATA/cydata.json", "r")
data = json.load(f1)
f2 = open("profit.json", "r+")
f2.write(json.dumps(data))
f2.seek(0)
f1.close()
data = json.load(f2)

s = 0
for state in data["states"]:
    for x in state:
        input = data["states"][s][x][0]
        #print(x)
        a = 0
        for i in input:
            #print(i)
            #an error here; likely unable to fix with time remaining
            try:
                i[a]['CORN_value'] = (7.68 * i[a]['CORN_value']) - 915
            except:
                i = "null"
            try:
                i[a]['SOYBEANS_value'] = (16.47 * i[a]['SOYBEANS_value']) - 635
            except:
                i = "null"           
            try:    
                i[a]['WHEAT_value'] = (11.06 * i[a]['WHEAT_value']) - 170
            except:
                i = "null"            
            try:
                i[a]['COTTON_value'] = (0.73 * i[a]['COTTON_value']) - 485
            except:
                i = "null"                       
            try:
                i[a]['HAY_value'] = (165 * i[a]['HAY_value']) - (132.79 * i[a]['HAY_value'])
            except:
                i = "null"
            a += 1
f2.close()

