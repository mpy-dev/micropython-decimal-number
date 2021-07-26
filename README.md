# Decimal floating point arithmetic for micropython
This python module provides support for decimal floating point arithmetic for micropython. It tries to overcome the limitations of single precision float numbers (32-bit) and provides a solution when double precision float numbers (64 bit) are not enough.

It defines a class named **DecimalNumber**. Each number is defined by three values: an integer, the number of decimals and a boolean value that defines whether it is a positive number or not. For example, the number 12345678.90123456789 is represented by:
* An integer: 1234567890123456789
* The number of decimals: 11
* Is positive: True

Python allows to use huge integers, basically limited by the amount of memory and processing speed. For example, you can calculate the 28th Mersenne number, 2<sup>86243</sup>-1, an integer with 25,962 digits, quite easily on a Raspberry Pi Pico:

    a = 2 ** 86243 - 1



