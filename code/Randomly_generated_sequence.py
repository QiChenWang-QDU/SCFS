import random



def generate_random_sequence(length,low,up):
    sequence = []
    for _ in range(length):
        sequence.append(random.randint(low, up))  # 这里可以修改数字的范围
    return sequence

def generate_unique_sequence(length, min_value, max_value):
    if length > (max_value - min_value + 1):
        raise ValueError("长度超过可用的唯一数字范围")

    unique_sequence = random.sample(range(min_value, max_value + 1), length)
    return unique_sequence

def insert_elements_in_order(A, B):
    a = A[:]  # 创建A的副本，以保持原始序列不变
    lastpos = 0
    for element in B:
        insertion_index = random.randint(lastpos+1, len(a))  # 随机选择一个插入位置

        if insertion_index > lastpos:
            a.insert(insertion_index, element)  # 在当前插入位置插入元素
            lastpos = a.index(element)
    return a

def seq(n,rep):
    num = []
    for i in range(0,n):
        num.append(i)
    num = num * rep
    random.shuffle(num)
    return num






if __name__ =="__main__":

    # aa = generate_random_sequence(40,1,30)
    # indexa = generate_unique_sequence(5,100,110)
    # bb = generate_random_sequence(40,1,30)
    # indexb = generate_unique_sequence(5,120,130)
    # for i in range(3):
    #     indexall = insert_elements_in_order(indexb,indexa)
    #     a = insert_elements_in_order(aa,indexall)
    #     aa = a
    #     b = insert_elements_in_order(bb,indexall)
    #     bb = b
    #
    # print(f"sequence1 = {aa}")
    # print(f"sequence2 = {bb}")
    # print(f"s1 = {indexa}")
    # print(f"s2 = {indexb}")


    # for i in range(10):
    #     length = 1024
    #     m = 8
    #     high = 7 * length / m
    #     file = open(f"C:\\Users\\ADaGe\\Desktop\\RFLCE_instance\\set2\\instance{length}-n_7_8({i+1}).txt", "w+", encoding="utf8")
    #     a = generate_random_sequence(length, 1, high)
    #     b = generate_random_sequence(length, 1, high)
    #     # 写入文本
    #     file.write(f"{a}\n")
    #     file.write(f"{b}\n")
    #
    #     # 关闭文件
    #     file.close()

    for i in range(10):
        n = 32
        rep = 8

        file = open(f"C:\\Users\\ADaGe\\Desktop\\RFLCE_instance\\set2\\instance{n}-{rep}({i + 1}).txt", "w+",
                    encoding="utf8")
        a = seq(n,rep)
        b = seq(n,rep)
        # 写入文本
        file.write(f"{a}\n")
        file.write(f"{b}\n")

        # 关闭文件
        file.close()

    # file = open("C:\\Users\\ADaGe\\Desktop\\RFLCE_instance\\instance128-n_4(1).txt", "r")
    # lines = file.readlines()
    # file.close()
    # a = lines[0].strip()
    # b = lines[1].strip()
    # data = [int(num) for num in a.strip('[]').split(',')]
    # data2 = [int(num) for num in b.strip('[]').split(',')]
