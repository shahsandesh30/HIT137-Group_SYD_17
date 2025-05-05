import turtle as trl

def draw_branch(length, recursion_depth, max_depth, angle_left, angle_right, reduction_factor):
    if recursion_depth == 0 or length < 2:
        return

    # Color and thickness based on recursion depth
    # Set brown color for main stem and green for other branches
    if recursion_depth == max_depth:
        trl.color("brown")
        trl.pensize(length/10)
    else:
        trl.color("green")
        trl.pensize(length / 10)

    trl.forward(length)

    # Save location and the direction of the turtle
    position = trl.position()
    heading = trl.heading()

    # Left branch
    trl.left(angle_left)
    draw_branch(length * reduction_factor, recursion_depth - 1, max_depth, angle_left, angle_right, reduction_factor)

    # go back to the previous location followed by direction 
    trl.setposition(position)
    trl.setheading(heading)

    # Right branch
    trl.right(angle_right)
    draw_branch(length * reduction_factor, recursion_depth - 1, max_depth, angle_left, angle_right, reduction_factor)

    # Return to the previous location
    trl.setposition(position)
    trl.setheading(heading)

# === User Inputs ===
angle_left = float(input("Enter left branch angle (e.g. 20): "))
angle_right = float(input("Enter right branch angle (e.g. 25): "))
start_length = float(input("Enter starting branch length (e.g. 100): "))
recursion_depth = int(input("Enter recursion depth (e.g. 5): "))
reduction_factor = float(input("Enter branch length reduction factor (e.g. 0.7): "))

# === Setup Turtle ===
trl.speed("fastest")
trl.left(90)
trl.penup()
trl.goto(0, -250)
trl.pendown()

# === Start Recursive Tree ===
draw_branch(start_length, recursion_depth, recursion_depth, angle_left, angle_right, reduction_factor)

trl.done()


'''To get the desired result from the code enter values as advised'''