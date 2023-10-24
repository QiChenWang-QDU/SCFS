import random



def generate_random_sequence(length,low,up):
    sequence = []
    for _ in range(length):
        sequence.append(random.randint(low, up))
    return sequence

def generate_unique_sequence(length, min_value, max_value):
    if length > (max_value - min_value + 1):
        raise ValueError("长度超过可用的唯一数字范围")

    unique_sequence = random.sample(range(min_value, max_value + 1), length)
    return unique_sequence

def insert_elements_in_order(A, B):
    a = A[:]
    lastpos = 0
    for element in B:
        insertion_index = random.randint(lastpos+1, len(a))

        if insertion_index > lastpos:
            a.insert(insertion_index, element)  
            lastpos = a.index(element)
    return a

def seq(n,rep):
    num = []
    for i in range(0,n):
        num.append(i)
    num = num * rep
    random.shuffle(num)
    return num






