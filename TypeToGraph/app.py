from displaying.display import GraphDisplayer
from graph import tree
from pprint import pprint

if __name__ == '__main__':
    displayer = GraphDisplayer()
    my_tree = tree.BinaryTree(3)

    my_tree.insert(7)
    my_tree.insert(2)
    my_tree.insert(3)
    my_tree.insert(12)
    my_tree.insert(7)
    my_tree.insert(3)
    my_tree.insert(4)
    
    displayer.display(my_tree, 'BinaryTree', True)