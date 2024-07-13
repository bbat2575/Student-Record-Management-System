class Student:
    """
    Represents a node of a binary tree.
    """
    def __init__(self, student_id, name, GPA) -> None:
        self.left = None
        self.right = None
        self.parent = None
        self.student_id = student_id
        self.name = name
        self.GPA = GPA

class BSTree:
    """
    Implements an unbalanced Binary Search Tree.
    """
    def __init__(self, *args) -> None:
        self.Root = None
        # Initialize the tree with a sequence if provided, don't modify the init
        if len(args) == 1:
            if isinstance(args[0],collections.Iterable):
                for x in args[0]:
                    self.insert(x[0],x[1])
            else:
                raise TypeError(str(args[0]) + " is not iterable")

    def insert(self, student_id, name, GPA) -> None:
        """
        Inserts a new Student into the tree.
        """

        # Create the Student object using input provided
        student = Student(student_id, name, GPA)

        # If a root node doesn't exist yet, make this student the root
        if not self.Root:
            self.Root = student
        # Else traverse the tree to find a place for the new student (based on student's ID)
        else:
            # Store the current node being check in a variable
            current_node = self.Root

            while True:
                # If the new student's ID is less than the current node's student ID
                if student.student_id < current_node.student_id:
                    # If the current node has no left child, place the new student there
                    if not current_node.left:
                        current_node.left = student
                        student.parent = current_node
                        break
                    # Else set current_node to the left child of the current node
                    else:
                        current_node = current_node.left
                # If the new student's ID is more than the current node's student ID
                elif student.student_id > current_node.student_id:
                    # If the current node has no right child, place the new student there
                    if not current_node.right:
                        current_node.right = student
                        student.parent = current_node
                        break
                    # Else set current_node to the right child of the current node
                    else:
                        current_node = current_node.right
                # If student ID already exists, ignore it
                elif student.student_id == current_node.student_id:
                    break

    def search(self, student_id) -> Student:
        """
        Searches for a student by student_id.
        """
        # If the tree is empty, return None
        if not self.Root:
            return None
        # Else if it's a tree with a single node, return that node
        elif not self.Root.left and not self.Root.right:
            return self.Root
        
        # Create list to store result of preorder traversal
        preorder = []
        # Find the student and place them in the preorder list
        BSTree.find_student(self.Root, student_id, preorder)
        # If student found (list is not empty), return them
        if preorder:
            return preorder[0]
        else:
            return None

    def delete(self, student_id) -> None:
        """
        Deletes a student from the tree by student_id.
        """
         # If the tree is empty
        if not self.Root:
            return
        # If tree has more than one node, find the student
        else:
            # Create list to store result of preorder traversal
            preorder = []
            # Find the student and place them in the preorder list
            BSTree.find_student(self.Root, student_id, preorder)
            # If student not found, exit function
            if not preorder:
                return
            else:
                # Save the student to be deleted to a variable
                student = preorder[0]
        
        # If student is the root node and has no children
        if student == self.Root and not self.Root.left and not self.Root.right:
            self.Root = None
        # If student is the root node and has a left child only
        elif student == self.Root and self.Root.left and not self.Root.right:
            # Save the current root node to a variable
            old_root = self.Root
            # Set the root node as the left child of root
            self.Root = self.Root.left
            # Update the new root node's parent to None
            self.Root.parent = None
            # Set the old root node's left child to None
            old_root.left = None
        # If student is the root node and has a right child only
        elif student == self.Root and not self.Root.left and self.Root.right:
            # Save the current root node to a variable
            old_root = self.Root
            # Set the root node as the right child of root
            self.Root = self.Root.right
            # Update the new root node's parent to None
            self.Root.parent = None
            # Set the old root node's right child to None
            old_root.right = None
        # If student is not the root node and has no children
        elif student is not self.Root and not student.left and not student.right:
            # Update the student's parent's child attribute
            # If student is the left child of its parent
            if student == student.parent.left:
                student.parent.left = None
            # If student is the right child of its parent
            else:
                student.parent.right = None
            
            # Set the student's parent to None
            student.parent = None
        # If student is not the root node and has a left child only
        elif student is not self.Root and student.left and not student.right:
            # Update the parent for the student's child
            student.left.parent = student.parent

            # Update the student's parent's child atrribute
            # If student is the left child of its parent
            if student == student.parent.left:
                student.parent.left = student.left
            # If student is the right child of its parent
            else:
                student.parent.right = student.left

            # Set the student's parent and left child to None
            student.parent = None
            student.left = None
        # If student is the root node and has a right child only
        elif student is not self.Root and not student.left and student.right:
            # Update the parent for the student's child
            student.right.parent = student.parent
            
            # Update the student's parent's child atrribute
            # If student is the left child of its parent
            if student == student.parent.left:
                student.parent.left = student.right
            # If student is the right child of its parent
            else:
                student.parent.right = student.right
            
            # Set the student's parent and right child to None
            student.parent = None
            student.right = None
        # If student has two children
        else:
            # Create list to store result of inorder traversal
            inorder = []
            # Populate inorder list
            BSTree.inorder_traversal(self.Root, inorder)
            
            # Find the next student after student in the tree
            for i in range(len(inorder)):
                if inorder[i] == student:
                    next_student = inorder[i+1]
                    break

            # If next_student is not the right child of student (since if it was, then next_student has no left children and it would just take student's place = the code after if statement)
            if student.right != next_student:
                # If next_student has a right child, link it with next_student's parent
                if next_student.right:
                    next_student.right.parent = next_student.parent
                    next_student.parent.left = next_student.right
                # Else set next_student's parent's left child to None
                else:
                    next_student.parent.left = None

                # Update next_student's right child to student's right child
                next_student.right = student.right
                # Update the new right child's parent attribute to next_student
                next_student.right.parent = next_student
                
            # Update next_student's left child to student's left child
            next_student.left = student.left
            # Update the new left child's parent attribute to next_student
            next_student.left.parent = next_student
            # Update next_student's parent to student's parent
            next_student.parent = student.parent

            # If student is not the root node
            if student is not self.Root:
                # Update the student's parent's child atrribute
                # If student is the left child of its parent, make next_student the left child instead
                if student == student.parent.left:
                    student.parent.left = next_student
                # If student is the right child of its parent, make next_student the right child instead
                else:
                    student.parent.right = next_student
                # Set the student's parent to None
                student.parent = None
            # If student is the root node
            else:
                # Update root node to next_student
                self.Root = next_student

            # Set the student's left child and right child to None
            student.left = None
            student.right = None

    def update_gpa(self, student_id, new_gpa) -> None:
        """
        Updates the GPA of a student.
        """
        # If tree is not empty
        if self.Root:
            # Create list to store result of preorder traversal
            preorder = []
            # Find the student and place them in the preorder list
            BSTree.find_student(self.Root, student_id, preorder)
            # If student found, update the student's gpa
            if preorder:
                preorder[0].GPA = new_gpa

    def update_name(self, student_id, new_name) -> None:
        """
        Updates the name of a student.
        """
        # If tree is not empty
        if self.Root:
            # Create list to store result of preorder traversal
            preorder = []
            # Find the student and place them in the preorder list
            BSTree.find_student(self.Root, student_id, preorder)
            # If student found, update the student's name
            if preorder:
                preorder[0].name = new_name

    def update_student_id(self, old_id, new_id) -> None:
        """
        Updates the student ID. This requires special handling to maintain tree structure.
        """
        # If tree is not empty
        if self.Root:
            # Create list to store result of preorder traversal
            preorder = []
            # Find the student and place them in the preorder list
            BSTree.find_student(self.Root, old_id, preorder)
            # If student found, update the student's ID
            if preorder:
                preorder[0].student_id = new_id

    def generate_report(self, student_id) -> str:
        """
        Generates a full report for a student.
        In the format of: Student ID: {student_id}, Name: {student.name}, GPA: {student.GPA}
        Otherwsie, prints: No student found with ID {student_id}
        """
        # If the tree is empty
        if not self.Root:
            return f"No student found with ID {student_id}"
        # If tree has more than one node, find the student
        else:
            # Create list to store result of preorder traversal
            preorder = []
            # Find the student and place them in the preorder list
            BSTree.find_student(self.Root, student_id, preorder)
            # If student found
            if preorder:
                return f"Student ID: {preorder[0].student_id}, Name: {preorder[0].name}, GPA: {preorder[0].GPA}"
            # If student not found
            else:
                return f"No student found with ID {student_id}"

    def find_max_gpa(self) -> float:
        """
        Finds the maximum GPA in the tree.
        """
        # If the tree is empty, return an empty list
        if not self.Root:
            return 0.0
        # Else if it's a tree with a single node, return a list containing that node
        elif not self.Root.left and not self.Root.right:
            return self.Root.GPA
        
        # Create list to store result of inorder traversal
        inorder = []
        # Populate inorder list
        BSTree.inorder_traversal(self.Root, inorder)
        # Create variable to store max gpa and set it to the first gpa in the list
        max_gpa = inorder[0].GPA
        # Find max gpa
        for i in inorder:
            if i.GPA > max_gpa:
                max_gpa = i.GPA

        return max_gpa

    def find_min_gpa(self) -> float:
        """
        Finds the minimum GPA in the tree.
        """
        # If the tree is empty, return an empty list
        if not self.Root:
            return 0.0
        # Else if it's a tree with a single node, return a list containing that node
        elif not self.Root.left and not self.Root.right:
            return self.Root.GPA
        
        # Create list to store result of inorder traversal
        inorder = []
        # Populate inorder list
        BSTree.inorder_traversal(self.Root, inorder)
        # Create variable to store min gpa and set it to the first gpa in the list
        min_gpa = inorder[0].GPA
        # Find min gpa
        for i in inorder:
            if i.GPA < min_gpa:
                min_gpa = i.GPA

        return min_gpa

    def levelorder(self, level=None) -> list:
        """
        Performs a level order traversal of the tree. If level is specified, returns all nodes at that level.
        """
        # Used to store all elements of binary tree in level order
        level_order = []
    
        # If the tree is empty, return an empty list
        if not self.Root:
            return level_order
        
        # Create a variable to keep track of the levels as we iterate through the tree
        level_count = 0
        
        # Stores the next level of nodes to be checked
        next_level = [self.Root]
    
        # While next_level is not empty
        while next_level:
            # Create a list to store the current level of nodes
            current_level = []
            
            # Iterate over each node in next_level
            for i in range(len(next_level), 0, -1):
                # Insert first node
                current_level.append(next_level.pop(0))
                
                # Check if left child exists and place them in next level
                if current_level[-1].left:
                    next_level.append(current_level[-1].left)
                # Check if right child exists and place them in next_level
                if current_level[-1].right:
                    next_level.append(current_level[-1].right)
                    
            for i in current_level:
                print(f"level {level_count}: {i.student_id}")
            
            # If all levels needed (no level specified), add the current_level nodes to level_order list
            if level is None:
                for i in current_level:
                    level_order.append(i)
            # If level specified by user
            else:
                # Check if current level_count equals the level specified by user
                if level == level_count:
                    # Return the current_level nodes
                    return current_level
                else:
                    level_count += 1
    
        return level_order

    def inorder(self) -> list:
        """
        Performs an in-order traversal of the tree.
        """
        # If the tree is empty, then return an empty list
        if not self.Root:
            return []
        # Else if it's a tree with a single node, return a list containing that node
        elif not self.Root.left and not self.Root.right:
            return [self.Root]
        
        # Create list to store result of inorder traversal
        inorder = []
        
        # Populate inorder list
        BSTree.inorder_traversal(self.Root, inorder)
        
        return inorder

    def is_valid(self) -> bool:
        """
        Checks if the tree is a valid Binary Search Tree. 
        Returns True if it is a valid BST; returns False or raises an Exception otherwise.
        """
         # If the tree is empty or if it's a tree with a single node, return True
        if not self.Root or (not self.Root.left and not self.Root.right):
            return True
        
        # Create list to store result of inorder traversal
        inorder = []
        # Populate inorder list
        BSTree.inorder_traversal(self.Root, inorder)
        # Check that the inorder traversal returned a sorted list
        # If so, then binary tree is valid -> abides by the rule: left-child < parent < right-child
        for i in range(len(inorder) - 1):
            if inorder[i].student_id > inorder[i+1].student_id:
                return False

        return True

    # Does and in-order traversal and populates list inorder
    def inorder_traversal(node, inorder) -> None:
        # If left child exists
        if node.left:
            # Recursion on the left child
            BSTree.inorder_traversal(node.left, inorder)

        # Append the node to list inorder
        inorder.append(node)

        # If right child exists
        if node.right:
            # Recursion on the right child
            BSTree.inorder_traversal(node.right, inorder)

    # Does a pre-order traversal and finds a student by their student ID
    def find_student(node, student_id, preorder) -> None:
        # If node is none, return    
        if not node:
            return
        # If node id matches student_id, append the node to preorder list
        elif node.student_id == student_id:
            preorder.append(node)
        else:
            # If left child exists
            if node.left:
                # Recursion on the left child
                BSTree.find_student(node.left, student_id, preorder)
            # If right child exists
            if node.right:
                # Recursion on the right child
                BSTree.find_student(node.right, student_id, preorder)
                
def main():
    # Create the Tree Object
    bst = BSTree()
    # Create a variable to store menu option
    option = None    

    # Main menu
    while option != '0':
        # Prompt user for menu option and check for valid selection
        while True:
            option = input("\nPlease select an option:\n1. Insert\n2. Search\n3. Delete\n4. Update GPA\n5. Update Name\n6. Update Student ID\n\
7. Generate Report\n8. Find Max GPA\n9. Find Min GPA\n10. Level-Order Traversal\n11. In-Order Traversal\n12. Tree Valid\n0. Exit\n")
            if option.isdigit():
                if int(option) >= 0 and int(option) <= 12:
                    break
            else:
                print("Please enter a valid option!\n")

        if option == '1':
            student_id = int(input("Please enter student ID: "))
            name = input("Please enter student name: ")
            gpa = float(input("Please enter student gpa: "))
            bst.insert(student_id, name, gpa)
        elif option == '2':
            student_id = int(input("Please enter student ID: "))
            student = bst.search(student_id)
            print(f"student_id: {student.student_id}, name: {student.name}, gpa: {student.GPA}")
        elif option == '3':
            student_id = int(input("Please enter student ID: "))
            bst.delete(student_id)
        elif option == '4':
            student_id = int(input("Please enter student ID: "))
            gpa = float(input("Please enter new gpa: "))
            bst.update_gpa(student_id, gpa)
        elif option == '5':
            student_id = int(input("Please enter student ID: "))
            name = input("Please enter new name: ")
            bst.update_name(student_id, name)
        elif option == '6':
            student_id = int(input("Please enter student ID: "))
            new_id = int(input("Please enter new ID: "))
            bst.update_student_id(student_id, new_id)
        elif option == '7':
            student_id = int(input("Please enter student ID: "))
            print(bst.generate_report(student_id))
        elif option == '8':
            print(bst.find_max_gpa())
        elif option == '9':
            print(bst.find_min_gpa())
        elif option == '10':
            try:
                level = int(input("Please enter level number: "))
            except:
                level = None
                
            for i in bst.levelorder(level):
                print(i.student_id)
        elif option == '11':
            for i in bst.inorder():
                print(i.student_id)
        elif option == '12':
            if bst.is_valid():
                print("Tree is valid.")
            else:
                print("Tree is not valid!")
    

if __name__ == '__main__':
    main()
    