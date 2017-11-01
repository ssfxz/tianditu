# -*- coding: utf-8 -*-
import urllib2
import json
import traceback
import os
import sys
import socket
import urllib
import time

def getRegion(region):
    coords = region.split(';')
    regionStr = ""
    for index, coord in enumerate(coords):
        regionStr += coord
        if (index % 2 == 0):
            regionStr += ' '
        elif (index % 2 == 1):
            regionStr += ','
    return {"region": regionStr}

def transData(data):
    regions = data["coords"].split('@')
    points = map(getRegion, regions)
    areaData = {
        "lonlat": data["longitude"] + "," + data["latitude"],
        "name": data["name"],
        "ename": data["ename"],
        "points": points
    }
    return areaData

def fetchData(city, fileName):
    print city,

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }

    url = "http://ditu.amap.com/service/poiInfo?query_type=TQUERY&keywords=" + urllib.quote(city)
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request, timeout=1).read()
        cityData = json.loads(response)
        data = cityData["data"]["locres"]["poi_list"][0]
        areaData = transData(data)

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
        return "Timeout"
    except urllib2.URLError:
        print "Timeout!"
        return "Timeout"
    except TypeError:
        print "Request Banned!"
        return "Banned"
    except:
        print "Failure!"
        traceback.print_exc()
        return "Failure"
    else:
        print "Done!"
        return "Done"

def fileSeek(file, lineSeek) :
    file.seek(0)
    if lineSeek == 0 :
        return 0
    offset = 0
    for index,line in enumerate(file.readlines()):
        if index + 1 == lineSeek :
            break
        else :
            offset += len(line)
    file.seek(offset)
    return index

def printInfo(successList, failureList) :
    print "成功:", len(successList)
    print "失败:", len(failureList)
    for c in failureList:
        print c,

def main() :
    fileName = sys.argv[1]
    lineSeek = 0
    if len(sys.argv) == 3 :
        lineSeek = int(sys.argv[2])
    # fileName = "city"
    # fileName = "province"
    file = open(fileName + ".txt")
    city = ""
    successList = []
    failureList = []
    retryNum = 5

    fileMode = "wb+"
    fileHead = "var collect = [\n"
    if not lineSeek == 0 :
        fileMode = "ab+"
        fileHead = ""
    fc = open("./data/collect-" + fileName + ".js", fileMode)
    fc.write(fileHead)
    fc.close()

    total = len(file.readlines())
    count = fileSeek(file, lineSeek)

    for line in file.readlines():
        city = line.strip('\n')
        count += 1
        progress = "%d/%d" %(count, total)
        print progress,
        i = 0
        while i < retryNum:
            time.sleep(0.1)
            res = fetchData(city, fileName)

            if res == "Done" :
                successList.append(city)
                break
            elif res == "Timeout" or res == "Failure":
                i += 1
                print "retry:", i
                if not i < retryNum:
                    print "Abandon Retry"
                    failureList.append(city)
            elif res == "Banned" :
                print "Current Progress:", progress, city
                printInfo(successList, failureList)
                sys.exit(0)


    fc = open("./data/collect-" + fileName + ".js", "ab+")
    fc.write("]\n")
    fc.close()
    os.system ("cp %s %s" % ("./data/collect-" + fileName + ".js", "./collect.js"))
    printInfo(successList, failureList)

if __name__=='__main__':
    main()