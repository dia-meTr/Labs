from tree import Tree
from anytree import Node
from random import random

'''
    The class "Nim" is our program's main class that contains all the game logic and UI elements
'''
class Nim:
    '''
        initialise Nim instance and set all variables to default and launch the game
    '''
    def __init__(self):
        self.number_of_sticks: int = None
        self.isPlayerFirst: bool = None
        self.tree: Tree = None
        self.isCurrentPlayer: bool = None
        self.isAlgoMinMax: bool = None
        self.play()

    # main game function that calls the ui elements, creates the game tree and shows result
    def play(self):
        self.show_insert_number_of_stick()
        self.show_Algorithm_choice()
        self.show_turn_choice()
        self.creating_tree()
        current_node = self.tree.rootNode   
        while not current_node.is_leaf:
            if not self.available_moving_point(current_node):
                break
            if self.isCurrentPlayer:
                current_node = self.get_human_moving_choice(current_node)
            else:
                current_node = self.get_comp_moving_choice(current_node)
            self.isCurrentPlayer = not self.isCurrentPlayer
        self.show_winner()
        self.show_rendered_tree()

    # show the possible routes from the current situation
    def available_moving_point(self, current_node):
        #print("_________________________________________________")
        print("\n\t\t\t It's"+(" YOUR" if self.isCurrentPlayer else " the COMPUTER's") + " TURN")
        #print("_________________________________________________")
        print("Available Moving Point(s)")
        for index, child in enumerate(current_node.children):
            if current_node.is_leaf:
                print("\nThere are no available moving point T____T", end="")
                return False
            else:
                print(str(index + 1) + ". [" + ("-".join(map(str, child.node_value))) + "]")
        print("")
        return True

    # Computer choice making
    def get_comp_moving_choice(self, current_node):
        choice_child = self.check_comp_moving_choice(current_node)
        print("Computer move\t: [" + ("-".join(map(str, choice_child.node_value))) + "]")
        return choice_child

    # Computer different choice checking to select the optimal one
    def check_comp_moving_choice(self, current_node) -> Node:
        is_comp_max = not self.isPlayerFirst
        child_choice = current_node.children[0]
        for child in current_node.children:
            if child.evaluator_value:
                if (is_comp_max and (child.evaluator_value > child_choice.evaluator_value)) or (
                        not is_comp_max and (child.evaluator_value < child_choice.evaluator_value)):
                    child_choice = child
        return child_choice

    # User choice making
    @staticmethod
    def get_human_moving_choice(current_node):
        while True:
            moving_choice = int(input("Choose your move\t: "))
            if moving_choice - 1 in range(0, len(current_node.children)):
                child = current_node.children[moving_choice - 1]
                print("Your move\t\t: [" + ("-".join(map(str, child.node_value))) + "]")
                return child
            print("Invalid move\n")


    # Input number of sticks to play with
    def show_insert_number_of_stick(self):
        while True:
            self.number_of_sticks = int(input("Insert number of sticks\t: "))
            if self.number_of_sticks > 0:
                break
            print("Must be positive.\n")

    # Choose Algorithm: MiniMax or Alpha-Beta
    def show_Algorithm_choice(self):
        print("\nChoose Algorithm:")
        print("1. MiniMax")
        print("2. Alpha Beta\n")
        while True:
            choice = int(input("Choose the computer's Algorithm\t: "))
            if choice in range(1, 3):
                self.isAlgoMinMax = (choice == 1)
                break
            print("Invalid Choice.\n")

    # Randomly choose first player (user or computer)
    def show_turn_choice(self):
        self.isPlayerFirst = True if random() >= 0.5 else False
        print("\n\t\t"+(" YOU are" if self.isPlayerFirst else " COMPUTER is") + " the FIRST player\n")
    # Creating instance from Class Tree with the chosen parameters
    def creating_tree(self):
        self.tree = Tree(self.number_of_sticks, self.isPlayerFirst,self.isAlgoMinMax)
        print("Tree created.")
        self.isCurrentPlayer = self.isPlayerFirst

    # Print the obtained tree (UI)
    def show_rendered_tree(self):
        print("Nodes Visited: " + str(self.tree.nodesVisited))
        is_show_tree = input("View rendered tree [y/n]? ")
        if is_show_tree.capitalize() == "Y":
            print("First player is: "+("YOU" if self.isPlayerFirst else "the COMPUTER"))
            print(str(self.tree))

    # Printing winner (user or computer)
    def show_winner(self):
        print("\t\t\t"+(" You WIN !!!" if not self.isCurrentPlayer else " The Computer WINS !"))
        self.isCurrentPlayer = not self.isCurrentPlayer
        print("\t\t\t"+(" You lose :( " if not self.isCurrentPlayer else "The Computer LOSES :) "))



# Start the Program
if __name__ == '__main__':
    Nim()
