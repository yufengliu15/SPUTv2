from sympy import *
import math

L1 = 60
L2 = 110
L3 = 5
L4 = 120

def derive_fk():
    # theta1, theta2, theta3
    t1,t2,t3 = symbols("theta1,theta2,theta3")
    l1,l2,l3,l4 = symbols("l1,l2,l3,l4")

    matrix_0_to_1 = Matrix([[cos(t1), -sin(t1), 0,0], [sin(t1), cos(t1), 0,0], [0,0,1,0], [0,0,0,1]])
    matrix_1_to_2 = Matrix([[cos(t2), -sin(t2), 0, 0], [0,0,1,-l1], [-sin(t2), -cos(t2),0,0], [0,0,0,1]])
    matrix_2_to_3 = Matrix([[cos(t3), -sin(t3), 0, l2], [sin(t3),cos(t3),0,0], [0,0,1,-l3], [0,0,0,1]])
    matrix_3_to_4 = Matrix([[1,0,0,l4], [0,1,0,0], [0,0,1,0], [0,0,0,1]])

    mult_matrices = matrix_0_to_1 * matrix_1_to_2 * matrix_2_to_3 * matrix_3_to_4
    mult_matrices.row_del(3)
    body_frame = trigsimp(mult_matrices.col(-1))

    # matrix_0_to_2 = matrix_0_to_1 * matrix_1_to_2
    # matrix_0_to_2.row_del(3)
    # print(f"hip pitch: {trigsimp(matrix_0_to_2.col(-1))}")
    # hip pitch:
    # return trigsimp(matrix_0_to_2.col(-1))}
    
    # matrix_0_to_3 = matrix_0_to_1 * matrix_1_to_2 * matrix_2_to_3
    # matrix_0_to_3.row_del(3)
    # print(f"knee: {trigsimp(matrix_0_to_3.col(-1))}")
    # knee:
    # return trigsimp(matrix_0_to_3.col(-1))}

    # from hiproll to end effector
    f = lambdify([t1, t2, t3, l1, l2, l3, l4], body_frame, modules="numpy")
    return f

def deg_to_radians(degree):
    return degree * (math.pi / 180)

def radians_to_deg(radian):
    return radian * (180 / math.pi)

def fk(_theta1, _theta2, _theta3, body_frame):
    return body_frame(_theta1, _theta2, _theta3, L1, L2, L3, L4)

# returns expressions needed for IK
def derive_ik():
    x0,y0,z0 = symbols("x0,y0,z0")
    l1,l2,l3,l4 = symbols("l1,l2,l3,l4")
    
    sqr_A = x0**2 + y0**2 - (l1 + l3)**2
    A = sqrt(sqr_A)
    sqr_D = sqr_A + z0**2
    D = sqrt(sqr_D)
    
    t3_check = (l2**2 + l4**2 - sqr_D)/(2*l2*l4)
    t2_check = (l2**2+sqr_D-l4**2)/(2*l2*D)
    t3 = math.pi - acos(t3_check)
    t2 = -atan2(z0,A) - acos(t2_check)
    t1 = atan2(y0,x0) - atan2(-(l1+l3), A)
    
    return t1,t2,t3,sqr_A,t2_check,t3_check

# returns servo angles in radians (theta1,theta2,theta3) or throws a ValueError if target coordinates is unreachable
def ik(x0,y0,z0):
    t1,t2,t3,sqr_A,t2_check,t3_check = derive_ik()
    t2_arccos_res = t2_check.subs({"x0": x0, "y0": y0, "z0": z0, "l1": L1, "l2": L2, "l3": L3, "l4": L4}).evalf()
    t3_arccos_res = t3_check.subs({"x0": x0, "y0": y0, "z0": z0, "l1": L1, "l2": L2, "l3": L3, "l4": L4}).evalf()
    if (sqr_A.subs({"x0": x0, "y0": y0, "l1": L1, "l3": L3}).evalf() < 0) or (t2_arccos_res > 1 or t2_arccos_res < -1) or (t3_arccos_res > 1 or t3_arccos_res < -1):
        raise ValueError("Provided x,y,z coordinates cannot be reached.")    
    
    final_t1 = t1.subs({"y0": y0, "x0": x0, "l1": L1, "l3":L3}).evalf()
    final_t2 = t2.subs({"x0": x0, "y0": y0, "z0": z0, "l1": L1, "l2": L2, "l3": L3, "l4": L4}).evalf()
    final_t3 = t3.subs({"x0": x0, "y0": y0, "z0": z0, "l1": L1, "l2": L2, "l3": L3, "l4": L4}).evalf()
    return float(final_t1), float(final_t2), float(final_t3)

theta1 = deg_to_radians(0)
theta2 = deg_to_radians(0)
theta3 = deg_to_radians(0)
body_frame = derive_fk()
x0 = 230
y0 = -65
z0 = 0


t1,t2,t3 = ik(168.462451,-49.3653681,-132.56512)
print(radians_to_deg(t1), radians_to_deg(t2), radians_to_deg(t3))
# print(fk(t1,t2,t3,body_frame))