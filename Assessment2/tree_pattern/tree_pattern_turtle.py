from turtle import *

# User inputs to make tree pattern
left_angle = float(input("Left branch angle: "))
right_angle = float(input("Right branch angle: "))
start_branch_lenght = float(input("Starting branch length: "))
recursion_depth = int(input("Recursion depth: "))
branch_reduction_factor = float(input("Branch length reduction factor(1-100): "))/100

# create and setup turtle
t = Turtle()
t.speed("fastest")
t.left(90)

# recursive function to draw tree pattern
def tree_pattern(t, start_branch_lenght, left_angle, right_angle, depth, reduction_factor, is_stem=True):
    if depth == 0 or start_branch_lenght < 1:
        return

    t.color("red" if is_stem else "green")
    t.pensize(3 if is_stem else 1)

    t.forward(start_branch_lenght)
    t.left(left_angle)

    tree_pattern(t, start_branch_lenght * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor, False)
    t.right(left_angle + right_angle)

    tree_pattern(t, start_branch_lenght * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor, False)
    
    t.left(right_angle)
    t.backward(start_branch_lenght)


if __name__ == "__main__":
    # Draw tree
    tree_pattern(t, start_branch_lenght, left_angle, right_angle, recursion_depth, branch_reduction_factor)
    done()

'''
To draw the tree pattern like in the assesment, please give the following inputs:
Left branch angle: 25
Right branch angle: 20
Starting branch length: 100
Recursion depth: 5
Branch length reduction factor(1-100): 70
'''