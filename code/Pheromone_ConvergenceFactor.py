from hashtable import *

def jury(tpbs,pos_index):

    result = int(any(tup[0] == pos_index[0] and tup[1] == pos_index[1] for tup in tpbs))
    return result


def maxx(a,b):
    if a > b:
        return a
    else:
        return b



def re_init(s,indexs):
    for index in indexs:
        h = s.search(index)
        for i in h:
            s.modify(index,i,(i[0], i[1], 0.5))


def  ApplyPheromoneUpdate(cf,bs_update,tpbs,trb,tbsf,s,indexs):

    for index in indexs:
        pos_indexs = s.search(index)
        for pos_index in pos_indexs:
            if bs_update == False:
                if cf < 0.4:
                    Pheromone = pos_index[2] + 0.2 * (1 * jury(tpbs, pos_index) - pos_index[2])
                    s.modify(index,pos_index,(pos_index[0], pos_index[1], Pheromone))
                elif 0.4 <= cf < 0.6:
                    Pheromone = pos_index[2] + 0.2 * (2/3 * jury(tpbs, pos_index) + 1/3 * jury(trb, pos_index) - pos_index[2])
                    s.modify(index, pos_index, (pos_index[0], pos_index[1], Pheromone))
                elif 0.6 <= cf < 0.8:
                    Pheromone = pos_index[2] + 0.2 * (1/3 * jury(tpbs, pos_index) + 2/3 * jury(trb, pos_index) - pos_index[2])
                    s.modify(index, pos_index, (pos_index[0], pos_index[1], Pheromone))
                else:
                    Pheromone = pos_index[2] + 0.15 * (1 * jury(trb, pos_index) - pos_index[2])
                    s.modify(index, pos_index, (pos_index[0], pos_index[1], Pheromone))
            else:
                Pheromone = pos_index[2] + 0.15 * (1 * jury(tbsf, pos_index) - pos_index[2])
                s.modify(index, pos_index, (pos_index[0], pos_index[1], Pheromone))



def ComputeConvergenceFactor(s,indexs):
    pos_indexs = []
    for index in indexs:
        pos_index = s.search(index)
        pos_indexs += pos_index
    v = [t[2] for t in pos_indexs]
    min_value = 0.001
    max_value = 0.999

    cf = 2 * (((sum(maxx(max_value - t[2], t[2] - min_value) for t in pos_indexs)) / len(pos_indexs) * (max_value - min_value)) - 0.5)
    return cf


def sort_with_index(arr):
    sorted_arr = sorted(arr, reverse=True)  # 对数组进行降序排序
    sorted_index = [i for i, _ in sorted(enumerate(arr), key=lambda x: x[1], reverse=True)]  # 获取排序后的索引

    return sorted_arr, sorted_index


def dealconflict(z,r):
    sorces = []
    for i in z:
        if i[2] == None:
            sorce = 0
            for j in z:
                if i[0] > j[0] and i[1] < j[1]:
                    sorce += 1
                if i[0] < j[0] and i[1] > j[1]:
                    sorce += 1
            sorces.append(sorce)
    sorted_arr, sorted_index = sort_with_index(sorces)
    delnum = []
    d = len(z) * r
    for i in range(round(d)):
        delnum.append(sorted_index[i])
    sorted_delnum = sorted(delnum, reverse=True)
    for i in sorted_delnum:
        z.pop(i)

def age(z,s,ratdio,a,tpbs):
    h = HashTable(len(z))
    cuts = []
    for i in z:
        if i[2] == None:
            sorce = 0
            for j in tpbs:
                if i[0] > j[0] and i[1] < j[1]:
                    sorce += 1

                if i[0] < j[0] and i[1] > j[1]:
                    sorce += 1


            h.insert(a[i[0]],(sorce,z.index(i)))

    for i in s:
        l = h.search(i)
        if len(l) > ratdio:
            cut = len(l) - ratdio

            orted_data = sorted(l, key=lambda x: x[0], reverse=True)
            for j in range(cut):
                cuts.append(orted_data[j][1])


    sorted_delnum = sorted(cuts, reverse=True)
    #print(sorted_delnum)
    for i in sorted_delnum:
        z.pop(i)