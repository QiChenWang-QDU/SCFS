import random

def lcs(nums1, nums2):
    m = len(nums1)
    n = len(nums2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):
        for j in range(n):
            if nums1[i] == nums2[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])


    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if nums1[i - 1] == nums2[j - 1]:
            lcs.append(nums1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs.reverse()
    return lcs

sequence1 = []
sequence2 = []
result = lcs(sequence1, sequence2)
print(len(result))


def select_10_percent(lst):
    n = len(lst)
    num_to_select = int(n * 0.1)
    selected = []

    for i in range(n):
        prob = (i + 1) / n
        if random.random() <= prob and len(selected) < num_to_select:
            selected.append(lst[i])

    return selected



lst = result
result = select_10_percent(lst)
print(result)