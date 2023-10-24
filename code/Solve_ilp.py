import cplex
import re
import search
import time
from cplex.exceptions import CplexError
from tqdm import *

def ins2(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    a = lines[0].strip()
    b = lines[1].strip()
    data = [int(num) for num in a.strip('[]').split(',')]
    data2 = [int(num) for num in b.strip('[]').split(',')]
    return data,data2
def solve_ilp(t,A,B,index):
    prob = cplex.Cplex()
    # prob.set_log_stream(None)
    # prob.set_error_stream(None)
    # prob.set_warning_stream(None)
    # prob.set_results_stream(None)
    prob.objective.set_sense(prob.objective.sense.maximize)
    my_obj = [1 for i in range(len(t))]
    # my_ctype = 'I' * len(t)
    my_ctype = ''
    for ct in range(len(t)):
        my_ctype += 'B'
    my_ub = [1 for i in range(len(t))]
    my_lb = [0 for i in range(len(t))]
    my_colnames = [f'x{i}' for i in range(len(t))]
    my_rhs = [1.0]
    my_rownames = ['r1']
    my_sense = 'L'

    # print(my_obj)
    prob.variables.add(obj=my_obj, ub=my_ub, lb=my_lb, types=my_ctype, names=my_colnames)



    for i in range(len(t)):
        # 添加约束条件
        for j in range(i,len(t)):

                if t[i][0] < t[j][0] and t[i][1] > t[j][1] or t[i][0] > t[j][0] and \
                        t[i][1] < t[j][1]:
                    rows = [[[f'x{i}', f'x{j}'], [1.0, 1.0]]]
                    #print(f"1:{rows}")
                    prob.linear_constraints.add(lin_expr=rows, senses=my_sense, rhs=my_rhs)

    for i in range(len(t)):
        for j in range(i,len(t)):
            if i != j and A[t[i][0]] == B[t[j][1]]:
                if A[t[i][0]] not in index:
                    rows = [[[f'x{i}', f'x{j}'], [1.0, 1.0]]]
                    #print(f"2:{rows}")
                    prob.linear_constraints.add(lin_expr=rows, senses=my_sense, rhs=my_rhs)
    #


    for indexs in index:
        rows1 = []
        for i in range(len(t)):
            if A[t[i][0]] == indexs:
                rows1.append(f'x{i}')
        rows1 = list(set(rows1))
       # print(f"3:{rows1}")
        prob.linear_constraints.add(lin_expr=[[rows1,[1.0] * len(rows1)]], senses="E", rhs=my_rhs)

    try:
        prob.solve()
        solution = prob.solution.get_values()
        objective_value = prob.solution.get_objective_value()

        #print('Objective Value:', objective_value)
        #print('Solution:', solution)
        data = open("D:/DILCES_PY/result.txt", 'w+')
        data.write(str(solution))
        data.close()
        # file = open('/home/bioinfo/wangqc/hyb-CMSA2/ result.txt', 'r')
        file = open("D:/DILCES_PY/result.txt", 'r')

        Stinfo = []

        lines = file.read().rstrip()
        lines2 = lines.strip('[]')
        a = re.sub(',', '', lines2)
        l = a.split()
        l1 = list(map(lambda x: str(round(abs(float(x)))), l))
        for cpn,cp in enumerate(l1):
            if cp == '1':

                Stinfo.append(t[cpn])
        return Stinfo
    except CplexError as  exc:
        print(exc
              )

