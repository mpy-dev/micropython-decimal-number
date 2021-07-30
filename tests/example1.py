from mpy_decimal.mpy_decimal import *


def solve_quadratic_equation(a: DecimalNumber, b: DecimalNumber, c: DecimalNumber) -> Tuple[bool, DecimalNumber, DecimalNumber]:
    """It solves quadratic equations:
    a * x² + b * x + c = 0
    x₁ = (-b + sqrt(b*b - 4*a*c)) / (2*a)
    x₂ = (-b - sqrt(b*b - 4*a*c)) / (2*a)
    """

    # This is done by catching the Exception raised when calculating
    # the square root of a negative number. It is instructive, but it
    # can be avoided by simply checking if (b * b - 4 * a * c) is a
    # negative number before calling square_root().
    try:
        r = (b * b - 4 * a * c).square_root()
        x1 = (-b + r) / (2 * a)
        x2 = (-b - r) / (2 * a)
        return True, x1, x2
    except DecimalNumberExceptionMathDomainError:
        return False, None, None


def string_equation(a: DecimalNumber, b: DecimalNumber, c: DecimalNumber) -> str:
    return "{0}x² {1}x {2} = 0".format(
        a,
        "- " + str(abs(b)) if b < 0 else '+ ' + str(b),
        "- " + str(abs(c)) if c < 0 else '+ ' + str(c)
    )


list_equations = [
    (7, -5, -9),
    (1, -3, 10),
    (4, 25, 21),
    (1, 3, -10)
]

print("-" * 50)
for e in list_equations:
    a = DecimalNumber(e[0])
    b = DecimalNumber(e[1])
    c = DecimalNumber(e[2])
    solution, x1, x2 = solve_quadratic_equation(a, b, c)
    print(string_equation(a, b, c))
    if solution:
        print("   x₁ =", x1)
        print("   x₂ =", x2)
    else:
        print("   The equation does not have a real solution.")
    print("-" * 50)
