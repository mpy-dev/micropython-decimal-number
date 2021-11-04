import sys

if sys.implementation.name == "cpython":        # micropython does not include 'typing' module
    from typing import Tuple
if sys.implementation.name == "micropython":    # Just in case...
    pass


class DecimalNumber:
    """DecimalNumber is a class for decimal floating point arithmetic with arbitrary precision."""
    VERSION = (1, 0, 0)
    VERSION_NAME = "v1.0.0 - August 2021"
    DEFAULT_SCALE: int = 16
    DECIMAL_SEP: str = "."
    THOUSANDS_SEP: str = ","
    USE_THOUSANDS_SEP: bool = False
    PI_NUMBER: int = 31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
    PI_SCALE: int = 100
    E_NUMBER: int = 27182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274
    E_SCALE: int = 100
    LN2_NUMBER: int = 6931471805599453094172321214581765680755001343602552541206800094933936219696947156058633269964186875
    LN2_SCALE: int = 100
    _scale: int = DEFAULT_SCALE

    def __init__(self, number=0, decimals: int = 0) -> None:
        """Initialization of a DecimalNumber.
        These are this posibilities:
        1) No parameters => number = 0.         Example: DecimalNumber()
        2) An integer => number = integer.      Example: DecimalNumber(1)
        3) Two integers => number and decimals. Example: Decimal(12345, 3) => Number = 12.345
        4) One string that contains the number. Example: Decimal("12.345") => Number = 12.345
        """
        if isinstance(number, int):
            self._is_positive: bool = (number >= 0)
            self._number: int = number if number >= 0 else -number
            if decimals >= 0:
                self._num_decimals: int = decimals
            else:
                raise DecimalNumberExceptionMathDomainError(
                    "__init__: the number of decimals must be positive")
            self._reduce_to_scale()
        elif isinstance(number, str):
            self.copy_from(DecimalNumber._from_string(number))
        else:
            raise DecimalNumberExceptionBadInit(
                "Only 'int' or 'str' instances are allowed for initialization")

    @classmethod
    def pi(cls) -> "DecimalNumber":
        """Calculation of PI using the very fast algorithm present on the
        documentation of the module "decimal" of the Python Standard Library:
        https://docs.python.org/3/library/decimal.html#recipes
        """
        # If it is precalculated
        if DecimalNumber.PI_SCALE >= DecimalNumber.get_scale():
            s: DecimalNumber = DecimalNumber(DecimalNumber.PI_NUMBER, DecimalNumber.PI_SCALE)
        else:
            # Calculates PI
            scale: int = DecimalNumber.get_scale()
            # extra digits for intermediate steps
            DecimalNumber.set_scale(scale + 4)
            lasts = DecimalNumber(0)
            t = DecimalNumber(3)
            s = DecimalNumber(3)
            n = DecimalNumber(1)
            na = DecimalNumber(0)
            d = DecimalNumber(0)
            da = DecimalNumber(24)
            eight = DecimalNumber(8)
            thirtytwo = DecimalNumber(32)
            while s != lasts:
                lasts.copy_from(s)
                n += na
                na += eight
                d += da
                da += thirtytwo
                t = (t * n) / d
                s += t
            DecimalNumber.set_scale(scale)
            # Stores the calculated PI
            DecimalNumber.PI_NUMBER = (+s)._number  # + adjusts to the scale
            DecimalNumber.PI_SCALE = (+s)._num_decimals
        return +s

    @classmethod
    def e(cls) -> "DecimalNumber":
        """Calculation of e.
        It uses the Taylor series:
            e = 1/0! + 1/1! + 1/2! + 1/3! + ... + 1/n!
        """
        # If it is precalculated
        if DecimalNumber.E_SCALE >= DecimalNumber.get_scale():
            e: DecimalNumber = DecimalNumber(DecimalNumber.E_NUMBER, DecimalNumber.E_SCALE)
        else:
            scale: int = DecimalNumber.get_scale()
            # extra digits for intermediate steps
            DecimalNumber.set_scale(scale + 4)

            i = DecimalNumber(0)
            f = DecimalNumber(1)
            e = DecimalNumber(1)
            e2 = DecimalNumber(0)
            one = DecimalNumber(1)
            while e2 != e:
                e2.copy_from(e)
                i += one		# counter
                f *= i
                t = one / f
                e += t

            DecimalNumber.set_scale(scale)
            # Stores the calculated E
            DecimalNumber.E_NUMBER = (+e)._number  # + adjusts to the scale
            DecimalNumber.E_SCALE = (+e)._num_decimals
        return +e

    @classmethod
    def ln2(cls) -> "DecimalNumber":
        """Calculation of ln(2).
        ln(2) = -ln(1/2) = -ln(1 - 1/2)
        It uses the Taylor series:
            ln(1-x) = -x -x²/2 - x³/3 ...
            ln(2) = x + x²/2 + x³/3 ... for x = 1/2
        """
        # If it is precalculated
        if DecimalNumber.LN2_SCALE >= DecimalNumber.get_scale():
            e: DecimalNumber =  DecimalNumber(DecimalNumber.LN2_NUMBER, DecimalNumber.LN2_SCALE)
        else:
            scale: int = DecimalNumber.get_scale()
            DecimalNumber.set_scale(scale + 4) # extra digits for intermediate steps

            i = DecimalNumber(0)    # counter
            half = DecimalNumber(5, 1) # 0.5
            x = DecimalNumber(1)
            one = DecimalNumber(1)
            e = DecimalNumber(0)
            e2 = DecimalNumber(1)
            while e2 != e:
                e2.copy_from(e)
                i += one
                x *= half
                e += x / i

            DecimalNumber.set_scale(scale)
            # Stores the calculated LN2
            DecimalNumber.LN2_NUMBER = (+e)._number  # + adjusts to the scale
            DecimalNumber.LN2_SCALE = (+e)._num_decimals
        return +e

    def exp(self, inc_scale: bool = True) -> "DecimalNumber":
        """Calculates exp(n)
        Works for any x, but for speed, it should have |x| < 1.
        For an arbitrary number, to guarantee that |x| < 1, it uses:
            exp(x) = exp(x - m * log(2)) * 2 ^ m ; where m = floor(x / log(2))

        Scale is increased if 'inc_false' is True.
        """
        scale = DecimalNumber.get_scale()
        # Calculating the necessary extra scale:
        extra = (abs(self) / DecimalNumber("2.3")).to_int_round() + 10
        DecimalNumber.set_scale(scale + extra)
        if abs(self) <= 1:
            r = DecimalNumber._exp_lt_1(self, inc_scale)
        else:
            m = (self / DecimalNumber.ln2()).to_int_truncate()
            r = DecimalNumber._exp_lt_1(self - m * DecimalNumber.ln2()) * (2 ** m)

        DecimalNumber.set_scale(scale)
        return +r

    @staticmethod
    def _exp_lt_1(n: "DecimalNumber", inc_scale: bool = True) -> "DecimalNumber":
        """ Auxiliary function to calculates exp(n)
        Expects |n| < 1 to converge rapidly
        """
        if n == 1:
            e = DecimalNumber.e()
        elif n == -1:
            e = 1 / DecimalNumber.e()
        else:
            i = DecimalNumber(0)
            x = DecimalNumber(1)
            f = DecimalNumber(1)
            e = DecimalNumber(1)
            e2 = DecimalNumber(0)
            one = DecimalNumber(1)
            while e2 != e:
                e2.copy_from(e)
                i += one		# counter
                x *= n
                f *= i
                t = x / f
                e += t

        # if inc_scale:
        #     DecimalNumber.set_scale(scale)
        return +e

    def ln(self) -> "DecimalNumber":
        """Calculates ln(n)
        Newton's method is used to solve: e**a - x = 0 ; a = ln(x)
        """
        if self == 1:
            return DecimalNumber(0)
        if self == 0:
            raise DecimalNumberExceptionMathDomainError("ln(0) = -Infinite")
        if self < 0:
            raise DecimalNumberExceptionMathDomainError("ln(x) exists for x > 0")
        n = self
        scale: int = DecimalNumber.get_scale()

        # Estimate first value
        DecimalNumber.set_scale(10) # Low scale for this is enough
        e = DecimalNumber.e()
        y0 = DecimalNumber(0)
        y1 = DecimalNumber(1)
        one = DecimalNumber(1)
        p: DecimalNumber = e.clone()
        while p < n:
            y1 += one
            p *= e

        DecimalNumber.set_scale(scale) # Restores scale
        DecimalNumber.set_scale(DecimalNumber.get_scale() + 10) # extra digits for intermediate steps
        two = DecimalNumber(2)
        while y0 != y1:
            y0.copy_from(y1)
            y1 = y0 + two * ((n - y0.exp(False)) / (n + y0.exp(False)))

        DecimalNumber.set_scale(scale)
        return +y1

    def sin(self) -> "DecimalNumber":
        """Calculates sin(x). x = radians
        It uses the Taylor series: sin(x) = x - x³/3! + x⁵/5! - x⁷/7! ...
        """
        x = self.clone()
        scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(scale + 4) # extra digits for intermediate steps

        negative_radians: bool = (x < 0)
        if negative_radians:
            x = -x
        # Calculates x mod 2π
        pi = DecimalNumber.pi()
        f: int = (x / (pi * 2)).to_int_truncate()
        if f > 0:
            x -= f * 2 * pi

        # Determines the quadrant and reduces the range of x to 0 - π/2
        # sin(-x) = -sin(x) ; cos(-x) = cos(x) ; tan(-x) = -tan(x) 
        half_pi = pi / 2
        r = half_pi.clone()
        quadrant: int = 1
        while x > r:
            r += half_pi
            quadrant += 1

        if quadrant == 2:
            x = pi - x
        elif quadrant == 3:
            x = x - pi
        elif quadrant == 4:
            x = 2 * pi - x

        i = DecimalNumber(1)    # counter
        two = DecimalNumber(2)
        n = x.clone()
        d = DecimalNumber(1)
        s = DecimalNumber(1)
        e = n.clone()
        e2 = DecimalNumber(0)
        while e2 != e:
            e2.copy_from(e)
            i += two
            n *= x * x
            d *= i * (i - 1)
            s = -s
            e += (n * s) / d

        if quadrant > 2:
            e = -e
        if negative_radians:
            e = -e

        DecimalNumber.set_scale(scale)
        return +e

    def cos(self) -> "DecimalNumber":
        """Calculates cos(x). x = radians
        It uses the Taylor series: cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! ...
        """
        x = self.clone()
        scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(scale + 4) # extra digits for intermediate steps

        if (x < 0): # cos(-x) = cos(x)
            x = -x

        # Calculates x mod 2π
        pi = DecimalNumber.pi()
        f: int = (x / (pi * 2)).to_int_truncate()
        if f > 0:
            x -= f * 2 * pi

        # Determines the quadrant and reduces the range of x to 0 - π/2
        half_pi = pi / 2
        r = half_pi.clone()
        quadrant: int = 1
        while x > r:
            r += half_pi
            quadrant += 1

        if quadrant == 2:
            x = pi - x
        elif quadrant == 3:
            x = x - pi
        elif quadrant == 4:
            x = 2 * pi - x

        i = DecimalNumber(1)    # counter
        two = DecimalNumber(2)
        n = DecimalNumber(1)
        d = DecimalNumber(1)
        s = DecimalNumber(1)
        e = n.clone()
        e2 = DecimalNumber(0)
        while e2 != e:
            e2.copy_from(e)
            n *= x * x
            d *= i * (i + 1)
            i += two
            s = -s
            e += (n * s) / d

        if quadrant == 2 or quadrant == 3:
            e = -e

        DecimalNumber.set_scale(scale)
        return +e

    def tan(self) -> "DecimalNumber":
        """Calculates tan(x) = sin(x) / cos(x). x = radians """
        x = self.clone()

        # Calculates x mod 2π
        pi = DecimalNumber.pi()
        f: int = (x / (pi * 2)).to_int_truncate()
        if f > 0:
            x -= f * 2 * pi

        half_pi = pi / 2
        three_halves_pi = (3 * pi) / 2
        # Determines the quadrant
        r = half_pi.clone()
        quadrant: int = 1
        while x > r:
            r += half_pi
            quadrant += 1

        # tan(x) = sin(x) / cos(x) ; if cos(x) == 0  =>  tan(x) = ∞

        if self == half_pi or self == three_halves_pi:
            raise DecimalNumberExceptionDivisionByZeroError("tan(x) = ±Infinite")
        else:
            scale: int = DecimalNumber.get_scale()
            DecimalNumber.set_scale(scale + 4)
            s = x.sin()
            c = x.cos()
            if c == 0:
                DecimalNumber.set_scale(scale)
                raise DecimalNumberExceptionDivisionByZeroError("tan(x) = ±Infinite")
            else:
                t = s / c
                DecimalNumber.set_scale(scale)
                return +t

    def asin(self) -> "DecimalNumber":
        """Calculates asin(x)
        It uses the Taylor series: arcsin(x) = x + 3x³/6 + 15x⁵/336 + ...
        It converges very slowly for |x| near 1. To avoid values near 1:
        If |n| between 0 and 0.707: arcsin(x) is calculated using the series.
        if |n| between 0.707 and 1: arcsin(x) is calculated as pi/2 - arcsin( sqrt(1 - x²) )
        This guarantees arcsin(x) using series with x <= 0.707 ; (sqrt(1/2)).
        """
        if self >= -1 and self <= 1:
            if self == -1:
                return -(DecimalNumber.pi() / 2)
            elif self == 1:
                return (DecimalNumber.pi() / 2)
            elif self == 0:
                return DecimalNumber(0)

            scale: int = DecimalNumber.get_scale()
            DecimalNumber.set_scale(DecimalNumber.get_scale() + 4) # extra digits for intermediate steps

            trick: bool = False
            if abs(self) > DecimalNumber("0.707"):
                trick = True
                x = (1 - self * self).square_root()
            else:                
                x = self.clone()
            
            i = DecimalNumber(1)    # counter
            one = DecimalNumber(1)
            two = DecimalNumber(2)
            four = DecimalNumber(4)
            n = DecimalNumber(1)
            d = DecimalNumber(1)
            n2 = x.clone()
            e = x.clone()
            e2 = DecimalNumber(0)
            counter: int = 0
            while e2 != e:
                e2.copy_from(e)
                n *= i
                i += two
                d *= i - one
                n2 *= x * x
                e += (n * n2) / (d * i)

            if trick:
                if self._is_positive:
                    e = DecimalNumber.pi() / 2 - e
                else:
                    e = e - DecimalNumber.pi() / 2

            DecimalNumber.set_scale(scale)
            return +e
        else:
            raise DecimalNumberExceptionMathDomainError("asin(x) admits -1 <= x <= 1 only")

    def acos(self) -> "DecimalNumber":
        """Calculates acos(x)
        It uses the equivalence: acos(x) = π/2 - asin(x)
        """
        if self >= -1 and self <= 1:
            scale: int = DecimalNumber.get_scale()
            DecimalNumber.set_scale(DecimalNumber.get_scale() + 4) # extra digits for intermediate steps

            a = (DecimalNumber.pi() / 2) - self.asin()

            DecimalNumber.set_scale(scale)
            return +a
        else:
            raise DecimalNumberExceptionMathDomainError("acos(x) admits -1 <= x <= 1 only")

    def atan(self) -> "DecimalNumber":
        """Calculates atan(x)
        It uses: atan(x) = asin( x / sqrt(1 + x²) )
        """
        scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(DecimalNumber.get_scale() + 4) # extra digits for intermediate steps
        one = DecimalNumber(1)
        v = self / (one + self * self).square_root()
        a = v.asin()

        DecimalNumber.set_scale(scale)
        return +a

    @staticmethod
    def atan2(y: "DecimalNumber", x: "DecimalNumber") -> "DecimalNumber":
        """Calculates atan2(y, x), 2-argument arctangent
        It uses:
            if x > 0:   atan(y/x)
            if x < 0:
                        if y >= 0:  atan(y/x) + pi
                        if y < 0:   atan(y/x) - pi
            if x = 0:
                        if y > 0:   +pi/2
                        if y < 0:   -pi/2
                        if y = 0:   undefined
        """
        if isinstance(y, int):
            y = DecimalNumber(y)
        if isinstance(x, int):
            x = DecimalNumber(x)

        scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(DecimalNumber.get_scale() + 4) # extra digits for intermediate steps
        r = DecimalNumber()
        if x == 0:
            if y == 0:
                raise DecimalNumberExceptionMathDomainError(
                    "Undefined value for atan2(0, 0)")
            elif y > 0:
                r = (DecimalNumber.pi() / 2)
            else:
                r = (-DecimalNumber.pi() / 2)
        else:
            r = (y / x).atan()
            if x < 0:
                if y >= 0:
                    r += DecimalNumber.pi()
                else:
                    r -= DecimalNumber.pi()
        
        DecimalNumber.set_scale(scale)
        return +r

    @staticmethod
    def version() -> str:
        """Returns a tuple (MINOR, MINOR, PATCH) with the version of DecimalNumber"""
        return DecimalNumber.VERSION

    @staticmethod
    def version_name() -> str:
        """Returns a string with the version of DecimalNumber"""
        return DecimalNumber.VERSION_NAME

    @staticmethod
    def set_scale(num_digits: int) -> None:
        """Sets the scale.
        Scale is a class value, the maximum number of decimals that a DecimalNumber can have.
        The default value is 16. The maximum value is only limited by the available
        memory and computer power."""
        if num_digits >= 0:
            DecimalNumber._scale = num_digits
        else:
            raise DecimalNumberExceptionMathDomainError(
                "set_scale: scale must be positive")

    @staticmethod
    def get_scale() -> int:
        """Gets the current scale value."""
        return DecimalNumber._scale

    @staticmethod
    def _parse_number(number: str) -> Tuple[bool, int, int]:
        """This is a static and auxiliary method to parse a string containing
        a number. If the string is parsed as a number, it returns three values:
            True --> string correctly parsed as number.
            Integer containing all the digits of the number.
            Integer representing the number of decimals.
        For example: "-12345.678" will be parsed and the values returned will be:
            (True, -12345678, 3)
        If the parsing fails, it returns (Falsem 0, 0).
        Note: this is faster than using a regular expression. Also, when using
        the regular expression "^\-?[0-9]+\.?[0-9]*" and exception was raised when
        using micropython when the string "number" was long.
        """
          # True: correct
        # Note: 
        step: int = 1   # 1: '-', 2: [0-9], 3: '.', 4: [0-9]
        position: int = 0
        integer_number: int = 0
        is_positive: bool = True
        num_decimals: int = 0
        number = tuple(number,)     # Faster than indexing the string
        length: int = len(number)
        digits: str = "0123456789"
        last_valid: int = 0
        while position < length:
            if step == 1:
                if number[position] == '-':
                    is_positive = False
                    position += 1
                step = 2
            elif step == 2:
                if digits.find(number[position]) != -1:  # [0-9]+
                    integer_number = integer_number * \
                        10 + int(number[position])
                    position += 1
                    last_valid = position
                else:
                    step = 3
            elif step == 3:
                if number[position] == DecimalNumber.DECIMAL_SEP:
                    position += 1
                    last_valid = position
                step = 4
            elif step == 4:
                if digits.find(number[position]) != -1:  # [0-9]*
                    integer_number = integer_number * \
                        10 + int(number[position])
                    num_decimals += 1
                    position += 1
                    last_valid = position
                else:
                    break
        if last_valid == length:
            if not is_positive:
                integer_number = -integer_number
            return (True, integer_number, num_decimals)
        else:
            return (False, 0, 0)

    @staticmethod
    def _from_string(number: str) -> "DecimalNumber":
        """static and auxiliary method to create a DecimalNumber from a string."""
        correct, integer_number, num_decimals = DecimalNumber._parse_number(
            number)
        if not correct:
            raise DecimalNumberExceptionParseError(
                "Syntax error parsing '{0}'".format(number))
        else:
            n = DecimalNumber(integer_number, num_decimals)
        return n

    @staticmethod
    def _make_integer_comparable(n1: "DecimalNumber", n2: "DecimalNumber") -> Tuple[int]:
        """Static and auxiliary method to creates two integers from two DecimalNumber,
        without decimals, that can be compared (or sum) by taking into account their decimals.
        Examples:
            n1: 12345.678, n2: 5.4321098  --> i1: 123456780000, i2: 54321098
            n1: 345.1, n2: 7.65: --> i1: 34510, i2: 765
        """
        max_decimals: int = max(n1._num_decimals, n2._num_decimals)
        n1_number: int = n1._number
        if not n1._is_positive:
            n1_number = -n1_number
        n2_number: int = n2._number
        if not n2._is_positive:
            n2_number = -n2_number
        if max_decimals > n1._num_decimals:
            n1_number *= 10 ** (max_decimals - n1._num_decimals)
        if max_decimals > n2._num_decimals:
            n2_number *= 10 ** (max_decimals - n2._num_decimals)
        return (n1_number, n2_number)

    @staticmethod
    def _isqrt(n: int) -> int:
        """Static and auxiliary method to calculate the square root
        of an integer.
        It uses Newton's method with integer division.
        """
        if n < 0:
            return 0
        # Calculates initial value
        t: int = n
        x1: int = 1
        while t > 100:
            x1 *= 10
            t //= 100
        # Uses Newton's method
        x2: int = (x1 + n // x1) // 2
        while abs(x2 - x1) > 1:
            x1 = x2
            x2 = (x1 + n // x1) // 2
        return x2

    def clone(self) -> "DecimalNumber":
        """Returns a new DecimalNumber as a clone of self."""
        n = DecimalNumber()
        n._number = self._number
        n._num_decimals = self._num_decimals
        n._is_positive = self._is_positive
        return n

    def copy_from(self, other: "DecimalNumber") -> None:
        """It copies on self other DecimalNumber."""
        self._number = other._number
        self._num_decimals = other._num_decimals
        self._is_positive = other._is_positive

    def square_root(self) -> "DecimalNumber":
        """Calculates the square root of a DecimalNumber.
        It converts the DecimalNumber to an integer (without decimals), calculates
        its square root using _isqrt() and then it sets the decimals.
        """
        if not self._is_positive:
            raise DecimalNumberExceptionMathDomainError(
                "No square root for negative numbers")

        n = DecimalNumber()
        num_integer: int = self._number
        num_integer *= (10 ** (DecimalNumber.get_scale() * 2))
        additional_decimals: int = 0
        if (self._num_decimals % 2) == 1:
            num_integer *= 10
            additional_decimals = 1

        num_integer = DecimalNumber._isqrt(num_integer)
        n._number = num_integer
        n._num_decimals = (
            (self._num_decimals + additional_decimals) // 2) + DecimalNumber.get_scale()
        n._reduce_to_scale()
        return n

    def __add__(self, other: "DecimalNumber") -> "DecimalNumber":
        """Adds two DecimalNumber.
        Returns (self + other)
        """
        if isinstance(other, int):
            other = DecimalNumber(other)

        #   123 + 456       : 123
        #                   : 456
        #                   : 579
        #   123 + 4.56      : 123   0
        #                   :   4   56
        #                   : 127   56  --> 127 + Apply 2 decimals to 56 --> 0.56
        #   123 + 0.0456    : 123   0
        #                   :   0   456
        #                   : 123   456 --> 123 + Apply 4 decimals to 456 --> 0.0456
        #   123.723 + 4.56  : 123   723
        #                   :   4   560 --> Apply 3 decimals to 56 --> 560
        #                   : 127  1283 --> 127 + Apply 3 decimals to 1283 --> 0.283 --> Add 1 to 127 --> 128
        #   0.0123 + 0.56   :   0   123
        #                   :   0    56 --> Apply 4 decimals to 56 --> 5600
        #                   :   0  5723 --> 123 + 5600

        max_decimals: int = max(self._num_decimals, other._num_decimals)

        a_factor: int = 10 ** self._num_decimals
        b_factor: int = 10 ** other._num_decimals

        a_integer: int = self._number // a_factor
        a_decimals: int = self._number % a_factor
        b_integer: int = other._number // b_factor
        b_decimals: int = other._number % b_factor

        if self._num_decimals < max_decimals:
            a_decimals *= (10 ** (max_decimals - self._num_decimals))

        if other._num_decimals < max_decimals:
            b_decimals *= (10 ** (max_decimals - other._num_decimals))

        c_factor: int = max(a_factor, b_factor)
        a_all: int = a_integer * c_factor + a_decimals
        b_all: int = b_integer * c_factor + b_decimals

        c_all: int = (a_all if self._is_positive else -a_all) + (b_all if other._is_positive else -b_all)
        c_is_positive: bool = (c_all > 0)
        if c_all < 0:
            c_all = -c_all

        new_number = DecimalNumber(c_all, max_decimals)
        new_number._is_positive = c_is_positive

        new_number._reduce_to_scale()

        return new_number

    def __iadd__(self, other: "DecimalNumber") -> "DecimalNumber":
        """Adds a DecimalNumber to itself.
        Returns (self += other)
        """
        n = self.__add__(other)
        self._number = n._number
        self._num_decimals = n._num_decimals
        self._is_positive = n._is_positive
        return self

    def __radd__(self, other: int) -> "DecimalNumber":
        """Reverse add.
        It is called for (integer + DecimalNumber).
        At this moment, micropython does not support it.
        """
        return self.__add__(DecimalNumber(other))

    def __sub__(self, other: "DecimalNumber") -> "DecimalNumber":
        if isinstance(other, int):
            other = DecimalNumber(other)
        s = other.clone()
        s._is_positive = not s._is_positive
        return self.__add__(s)

    def __isub__(self, other: "DecimalNumber") -> "DecimalNumber":
        n = self.__sub__(other)
        self._number = n._number
        self._num_decimals = n._num_decimals
        self._is_positive = n._is_positive
        return self

    def __rsub__(self, other: int) -> "DecimalNumber":
        return DecimalNumber(other).__sub__(self)

    def __mul__(self, other: "DecimalNumber") -> "DecimalNumber":
        if isinstance(other, int):
            other = DecimalNumber(other)
        a_integer: int = self._number if self._is_positive else -self._number
        b_integer: int = other._number if other._is_positive else -other._number
        c_integer: int = a_integer * b_integer
        new_number = DecimalNumber(
            c_integer, self._num_decimals + other._num_decimals)
        return new_number

    def __imul__(self, other: "DecimalNumber") -> "DecimalNumber":
        n = self.__mul__(other)
        self._number = n._number
        self._num_decimals = n._num_decimals
        self._is_positive = n._is_positive
        return self

    def __rmul__(self, other: int) -> "DecimalNumber":
        return self.__mul__(DecimalNumber(other))

    def __truediv__(self, other: "DecimalNumber") -> "DecimalNumber":
        if isinstance(other, int):
            other = DecimalNumber(other)
        # a_integer: int = self._number if self._is_positive else -self._number
        # b_integer: int = other._number if other._is_positive else -other._number
        a_integer: int
        b_integer: int
        a_integer, b_integer = DecimalNumber._make_integer_comparable(self, other)
        if b_integer != 0:
            c_factor: int = 10 ** (DecimalNumber.get_scale() + 2)
            c_integer: int = (a_integer * c_factor) // b_integer
            new_number = DecimalNumber(
                c_integer, (DecimalNumber.get_scale() + 2))
        else:
            raise DecimalNumberExceptionDivisionByZeroError("Division by zero")
        return new_number

    def __itruediv__(self, other: "DecimalNumber") -> "DecimalNumber":
        n = self.__truediv__(other)
        self._number = n._number
        self._num_decimals = n._num_decimals
        self._is_positive = n._is_positive
        return self

    def __rtruediv__(self, other: int) -> "DecimalNumber":
        return DecimalNumber(other).__truediv__(self)

    def __pow__(self, other: int) -> "DecimalNumber":
        # Exponentition by squaring: https://en.wikipedia.org/wiki/Exponentiation_by_squaring
        e: int = other
        x = self.clone()
        x._is_positive = True
        if other == 0:
            return DecimalNumber(1)
        scale: int = DecimalNumber.get_scale()
        
        # Calculating the necessary extra scale:
        extra = abs(other) * (len(str(self._number)) - self._num_decimals)
        # extra digits for intermediate steps
        DecimalNumber.set_scale(scale + extra)
        if other < 0:
            x = DecimalNumber(1) / x
            other = -other
        y = DecimalNumber(1)
        while other > 1:
            if (other % 2) == 0:
                x *= x
                other //= 2
            else:
                y *= x
                x *= x
                other = (other - 1) // 2
        x *= y
        DecimalNumber.set_scale(scale)
        if not self._is_positive and (e % 2) == 1:
            return -x
        else:
            return +x

    def __neg__(self) -> "DecimalNumber":
        n = self.clone()
        n._is_positive = not self._is_positive
        n._reduce_to_scale()
        return n

    def __pos__(self) -> "DecimalNumber":
        n = self.clone()
        n._reduce_to_scale()
        return n

    def __abs__(self) -> "DecimalNumber":
        n = self.clone()
        n._is_positive = True
        n._reduce_to_scale()
        return n

    def __lt__(self, other: "DecimalNumber") -> bool:  # Less than
        if isinstance(other, int):
            other = DecimalNumber(other)
        n1, n2 = DecimalNumber._make_integer_comparable(self, other)
        return (n1 < n2)

    def __le__(self, other: "DecimalNumber") -> bool:  # Less than or equal to
        if isinstance(other, int):
            other = DecimalNumber(other)
        n1, n2 = DecimalNumber._make_integer_comparable(self, other)
        return (n1 <= n2)

    def __eq__(self, other: "DecimalNumber") -> bool:  # Equal to
        if isinstance(other, int):
            other = DecimalNumber(other)
        n1, n2 = DecimalNumber._make_integer_comparable(self, other)
        return (n1 == n2)

    def __ne__(self, other: "DecimalNumber") -> bool:  # Not equal to
        if isinstance(other, int):
            other = DecimalNumber(other)
        n1, n2 = DecimalNumber._make_integer_comparable(self, other)
        return (n1 != n2)

    def __gt__(self, other: "DecimalNumber") -> bool:  # Greater than
        if isinstance(other, int):
            other = DecimalNumber(other)
        n1, n2 = DecimalNumber._make_integer_comparable(self, other)
        return (n1 > n2)

    def __ge__(self, other: "DecimalNumber") -> bool:  # Greater than or equal to
        if isinstance(other, int):
            other = DecimalNumber(other)
        n1, n2 = DecimalNumber._make_integer_comparable(self, other)
        return (n1 >= n2)

    def __str__(self, thousands: bool = False) -> str:
        #   Integer / Decimals: String
        #   12345 / 0: 12345
        #   12345 / 1: 1234.5
        #   12345 / 2: 123.45
        #   12345 / 3: 12.345
        #   12345 / 4: 1.2345
        #   12345 / 5: 0.12345
        #   12345 / 6: 0.012345
        #   12345 / 7: 0.0012345
        #   12345 / 8: 0.00012345
        str_number: str = str(
            self._number) if self._number >= 0 else str(-self._number)
        if self._num_decimals != 0:
            num_digits: int = len(str_number)
            if self._num_decimals < num_digits:
                str_number = str_number[:(
                    num_digits - self._num_decimals)] + "." + str_number[-self._num_decimals:]
            else:
                str_number = "0" + "." + \
                    ("0" * (self._num_decimals - num_digits)) + str_number

        if thousands:
            pos_decimal: int = str_number.find(".")
            if pos_decimal == -1:
                first_part: str = str_number
                second_part: str = ""
            else:
                first_part: str = str_number[:pos_decimal]
                second_part: str = str_number[pos_decimal + 1:]
            first_part = "{:,d}".format(int(first_part))
            ##### Commenting this part to not separate decimals ###############################
            # if len(second_part) > 0:
            #     # Note: reversing with second_part[::-1] is not available for micropython
            #     second_part = "{:,d}".format(int( ''.join(reversed(second_part)) ))
            #     second_part = ''.join(reversed(second_part))
            ###################################################################################
            str_number = first_part
            if len(second_part) > 0:
                str_number += "." + second_part

        str_number = str_number.replace(".", "#")
        str_number = str_number.replace(",", DecimalNumber.THOUSANDS_SEP)
        str_number = str_number.replace("#", DecimalNumber.DECIMAL_SEP)

        if not self._is_positive:
            str_number = "-" + str_number

        return str_number

    def __repr__(self) -> str:
        return 'DecimalNumber("' + str(self) + '")'

    def to_int_truncate(self) -> int:
        return self._number // (10 ** self._num_decimals)

    def to_int_round(self) -> int:
        n = self.clone()
        s = DecimalNumber.get_scale()
        DecimalNumber.set_scale(0)
        n._reduce_to_scale()
        DecimalNumber.set_scale(s)
        return n._number

    def to_string_thousands(self) -> str:
        return self.__str__(True)

    # Returns a string representing the number limited to N characters, including '.', '-' and, optionally thousands.
    # It is useful to limit the number to the length of a calculator's LCD display, for example.
    # If the number does not fit, it returns "Overflow".
    def to_string_max_length(self, max_length: int, thousands: bool = False) -> None:
        if max_length < 8:
            max_length = 8

        str_number: str = self.__str__(thousands)
        #   1,234,567,890.1234567
        #   If the number of characters before '.' is greater than max_length --> Overflow
        pos_point: int = str_number.find('.')
        if pos_point == -1:     # No decimals
            pos_point = len(str_number)
        if pos_point > max_length:
            return "Overflow"
        else:
            str_number = str_number[:max_length]
            # If there are decimals, we can eliminate trailing zeros
            pos_point: int = str_number.find('.')
            if pos_point != -1:
                # 123.34000
                while str_number[-1:] == '0':
                    str_number = str_number[:-1]
                # If the last character is a point, it can be deleted
                if str_number[-1:] == '.':
                    str_number = str_number[:-1]
            if str_number == "-0":
                str_number = "0"
            return str_number

    def _eliminate_decimal_trailing_zeros(self) -> None:
        while self._num_decimals > 0 and (self._number % 10) == 0:
            self._number //= 10
            self._num_decimals -= 1

    def _reduce_to_scale(self) -> None:
        if self._num_decimals > DecimalNumber.get_scale():
            # Round half to even: https://en.wikipedia.org/wiki/Rounding#Round_half_to_even

            # Example:
            #   scale = 3
            #   Number: 123.456789
            #   n = 123456789, decimals = 6
            #   It should be  123.457 ;  n = 123457, decimals = scale = 3

            n: int = self._number
            s: int = self._num_decimals - DecimalNumber.get_scale()  # s: 6 - 3 = 3
            ds: int = (10 ** s)

            v: int = n % (ds * 10)  # v: n % 10**4 =  6789      1000
            b: int = v % ds         # b: v % 10**3 =   789
            a: int = v // ds        # a: v // 10**3 = 6
            m: int = ds // 2        # m: 10**3 // 2 = 500 (to be compared to b)

            if (a % 2) == 1:        # Calculating differences to get to the nearest even
                if b < m:
                    x: int = -b
                else:
                    x: int = ds - b
            else:
                if b <= m:
                    x: int = -b
                else:
                    x: int = ds - b

            self._number = (n + x) // ds
            self._num_decimals = DecimalNumber.get_scale()

        self._eliminate_decimal_trailing_zeros()

        if self._number == 0 and not self._is_positive:  # Prevents -0
            self._is_positive = True


class DecimalNumberException(Exception):
    pass


class DecimalNumberExceptionParseError(DecimalNumberException):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return "DecimalNumberExceptionParseError: {0}".format(self.message)
        else:
            return "DecimalNumberExceptionParseError"


class DecimalNumberExceptionBadInit(DecimalNumberException):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return "DecimalNumberExceptionBadInit: {0}".format(self.message)
        else:
            return "DecimalNumberExceptionBadInit"


class DecimalNumberExceptionMathDomainError(DecimalNumberException):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return "DecimalNumberExceptionMathDomainError: {0}".format(self.message)
        else:
            return "DecimalNumberExceptionMathDomainError"


class DecimalNumberExceptionDivisionByZeroError(DecimalNumberException):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return "DecimalNumberExceptionDivisionByZeroError: {0}".format(self.message)
        else:
            return "DecimalNumberExceptionDivisionByZeroError"


if __name__ == "__main__":
    print("DecimalNumber module -", DecimalNumber.VERSION)
