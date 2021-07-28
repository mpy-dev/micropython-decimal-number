# Decimal floating point arithmetic for micropython
This Python module for [*micropython*](https://micropython.org/) provides support for decimal floating point arithmetic. It tries to overcome the limitations of single precision float numbers (32-bit) and provides a solution when double precision float numbers (64 bit) are not enough.

The Python Standard Library contains the wonderful module [*decimal*](https://docs.python.org/3/library/decimal.html), but it has not been ported to *micropython*. This module provides a small part of the functionality of *decimal*.

## Introduction

The module **mpy_decimal** defines the class **DecimalNumber** that contains all the functionality for decimal floating point arithmetic. A **DecimalNumber** can be of arbitrary precision. Internally, it is composed of an *int* (built-in type of Python) that contains all the digits of the **DecimalNumber**, an *int* equal to the number of decimal places and a *bool* that determines whether the **DecimalNumber** is positive or negative. Example:

    DecimalNumber: -12345678901.23456789
        number   = 1234567890123456789
        decimals = 8
        positive = False

The precision of **DecimalNumber** is mainly limited by available memory and procesing power. **DecimalNumber** uses the concept **scale**, which is the number of decimal places that the class uses for its numbers and operations. The concept is similar to the calculator an language [*bc*](https://www.gnu.org/software/bc/manual/html_mono/bc.html).  The default value for **scale** is 16. It is a global value of the class that can be changed at any time. For rounding, **DecimalNumber** uses [*round half to even*](https://en.wikipedia.org/wiki/Rounding#Round_half_to_even).

## Performance ##

All the internal operations of **DecimalNumber** are done with integers (*int* built-in type of Python) and the number of decimals are adjusted according to the operation. It is fast, but not as fast as Python's *decimal* class because **DecimalNumber** is pure Python and *decimal* is written in C. The *test* folder contains the file "*perf_decimal_number.py*" that calculates the performance of **DecimalNumber** on the device it runs. This is the performance on a [*Raspberry Pi Pico*](https://www.raspberrypi.org/products/raspberry-pi-pico/):

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



## Available operations and functions

## Limitations
