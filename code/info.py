import random

import pandas as pd
def addCommonMinus(list1,list2,sapn):
    for index in range(len(list1)-1,-1,-1):
        tmp = list1[index]
        if tmp < 0:
            if tmp not in list2:
                list1.remove(tmp)
            else:
                list1[index] = abs(tmp) + sapn
                for i in range(len(list2)):
                    if list2[i] == tmp:
                        list2[i] = abs(tmp) + sapn
    for index in range(len(list2) - 1, -1, -1):
        tmp = list2[index]
        if tmp < 0:
            if tmp not in list1:
                list2.remove(tmp)
            else:
                list2[index] = abs(tmp) + sapn
                for i in range(len(list1)):
                    if list1[i] == tmp:
                        list1[i] = abs(tmp) + sapn



