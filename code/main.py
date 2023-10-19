import Pheromone_ConvergenceFactor
import Constructing_Random_Solutions
import Solve_ilp
import time
from tqdm import *
import pandas as pd
import Randomly_generated_sequence
import search
import matplotlib.pyplot as plt
import info



def merge_lists(list1, list2):
    merged_dict = {}

    # 合并列表1中的元组
    for item in list1:
        key = item[:2]  # 取元组的前两个元素作为键
        merged_dict[key] = item

    # 合并列表2中的元组
    for item in list2:
        key = item[:2]  # 取元组的前两个元素作为键
        merged_dict[key] = item

    # 提取字典的值，即为合并后的列表
    merged_list = list(merged_dict.values())

    return merged_list

def ag(datanum):

    df = pd.read_excel(
        f"C:\\Users\\ADaGe\\Desktop\\LCES-master\\LCES-master\\Supplemental Material\\Supplemental Material\\LCES-AG\\LCES-chr[{datanum}].xls",
        index_col=0)
    humen_data = df.iloc[:, 0]
    gor_data = df.iloc[:, 2]
    humendata = list(col for col in humen_data)
    gordata = list(col1 for col1 in gor_data)
    del gordata[gordata.index(' '):len(gordata)]
    humengen = []
    for i, j in enumerate(humendata):
        if j not in humendata[:i]:
            humengen.append(i)
        else:
            humengen.append(humendata.index(j))

    # print(len(humengen), len(set(humengen)))
    gorgen = []
    for i, j in enumerate(gordata):
        if j == None:
            gorgen.append(9999)
        elif j in humendata:
            gorgen.append(humendata.index(j))
        else:
            gorgen.append(985211)

    sequence1 = humengen
    sequence2 = gorgen


    return sequence1,sequence2

def seq():
    aa = Randomly_generated_sequence.generate_random_sequence(10,1,30)
    indexa = Randomly_generated_sequence.generate_unique_sequence(20,100,120)
    bb = Randomly_generated_sequence.generate_random_sequence(10,1,30)
    indexb = Randomly_generated_sequence.generate_unique_sequence(20,120,140)
    for i in range(1):
        indexall = Randomly_generated_sequence.insert_elements_in_order(indexb,indexa)
        a = Randomly_generated_sequence.insert_elements_in_order(aa,indexall)
        aa = a
        b = Randomly_generated_sequence.insert_elements_in_order(bb,indexall)
        bb = b
    return aa,bb,indexa,indexb

def pg(datanum):

    f = open(
        f'C:\\Users\\ADaGe\\Desktop\\LCES-master\\LCES-master\\LCESdata\\LCESdata-ide95len500\\MosaicSDs_SDblockIndexes{datanum}.txt',
        'r',
        encoding='utf-8')
    # f = open('C:\\Users\\ADaGe\\Desktop\\LCESdata\\MosaicSDs_SDblockIndexes1.txt', 'r', encoding='utf-8')
    result_hg = []
    result_gor = []
    lines = f.readlines()
    for num, line in enumerate(lines):
        c = []
        if num != 0:
            for i in line.split():
                c.append(i)
            if c[0] == f'Hg38_Chr{datanum}':
                for i, j in enumerate(c):
                    if j == ":":
                        for r in range(len(c)):
                            if r > i:
                                result_hg.append(c[r])
            if c[0] == f'Gor4_Chr{datanum}':
                for i, j in enumerate(c):
                    if j == ":":
                        for r in range(len(c)):
                            if r > i:
                                result_gor.append(c[r])
    # x = result_hg
    # y = result_gor
    list1 = list(map(lambda x: abs(int(x)), result_hg))
    list2 = list(map(lambda x: abs(int(x)), result_gor))
    print(len(list1), len(list2))

    list3 = list(map(lambda x: int(x), result_hg))
    list4 = list(map(lambda x: int(x), result_gor))
    print(len(list3), len(list4))

    list5 = list(filter(lambda x: int(x) > 0, result_hg))
    list6 = list(filter(lambda x: int(x) > 0, result_gor))
    print(len(list5), len(list6))

    for item in list5[::-1]:
        if item not in list6:
            list5.remove(item)
    for item in list6[::-1]:
        if item not in list5:
            list6.remove(item)

    print(f'绝对值长度：{len(list1)}')
    print(f'绝对值长度：{len(list2)}')

    print(f'去掉负数长度：{len(list5)}')
    print(f'去掉负数长度：{len(list6)}')

    info.addCommonMinus(list3, list4, 11000)
    print(f'相同负数处理之后长度：{len(list3)}')
    print(f'相同负数处理之后长度：{len(list4)}')

    for item in list3[::-1]:
        if item not in list4:
            list3.remove(item)
    for item in list4[::-1]:
        if item not in list3:
            list4.remove(item)

    print(f'相同负数处理去唯一长度：:{len(list3)}')
    print(f'相同负数处理去唯一长度：:{len(list4)}')

    for index in range(len(list3) - 1, -1, -1):
        if list3[index - 1] == list3[index]:
            list3.pop(index)
    for index in range(len(list4) - 1, -1, -1):
        if list4[index - 1] == list4[index]:
            list4.pop(index)

    print(f'相同负数处理去唯一去相邻重复长度：:{len(list3)}')
    print(f'相同负数处理去唯一去相邻重复长度：:{len(list4)}')
    return list3,list4

def ins(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    a = lines[0].strip()
    b = lines[1].strip()
    data = [int(num) for num in a.strip('[]').split(',')]
    data2 = [int(num) for num in b.strip('[]').split(',')]
    return data,data2


def testins():
    times = []
    lens = []
    insnum = 512
    insnam = 'n_7_8'
    for num in tqdm(range(10)):
        path = f'C:\\Users\\ADaGe\\Desktop\\RFLCE_instance\\set1\\instance{insnum}-{insnam}({num + 1}).txt'
        sequence1, sequence2 = ins(path)
        tbsf = []
        trb = []
        tpbs = []
        cf = 0
        cfp = []
        bs_update = False

        # sequence1,sequence2 = pg()
        # sequence1 = [52, 41, 46, 38, 8, 57, 13, 35, 9, 4, 54, 12, 16, 31, 47, 4, 27, 58, 15, 60, 13, 3, 48, 64, 4, 2, 6, 35, 7, 48, 25, 44, 57, 3, 42, 11, 24, 9, 4, 36, 59, 15, 58, 60, 60, 58, 9, 41, 31, 58, 64, 59, 28, 23, 37, 18, 43, 34, 15, 63, 57, 32, 50, 26, 25, 36, 34, 46, 2, 50, 3, 30, 21, 58, 16, 7, 15, 44, 3, 54, 31, 48, 17, 43, 11, 52, 9, 41, 62, 15, 63, 10, 57, 51, 24, 18, 49, 27, 41, 58, 55, 13, 6, 17, 54, 37, 37, 2, 18, 35, 17, 32, 42, 19, 22, 53, 39, 41, 10, 60, 39, 27, 58, 49, 51, 20, 7, 28, 8, 34, 5, 38, 27, 32, 17, 15, 19, 49, 48, 51, 16, 35, 6, 61, 25, 22, 18, 60, 47, 56, 6, 23, 59, 2, 41, 22, 44, 4, 18, 42, 16, 37, 59, 47, 12, 49, 36, 2, 3, 9, 12, 20, 12, 22, 42, 52, 16, 64, 53, 36, 6, 18, 15, 15, 38, 24, 12, 10, 7, 28, 47, 40, 12, 56, 10, 52, 4, 58, 21, 39, 14, 18, 26, 28, 17, 29, 37, 53, 54, 53, 55, 32, 51, 19, 46, 38, 41, 42, 23, 16, 4, 28, 23, 12, 32, 10, 11, 4, 30, 33, 9, 4, 27, 44, 12, 2, 5, 45, 44, 1, 52, 30, 13, 1, 56, 47, 42, 60, 17, 43, 20, 14, 28, 8, 51, 41, 60, 5, 8, 21, 12, 1, 26, 19, 5, 30, 8, 19, 20, 36, 8, 34, 46, 29, 62, 56, 12, 57, 6, 25, 34, 34, 1, 10, 16, 14, 63, 7, 51, 28, 40, 48, 5, 9, 32, 31, 51, 35, 54, 27, 61, 20, 50, 2, 15, 34, 14, 3, 41, 28, 2, 30, 50, 60, 17, 45, 19, 18, 39, 28, 64, 53, 36, 37, 22, 5, 15, 30, 64, 46, 32, 42, 50, 26, 36, 32, 21, 8, 56, 34, 24, 3, 56, 59, 40, 30, 20, 28, 40, 5, 22, 30, 3, 50, 44, 27, 39, 39, 48, 57, 46, 13, 50, 52, 16, 26, 46, 64, 53, 59, 59, 44, 2, 48, 12, 1, 62, 62, 1, 25, 24, 2, 13, 15, 43, 5, 25, 48, 52, 54, 47, 15, 25, 10, 36, 19, 63, 17, 16, 60, 35, 58, 37, 15, 19, 60, 64, 19, 16, 46, 57, 48, 50, 41, 27, 7, 9, 26, 25, 35, 4, 49, 23, 36, 39, 25, 18, 35, 60, 42, 7, 2, 38, 32, 32, 16, 58, 37, 62, 2, 63, 18, 62, 6, 11, 29, 12, 42, 11, 46, 33, 52, 8, 8, 15, 9, 28, 29, 14, 61, 35, 54, 52, 41, 2, 36, 34, 53, 19, 54, 15, 59, 31, 21, 11, 58, 23, 16, 41, 20, 55, 7, 5, 21, 27, 5, 16, 19, 32, 49, 32, 38, 45, 48, 51, 3, 15, 22, 13, 57, 49, 1, 47, 4, 52, 21, 44, 25, 22, 54, 34, 32]
        # sequence2 = [60, 14, 25, 31, 43, 38, 12, 56, 2, 31, 44, 42, 25, 38, 57, 16, 10, 5, 56, 2, 58, 33, 41, 2, 42, 1, 14, 15, 32, 49, 7, 52, 6, 43, 16, 37, 58, 64, 36, 56, 44, 61, 26, 27, 59, 25, 41, 4, 64, 16, 3, 21, 64, 14, 48, 55, 2, 29, 64, 61, 57, 5, 10, 30, 25, 28, 54, 34, 31, 61, 46, 8, 32, 3, 2, 64, 25, 60, 49, 4, 50, 64, 21, 36, 11, 18, 35, 29, 58, 45, 3, 6, 14, 47, 13, 32, 32, 26, 47, 55, 54, 6, 58, 53, 16, 57, 24, 10, 38, 35, 35, 44, 3, 53, 9, 3, 56, 49, 58, 28, 22, 51, 1, 35, 25, 33, 23, 5, 15, 44, 59, 6, 34, 63, 42, 45, 23, 35, 13, 3, 4, 42, 6, 61, 64, 40, 46, 15, 11, 2, 56, 20, 14, 5, 35, 14, 14, 4, 47, 54, 36, 62, 43, 8, 59, 63, 48, 20, 26, 10, 5, 43, 23, 5, 12, 22, 35, 6, 40, 16, 24, 48, 13, 62, 6, 26, 55, 43, 9, 39, 6, 43, 47, 54, 47, 7, 14, 53, 13, 53, 52, 63, 59, 54, 18, 12, 38, 2, 29, 4, 15, 64, 42, 35, 52, 13, 29, 41, 37, 8, 63, 43, 64, 2, 12, 53, 44, 26, 39, 5, 54, 28, 59, 54, 33, 37, 37, 13, 58, 37, 45, 17, 20, 59, 4, 30, 54, 12, 53, 50, 44, 36, 30, 7, 51, 29, 29, 18, 47, 55, 10, 5, 44, 47, 57, 36, 34, 46, 22, 3, 59, 63, 21, 23, 8, 30, 24, 33, 13, 45, 58, 59, 48, 12, 16, 22, 1, 40, 63, 36, 46, 4, 20, 16, 55, 27, 10, 51, 53, 36, 60, 48, 54, 41, 24, 43, 50, 57, 26, 58, 42, 12, 61, 64, 44, 15, 6, 22, 19, 36, 25, 16, 27, 35, 39, 3, 14, 23, 50, 47, 5, 41, 60, 62, 56, 50, 49, 3, 6, 19, 26, 2, 47, 30, 36, 21, 50, 23, 31, 28, 53, 4, 23, 7, 63, 46, 17, 16, 48, 33, 63, 42, 24, 19, 6, 36, 55, 8, 29, 2, 20, 23, 59, 56, 41, 55, 8, 9, 24, 57, 1, 58, 20, 46, 52, 19, 22, 21, 26, 52, 10, 56, 51, 43, 25, 53, 19, 64, 33, 33, 45, 12, 32, 31, 17, 20, 5, 58, 64, 64, 12, 40, 35, 28, 6, 54, 36, 35, 2, 7, 31, 16, 40, 61, 40, 45, 50, 44, 26, 5, 62, 46, 53, 38, 25, 3, 4, 2, 41, 25, 8, 44, 26, 43, 63, 52, 31, 52, 16, 39, 61, 26, 23, 43, 33, 28, 2, 64, 42, 40, 61, 59, 1, 51, 6, 51, 9, 40, 41, 60, 63, 27, 11, 54, 43, 45, 32, 6, 1, 50, 2, 10, 6, 23, 36, 1, 13, 40, 32, 4, 28, 35, 6, 35, 61, 60, 56, 23, 9, 3, 6, 22, 2, 59, 38, 53, 20, 32, 28, 12, 7, 61]

        s1 = []
        s2 = []
        zimu = list(set(sequence1 + sequence2))
        # print(len(zimu))
        index = s1 + s2
        t = []

        s = search.generate_Z(sequence1, sequence2, s1, s2)
        start = time.process_time()
        ss = True
        turn = 0
        cutes = []
        while ss:
            turn += 1
            # print("turn%d"%turn)
            hhs = []
            for i in index:
                hs = s.search(i)
                hhs += hs
            start_time = time.process_time()
            for i in range(30):
                h = Constructing_Random_Solutions.Generate_random_solutions(sequence1, sequence2, s1, s2, 0.7, s)
                tt = merge_lists(t, h)
                t = tt
            t = merge_lists(t, hhs)
            z = list(set(t))

            # print(len(z))
            # Pheromone_ConvergenceFactor.dealconflict(z,0.5)
            # print(len(z))
            Pheromone_ConvergenceFactor.age(z, zimu, 2, sequence1, tpbs)

            # print(f'reduced length :{len(z)}')
            tpbs = Solve_ilp.solve_ilp(z, sequence1, sequence2, index)

            if len(tpbs) > len(trb):
                trb = tpbs
            if len(tpbs) > len(tbsf):
                tbsf = tpbs
                endd = time.process_time()
                findbest = endd - start
            if len(index) != 0:
                Pheromone_ConvergenceFactor.ApplyPheromoneUpdate(cf, bs_update, tpbs, trb, tbsf, s, index)

                cfd = Pheromone_ConvergenceFactor.ComputeConvergenceFactor(s, index)
                cf = cfd
                cfp.append(cf)
                if cf > 0.99:

                    if bs_update == True:
                        bs_update = False
                        trb = []
                        Pheromone_ConvergenceFactor.re_init(s, index)
                    else:
                        bs_update = True
            end_time = time.process_time()
            # 计算运行时间，精确到毫秒
            run_time = (end_time - start_time) * 1000
            # print("运行时间：%.2f 毫秒" % run_time)

            end = time.process_time()

            if end - start > len(sequence1) / 10:
                ss = False

        # print(f"最优解长度{len(tbsf)},查找到最优解耗时{findbest * 1000}ms")
        times.append(findbest)
        lens.append(len(tbsf))

        result = []
        sorted_list = sorted(tbsf, key=lambda x: x[0])
        for i in sorted_list:
            result.append(sequence1[i[0]])
        # print(result)
        # print(len(z))
        if len(cfp) != 0:
            plt.plot(cfp)
            plt.show()
    total_len = sum(lens) / 10
    total_time = sum(times) / 10
    print(total_len, total_time)
    flie = open(f"C:\\Users\\ADaGe\\Desktop\\RFLCE_instance\\set1\\result\\instance{insnum}-{insnam}.txt","a",encoding='UTF-8')
    for item in lens:
        flie.write(str(item) + ' ')
    flie.write("\n")
    for item in times:
        flie.write(str(item) + ' ')
    flie.write("\n")
    flie.write(str(total_len)+"\n")
    flie.write(str(total_time))
    flie.close()


def testnom():
    tbsf = []
    trb = []
    tpbs = []
    cf = 0
    cfp = []
    bs_update = False

    # sequence1,sequence2 = pg()
    sequence1 = [4, 2, 4, 5, 3, 4, 2, 1]
    sequence2 = [3, 5, 2, 4, 5, 3, 1, 2]
    s1 = []
    s2 = []
    zimu = list(set(sequence1 + sequence2))
    # print(len(zimu))
    index = s1 + s2
    t = []

    s = search.generate_Z(sequence1, sequence2, s1, s2)
    start = time.process_time()
    ss = True
    turn = 0
    cutes = []
    while ss:
        turn += 1
        # print("turn%d"%turn)
        hhs = []
        for i in index:
            hs = s.search(i)
            hhs += hs
        start_time = time.process_time()
        for i in range(30):
            h = Constructing_Random_Solutions.Generate_random_solutions(sequence1, sequence2, s1, s2, 0.7, s)
            tt = merge_lists(t, h)
            t = tt
        t = merge_lists(t, hhs)
        z = list(set(t))

        # print(len(z))
        # Pheromone_ConvergenceFactor.dealconflict(z,0.5)
        # print(len(z))
        Pheromone_ConvergenceFactor.age(z, zimu, 2, sequence1, tpbs)

        # print(f'reduced length :{len(z)}')
        tpbs = Solve_ilp.solve_ilp(z, sequence1, sequence2, index)

        if len(tpbs) > len(trb):
            trb = tpbs
        if len(tpbs) > len(tbsf):
            tbsf = tpbs
            endd = time.process_time()
            findbest = endd - start
        if len(index) != 0:
            Pheromone_ConvergenceFactor.ApplyPheromoneUpdate(cf, bs_update, tpbs, trb, tbsf, s, index)

            cfd = Pheromone_ConvergenceFactor.ComputeConvergenceFactor(s, index)
            cf = cfd
            cfp.append(cf)
            if cf > 0.99:

                if bs_update == True:
                    bs_update = False
                    trb = []
                    Pheromone_ConvergenceFactor.re_init(s, index)
                else:
                    bs_update = True
        end_time = time.process_time()
        # 计算运行时间，精确到毫秒
        run_time = (end_time - start_time) * 1000
        # print("运行时间：%.2f 毫秒" % run_time)

        end = time.process_time()

        if end - start > len(sequence1) / 10:
            ss = False

    print(f"最优解长度{len(tbsf)},查找到最优解耗时{findbest * 1000}ms")

    result = []
    sorted_list = sorted(tbsf, key=lambda x: x[0])
    for i in sorted_list:
        result.append(sequence1[i[0]])
    print(result)
    # print(len(z))
    if len(cfp) != 0:
        plt.plot(cfp)
        plt.show()

if __name__ == "__main__":
    xx = ['2']
    for datanum in tqdm(xx):
        sequence1, sequence2 = pg(datanum)
        print(sequence1,sequence2)
        tbsf = []
        trb = []
        tpbs = []
        cf = 0
        cfp = []
        bs_update = False

        # sequence1,sequence2 = pg()
        # sequence1 = [52, 41, 46, 38, 8, 57, 13, 35, 9, 4, 54, 12, 16, 31, 47, 4, 27, 58, 15, 60, 13, 3, 48, 64, 4, 2, 6, 35, 7, 48, 25, 44, 57, 3, 42, 11, 24, 9, 4, 36, 59, 15, 58, 60, 60, 58, 9, 41, 31, 58, 64, 59, 28, 23, 37, 18, 43, 34, 15, 63, 57, 32, 50, 26, 25, 36, 34, 46, 2, 50, 3, 30, 21, 58, 16, 7, 15, 44, 3, 54, 31, 48, 17, 43, 11, 52, 9, 41, 62, 15, 63, 10, 57, 51, 24, 18, 49, 27, 41, 58, 55, 13, 6, 17, 54, 37, 37, 2, 18, 35, 17, 32, 42, 19, 22, 53, 39, 41, 10, 60, 39, 27, 58, 49, 51, 20, 7, 28, 8, 34, 5, 38, 27, 32, 17, 15, 19, 49, 48, 51, 16, 35, 6, 61, 25, 22, 18, 60, 47, 56, 6, 23, 59, 2, 41, 22, 44, 4, 18, 42, 16, 37, 59, 47, 12, 49, 36, 2, 3, 9, 12, 20, 12, 22, 42, 52, 16, 64, 53, 36, 6, 18, 15, 15, 38, 24, 12, 10, 7, 28, 47, 40, 12, 56, 10, 52, 4, 58, 21, 39, 14, 18, 26, 28, 17, 29, 37, 53, 54, 53, 55, 32, 51, 19, 46, 38, 41, 42, 23, 16, 4, 28, 23, 12, 32, 10, 11, 4, 30, 33, 9, 4, 27, 44, 12, 2, 5, 45, 44, 1, 52, 30, 13, 1, 56, 47, 42, 60, 17, 43, 20, 14, 28, 8, 51, 41, 60, 5, 8, 21, 12, 1, 26, 19, 5, 30, 8, 19, 20, 36, 8, 34, 46, 29, 62, 56, 12, 57, 6, 25, 34, 34, 1, 10, 16, 14, 63, 7, 51, 28, 40, 48, 5, 9, 32, 31, 51, 35, 54, 27, 61, 20, 50, 2, 15, 34, 14, 3, 41, 28, 2, 30, 50, 60, 17, 45, 19, 18, 39, 28, 64, 53, 36, 37, 22, 5, 15, 30, 64, 46, 32, 42, 50, 26, 36, 32, 21, 8, 56, 34, 24, 3, 56, 59, 40, 30, 20, 28, 40, 5, 22, 30, 3, 50, 44, 27, 39, 39, 48, 57, 46, 13, 50, 52, 16, 26, 46, 64, 53, 59, 59, 44, 2, 48, 12, 1, 62, 62, 1, 25, 24, 2, 13, 15, 43, 5, 25, 48, 52, 54, 47, 15, 25, 10, 36, 19, 63, 17, 16, 60, 35, 58, 37, 15, 19, 60, 64, 19, 16, 46, 57, 48, 50, 41, 27, 7, 9, 26, 25, 35, 4, 49, 23, 36, 39, 25, 18, 35, 60, 42, 7, 2, 38, 32, 32, 16, 58, 37, 62, 2, 63, 18, 62, 6, 11, 29, 12, 42, 11, 46, 33, 52, 8, 8, 15, 9, 28, 29, 14, 61, 35, 54, 52, 41, 2, 36, 34, 53, 19, 54, 15, 59, 31, 21, 11, 58, 23, 16, 41, 20, 55, 7, 5, 21, 27, 5, 16, 19, 32, 49, 32, 38, 45, 48, 51, 3, 15, 22, 13, 57, 49, 1, 47, 4, 52, 21, 44, 25, 22, 54, 34, 32]
        # sequence2 = [60, 14, 25, 31, 43, 38, 12, 56, 2, 31, 44, 42, 25, 38, 57, 16, 10, 5, 56, 2, 58, 33, 41, 2, 42, 1, 14, 15, 32, 49, 7, 52, 6, 43, 16, 37, 58, 64, 36, 56, 44, 61, 26, 27, 59, 25, 41, 4, 64, 16, 3, 21, 64, 14, 48, 55, 2, 29, 64, 61, 57, 5, 10, 30, 25, 28, 54, 34, 31, 61, 46, 8, 32, 3, 2, 64, 25, 60, 49, 4, 50, 64, 21, 36, 11, 18, 35, 29, 58, 45, 3, 6, 14, 47, 13, 32, 32, 26, 47, 55, 54, 6, 58, 53, 16, 57, 24, 10, 38, 35, 35, 44, 3, 53, 9, 3, 56, 49, 58, 28, 22, 51, 1, 35, 25, 33, 23, 5, 15, 44, 59, 6, 34, 63, 42, 45, 23, 35, 13, 3, 4, 42, 6, 61, 64, 40, 46, 15, 11, 2, 56, 20, 14, 5, 35, 14, 14, 4, 47, 54, 36, 62, 43, 8, 59, 63, 48, 20, 26, 10, 5, 43, 23, 5, 12, 22, 35, 6, 40, 16, 24, 48, 13, 62, 6, 26, 55, 43, 9, 39, 6, 43, 47, 54, 47, 7, 14, 53, 13, 53, 52, 63, 59, 54, 18, 12, 38, 2, 29, 4, 15, 64, 42, 35, 52, 13, 29, 41, 37, 8, 63, 43, 64, 2, 12, 53, 44, 26, 39, 5, 54, 28, 59, 54, 33, 37, 37, 13, 58, 37, 45, 17, 20, 59, 4, 30, 54, 12, 53, 50, 44, 36, 30, 7, 51, 29, 29, 18, 47, 55, 10, 5, 44, 47, 57, 36, 34, 46, 22, 3, 59, 63, 21, 23, 8, 30, 24, 33, 13, 45, 58, 59, 48, 12, 16, 22, 1, 40, 63, 36, 46, 4, 20, 16, 55, 27, 10, 51, 53, 36, 60, 48, 54, 41, 24, 43, 50, 57, 26, 58, 42, 12, 61, 64, 44, 15, 6, 22, 19, 36, 25, 16, 27, 35, 39, 3, 14, 23, 50, 47, 5, 41, 60, 62, 56, 50, 49, 3, 6, 19, 26, 2, 47, 30, 36, 21, 50, 23, 31, 28, 53, 4, 23, 7, 63, 46, 17, 16, 48, 33, 63, 42, 24, 19, 6, 36, 55, 8, 29, 2, 20, 23, 59, 56, 41, 55, 8, 9, 24, 57, 1, 58, 20, 46, 52, 19, 22, 21, 26, 52, 10, 56, 51, 43, 25, 53, 19, 64, 33, 33, 45, 12, 32, 31, 17, 20, 5, 58, 64, 64, 12, 40, 35, 28, 6, 54, 36, 35, 2, 7, 31, 16, 40, 61, 40, 45, 50, 44, 26, 5, 62, 46, 53, 38, 25, 3, 4, 2, 41, 25, 8, 44, 26, 43, 63, 52, 31, 52, 16, 39, 61, 26, 23, 43, 33, 28, 2, 64, 42, 40, 61, 59, 1, 51, 6, 51, 9, 40, 41, 60, 63, 27, 11, 54, 43, 45, 32, 6, 1, 50, 2, 10, 6, 23, 36, 1, 13, 40, 32, 4, 28, 35, 6, 35, 61, 60, 56, 23, 9, 3, 6, 22, 2, 59, 38, 53, 20, 32, 28, 12, 7, 61]

        s1 = [217, 325, 364, 419, 441, 468, 469, 531, 587, 117, 119, 658, 663, 688, 701, 704, 710, 126, 734, 736, 780, 822, 827, 840, 848, 860, 861, 876, 884, 894, 914, 922, 944, 945, 958, 961, 969, 971, 981, 982, 990, 1005, 1009, 1017, 1024, 1029, 1036, 1038, 1042, 1055, 1057, 1061, 1076, 1078, 1079, 1080, 1098, 1112, 1121, 1126, 1129, 1147, 1153, 1159, 1160, 1162, 1165, 1187, 1194, 1200, 1214, 1226, 1232, 1239, 1245, 1272, 1276, 1278, 1289, 1305, 1316, 11886, 1332, 1342, 1346, 1340, 1360, 1369, 1370, 1373, 1378, 1379, 1382, 1385, 1389, 1391, 1399, 1402, 1403, 1405, 1406, 1412, 1414, 1445, 1452, 1457, 1464, 11767, 1468, 1480, 1490, 1499, 1504, 1510, 1511, 1513, 1515, 1523, 1525, 1528, 1529, 1531, 1535, 1538, 1539, 1544, 1545, 1548, 1550, 1557, 1558, 1559, 1560, 1563, 1567, 1581, 1586, 1592, 1594, 1600, 1613, 1617, 1618, 1620, 1625, 1626, 1631, 1634, 1642, 1643, 1646, 1647, 1649, 1650, 1650, 1652, 1650, 1653, 1656, 1660, 1662, 1664, 1669, 1671, 1672, 1675, 1684, 1688, 1692, 1693, 1694, 1696, 1697, 1700, 1703, 1704, 1706, 1708, 1709, 1720, 1723, 1734, 1745, 1750, 1752, 1754, 1758, 1760, 1762, 1764, 1771, 1772, 1774, 1784, 1785, 1791, 1792, 1793, 1798, 1808, 1810, 1817, 1818, 1819, 1816, 1822, 1828, 1835, 1836, 1837, 1842, 1843, 1849, 1852, 1854, 1855, 1860, 1864, 1865, 1867, 1870, 1871, 1872, 1875, 1878, 1879, 1881, 1882, 1884, 1889, 1896, 1894, 1897, 1898, 1900, 1906, 1911, 1913, 1914, 1917, 1920, 1923, 1924, 1925, 1926, 1930, 1938, 1939, 1941, 1947, 1951, 1954, 1958, 1962, 1965, 1966, 1967, 1984, 1986, 1991, 2003, 2013, 2015, 2017, 2022, 2032, 2035, 2036, 2037, 2042, 2046, 2051, 2052, 11009, 2054, 2071, 2073, 2076, 2081, 2082, 2087, 2088, 2091, 2087, 2095, 2101, 2103, 2107, 2111, 2115, 2128, 2133, 2141, 2144, 2148, 2150, 2155, 2158, 2161, 2166, 2184, 2189, 2190, 2193, 2194, 2195, 2197, 2205, 2210, 2211, 2214, 2224, 2229, 2234, 2236, 2239, 2242, 2243, 2245, 2246, 2247, 2249, 2254, 2259, 2264, 2269, 2270, 2271, 2274, 2276, 2278, 2279, 2288, 2293, 2295, 2296, 2298, 2299, 2303, 2304, 2305, 2307, 2311, 2316, 2319, 2321, 2322, 2325, 2327, 2328, 2335, 2336, 2338, 2339, 2345, 2346, 2350, 2353, 2356, 11022, 2362, 2364, 2367, 2368, 2369, 2373, 2374, 2375, 2376, 2377, 2381, 2379, 2382, 2388, 2389, 2390, 2400, 2401, 2404, 2405, 2408, 2410, 2423, 2428, 2429, 2435, 2443, 2446, 2458, 2463, 2465, 2468, 2470, 2473, 2477, 2479, 2480, 2483, 2485, 2486, 2488, 2491, 2494, 2497, 2498, 2504, 2505, 2511, 2512, 2520, 2523, 2528, 2529, 2535, 2536, 2540, 2541, 2542, 2543, 2544, 2552, 2553, 2564, 2565, 2567, 2568, 2570, 2574, 2575, 2578, 2579, 2581, 2582, 2587, 2589, 2593, 2594, 2597, 2600, 2601, 2603, 2605, 2607, 2619, 2621, 2622, 2630, 2633, 2636, 2647, 2655, 2658, 2659, 2660, 2663, 2664, 2666, 2668, 2671, 2674, 2671, 2677, 2684, 2685, 2691, 2693, 2694, 2696, 2697, 2699, 2701, 11026, 11029, 11027, 2710, 2711, 2712, 2714, 2715, 2718, 2720, 2719, 2725, 2728, 2733, 2727, 2736, 2739, 2741, 2743, 2745, 2746, 2749, 2750, 2752, 2753, 2756, 2761, 2762, 2763, 2765, 2766, 2767, 2769, 2771, 2774, 2780, 2781, 2785, 2786, 2787, 2789, 2792, 2794, 2795, 2796, 2810, 2813, 2814, 2815, 2821, 2822, 2825, 2833, 2836, 2840, 2842, 2843, 2844, 2846, 2850, 2852, 2853, 2854, 2855, 2857, 2860, 2866, 2868, 2872, 2873, 11039, 2876, 2892, 2893, 2899, 2901, 2905, 2906, 2910, 2915, 2916, 2918, 2922, 2924, 2926, 2929, 2931, 2932, 2936, 2937, 2938, 2939, 2940, 2944, 2946, 2950, 2960, 2961, 2962, 2966, 2969, 2973, 2974, 2977, 2978, 2979, 2982, 2983, 2986, 2989, 2990, 2991, 2992, 2993, 2997, 3006, 3008, 11044, 3011, 3012, 3013, 3017, 3019, 3026, 3028, 3032, 3033, 3034, 3035, 3037, 3038, 3043, 3044, 3045, 3048, 3051, 3055, 3057, 3058, 3062, 3063, 3066, 3067, 3068, 3070, 3072, 3075, 3076, 3077, 3078, 3080, 3081, 3085, 3091, 3093, 3096, 3103, 3109, 3110, 3111, 3112, 3113, 3114, 3115, 3116, 3119, 3120, 3124, 3125, 3128, 3129, 3131, 3132, 3134, 3136, 3139, 3144, 3145, 3146, 3151, 3152, 3156, 3160, 3161, 3163, 3166, 3170, 3171, 3172, 3175, 3176, 3177, 3183, 3184, 3185, 3187, 3188, 3189, 3190, 3192, 3191, 3198, 3199, 3201, 3203, 3204, 3206, 3207, 3208, 3212, 3217, 3218, 3219, 3221, 3222, 3225, 3226, 3229, 3237, 3240, 3242, 3244, 3246, 3247, 3249, 3251, 3252, 3256, 3258, 3260, 3261, 3263, 3264, 3266, 3271, 3273]
        s2= []


        zimu = list(set(sequence1 + sequence2))
        # print(len(zimu))
        index = s1 + s2
        t = []

        s = search.generate_Z(sequence1, sequence2, s1, s2)
        start = time.process_time()
        ss = True
        turn = 0
        cutes = []
        while ss:
            turn += 1
            # print("turn%d"%turn)
            hhs = []
            for i in index:
                hs = s.search(i)
                hhs += hs
            start_time = time.process_time()
            for i in range(10):
                h = Constructing_Random_Solutions.Generate_random_solutions(sequence1, sequence2, s1, s2, 0.7, s)
                tt = merge_lists(t, h)
                t = tt
            t = merge_lists(t, hhs)
            z = list(set(t))

            # print(len(z))
            # Pheromone_ConvergenceFactor.dealconflict(z,0.5)
            # print(len(z))
            Pheromone_ConvergenceFactor.age(z, zimu, 2, sequence1, tbsf)

            # print(f'reduced length :{len(z)}')
            tpbs = Solve_ilp.solve_ilp(z, sequence1, sequence2, index)

            if len(tpbs) > len(trb):
                trb = tpbs
            if len(tpbs) > len(tbsf):
                tbsf = tpbs
                endd = time.process_time()
                findbest = endd - start
            if len(index) != 0:
                Pheromone_ConvergenceFactor.ApplyPheromoneUpdate(cf, bs_update, tpbs, trb, tbsf, s, index)

                cfd = Pheromone_ConvergenceFactor.ComputeConvergenceFactor(s, index)
                cf = cfd
                cfp.append(cf)
                if cf > 0.99:

                    if bs_update == True:
                        bs_update = False
                        trb = []
                        Pheromone_ConvergenceFactor.re_init(s, index)
                    else:
                        bs_update = True
            end_time = time.process_time()
            # 计算运行时间，精确到毫秒
            run_time = (end_time - start_time) * 1000
            # print("运行时间：%.2f 毫秒" % run_time)

            end = time.process_time()
            print(f"最优解长度{len(tbsf)},查找到最优解耗时{findbest * 1000}ms")
            if end - start > len(sequence1) / 10:
                ss = False


        print(f"最优解长度{len(tbsf)},查找到最优解耗时{findbest * 1000}ms")


        result = []
        sorted_list = sorted(tbsf, key=lambda x: x[0])
        for i in sorted_list:
            result.append(sequence1[i[0]])
        print(result)
        # print(len(z))
        if len(cfp) != 0:
            plt.plot(cfp)
            plt.show()

        flie = open(f"C:\\Users\\ADaGe\\Desktop\\RFLCE_instance\\pg\\result\\pg{datanum}.txt", "a",
                    encoding='UTF-8')

        flie.write(str(len(tbsf)) + "\n")
        flie.write(str(findbest * 1000))
        flie.close()
