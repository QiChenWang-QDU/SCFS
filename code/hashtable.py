class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash_function(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self._hash_function(key)
        self.table[index].append((key, value))

    def search(self, key):
        index = self._hash_function(key)
        values = []
        for item in self.table[index]:
            if item[0] == key:
                values.append(item[1])
        return values

    def remove(self, key):
        index = self._hash_function(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                return True
        return False

    def modify(self, key, old_value, new_value):
        index = self._hash_function(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key and item[1] == old_value:
                self.table[index][i] = (key, new_value)
                return True
        return False
    def traverse(self):
        result = []
        for bucket in self.table:
            for item in bucket:
                result.append(item)
        return result

if __name__ == '__main__':

    hash_table = HashTable(10)
    hash_table.insert(5, (1,2))
    hash_table.insert(15, "B")
    hash_table.insert(25, "C")
    hash_table.insert(5, "D")  # 添加重复键的值
    print("遍历哈希表：", hash_table.traverse())
    print(hash_table.search(5))  # 输出：['A', 'D']
    print(hash_table.search(15))  # 输出：['B']
    print(hash_table.search(25))  # 输出：['C']
    print(hash_table.search(35))  # 输出：[]