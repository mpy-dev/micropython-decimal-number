import sys
import random
from mpy_decimal.mpy_decimal import *

# Imports modules and it sets limits depending on the implementation
if sys.implementation.name == "cpython":
    import traceback
    import time
    iteration_limit: int = 100000
    iteration_limit2: int = 40000
    pi_decimals: int = 1000
if sys.implementation.name == "micropython":
    import machine
    import utime
    iteration_limit: int = 1000
    iteration_limit2: int = 400
    pi_decimals: int = 300

format_str: str = "{:<36}"

def system_machine_info() -> None:
    """It prints system information."""
    print(format_str.format("Implementation name:"), sys.implementation.name)
    print(format_str.format("Implementation version:"),
          "{0}.{1}.{2}".format(
        sys.implementation.version[0],
        sys.implementation.version[1],
        sys.implementation.version[2]
    )
    )
    print(format_str.format("Implementation platform:"), sys.platform)
    if sys.implementation.name == "micropython":
        print(format_str.format("CPU frequency:"),
              machine.freq() // 1000000, "Mhz")

def get_time_ms() -> int:
    """It gets the time in miliseconds.
    The way to get it depends on the implementation."""
    if sys.implementation.name == "cpython":
        return round(time.time() * 1000)
    if sys.implementation.name == "micropython":
        return utime.ticks_ms()

def gen_random_number() -> DecimalNumber:
    """Generates a random number with a number of decimals equal to scale.
    The number of digits for the integer part is between scale/2 and scale.
    It can be either positive or negative.
    abs(gen_random_number()) can be used for postive numbers only.
    """
    n: int = 0
    length: int = DecimalNumber.get_scale(
    ) + random.randrange(DecimalNumber.get_scale() // 2, DecimalNumber.get_scale())
    for _ in range(0, length):
        n = n * 10 + random.randrange(0, 9)
    if random.randrange(0, 2) == 0:
        n = -n
    return DecimalNumber(n, DecimalNumber.get_scale())

def perf_decimal_number(limit1: int, limit2: int) -> None:
    global iteration_limit

    """Performance calculations of DecimalNumber class"""
    print(format_str.format("Scale (max. decimals):"), DecimalNumber.get_scale())
    print(format_str.format("Iterations per test:"), limit1)

    n1 = gen_random_number()
    zero: bool = True
    while zero:
        n2 = gen_random_number()
        zero = (n2 == DecimalNumber(0))
    print(format_str.format("Number 1:"), n1)
    print(format_str.format("Number 2:"), n2)

    # Addition
    t = get_time_ms()
    for _ in range(0, limit1):
        n3 = n1 + n2
    t = get_time_ms() - t
    print(format_str.format("Addition (n1 + n2):"), t / limit1, "ms")

    # Subtraction
    t = get_time_ms()
    for _ in range(0, limit1):
        n3 = n1 - n2
    t = get_time_ms() - t
    print(format_str.format("Subtraction (n1 - n2):"), t / limit1, "ms")

    # Multiplication
    t = get_time_ms()
    for _ in range(0, limit1):
        n3 = n1 * n2
    t = get_time_ms() - t
    print(format_str.format("Multiplication (n1 * n2):"), t / limit1, "ms")

    # Division
    t = get_time_ms()
    for _ in range(0, limit1):
        n3 = n1 / n2
    t = get_time_ms() - t
    print(format_str.format("Division (n1 / n2):"), t / limit1, "ms")

    # Square root
    n = abs(n1)
    t = get_time_ms()
    for _ in range(0, limit1):
        n3 = n.square_root()
    t = get_time_ms() - t
    print(format_str.format("Square root abs(n1):"), t / limit1, "ms")

    # Power
    n = DecimalNumber.pi() / 2
    e: int = 15
    t = get_time_ms()
    for _ in range(0, limit1):
        n3 = n ** e
    t = get_time_ms() - t
    print(format_str.format("Power: (pi/2) ** 15"), t / limit1, "ms")

    # Creation from integer
    n = n1._number
    d = n1._num_decimals
    t = get_time_ms()
    for _ in range(0, limit1):
        n3 = DecimalNumber(n, d)
    t = get_time_ms() - t
    print(format_str.format("DecimalNumber from int:"), t / limit1, "ms")

    # Creation from string
    n = str(n1)
    t = get_time_ms()
    for _ in range(0, limit1):
        n3 = DecimalNumber(n)
    t = get_time_ms() - t
    print(format_str.format("DecimalNumber from string:"), t / limit1, "ms")


    # From this point, the iterations are reduced
    print(format_str.format("Iterations per test:"), limit2)

    # Sine
    n = DecimalNumber("0.54321")
    t = get_time_ms()
    for _ in range(0, limit2):
        n3 = n.sin()
    t = get_time_ms() - t
    print(format_str.format("Sine: sin(" + str(n) + ")"), t / limit2, "ms")

    # Cosine
    n = DecimalNumber("0.54321")
    t = get_time_ms()
    for _ in range(0, limit2):
        n3 = n.sin()
    t = get_time_ms() - t
    print(format_str.format("Cosine: cos(" + str(n) + ")"), t / limit2, "ms")

    # Tangent
    n = DecimalNumber("0.54321")
    t = get_time_ms()
    for _ in range(0, limit2):
        n3 = n.tan()
    t = get_time_ms() - t
    print(format_str.format("Tangent: tan(" + str(n) + ")"), t / limit2, "ms")


    # Arcsine
    n = DecimalNumber("0.54321")
    t = get_time_ms()
    for _ in range(0, limit2):
        n3 = n.asin()
    t = get_time_ms() - t
    print(format_str.format("Arcsine: asin(" + str(n) + ")"), t / limit2, "ms")

    # Arccosine
    n = DecimalNumber("0.65432")
    t = get_time_ms()
    for _ in range(0, limit2):
        n3 = n.acos()
    t = get_time_ms() - t
    print(format_str.format("Arccosine: acos(" + str(n) + ")"), t / limit2, "ms")

    # Arctangent
    n = DecimalNumber("1.2345")
    t = get_time_ms()
    for _ in range(0, limit2):
        n3 = n.atan()
    t = get_time_ms() - t
    print(format_str.format("Arctangent: atan(" + str(n) + ")"), t / limit2, "ms")

    # 2-argument arctangent
    n = DecimalNumber("2.3456")
    n2 = DecimalNumber("1.2334")
    t = get_time_ms()
    for _ in range(0, limit2):
        n3 = DecimalNumber.atan2(n, n2)
    t = get_time_ms() - t
    print(format_str.format("Arctangent2: atan2(" + str(n) + ", " + str(n2) + ")"), t / limit2, "ms")

    # Exponential
    n = DecimalNumber("12.345")
    t = get_time_ms()
    for _ in range(0, limit2):
        n3 = n.exp()
    t = get_time_ms() - t
    print(format_str.format("Exponential: exp(" + str(n) + ")"), t / limit2, "ms")

    # Natural logarithm
    n = DecimalNumber("12.345")
    t = get_time_ms()
    for _ in range(0, limit2):
        n3 = n.exp()
    t = get_time_ms() - t
    print(format_str.format("Natural logarithm: ln(" + str(n) + ")"), t / limit2, "ms")

def perf_decimal_number_pi() -> None:
    """Performance of the calculation of PI."""
    global pi_decimals

    # Calculating PI
    # PI is precalculated up to 100 decimals.
    # We need to set scale > 100 to actually calculated.
    current_scale = DecimalNumber.get_scale()
    DecimalNumber.set_scale(pi_decimals)
    t = get_time_ms()
    pi = DecimalNumber.pi()
    t = get_time_ms() - t
    print(format_str.format("Pi with " + str(pi_decimals) + " decimals:"), t/1000, "s")
    print(pi)
    DecimalNumber.set_scale(current_scale)

def print_title(title: str) -> None:
    """Auxiliary function to print a title."""
    line: str = '+' + ('-' * 73) + '+'
    print("")
    print(line)
    print("|  " + "{:<69}".format(title) + "  |")
    print(line)


print_title("SYSTEM INFORMATION")
system_machine_info()

print_title("PERFORMANCE WITH SCALE = 16")
DecimalNumber.set_scale(16)
perf_decimal_number(iteration_limit, iteration_limit // 100)

print_title("PERFORMANCE WITH SCALE = 50")
DecimalNumber.set_scale(50)
perf_decimal_number(iteration_limit2, iteration_limit2 // 100)

print_title("CALCULATING PI")
perf_decimal_number_pi()
