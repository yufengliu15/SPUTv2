from sympy import *

# theta1, theta2, theta3
t1,t2,t3 = symbols("theta1,theta2,theta3")
l1,l2,l3,l4 = symbols("l1,l2,l3,l4")

matrix_1_to_2 = Matrix([[cos(t2), -sin(t2), 0, 0], [0,0,1,-l1], [-sin(t2), -cos(t2),0,0], [0,0,0,1]])
matrix_0_to_1 = Matrix([[cos(t1), -sin(t1), 0,0], [sin(t1), cos(t1), 0,0], [0,0,1,0], [0,0,0,1]])
matrix_2_to_3 = Matrix([[cos(t3), -sin(t3), 0, l2], [sin(t3),cos(t3),0,0], [0,0,1,-l3], [0,0,0,1]])
matrix_3_to_4 = Matrix([[1,0,0,l4], [0,1,0,0], [0,0,1,0], [0,0,0,1]])

mult_matrices = matrix_0_to_1 * matrix_1_to_2 * matrix_2_to_3 * matrix_3_to_4
mult_matrices.row_del(3)
body_frame = trigsimp(mult_matrices.col(-1))

matrix_0_to_2 = matrix_0_to_1 * matrix_1_to_2
matrix_0_to_2.row_del(3)
print(f"hip pitch: {trigsimp(matrix_0_to_2.col(-1))}")

matrix_0_to_3 = matrix_0_to_1 * matrix_1_to_2 * matrix_2_to_3
matrix_0_to_3.row_del(3)
print(f"knee: {trigsimp(matrix_0_to_3.col(-1))}")

# zero pose
print(f"body_frame: {body_frame}")

