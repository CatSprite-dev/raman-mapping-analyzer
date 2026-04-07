class MaxHeap:
    def __init__(self):
        self.elements = []
        
    def pop(self):
        if len(self.elements) == 0:
            return None

        if len(self.elements) == 1:
            return self.elements.pop()

        root_value = self.elements[0]
        self.elements[0] = self.elements.pop()
        self.bubble_down(0)

        return root_value

    def bubble_down(self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        max_index = index

        if (
            left_child_index < len(self.elements)
            and self.elements[left_child_index][0] > self.elements[max_index][0]
        ):
            max_index = left_child_index

        if (
            right_child_index < len(self.elements)
            and self.elements[right_child_index][0] > self.elements[max_index][0]
        ):
            max_index = right_child_index

        if max_index != index:
            self.elements[index], self.elements[max_index] = (
                self.elements[max_index],
                self.elements[index],
            )
            self.bubble_down(max_index)


    def push(self, priority, value):
        self.elements.append((priority, value))
        self.bubble_up(len(self.elements) - 1)

    def bubble_up(self, index):
        if index == 0:
            return

        parent_index = (index - 1) // 2
        parent_priority = self.elements[parent_index][0]
        current_priority = self.elements[index][0]

        if parent_priority < current_priority:
            self.elements[parent_index], self.elements[index] = (
                self.elements[index],
                self.elements[parent_index],
            )
            self.bubble_up(parent_index)

    def peek(self):
        if len(self.elements) == 0:
            return None

        return self.elements[0][1]
