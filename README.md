# Decimal floating point arithmetic for micropython
This Python module for [*micropython*](https://micropython.org/) provides support for decimal floating point arithmetic. It tries to overcome the limitations of single precision float numbers (32-bit) and provides a solution when double precision float numbers (64 bit) are not enough.

The Python Standard Library contains the wonderful module [*decimal*](https://docs.python.org/3/library/decimal.html), but it has not been ported to *micropython*. This module provides a small, but valuable, part of the functionality of *decimal*.

## Introduction

The module **mpy_decimal** defines the class **DecimalNumber** that contains all the functionality for decimal floating point arithmetic. A **DecimalNumber** can be of arbitrary precision. Internally, it is composed of an *int* that contains all the digits of the **DecimalNumber**, an *int* equal to the number of decimal places and a *bool* that determines whether the **DecimalNumber** is positive or negative. Example:

    DecimalNumber: -12345678901.23456789
        number   = 1234567890123456789
        decimals = 8
        positive = False

The precision of **DecimalNumber** is mainly limited by available memory and procesing power. **DecimalNumber** uses the concept **scale**, which is the number of decimal places that the class uses for its numbers and operations. The concept is similar to the use of 'scale' in the calculator an language <a href="https://www.gnu.org/software/bc/manual/html_mono/bc.html" target="_blank">*bc*</a>.  The default value for **scale** is 16. It is a global value of the class that can be changed at any time. For rounding, **DecimalNumber** uses [*round half to even*](https://en.wikipedia.org/wiki/Rounding#Round_half_to_even).

## Performance ##

All the internal operations of **DecimalNumber** are done with integers (*int* built-in type of Python) and the number of decimals are adjusted according to the operation. It is fast, but not as fast as Python's *decimal* class because **DecimalNumber** is pure Python and *decimal* is written in C. The *test* folder contains the file "*perf_decimal_number.py*" that calculates the performance of **DecimalNumber** on the device it runs. This is the output of that program executed on a [*Raspberry Pi Pico*](https://www.raspberrypi.org/products/raspberry-pi-pico/). Basic operations take about one millisecond with scale = 16:

    +---------------------------------------------------------------+
    |  SYSTEM INFORMATION                                           |
    +---------------------------------------------------------------+
    Implementation name:           micropython
    Implementation version:        1.16.0
    Implementation platform:       rp2
    CPU frequency:                 125 Mhz

    +---------------------------------------------------------------+
    |  PERFORMANCE OF DecimalNumber                                 |
    +---------------------------------------------------------------+
    Scale (max. decimals):         16
    Iterations per test:           1000
    Number 1:                      -35538508.685313420325041
    Number 2:                      -88138453.0826150738002763
    Addition (n1 + n2):            1.488 ms
    Subtraction (n1 - n2):         1.445 ms
    Multiplication (n1 * n2):      0.877 ms
    Division (n1 / n2):            1.197 ms
    Square root abs(n1):           3.454 ms
    Power: 1.01234567 ** 15        5.873 ms
    DecimalNumber from int:        0.261 ms
    DecimalNumber from string:     2.879 ms

    +---------------------------------------------------------------+
    |  CALCULATING PI                                               |
    +---------------------------------------------------------------+
    Pi with 300 decimals:          5.884 s
    3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141274

## Examples

You can start by importing the module:

    from mpy_decimal.mpy_decimal import *

If you need (and can) run your code on both, a computer and a micropython board, you will probably need to run different code depending on the device. You can do it this way:

    import sys

    if sys.implementation.name == "cpython":
        ... your imports or code for CPython here ...

    if sys.implementation.name == "micropython":
        ... your imports or code for Micropython here ...

### Initialization ###
A number with default value, equal to zero:

    n = DecimalNumber()

A integer, for example, 748:

    n = DecimalNumber(748)

A decimal number, for example, 93402.5184:

    n = DecimalNumber(934025184, 4)

Notice that the first parameter is an integer with all the digits and the second one the number of decimals.

The same number can be created providing a string with the number:

    n = DecimalNumber("93402.5184")

### Printing and formating ###
Numbers can be printed using 'print()':

    print(n)
        Result: 93402.5184

They can be converted to a string using 'str()':

    str(n)


The method **to_string_thousands()** of **DecimalNumber** returns a string with the number formated with ',' as thousands separator. Decimals are not affected:

    print(n.to_string_thousands())
        Result: 93,402.5184

Micropython can be used to display information on a display with limited characters. For example, on a 16x2 LCD (two lines of 16 characters). For these kind of cases exists the method **to_string_max_length**. It limits the representation of the number to a maximum length of characters. The minimum value is 8. If decimals cannot fit in, they are discarded. If the integer part of the number is bigger than the maximum length, the result is the string "Overflow". The decimal point is also considered. Some examples:

    n = DecimalNumber("123456789.012")
    print(n.to_string_max_length(12))
        Result: 123456789.01
    print(n.to_string_max_length(11))
        Result: 123456789
    print(n.to_string_max_length(8))
        Result: Overflow

### Operations ###





## Limitations
