from displaying.display import GraphDisplayer
from graph import tree
from pprint import pprint

if __name__ == '__main__':
    displayer = GraphDisplayer()
    my_tree = tree.DateBasedNoteTree()

    # AI Test Data

    # Root notes
    note1 = my_tree.add_note('Root 1', 'Author A')
    note2 = my_tree.add_note('Root 2', 'Author B')
    note3 = my_tree.add_note('Root 3', 'Author C')

    # Children for note1
    child1_1 = my_tree.add_note('Child 1-1', 'Author D')
    child1_2 = my_tree.add_note('Child 1-2', 'Author E')
    note1.add_note_as_child(child1_1)
    note1.add_note_as_child(child1_2)

    # Children for note2
    child2_1 = my_tree.add_note('Child 2-1', 'Author F')
    child2_2 = my_tree.add_note('Child 2-2', 'Author G')
    note2.add_note_as_child(child2_1)
    note2.add_note_as_child(child2_2)

    # Children for note3
    child3_1 = my_tree.add_note('Child 3-1', 'Author H')
    child3_2 = my_tree.add_note('Child 3-2', 'Author I')
    note3.add_note_as_child(child3_1)
    note3.add_note_as_child(child3_2)

    # Grandchildren for child1_1
    grandchild1_1_1 = my_tree.add_note('Grandchild 1-1-1', 'Author J')
    grandchild1_1_2 = my_tree.add_note('Grandchild 1-1-2', 'Author K')
    child1_1.add_note_as_child(grandchild1_1_1)
    child1_1.add_note_as_child(grandchild1_1_2)

    # Grandchildren for child2_2
    grandchild2_2_1 = my_tree.add_note('Grandchild 2-2-1', 'Author L')
    child2_2.add_note_as_child(grandchild2_2_1)

    # Add more notes for variety
    extra1 = my_tree.add_note('Extra Note 1', 'Author M')
    extra2 = my_tree.add_note('Extra Note 2', 'Author N')
    note1.add_note_as_child(extra1)
    child3_2.add_note_as_child(extra2)

    # Display the tree
    displayer.display(my_tree, 'DateBasedNodeTree', True)