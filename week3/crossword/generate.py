import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
         The enforce_node_consistency function should update self.domains such that each variable is node consistent.

        Recall that node consistency is achieved when, for every variable, each value in its domain is consistent with the variable’s unary constraints. In the case of a crossword puzzle, this means making sure that every value in a variable’s domain has the same number of letters as the variable’s length.
        To remove a value x from the domain of a variable v, since self.domains is a dictionary mapping variables to sets of values, you can call self.domains[v].remove(x).
        No return value is necessary for this function.
        """
        print("In enforce_node_consistency")
        print(self.domains)
        for variable in self.crossword.variables:
            for word in self.crossword.words:
                if len(word) != variable.length:
                    print("Removing word: ", word , " from variable: ", variable)
                    self.domains[variable].remove(word)
        print(self.domains)



    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        The revise function should make the variable x arc consistent with the variable y.

        x and y will both be Variable objects representing variables in the puzzle.
        Recall that x is arc consistent with y when every value in the domain of x has a possible value in the domain of y that does not cause a conflict. (A conflict in the context of the crossword puzzle is a square for which two variables disagree on what character value it should take on.)
        To make x arc consistent with y, you’ll want to remove any value from the domain of x that does not have a corresponding possible value in the domain of y.
        Recall that you can access self.crossword.overlaps to get the overlap, if any, between two variables.
        The domain of y should be left unmodified.
        The function should return True if a revision was made to the domain of x; it should return False if no revision was made.
        """
        print()
        print("In revise")
        revised = False
        to_remove = set()
        print("x: ", x, " y: ", y)
        if self.crossword.overlaps[x,y] is not None:
            print("Overlaps: ", self.crossword.overlaps[x,y])
            (i,j) = self.crossword.overlaps[x,y]
            for word_var1 in self.domains[x]:
                for word_var2 in self.domains[y]:
                    print("Comparing: ", word_var1, word_var2)
                    if word_var1[i] == word_var2[j]:
                        if word_var1 in to_remove:
                            to_remove.remove(word_var1)
                        break
                    else:
                        print("Removing word: ", word_var1)
                        to_remove.add(word_var1)
            for word in to_remove:
                print("Removing word: ", word, " from variable: ", x)
                revised = True
                self.domains[x].remove(word)
        print("Revised: ", revised)
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        The ac3 function should, using the AC3 algorithm, enforce arc consistency on the problem. Recall that arc consistency is achieved when all the values in each variable’s domain satisfy that variable’s binary constraints.

        Recall that the AC3 algorithm maintains a queue of arcs to process. This function takes an optional argument called arcs, representing an initial list of arcs to process. If arcs is None, your function should start with an initial queue of all of the arcs in the problem. Otherwise, your algorithm should begin with an initial queue of only the arcs that are in the list arcs (where each arc is a tuple (x, y) of a variable x and a different variable y).
        Recall that to implement AC3, you’ll revise each arc in the queue one at a time. Any time you make a change to a domain, though, you may need to add additional arcs to your queue to ensure that other arcs stay consistent.
        You may find it helpful to call on the revise function in your implementation of ac3.
        If, in the process of enforcing arc consistency, you remove all of the remaining values from a domain, return False (this means it’s impossible to solve the problem, since there are no more possible values for the variable). Otherwise, return True.
        You do not need to worry about enforcing word uniqueness in this function (you’ll implement that check in the consistent function.)
        """
        print()
        print()
        print("In ac3")
        if arcs is None:
            print("Arcs is None")
            arcs = []
            for var1 in self.crossword.variables:
                for var2 in self.crossword.variables:
                    if var1 != var2:
                        print("Adding arc: ", var1, var2)
                        arcs.append((var1,var2))
        while len(arcs) > 0:
            var1, var2 = arcs.pop(0)
            print(self.domains[var1])
            if self.revise(var1,var2):
                print(self.domains[var1])
                if len(self.domains[var1]) == 0:
                    print("Returning False")
                    return False
                for var3 in self.crossword.variables:
                    if var3 != var1:
                        print("Adding arc: ", var3, var1)
                        arcs.append((var3,var1))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        The assignment_complete function should (as the name suggests) check to see if a given assignment is complete.

        An assignment is a dictionary where the keys are Variable objects and the values are strings representing the words those variables will take on.
        An assignment is complete if every crossword variable is assigned to a value (regardless of what that value is).
        The function should return True if the assignment is complete and return False otherwise.
        """
        print()
        print()
        print("In assignment_complete")
        for var in self.crossword.variables:
            print("Var: ", var)
            if var not in assignment.keys() or assignment[var] == None:
                if var not in assignment.keys():
                    print("var not in assignment.keys()")
                elif assignment[var] == None:
                    print("assignment[var] == None")
                print("Returning False")
                return False
        print("Returning True")
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        The consistent function should check to see if a given assignment is consistent.

        An assignment is a dictionary where the keys are Variable objects and the values are strings representing the words those variables will take on. Note that the assignment may not be complete: not all variables will necessarily be present in the assignment.
        An assignment is consistent if it satisfies all of the constraints of the problem: 
        that is to say, all values are distinct, every value is the correct length, and there are no conflicts between neighboring variables.
        The function should return True if the assignment is consistent and return False otherwise.
        """
        print()
        print()
        print("In consistent")
        is_consistent = True
        is_consistent = self.assignment_complete(assignment)
        if is_consistent is False:
            for var1 in assignment:
              for var2 in assignment:
                if var1 != var2:
                    if var1.length != len(assignment[var1]) or var2.length != len(assignment[var2]):
                        return False
                    else:
                        if self.crossword.overlaps[var1,var2] is not None:
                            i,j = self.crossword.overlaps[var1,var2]
                            if assignment[var1][i] != assignment[var2][j]:
                                return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        The order_domain_values function should return a list of all of the values in the domain of var, ordered according to the least-constraining values heuristic.

        var will be a Variable object, representing a variable in the puzzle.
        Recall that the least-constraining values heuristic is computed as the number of values ruled out for neighboring unassigned variables. That is to say, if assigning var to a particular value results in eliminating n possible choices for neighboring variables, you should order your results in ascending order of n.
        Note that any variable present in assignment already has a value, and therefore shouldn’t be counted when computing the number of values ruled out for neighboring unassigned variables.
        For domain values that eliminate the same number of possible choices for neighboring variables, any ordering is acceptable.
        Recall that you can access self.crossword.overlaps to get the overlap, if any, between two variables.
        It may be helpful to first implement this function by returning a list of values in any arbitrary order (which should still generate correct crossword puzzles). Once your algorithm is working, you can then go back and ensure that the values are returned in the correct order.
        You may find it helpful to sort a list according to a particular key: Python contains some helpful functions for achieving this.
        """
        print("In order_domain_values")
        return list(self.domains[var])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.

        The select_unassigned_variable function should return a single variable in the crossword puzzle that is not yet assigned by assignment, according to the minimum remaining value heuristic and then the degree heuristic.

        An assignment is a dictionary where the keys are Variable objects and the values are strings representing the words those variables will take on. You may assume that the assignment will not be complete: not all variables will be present in the assignment.
        Your function should return a Variable object. You should return the variable with the fewest number of remaining values in its domain. If there is a tie between variables, you should choose among whichever among those variables has the largest degree (has the most neighbors). If there is a tie in both cases, you may choose arbitrarily among tied variables.
        It may be helpful to first implement this function by returning any arbitrary unassigned variable (which should still generate correct crossword puzzles). Once your algorithm is working, you can then go back and ensure that you are returning a variable according to the heuristics.
        You may find it helpful to sort a list according to a particular key: Python contains some helpful functions for achieving this.
        """
        print("In select_unassigned_variable")
        unused_vars = []
        for var in self.crossword.variables:
            if var not in assignment:
                unused_vars.append(var)
        sorted_vars = sorted(unused_vars, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))
        if len(sorted_vars) > 0:
            return sorted_vars[0]
        return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.

        The backtrack function should accept a partial assignment assignment as input and, using backtracking search, return a complete satisfactory assignment of variables to values if it is possible to do so.

        An assignment is a dictionary where the keys are Variable objects and the values are strings representing the words those variables will take on. The input assignment may not be complete (not all variables will necessarily have values).
        If it is possible to generate a satisfactory crossword puzzle, your function should return the complete assignment: a dictionary where each variable is a key and the value is the word that the variable should take on. If no satisfying assignment is possible, the function should return None.
        If you would like, you may find that your algorithm is more efficient if you interleave search with inference (as by maintaining arc consistency every time you make a new assignment). You are not required to do this, but you are permitted to, so long as your function still produces correct results. (It is for this reason that the ac3 function allows an arcs argument, in case you’d like to start with a different queue of arcs.)
        """
        print()
        print()
        print("In backtrack")

        if len(assignment) == len(self.crossword.variables):
            print("Returning assignment")
            print(assignment)
            return assignment
        var = self.select_unassigned_variable(assignment)
        print("Var: ", var)
        for value in self.domains[var]:
            print("Value: ", value)
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None 
    
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
