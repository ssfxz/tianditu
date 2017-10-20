# -*- coding: utf-8 -*-
import re


fchina = open("./china.txt", "r")
fprovince = open("./province.txt", "wb+")
fcity = open("./city.txt", "wb+")
fcounty = open("./county.txt", "wb+")

for line in fchina.readlines():
    if not line.find("市辖区") == -1:
        continue
    elif not line.find("省直辖县级行政区划") == -1:
        continue
    elif not line.find("自治区直辖县级行政区划") == -1:
        continue

    if not line[0] == " ":
        fprovince.write(line[7:len(line)])
        print line[7:len(line)]
    elif not line[1] == " ":
        fcity.write(line[8:len(line)])
        print "\t", line[8:len(line)]
    else:
        fcounty.write(line[9:len(line)])
        print "\t", line[9:len(line)]

fchina.close()
fprovince.close()
fcity.close()
fcounty.close()