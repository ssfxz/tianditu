# -*- coding: utf-8 -*-
import urllib2
import json
import traceback
import os
import sys
import socket

def fetchData(city, fileName):
    print city,

    url = "http://api.tianditu.com/search?postStr={\"keyWord\":\"" + city+ "\",\"level\":\"1\",\"mapBound\":\"60,0,150,60\",\"queryType\":\"1\",\"start\":\"0\",\"count\":\"10\"}"
    try:
        response = urllib2.urlopen(url, timeout=1).read()
        cityData = json.loads(response)
        # print cityData
        areaData = cityData["area"]

        if not os.path.exists("./data/" + fileName):
            os.mkdir("./data/" + fileName)
        fo = open("./data/" + fileName + "/" + city + ".js", "wb+")
        # fo.write(response)
        fo.write(json.dumps(areaData, ensure_ascii=False, indent=4).encode("utf-8"))
        fo.close()

        fc = open("./data/collect-" + fileName + ".js", "ab+")
        fc.write(json.dumps(areaData, ensure_ascii=False, indent=4).encode("utf-8"))
        fc.write(",\n")
        fc.close()
    except socket.timeout:
        print "Timeout!"
        return False
    except:
        print "Failure!"
        traceback.print_exc()
        return False
    else:
        print "Done!"
        return True

# fetchData("海南")

fileName = sys.argv[1]
# fileName = "city"
# fileName = "province"
file = open(fileName + ".txt")
city = ""
successList = []
failureList = []
retryNum = 5

fc = open("./data/collect-" + fileName + ".js", "wb+")
fc.write("var collect = [\n")
fc.close()

for line in file.readlines():
    city = line.strip('\n')
    i = 0
    while i < retryNum:
        res = fetchData(city, fileName)
        if res:
            successList.append(city)
            break
        else:
            print "retry:",
            i += 1
            if not i < retryNum:
                failureList.append(city)

fc = open("./data/collect-" + fileName + ".js", "ab+")
fc.write("]\n")
fc.close()
os.system ("cp %s %s" % ("./data/collect-" + fileName + ".js", "./collect.js"))

print "成功:", len(successList)
print "失败:", len(failureList)
for c in failureList:
    print c,

