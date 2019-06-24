class SList:
    def __init__(self):
        self.head = None


    def add_to_front(self, val):
        new_node = Node(val)
        current_head = self.head
        new_node.next = current_head
        self.head = new_node
        return self


    def print_values(self):
        runner = self.head
        while runner is not None:
            print(runner.value)
            runner = runner.next  # set the runner to its neighbor
        return self


    def add_to_back(self, val):
        if self.head is None:  # if the list is empty
            self.add_to_front(val)  # run the add_to_front method
            return self  # let's make sure the rest of this function doesn't happen if we add to the front
        new_node = Node(val)
        runner = self.head
        while runner.next is not None:
            runner = runner.next
        runner.next = new_node  # increment the runner to the next node in the list
        return self


    def remove_val(self, val):
        if self.head is None: # if list is empty
            return self
        current = self.head # get the current value
        while current.value != val: # matching value to value given
            prev = current # saving the current so we have its place
            current = current.next # sets current as the next value so when we get to our matching value it
                                   # will be skipped and its next value will be put in its place
        prev.next = current.next
        return self

    def remove_from_back(self):
        if self.head is None:
            return self
        runner = self.head
        while runner.next is not None:
            prev = runner
            runner = runner.next
            deleted_val = runner.value
        prev.next = None
        return deleted_val, self
    def remove_from_front(self):
        if self.head is None:
            return self
        current = self.head
        self.head = current.next
        return self


    def insert_at_index(self, val, n):
        insert_val = Node(val)
        if self.head is None:
            if n > 0:
                return False
            new_node = Node(val)
            self.head = new_node
            return self
        runner = self.head
        while n > 0:
            current = runner
            hold = runner.next
            runner = runner.next
            n -= 1
        current.next = insert_val
        insert_val.next = hold
        return self



class Node:
    def __init__(self, val):
        self.value = val
        self.next = None

my_list = SList()	# create a new instance of a list
my_list.add_to_front("is").add_to_front("Linked lists").add_to_back("fun!").add_to_front("Making").add_to_front('learning about').add_to_back('so much').insert_at_index('blah', 0)

print(my_list.remove_from_back())

my_list.print_values()

