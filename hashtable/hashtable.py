
class HashTableEntry:
    """
    Linked List hash table key/value pair
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity, load_factor_top_limit=0.8, load_factor_bottom_limit=0.1, multiplier=2):
        # Your code here
        self.capacity = capacity
        self.data = [None] * capacity
        self.count = 0
        self.load_factor_top_limit = load_factor_top_limit
        self.load_factor_bottom_limit = load_factor_bottom_limit
        self.multiplier = multiplier

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # Your code here
        return self.capacity

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # Your code here
        return self.count / self.capacity

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for c in key:
            # The ord() function returns an integer representing the Unicode character.
            hash = (hash * 33) + ord(c)
        return hash

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.djb2(key) % self.capacity

    def increment_count(self):
        self.count = self.count + 1

    def decrement_count(self):
        self.count = self.count - 1

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Your code here
        index = self.hash_index(key)
        # First check the if index is None
        if self.data[index] is None:
            # If None, put replace None with instance of HashTableEntry
            self.data[index] = HashTableEntry(key, value)
            self.increment_count()
        else:
            current_node = self.data[index]
            # When this loop breaks, current node will either have the same key as
            # argument, or current_node.next will be None, which means we can append to end of list
            while current_node.key != key and current_node.next:
                current_node = current_node.next
            # If we dropped out of loop because we found the same key, we change the value of the existing key
            if current_node.key == key:
                current_node.value = value
            else:
                current_node.next = HashTableEntry(key, value)
                self.increment_count()
        self.check_load_and_resize()

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here

        index = self.hash_index(key)
        current_node = self.data[index]
        previous_node = None  # Get reference for prev node

        if current_node is None:
            print('Nothing at this index')
            return
        elif current_node.next is None:
            # If current_node's next is None, it means it's the only
            # value at that index, so make it None
            if(current_node.key == key):
                self.data[index] = None
                self.decrement_count()
            else:
                print('Index exists, but key missing in linked list')
                return
        else:
            # Go through the list, and find by key, makeing it's previous node's next None
            while current_node is not None and current_node.key != key:
                previous_node = current_node
                current_node = current_node.next
            # If we got to the end of the list, and the current_nodes key does not match,
            # we warn user key does not exist
            if current_node.key != key:
                print('Index exists, but key missing in linked list')
                return
            # else we make previous node's next None to delete current_node
            else:
                previous_node.next = None

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Your code here
        # Find the linked list by index, look for key in linked list, return value, otherwise None
        index = self.hash_index(key)
        current_node = self.data[index]
        if current_node is None:
            return None
        else:
            while current_node is not None:
                if current_node.key == key:
                    return current_node.value
                current_node = current_node.next
            return None

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # To increase size of storage, we loop over existing storage
        # and add it to new array, make that new array new storage
        old_data = self.data
        self.capacity = new_capacity
        self.data = [None] * new_capacity
        for i in old_data:
            if i is not None:
                # We use our put method to put old items into new data array
                self.put(i.key, i.value)

    def check_load_and_resize(self):
        if self.get_load_factor() > self.load_factor_top_limit:
            self.resize(self.capacity * self.multiplier)
       

if __name__ == "__main__":
    ht = HashTable(192299357)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
