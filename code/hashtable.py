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

