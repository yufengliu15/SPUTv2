from sympy import *
import math

# Front-left leg, measured from spotmicroesp32_assembled_quick_and_dirty.FCStd (2026-11-18)
# Joint axes taken from the servo output shafts, cross-checked against the bearing pins.
A1 = 10.0     # roll axis -> pitch axis, height (pitch axis is below the roll axis), along x1
L1 = 60.6     # roll axis -> leg plane, sideways (along the pitch axis)
L2 = 111.1    # pitch axis -> knee axis (thigh)
L3 = 0.0      # knee sideways offset (thigh and shin share a plane, 0.4 mm apart)
L4 = 118.1    # knee axis -> foot-tip ball CENTRE (shin)
FOOT_RADIUS = 20.0  # foot-tip ball radius; ground contact is FOOT_RADIUS straight below the ball centre

LENGTHS = {"a1": A1, "l1": L1, "l2": L2, "l3": L3, "l4": L4}

def derive_fk():
    # theta1, theta2, theta3
    t1,t2,t3 = symbols("theta1,theta2,theta3")
    a1,l1,l2,l3,l4 = symbols("a1,l1,l2,l3,l4")

    # Craig DH rows:
    # 1: a0=0,  alpha0=0,   d1=0,   theta1
    # 2: a1=A1, alpha1=-90, d2=-L1, theta2
    # 3: a2=L2, alpha2=0,   d3=-L3, theta3
    # 4: a3=L4, alpha3=0,   d4=0,   theta4=0
    matrix_0_to_1 = Matrix([[cos(t1), -sin(t1), 0,0], [sin(t1), cos(t1), 0,0], [0,0,1,0], [0,0,0,1]])
    matrix_1_to_2 = Matrix([[cos(t2), -sin(t2), 0, a1], [0,0,1,-l1], [-sin(t2), -cos(t2),0,0], [0,0,0,1]])
    matrix_2_to_3 = Matrix([[cos(t3), -sin(t3), 0, l2], [sin(t3),cos(t3),0,0], [0,0,1,-l3], [0,0,0,1]])
    matrix_3_to_4 = Matrix([[1,0,0,l4], [0,1,0,0], [0,0,1,0], [0,0,0,1]])

    mult_matrices = matrix_0_to_1 * matrix_1_to_2 * matrix_2_to_3 * matrix_3_to_4
    mult_matrices.row_del(3)
    body_frame = trigsimp(mult_matrices.col(-1))

    # from hip roll to foot-tip ball centre
    f = lambdify([t1, t2, t3, a1, l1, l2, l3, l4], body_frame, modules="numpy")
    return f

def deg_to_radians(degree):
    return degree * (math.pi / 180)

def radians_to_deg(radian):
    return radian * (180 / math.pi)

def fk(_theta1, _theta2, _theta3, body_frame):
    return body_frame(_theta1, _theta2, _theta3, A1, L1, L2, L3, L4)

# returns expressions needed for IK
def derive_ik():
    x0,y0,z0 = symbols("x0,y0,z0")
    a1,l1,l2,l3,l4 = symbols("a1,l1,l2,l3,l4")

    # End-on view (down the roll axis): the foot sits (l1+l3) sideways and E "down" from the roll axis.
    # E = a1 + (thigh+shin reach), so the swing-plane reach is A = E - a1.
    sqr_E = x0**2 + y0**2 - (l1 + l3)**2
    E = sqrt(sqr_E)
    A = E - a1
    sqr_D = A**2 + z0**2
    D = sqrt(sqr_D)

    t3_check = (l2**2 + l4**2 - sqr_D)/(2*l2*l4)
    t2_check = (l2**2+sqr_D-l4**2)/(2*l2*D)
    t3 = math.pi - acos(t3_check)
    t2 = -atan2(z0,A) - acos(t2_check)
    t1 = atan2(y0,x0) - atan2(-(l1+l3), E)

    return t1,t2,t3,sqr_E,t2_check,t3_check

_IK = None

# returns servo angles in radians (theta1,theta2,theta3) for the foot-tip ball CENTRE at (x0,y0,z0) in frame {0}
# raises ValueError if the target cannot be reached
def ik(x0,y0,z0):
    global _IK
    if _IK is None:
        _IK = derive_ik()
    t1,t2,t3,sqr_E,t2_check,t3_check = _IK
    values = {"x0": x0, "y0": y0, "z0": z0, **LENGTHS}

    if sqr_E.subs(values).evalf() < 0:
        raise ValueError("Provided x,y,z coordinates cannot be reached.")
    t2_arccos_res = t2_check.subs(values).evalf()
    t3_arccos_res = t3_check.subs(values).evalf()
    if not (-1 <= t2_arccos_res <= 1) or not (-1 <= t3_arccos_res <= 1):
        raise ValueError("Provided x,y,z coordinates cannot be reached.")

    final_t1 = t1.subs(values).evalf()
    final_t2 = t2.subs(values).evalf()
    final_t3 = t3.subs(values).evalf()
    return float(final_t1), float(final_t2), float(final_t3)

# same as ik(), but (x0,y0,z0) is where the foot should touch the ground (body level, +x0 points down)
def ik_ground(x0,y0,z0):
    return ik(x0 - FOOT_RADIUS, y0, z0)

if __name__ == "__main__":
    body_frame = derive_fk()

    print("zero pose foot:", fk(0, 0, 0, body_frame).ravel())

    for pose in [(5.4, 14, 48), (-20, 30, 60), (15, -25, 90), (0, 0, 0)]:
        angles = [deg_to_radians(a) for a in pose]
        foot = fk(*angles, body_frame).ravel()
        back = [radians_to_deg(a) for a in ik(*foot)]
        ok = all(math.isclose(a, b, abs_tol=1e-4) for a, b in zip(pose, back))  # degrees; straight leg is numerically touchy
        print(pose, "->", [round(b, 4) for b in back], "OK" if ok else "MISMATCH")
