import random
import numpy as np
from hashtable import *

def generate_Z(A, B,indexA,indexB):
    m = len(A)
    n = len(B)

    if m>n:
        h = n
    else:
        h = m
    S = HashTable(h)

    for i in range(m):
        for j in range(n):
            if A[i] == B[j]:
                if A[i] in indexA or B[j] in indexB:
                    S.insert(A[i], (i, j, 0.5))

                else:
                    S.insert(A[i], (i, j, None))
    return S

def generate_index(A, B,indexA,indexB):
    m = len(A)
    n = len(B)

    if m>n:
        h = n
    else:
        h = m
    S = HashTable(h)

    for i in range(m):
        for j in range(n):
            if A[i] == B[j]:
                if A[i] in indexA or B[j] in indexB:
                    S.insert(A[i], (i, j, 0.5))
    return S


def character_set(A,B):
    char = set(A+B)
    return char

def initialize_pheromone_matrix(size_indexA,size_indexB):
    matrix = [[0.5 for _ in range(len(size_indexA))] for _ in range(len(size_indexB))]
    return matrix

def find_positions(A, B, element):
    positions = [i for i, (x, y) in enumerate(zip(A, B)) if x == element or y == element]
    return positions

def find_positions2(sequence, element):
    positions = [i for i, x in enumerate(sequence) if x == element]
    return positions

def maxx(a,b):
    if a > b:
        return a
    else:
        return b

def min(a,b):
    if a > b:
        return b
    else:
        return a


