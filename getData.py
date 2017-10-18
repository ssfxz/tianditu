# -*- coding: utf-8 -*-
import urllib2
import json
import traceback
import os

def obtainData(city, fileName):
    print city,

    url = "http://api.tianditu.com/search?postStr={\"keyWord\":\"" + city+ "\",\"level\":\"1\",\"mapBound\":\"60,0,150,60\",\"queryType\":\"1\",\"start\":\"0\",\"count\":\"10\"}"
    try:
        response = urllib2.urlopen(url).read()
        cityData = json.loads(response)
        # print cityData
        areaData = cityData["area"]

        if not os.path.exists("./" + fileName):
            os.mkdir("./" + fileName)
        fo = open("./" + fileName + "/" + city + ".js", "wb+")
        # fo.write(response)
        fo.write(json.dumps(areaData, ensure_ascii=False, indent=4).encode("utf-8"))
        fo.close()

        fc = open("./collect.js", "ab+")
        fc.write(json.dumps(areaData, ensure_ascii=False, indent=4).encode("utf-8"))
        fc.write(",\n")
        fc.close()

    except:
        print "Failure!"
        traceback.print_exc()
        return False
    else:
        print "Done!"
        return True

# obtainData("海南")

fileName = "city"
file = open(fileName + ".txt")
city = ""
successList = []
failureList = []

fc = open("./collect.js", "wb+")
fc.write("var collect = [\n")
fc.close()

for line in file.readlines(10):
    city = line.strip('\n')
    if obtainData(city, fileName):
        successList.append(city)
    else:
        failureList.append(city)

fc = open("./collect.js", "ab+")
fc.write("]\n")
fc.close()

print "成功:", len(successList)
print "失败:", len(failureList)
for c in failureList:
    print c,

