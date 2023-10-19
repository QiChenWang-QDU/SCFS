from search import *
import random
import threading
import time
import multiprocessing

def th_Choose_cutting_point(s,index_gene,lena,lenb):
    cutting_point = []
    for ii in index_gene:
        total_fitness = 0
        fitness_values = []
        h = s.search(ii)
        for j in h:
            w = ((j[0] / lena + j[1] / lenb ) ** -1 ) * j[2]
            fitness_values.append(w)
            total_fitness += w
        probabilities = [fitness / total_fitness for fitness in fitness_values]
        cumulative_probabilities = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        r = random.uniform(0, 1)
        for i, probability in enumerate(cumulative_probabilities):
            if r <= probability:
                cutting_point.append(h[i])
                break
    result = cutting_point
    lock.acquire()
    results.append(result)
    lock.release()

def mu_Choose_cutting_point(s,index_gene,lena,lenb,result_queue):
    cutting_point = []
    for ii in index_gene:
        total_fitness = 0
        fitness_values = []
        h = s.search(ii)
        for j in h:
            w = ((j[0] / lena + j[1] / lenb ) ** -1 ) * j[2]
            fitness_values.append(w)
            total_fitness += w
        probabilities = [fitness / total_fitness for fitness in fitness_values]
        cumulative_probabilities = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        r = random.uniform(0, 1)
        for i, probability in enumerate(cumulative_probabilities):
            if r <= probability:
                cutting_point.append(h[i])
                break
    result = cutting_point
    result_queue.put(result)


def Choose_cutting_point(s,index_gene,lena,lenb):
    cutting_point = []
    for ii in index_gene:
        total_fitness = 0
        fitness_values = []
        h = s.search(ii)
        for j in h:
            w = (((j[0] + 1) / lena + (j[1] + 1) / lenb ) ** -1 ) * (j[2] + 1)
            fitness_values.append(w)
            total_fitness += w
        probabilities = [fitness / total_fitness for fitness in fitness_values]
        cumulative_probabilities = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        r = random.uniform(0, 1)
        for i, probability in enumerate(cumulative_probabilities):
            if r <= probability:
                cutting_point.append(h[i])
                break
    return cutting_point






def random_selection(A,B,indexA_cuts,s,drate):
    lastpos = (-1,-1)
    endpos = (len(A)-1,len(B)-1,None)
    sub = []
    indexA_cuts.append((len(A),len(B),None))
    for indexA_cut in indexA_cuts:
        if indexA_cut[0] > lastpos[0] and indexA_cut[1] > lastpos[1]:
            zs = set(A[lastpos[0] + 1: indexA_cut[0]] + B[lastpos[1] + 1: indexA_cut[1]])

            for z in zs:

                zp = []
                h = s.search(z)

                if len(h) != 0:
                    for hs in h:
                        if hs[0] > lastpos[0] and hs[0] <= indexA_cut[0] and hs[1] > lastpos[1] and hs[1] <= indexA_cut[1]:
                            zp.append(hs)

                    if len(zp) != 0:
                        r = random.uniform(0,1)
                        if len(zp) == 1:
                            sub.append(zp[0])
                        else:
                            if r <= drate:
                                lowpos = 0
                                loww = 9999999
                                for rs in range(len(zp)):
                                    w = (zp[rs][0] - lastpos[0] + 1) / (indexA_cut[0] - lastpos[0] + 1) + (zp[rs][1] - lastpos[1] + 1) / (indexA_cut[1] - lastpos[1] + 1)
                                    if w < loww:
                                        lowpos = rs
                                        loww = w


                                sub.append(zp[lowpos])
                            else:
                                add = random.randint(0,len(zp)-1)
                                sub.append(zp[add])
            lastpos = (indexA_cut[0], indexA_cut[1])
    indexA_cuts.pop(len(indexA_cuts)-1)


    return sub




def Generate_random_solutions(A, B, indexA, indexB, drate,s):


    cutting_indexA = Choose_cutting_point(s,indexA,len(A),len(B))
    cutting_indexB = Choose_cutting_point(s,indexB,len(A),len(B))

    sub = random_selection(A,B,cutting_indexA,s,drate)
    sub2 = random_selection(A, B, cutting_indexB, s, drate)
    finl_sub = list(set(sub+sub2))
    return finl_sub







if __name__ == '__main__':
    sequence1 = [1, 2, 4, 100, 100, 3]
    sequence2 = [2, 3, 4, 100,  2]
    m = len(sequence1)
    n = len(sequence2)
    s1 = [2]
    s2 = [100]
    s = generate_Z(sequence1, sequence2,s1,s2)
    results = []
    start_time = time.time()
    lock = threading.Lock()
    # 创建多个线程
    threads = []
    t1 = threading.Thread(target=th_Choose_cutting_point, args=(s, s1, m, n))
    threads.append(t1)
    t2 = threading.Thread(target=th_Choose_cutting_point, args=(s, s2, m, n))
    threads.append(t2)

    # 启动所有线程
    for t in threads:
        t.start()

    # 等待所有线程执行完毕
    for t in threads:
        t.join()
    end_time = time.time()
    # 计算运行时间，精确到毫秒
    run_time = (end_time - start_time) * 1000
    print("多线程运行时间：%.2f 毫秒" % run_time)


    start_time = time.time()
    result_queue = multiprocessing.Queue()

    # 创建多个进程
    processes = []
    p1 = multiprocessing.Process(target=mu_Choose_cutting_point, args=(s, s1, m, n, result_queue))
    processes.append(p1)
    p2 = multiprocessing.Process(target=mu_Choose_cutting_point, args=(s, s2, m, n, result_queue))
    processes.append(p2)

    # 启动所有进程
    for p in processes:
        p.start()

    # 等待所有进程执行完毕
    for p in processes:
        p.join()

    # 从队列中获取处理结果
    results = []
    while not result_queue.empty():
        result = result_queue.get()
        results.append(result)
    end_time = time.time()
    # 计算运行时间，精确到毫秒
    run_time = (end_time - start_time) * 1000
    print("多进程运行时间：%.2f 毫秒" % run_time)


    start_time = time.time()
    h = Choose_cutting_point(s,s1,m,n)
    h2 = Choose_cutting_point(s,s2,m,n)
    end_time = time.time()
    # 计算运行时间，精确到毫秒
    run_time = (end_time - start_time) * 1000
    print("串行运行时间：%.2f 毫秒" % run_time)
    print(h,h2)
    sub = random_selection(sequence1,sequence2,h,s,0.5)
    sub2 = random_selection(sequence1,sequence2,h2,s,0.5)
    print(sub,sub2)