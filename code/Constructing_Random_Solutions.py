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







