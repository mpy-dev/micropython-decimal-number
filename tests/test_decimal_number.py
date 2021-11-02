import sys
import random
from mpy_decimal.mpy_decimal import *

if sys.implementation.name == "cpython":
    import traceback
if sys.implementation.name == "micropython":
    pass


class TestDecimalNumber():

    def __init__(self) -> None:
        """Initializes TestDecimalNumber, creating a counter for the tests run"""
        self.test_counter: int = 0

    def assertRaises(self, exc, function) -> None:
        """Method to assert that an exception is raised.
        It takes as parameters de Exception expected to occur an a function to be executed.
        """
        try:
            function()
            return False        # Exception not raised
        except Exception as e:
            if isinstance(e, exc):
                return True     # Expected exception raised
            else:
                return False    # Other exception raised

    def assertEqual(self, v1, v2, message: str) -> bool:
        """Assert that parameters v1 and v2 are equal.
        It prints the message provided as parameter in case v1 and v2 are not equal.
        """
        if v1 == v2:
            return True
        else:
            print("\t" + message)
            return False

    def assertTrue(self, v, message: str) -> bool:
        """Assert that parameter v is True.
        It prints the message provided as parameter in case v is not true.
        """
        if v:
            return True
        else:
            print("\t" + message)
            return False

    def assertFalse(self, v, message: str) -> bool:
        """Assert that parameter v is False.
        It prints the message provided as parameter in case v is not false.
        """
        if not v:
            return True
        else:
            print("\t" + message)
            return False

    def test_init(self) -> bool:
        """Tests that method __init__() method works correctly.
        It tests that a negative number of decimals raises an Exception.
        Init accepts a string also, but that is tested by 'test_parse_number'
        and 'test_from_string'.
        """
        self.test_counter += 1
        failed: bool = False
        # Creation of a number with negative number of decimals
        if not self.assertRaises(DecimalNumberExceptionMathDomainError, lambda: DecimalNumber(1, -5)):
            failed = True
        return failed

    def test_parse_number(self) -> bool:
        """Tests that method _parse_number() works correctly.
        This method tests if a string containing a DecimalNumber number is valid.
        """
        self.test_counter += 1
        failed: bool = False
        # Parsing a string to create a number
        list_invalid = [
            "1..4", "-", "1.-4", "--5", "0..", "12a345", "123v", "7O"
        ]
        list_valid = [
            "0", "0.", "0.1", "0.01", "1", "12", "-0", "-0.", "-0.1", "-0.01", "-1", "-12",
            "12.34", "-12.34", "3.141592653589793238462643383279", "123456789012345", "98765.43210"
        ]
        for n in list_invalid:
            if not self.assertFalse(DecimalNumber._parse_number(n)[0], "Incorrect parsing of {0} as a number".format(n)):
                failed = True
        for n in list_valid:
            if not self.assertTrue(DecimalNumber._parse_number(n)[0], "Incorrect parsing of {0} as a number".format(n)):
                failed = True

        return failed

    def test_from_string(self) -> bool:
        """Tests that method _from_string() of DecimalNumber works correctly.
        It tests that the number is parsed as valid a the Decimal Number is created.
        The list of valid number should not raised and exception.
        The list of invalid numbers a tested for a "parse error' exception.
        """
        self.test_counter += 1
        failed: bool = False
        # Parsing a string to create a number
        list_valid = [
            "0", "0.", "0.1", "0.01", "1", "12", "-0", "-0.", "-0.1", "-0.01", "-1", "-12",
            "12.34", "-12.34", "3.141592653589793238462643383279", "123456789012345", "98765.43210"
        ]
        list_invalid = [
            "1..4", "-", "1.-4", "--5", "0..", "12a345", "7O"
        ]
        for n in list_invalid:
            if not self.assertRaises(DecimalNumberExceptionParseError, lambda: DecimalNumber(n)):
                failed = True
        for n in list_valid:
            number = DecimalNumber(n)
        return failed

    def test_set_scale(self) -> bool:
        """Tests that method set_scale() of DecimalNumber works correctly.
        It tests that the scale of the class that is set is the same as the scale that can be got.
        """
        self.test_counter += 1
        failed: bool = False
        # scale must be positive
        if not self.assertRaises(DecimalNumberExceptionMathDomainError, lambda: DecimalNumber.set_scale(-5)):
            failed = True

        # scale is really set
        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(77)
        new_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(current_scale)
        if not self.assertEqual(new_scale, 77, "Method 'set_scale': setting the scale to 77 did not work"):
            failed = True
        return failed

    def test_square_root(self) -> bool:
        """Tests that method square_root() of DecimalNumber works correctly.
        It processes a list of numbers with their corresponding scale.
        Calculates their square root using the scale specified and test the known result.
        Also, it checks that the square root of a negative number raises an exception.
        """
        self.test_counter += 1
        failed: bool = False
        list_values = [  # scale, number, square root
            ("16", "1", "1"),
            ("16", "2", "1.414213562373095"),
            ("16", "3", "1.7320508075688772"),
            ("16", "4", "2"),
            ("16", "5", "2.2360679774997896"),
            ("16", "123456789", "11111.1110605555554405"),
            ("100", "6785678591231241027553456732298341",
             "82375230447211745.7368866296777842344492194107322494030818769086621615900281496437753626890475423118552055519336463298")
        ]
        for n in list_values:
            current_scale: int = DecimalNumber.get_scale()
            DecimalNumber.set_scale(int(n[0]))
            sr = str(DecimalNumber(n[1]).square_root())
            if not self.assertEqual(sr, n[2], "Error calculating square_root({0})".format(n[1])):
                failed = True
            DecimalNumber.set_scale(current_scale)

        if not self.assertRaises(DecimalNumberExceptionMathDomainError, lambda: DecimalNumber(-1).square_root()):
            failed = True
        return failed

    def test_pi(self) -> bool:
        """Tests that method pi() of DecimalNumber works correctly.
        It tests it with scale = 100, meaning 100 decimals.
        Pi with up to 100 decimals is precalculated. It tests that is returned correctly.
        Pi with 200 decimals is calculated and checked.
        """
        self.test_counter += 1
        failed: bool = False
        # PI with 100 decimals is already calculated. It is checked and the it is calculated with 200 decimals
        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(100)
        if not self.assertEqual(
            str(DecimalNumber.pi()),
            "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679",
            "Value of PI with one hundred decimals is incorrect"
        ):
            failed = True
        DecimalNumber.set_scale(200)
        if not self.assertEqual(
            str(DecimalNumber.pi()),
            "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196",
            "Value of PI with two hundred decimals is incorrect"
        ):
            failed = True
        DecimalNumber.set_scale(current_scale)
        return failed

    def test_add_iadd(self) -> bool:
        """Tests that methods __add__() and __iadd__() of DecimalNumber work correctly.
        It tests a list of numbers and their known addition.
        """
        list_numbers = [
            ("0", "0", "0"),
            ("0", "1", "1"),
            ("1", "0", "1"),
            ("-1", "0", "-1"),
            ("0", "-1", "-1"),
            ("-1", "-1", "-2"),
            ("0.5", "0.123456789", "0.623456789"),
            ("0.987654321", "0.5", "1.487654321"),
            ("1000001", "0.000001", "1000001.000001"),
            ("1000001", "-0.000001", "1000000.999999"),
            ("0.000001", "-1000001", "-1000000.999999"),
            ("4533.04", "955.671", "5488.711"),
            ("-194.406", "-37893.4", "-38087.806"),
            ("-93670.7", "805.483", "-92865.217"),
            ("508.77", "156.918", "665.688"),
            ("710.233", "5645.94", "6356.173"),
            ("8249.8", "-8285.15", "-35.35"),
            ("309.046", "174.381", "483.427"),
            ("6346.2", "4780.7", "11126.9"),
            ("-78586.1", "-753.691", "-79339.791"),
            ("-25283.3", "69385.1", "44101.8"),
            ("55960", "-3160.14", "52799.86"),
            ("90505", "-99802.7", "-9297.7"),
            ("-9199.8", "-58138.1", "-67337.9"),
            ("643.213", "11178.3", "11821.513"),
            ("-38046.6", "242.139", "-37804.461")
        ]
        self.test_counter += 1
        failed: bool = False
        for n in list_numbers:
            a = DecimalNumber(n[0])
            b = DecimalNumber(n[1])
            c = DecimalNumber(n[2])
            cc = a + b
            aa = DecimalNumber(n[0])
            aa += b

            if not self.assertEqual(c, cc, "Incorrect addition for ({0} + {1})".format(str(a), str(b))):
                failed = True
            if not self.assertEqual(aa, cc, "Incorrect addition to itself for ({0} + {1})".format(str(a), str(b))):
                failed = True

        # Addition with integers
        if sys.implementation.name == "cpython":
            one_int: int = 1
            minus_one_int: int = -1
            three = DecimalNumber(3)
            minus_three = DecimalNumber(-3)
            if not self.assertEqual(one_int + three, DecimalNumber("4"), "Incorrect addition for ({0} + {1})".format(one_int, three)):
                failed = True
            if not self.assertEqual(one_int + minus_three, DecimalNumber("-2"), "Incorrect addition for ({0} + {1})".format(one_int, minus_three)):
                failed = True
            if not self.assertEqual(minus_one_int + three, DecimalNumber("2"), "Incorrect addition for ({0} + {1})".format(minus_one_int, three)):
                failed = True
            if not self.assertEqual(minus_one_int + minus_three, DecimalNumber("-4"), "Incorrect addition for ({0} + {1})".format(minus_one_int, minus_three)):
                failed = True

        return failed

    def test_sub_iub(self) -> bool:
        """Tests that methods __sub__() and __isub__() of DecimalNumber work correctly.
        It tests a list of numbers and their known subtraction.
        """
        list_numbers = [
            ("0", "0", "0"),
            ("0", "1", "-1"),
            ("1", "0", "1"),
            ("-1", "0", "-1"),
            ("0", "-1", "1"),
            ("-1", "1", "-2"),
            ("-1", "-1", "0"),
            ("0.5", "0.123456789", "0.376543211"),
            ("0.987654321", "-0.5", "1.487654321"),
            ("1000001", "-0.000001", "1000001.000001"),
            ("1000001", "0.000001", "1000000.999999"),
            ("0.000001", "1000001", "-1000000.999999"),
            ("4533.04", "955.671", "3577.369"),
            ("-194.406", "-37893.4", "37698.994"),
            ("-93670.7", "805.483", "-94476.183"),
            ("508.77", "156.918", "351.852"),
            ("710.233", "5645.94", "-4935.707"),
            ("8249.8", "-8285.15", "16534.95"),
            ("309.046", "174.381", "134.665"),
            ("6346.2", "4780.7", "1565.5"),
            ("-78586.1", "-753.691", "-77832.409"),
            ("-25283.3", "69385.1", "-94668.4"),
            ("55960", "-3160.14", "59120.14"),
            ("90505", "-99802.7", "190307.7"),
            ("-9199.8", "-58138.1", "48938.3"),
            ("643.213", "11178.3", "-10535.087"),
            ("-38046.6", "242.139", "-38288.739")
        ]
        self.test_counter += 1
        failed: bool = False
        for n in list_numbers:
            a = DecimalNumber(n[0])
            b = DecimalNumber(n[1])
            c = DecimalNumber(n[2])
            cc = a - b
            aa = DecimalNumber(n[0])
            aa -= b

            if not self.assertEqual(c, cc, "Incorrect subtruction for ({0} - {1})".format(str(a), str(b))):
                failed = True
            if not self.assertEqual(aa, cc, "Incorrect subtruction from itself for ({0} - {1})".format(str(a), str(b))):
                failed = True

        # Subtruction with integers
        if sys.implementation.name == "cpython":
            one_int: int = 1
            minus_one_int: int = -1
            three = DecimalNumber(3)
            minus_three = DecimalNumber(-3)
            if not self.assertEqual(one_int - three, DecimalNumber("-2"), "Incorrect subtruction for ({0} - {1})".format(one_int, three)):
                failed = True
            if not self.assertEqual(one_int - minus_three, DecimalNumber("4"), "Incorrect subtruction for ({0} - {1})".format(one_int, minus_three)):
                failed = True
            if not self.assertEqual(minus_one_int - three, DecimalNumber("-4"), "Incorrect subtruction for ({0} - {1})".format(minus_one_int, three)):
                failed = True
            if not self.assertEqual(minus_one_int - minus_three, DecimalNumber("2"), "Incorrect subtruction for ({0} - {1})".format(minus_one_int, minus_three)):
                failed = True

        return failed

    def test_mul_imul(self) -> bool:
        """Tests that methods __mul__() and __imul__() of DecimalNumber work correctly.
        It tests a list of numbers and their known multiplication.
        """
        list_numbers = [
            ("0", "13579.2468", "0"),
            ("1.1", "1.1", "1.21"),
            ("1.1", "-1.1", "-1.21"),
            ("-1.1", "1.1", "-1.21"),
            ("-1.1", "-1.1", "1.21"),
            ("0.000001", "123456", "0.123456"),
            ("123456", "0.000001", "0.123456"),
            ("0.0000001", "123456", "0.0123456"),
            ("123456", "0.0000001", "0.0123456"),
            ("0.00001", "123456", "1.23456"),
            ("123456", "0.00001", "1.23456"),
            ("4533.04", "955.671", "4332094.86984"),
            ("-194.406", "-37893.4", "7366704.3204"),
            ("-93670.7", "805.483", "-75450156.4481"),
            ("508.77", "156.918", "79835.17086"),
            ("710.233", "5645.94", "4009932.90402"),
            ("8249.8", "-8285.15", "-68350830.47"),
            ("309.046", "174.381", "53891.750526"),
            ("6346.2", "4780.7", "30339278.34"),
            ("-78586.1", "-753.691", "59229636.2951"),
            ("-25283.3", "69385.1", "-1754284298.83"),
            ("55960", "-3160.14", "-176841434.4"),
            ("90505", "-99802.7", "-9032643363.5"),
            ("-9199.8", "-58138.1", "534858892.38"),
            ("643.213", "11178.3", "7190027.8779"),
            ("-38046.6", "242.139", "-9212565.6774")
        ]
        self.test_counter += 1
        failed: bool = False
        for n in list_numbers:
            a = DecimalNumber(n[0])
            b = DecimalNumber(n[1])
            c = DecimalNumber(n[2])
            cc = a * b
            aa = DecimalNumber(n[0])
            aa *= b

            if not self.assertEqual(c, cc, "Incorrect multiplication for ({0} - {1})".format(str(a), str(b))):
                failed = True
            if not self.assertEqual(aa, cc, "Incorrect multiplication by itself for ({0} - {1})".format(str(a), str(b))):
                failed = True

        # Multiplication with integers
        if sys.implementation.name == "cpython":
            one_int: int = 1
            minus_one_int: int = -1
            three = DecimalNumber(3)
            minus_three = DecimalNumber(-3)
            if not self.assertEqual(one_int * three, DecimalNumber("3"), "Incorrect multiplication for ({0} * {1})".format(one_int, three)):
                failed = True
            if not self.assertEqual(one_int * minus_three, DecimalNumber("-3"), "Incorrect multiplication for ({0} * {1})".format(one_int, minus_three)):
                failed = True
            if not self.assertEqual(minus_one_int * three, DecimalNumber("-3"), "Incorrect multiplication for ({0} * {1})".format(minus_one_int, three)):
                failed = True
            if not self.assertEqual(minus_one_int * minus_three, DecimalNumber("3"), "Incorrect multiplication for ({0} * {1})".format(minus_one_int, minus_three)):
                failed = True

        return failed

    def test_truediv(self) -> bool:
        """Tests that method __truediv__() of DecimalNumber works correctly.
        It multiplies two numbers and test that the result divided by one of the numbers
        return the other number.
        """
        self.test_counter += 1
        failed: bool = False
        # Creates 100 random multiplications and checks them
        for _ in range(0, 100):
            a = (random.randrange(0, 990) * 1000 +
                 random.randrange(0, 1000)) / 1000
            if random.randrange(0, 2) == 0:
                a = -a

            zero: bool = True
            while zero:
                b = (random.randrange(0, 990) * 1000 +
                     random.randrange(0, 1000)) / 1000
                if random.randrange(0, 2) == 0:
                    b = -b
                zero = (b == 0.0)

            aa = DecimalNumber(str(a))
            bb = DecimalNumber(str(b))
            cc = aa * bb

            aa2 = cc / bb

            if not self.assertEqual(aa, aa2, "Incorrect division for ({0} / {1})".format(str(a), str(b))):
                failed = True

        list_numbers = [
            ("0", "1", "0"),
            ("0", "-1", "0"),
            ("10", "0.125", "80"),
            ("-10", "0.125", "-80"),
            ("10", "-0.125", "-80"),
            ("-10", "-0.125", "80"),
            ("12345", "181", "68.2044198895027624309392265193370165745856353591160220994475138121546961325966850828729281767955801105")
        ]
        scale = DecimalNumber.get_scale()
        DecimalNumber.set_scale(100)
        self.test_counter += 1
        failed: bool = False
        for n in list_numbers:
            a = DecimalNumber(n[0])
            b = DecimalNumber(n[1])
            c = DecimalNumber(n[2])

            cc = a / b

            if not self.assertEqual(c, cc, "Incorrect division for ({0} / {1})".format(str(a), str(b))):
                failed = True

        DecimalNumber.set_scale(scale)

        if not self.assertRaises(DecimalNumberExceptionDivisionByZeroError, lambda: DecimalNumber(1) / DecimalNumber(0)):
            failed = True

        # Division with integers
        if sys.implementation.name == "cpython":
            one_int: int = 1
            minus_one_int: int = -1
            five = DecimalNumber(5)
            minus_five = DecimalNumber(-5)
            if not self.assertEqual(one_int / five, DecimalNumber("0.2"), "Incorrect division for ({0} / {1})".format(one_int, five)):
                failed = True
            if not self.assertEqual(one_int / minus_five, DecimalNumber("-0.2"), "Incorrect division for ({0} / {1})".format(one_int, minus_five)):
                failed = True
            if not self.assertEqual(minus_one_int / five, DecimalNumber("-0.2"), "Incorrect division for ({0} / {1})".format(minus_one_int, five)):
                failed = True
            if not self.assertEqual(minus_one_int / minus_five, DecimalNumber("0.2"), "Incorrect division for ({0} / {1})".format(minus_one_int, minus_five)):
                failed = True

        return failed

    @staticmethod
    def self_division_zero():
        a = DecimalNumber(1)
        a /= 0

    def test_itruediv(self) -> bool:
        """Tests that method __itruediv__() of DecimalNumber works correctly.
        It multiplies two numbers and test that the result divided by one of the numbers
        return the other number.
        """
        self.test_counter += 1
        failed: bool = False
        # Creates 100 random divisions to itself and checks them
        for _ in range(0, 100):
            a = (random.randrange(0, 990) * 1000 +
                 random.randrange(0, 1000)) / 1000
            if random.randrange(0, 2) == 0:
                a = -a

            b = (random.randrange(0, 990) * 1000 +
                 random.randrange(0, 1000)) / 1000
            if random.randrange(0, 2) == 0:
                b = -b

            aa = DecimalNumber(str(a))
            bb = DecimalNumber(str(b))
            cc = aa * bb
            aa2 = cc.clone()
            aa2 /= bb

            if not self.assertEqual(aa2, aa, "Incorrect division of itself for ({0} /= {1})".format(str(a), str(b))):
                failed = True

        list_numbers = [
            ("0", "1", "0"),
            ("0", "-1", "0"),
            ("10", "0.125", "80"),
            ("-10", "0.125", "-80"),
            ("10", "-0.125", "-80"),
            ("-10", "-0.125", "80"),
            ("12345", "181", "68.2044198895027624309392265193370165745856353591160220994475138121546961325966850828729281767955801105")
        ]
        scale = DecimalNumber.get_scale()
        DecimalNumber.set_scale(100)
        self.test_counter += 1
        failed: bool = False
        for n in list_numbers:
            a = DecimalNumber(n[0])
            b = DecimalNumber(n[1])
            c = DecimalNumber(n[2])

            aa2 = a.clone()
            aa2 /= b

            if not self.assertEqual(c, aa2, "Incorrect division of itself for ({0} / {1})".format(str(a), str(b))):
                failed = True

        DecimalNumber.set_scale(scale)

        if not self.assertRaises(DecimalNumberExceptionDivisionByZeroError, lambda: TestDecimalNumber.self_division_zero()):
            failed = True

        return failed

    def test_neg(self) -> bool:
        """Tests that method __neg__() of DecimalNumber works correctly.
        Given a number n, it tests that -n returns the correct result.
        """
        self.test_counter += 1
        failed: bool = False
        n = DecimalNumber(12345)
        n2 = -n
        if not self.assertTrue((n._number == n2._number and n._is_positive and not n2._is_positive), "Error on __neg__ method"):
            failed = True
        return failed

    def test_pos(self) -> bool:
        """Tests that method __pos__() of DecimalNumber works correctly.
        Given a number n, it tests that +n returns the correct result.
        """
        self.test_counter += 1
        failed: bool = False
        n = DecimalNumber(-12345)
        n2 = +n
        if not self.assertTrue((n._number == n2._number and n._is_positive == n2._is_positive), "Error on __pos__ method"):
            failed = True
        return failed

    def test_abs(self) -> bool:
        """Tests that method __abs__() of DecimalNumber works correctly.
        It tests that abs(n), being n either negative or positive, returns +n.
        """
        self.test_counter += 1
        failed: bool = False
        n = DecimalNumber(12345)
        n2 = abs(n)
        if not self.assertTrue((n._number == n2._number and n2._is_positive), "Error on __abs__ method"):
            failed = True
        n = DecimalNumber(-12345)
        n2 = abs(n)
        if not self.assertTrue((n._number == n2._number and n2._is_positive), "Error on __abs__ method"):
            failed = True
        return failed

    def test_compare(self) -> bool:
        """Tests that methods:
        __lt__(), __le__(), __eq__(), __ne__(), __ge__(), __gt__()
        of DecimalNumber works correctly.
        Two numbers are created and they are compare for: <, <=, ==, !=, >=, >
        """
        self.test_counter += 1
        failed: bool = False
        n1 = DecimalNumber("12.3")
        n1b: int = 12
        n2 = DecimalNumber("-0.98765")

        if not self.assertFalse(n1 < n2, "Error evaluating {0} < {1}".format(n1, n2)):
            failed = True
        if not self.assertTrue(n2 < n1, "Error evaluating {0} < {1}".format(n2, n1)):
            failed = True
        if sys.implementation.name == "cpython":
            if not self.assertFalse(n1b < n2, "Error evaluating {0} < {1}".format(n1b, n2)):
                failed = True
            if not self.assertTrue(n2 < n1b, "Error evaluating {0} < {1}".format(n2, n1b)):
                failed = True

        if not self.assertFalse(n1 <= n2, "Error evaluating {0} <= {1}".format(n1, n2)):
            failed = True
        if not self.assertTrue(n2 <= n1, "Error evaluating {0} <= {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n1 <= n1, "Error evaluating {0} <= {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n2 <= n2, "Error evaluating {0} <= {1}".format(n2, n2)):
            failed = True
        if sys.implementation.name == "cpython":
            if not self.assertFalse(n1b <= n2, "Error evaluating {0} <= {1}".format(n1b, n2)):
                failed = True
            if not self.assertTrue(n2 <= n1b, "Error evaluating {0} <= {1}".format(n1, n1b)):
                failed = True

        if not self.assertFalse(n1 == n2, "Error evaluating {0} == {1}".format(n1, n2)):
            failed = True
        if not self.assertFalse(n2 == n1, "Error evaluating {0} == {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n1 == n1, "Error evaluating {0} == {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n2 == n2, "Error evaluating {0} == {1}".format(n2, n2)):
            failed = True
        if sys.implementation.name == "cpython":
            if not self.assertFalse(n1b == n2, "Error evaluating {0} == {1}".format(n1b, n2)):
                failed = True
            if not self.assertFalse(n2 == n1b, "Error evaluating {0} == {1}".format(n1, n1b)):
                failed = True


        if not self.assertTrue(n1 != n2, "Error evaluating {0} != {1}".format(n1, n2)):
            failed = True
        if not self.assertTrue(n2 != n1, "Error evaluating {0} != {1}".format(n1, n1)):
            failed = True
        if not self.assertFalse(n1 != n1, "Error evaluating {0} != {1}".format(n1, n1)):
            failed = True
        if not self.assertFalse(n2 != n2, "Error evaluating {0} != {1}".format(n2, n2)):
            failed = True
        if sys.implementation.name == "cpython":
            if not self.assertTrue(n1b != n2, "Error evaluating {0} != {1}".format(n1b, n2)):
                failed = True
            if not self.assertTrue(n2 != n1b, "Error evaluating {0} != {1}".format(n1, n1b)):
                failed = True

        if not self.assertTrue(n1 >= n2, "Error evaluating {0} >= {1}".format(n1, n2)):
            failed = True
        if not self.assertFalse(n2 >= n1, "Error evaluating {0} >= {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n1 >= n1, "Error evaluating {0} >= {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n2 >= n2, "Error evaluating {0} >= {1}".format(n2, n2)):
            failed = True
        if sys.implementation.name == "cpython":
            if not self.assertTrue(n1b >= n2, "Error evaluating {0} >= {1}".format(n1b, n2)):
                failed = True
            if not self.assertFalse(n2 >= n1b, "Error evaluating {0} >= {1}".format(n1, n1b)):
                failed = True

        if not self.assertTrue(n1 > n2, "Error evaluating {0} > {1}".format(n1, n2)):
            failed = True
        if not self.assertFalse(n2 > n1, "Error evaluating {0} > {1}".format(n2, n1)):
            failed = True
        if sys.implementation.name == "cpython":
            if not self.assertTrue(n1b > n2, "Error evaluating {0} > {1}".format(n1b, n2)):
                failed = True
            if not self.assertFalse(n2 > n1b, "Error evaluating {0} > {1}".format(n2, n1b)):
                failed = True

        return failed

    def test_to_string_thousands(self) -> bool:
        """Tests that method _to_string_thousands() of DecimalNumber works correctly.
        Indirectly, it checks __str__() also.
        It tests a list of numbers and their corresponding representation separating
        the thousands with ','.
        """
        self.test_counter += 1
        failed: bool = False
        list_numbers = [
            ("1", "1"),
            ("1.1", "1.1"),
            ("1.23456789012345", "1.23456789012345"),
            ("12.3456789012345", "12.3456789012345"),
            ("123.456789012345", "123.456789012345"),
            ("1234.56789012345", "1,234.56789012345"),
            ("12345.6789012345", "12,345.6789012345"),
            ("123456.789012345", "123,456.789012345"),
            ("1234567.89012345", "1,234,567.89012345"),
            ("12345678.9012345", "12,345,678.9012345"),
            ("123456789.012345", "123,456,789.012345"),
            ("1234567890.12345", "1,234,567,890.12345"),
        ]
        for n in list_numbers:
            number = DecimalNumber(n[0])
            if not self.assertEqual(n[1], number.to_string_thousands(), "Error in to_string_thousands"):
                failed = True
        return failed

    def test_to_string_max_length(self) -> bool:
        """Tests that method __to_string_max_length() of DecimalNumber works correctly.
        That functions limits the length of the string returned.
        It tests a list of numbers and their known conversion.
        """
        self.test_counter += 1
        failed: bool = False
        list_numbers = [
            ("123",             "123"),
            ("123.45",          "123.45"),
            ("123.456789",      "123.4567"),
            ("0.0067",          "0.0067"),
            ("0.00678901234",   "0.006789"),
            ("0.0000001",       "0"),
            ("123.00001",       "123"),
            ("12345678",        "12345678"),
            ("1234567.8",       "1234567"),
            ("12345678.5",      "12345678"),
            ("123456789",       "Overflow"),
            ("123456789.123",   "Overflow"),
        ]
        for n in list_numbers:
            number = DecimalNumber(n[0])
            if not self.assertEqual(n[1], number.to_string_max_length(8), "Error in to_string_max_length"):
                failed = True
        for n in list_numbers:
            number = DecimalNumber('-'+n[0])
            result: str = n[1]
            if result != "0" and result != "Overflow":
                result = '-' + result
            if not self.assertEqual(result, number.to_string_max_length(9), "Error in to_string_max_length"):
                failed = True
        return failed

    def test_make_integer_comparable(self) -> bool:
        """Tests that method _make_integercomparable() of DecimalNumber works correctly.
        It tests a list of numbers and their known conversions needed for comparison.
        """
        self.test_counter += 1
        failed: bool = False
        list_numbers = [
            ("123", "123", 123, 123),
            ("123", "123.45", 12300, 12345),
            ("123.45", "123", 12345, 12300),
            ("-123", "123", -123, 123),
            ("123", "-123.45", 12300, -12345),
            ("-123.45", "123", -12345, 12300)
        ]
        for n in list_numbers:
            n1 = DecimalNumber(n[0])
            n2 = DecimalNumber(n[1])
            a, b = n1._make_integer_comparable(n1, n2)
            if not self.assertTrue(
                n[2] == a and n[3] == b,
                "Error in _make_integer_comparable for numbers {0} and {1}, {2} != {3} or {4} != {5}".format(
                    n1, n2, n[2], a, n[3], b)
            ):
                failed = True
        return failed

    def test_reduce_to_scale(self) -> bool:
        """Tests that method __reduce_to_scale() of DecimalNumber works correctly.
        That functions reduces, if needed, the number of decimals of a number to
        not to be greater than the scale of DecimalNumber class.
        It tests a list of numbers and their known reduction.
        """
        self.test_counter += 1
        failed: bool = False
        list_numbers = [    # reduced_scale, number, reduced_number
            (3, "123.456789", "123.457"),
            (3, "123.4577", "123.458"),
            (3, "123.4578", "123.458"),
            (3, "123.4579", "123.458"),
            (3, "123.4580", "123.458"),
            (3, "123.4581", "123.458"),
            (3, "123.4582", "123.458"),
            (3, "123.4583", "123.458"),
            (3, "123.4584", "123.458"),
            (3, "123.4585", "123.458"),
            (3, "123.4586", "123.459"),
            (3, "123.4587", "123.459"),
            (3, "123.4588", "123.459"),
            (3, "123.4589", "123.459"),
            (3, "123.4590", "123.459"),
            (3, "123.4591", "123.459"),
            (3, "123.4592", "123.459"),
            (3, "123.4593", "123.459"),
            (3, "123.4594", "123.459"),
            (3, "123.4595", "123.46"),
            (3, "123.4596", "123.46"),
            (3, "123.4597", "123.46"),
            (3, "123.4598", "123.46"),
            (3, "123.4599", "123.46"),
            (3, "123.4600", "123.46"),
            (3, "123.4601", "123.46"),
            (3, "123.4602", "123.46"),
            (3, "123.4603", "123.46"),
            (3, "123.4604", "123.46"),
            (3, "123.4605", "123.46"),
            (3, "123.4606", "123.461"),
            (3, "0.123456", "0.123"),
            (7, "0.0000123456", "0.0000123"),
            (3, "123", "123"),
            (3, "123.1", "123.1"),
            (3, "123.12", "123.12"),
            (3, "123.123", "123.123"),
            (3, "-123.4592", "-123.459"),
            (3, "-123.4593", "-123.459"),
            (3, "-123.4594", "-123.459"),
            (3, "-123.4595", "-123.46"),
            (3, "-123.4596", "-123.46"),
            (3, "-123.4597", "-123.46"),
            (7, "-0.0000123456", "-0.0000123"),
            (3, "-123", "-123"),
            (3, "-123.1", "-123.1"),
            (3, "-123.12", "-123.12"),
            (3, "-123.123", "-123.123"),
            (0, "1.1", "1"),
            (0, "1.2", "1"),
            (0, "1.3", "1"),
            (0, "1.4", "1"),
            (0, "1.5", "2"),
            (0, "1.6", "2"),
            (0, "1.7", "2"),
            (0, "1.8", "2"),
            (0, "1.9", "2"),
            (0, "2.0", "2"),
            (0, "2.1", "2"),
            (0, "2.2", "2"),
            (0, "2.3", "2"),
            (0, "2.4", "2"),
            (0, "2.5", "2"),
            (0, "2.6", "3"),
            (0, "2.7", "3"),
            (0, "2.8", "3"),
            (0, "2.9", "3"),
            (0, "3.0", "3"),
            (0, "3.1", "3")
        ]
        current_scale = DecimalNumber.get_scale()
        for n in list_numbers:
            s: int = n[0]
            DecimalNumber.set_scale(s)
            n1 = DecimalNumber(n[1])
            if not self.assertTrue(
                str(n1) == n[2],
                "Error in _reduce_to_scale for numbers {0} and {1}; {2} != {3}".format(
                    n[1], n[2], n1, n[2])
            ):
                failed = True
        DecimalNumber.set_scale(current_scale)

        return failed

    def test_pow(self) -> bool:
        """Tests that method __pow__() of DecimalNumber works correctly.
        It tests a list of numbers and exponents by calculating number ** exponent
        and checking the expected result.
        """
        self.test_counter += 1
        failed: bool = False
        list_numbers = [    # base, exponent, result
            ("1.1234567", 15, "5.7325134061519317"),
            ("-1.1234567", 15, "-5.7325134061519317"),
            ("1.1234567", 22, "12.9490959609285781"),
            ("-1.1234567", 22, "12.9490959609285781"),
            ("1.1234567", 29, "29.2505353804126336"),
            ("-1.1234567", 29, "-29.2505353804126336"),
            ("1.1234567", 36, "66.0736334507337083"),
            ("-1.1234567", 36, "66.0736334507337083"),
            ("1.1234567", 43, "149.2528249689879598"),
            ("-1.1234567", 43, "-149.2528249689879598"),
            ("1.1234567", 50, "337.145160600759872"),
            ("-1.1234567", 50, "337.145160600759872"),
            ("1.1234567", 57, "761.5725822283771598"),
            ("-1.1234567", 57, "-761.5725822283771598"),
            ("1.1234567", 64, "1720.3058675631219436"),
            ("-1.1234567", 64, "1720.3058675631219436"),
            ("1.1234567", 71, "3885.9753450061016559"),
            ("-1.1234567", 71, "-3885.9753450061016559"),
            ("1.1234567", 78, "8777.9764440297753385"),
            ("-1.1234567", 78, "8777.9764440297753385"),
            ("1.1234567", -1, "0.8901099615143156"),
            ("-1.1234567", -1, "-0.8901099615143156"),
            ("1.1234567", -4, "0.6277325453061032"),
            ("-1.1234567", -4, "0.6277325453061032"),
            ("1.1234567", -7, "0.4426960324835568"),
            ("-1.1234567", -7, "-0.4426960324835568"),
            ("1.1234567", -10, "0.3122026707745671"),
            ("-1.1234567", -10, "0.3122026707745671"),
            ("1.1234567", -13, "0.2201747937336509"),
            ("-1.1234567", -13, "-0.2201747937336509"),
            ("1.1234567", -16, "0.1552739432862173"),
            ("-1.1234567", -16, "0.1552739432862173"),
            ("1.1234567", -19, "0.1095038948591804"),
            ("-1.1234567", -19, "-0.1095038948591804"),
            ("1.1234567", -22, "0.0772254683274654"),
            ("-1.1234567", -22, "0.0772254683274654"),
            ("1.1234567", -25, "0.054461742808926"),
            ("-1.1234567", -25, "-0.054461742808926"),
            ("1.1234567", -28, "0.0384080730622221"),
            ("-1.1234567", -28, "0.0384080730622221")
        ]
        current_scale = DecimalNumber.get_scale()
        for n in list_numbers:
            DecimalNumber.set_scale(16)
            n1 = DecimalNumber(n[0])
            e: int = n[1]
            r = n1 ** e
            if not self.assertTrue(
                n[2] == str(r),
                "Error in power (n ** e) for n = {0} and e = {1}; {2} != {3}".format(
                    n1, e, r, n[2])
            ):
                failed = True

        # 19th Mersenne prime number: 2**4253 - 1
        m19 = "190797007524439073807468042969529173669356994749940177394741882673528979787005053706368049835514900244303495954950709725762186311224148828811920216904542206960744666169364221195289538436845390250168663932838805192055137154390912666527533007309292687539092257043362517857366624699975402375462954490293259233303137330643531556539739921926201438606439020075174723029056838272505051571967594608350063404495977660656269020823960825567012344189908927956646011998057988548630107637380993519826582389781888135705408653045219655801758081251164080554609057468028203308718724654081055323215860189611391296030471108443146745671967766308925858547271507311563765171008318248647110097614890313562856541784154881743146033909602737947385055355960331855614540900081456378659068370317267696980001187750995491090350108417050917991562167972281070161305972518044872048331306383715094854938415738549894606070722584737978176686422134354526989443028353644037187375385397838259511833166416134323695660367676897722287918773420968982326089026150031515424165462111337527431154890666327374921446276833564519776797633875503548665093914556482031482248883127023777039667707976559857333357013727342079099064400455741830654320379350833236245819348824064783585692924881021978332974949906122664421376034687815350484991"
        n = DecimalNumber(2)
        p = n ** 4253 - DecimalNumber(1)
        DecimalNumber.set_scale(current_scale)
        if not self.assertTrue(
            m19 == str(p),
            "Error in power (n ** e). Calculated 19th Mersenne prime number is incorrect"
        ):
            print("19th Mersenne prime number:")
            print(m19)
            print(p)
            failed = True

        return failed

    def test_exp(self) -> bool:
        """Tests exp()
        It tests a list of numbers calculating exp(number)
        and checking the expected result.
        """
        self.test_counter += 1
        failed: bool = False

        list_numbers = [
            ('-3',    '0.04978706836786394297934241565006177663169959218842'),
            ('-2.75', '0.06392786120670757270243002555795174930863409507877'),
            ('-2.50', '0.08208499862389879516952867446715980783780412101544'),
            ('-2.25', '0.10539922456186433678321768924069809726849107337728'),
            ('-2.00', '0.13533528323661269189399949497248440340763154590958'),
            ('-1.75', '0.17377394345044512668071725866637101601472085333991'),
            ('-1.50', '0.22313016014842982893328047076401252134217162936108'),
            ('-1.25', '0.28650479686019010032488542664783760279315079232825'),
            ('-1.00', '0.36787944117144232159552377016146086744581113103177'),
            ('-0.75',  '0.47236655274101470713804655094326791297020357913648'),
            ('-0.50',  '0.60653065971263342360379953499118045344191813548719'),
            ('-0.25',  '0.77880078307140486824517026697832064729677229042614'),
            ('0',     '1'),
            ('0.25',   '1.28402541668774148407342056806243645833628086528146'),
            ('0.50',   '1.64872127070012814684865078781416357165377610071015'),
            ('0.75',   '2.1170000166126746685453698198370956101344915847024'),
            ('1.00',  '2.71828182845904523536028747135266249775724709369996'),
            ('1.25',  '3.49034295746184137613054602967226548265173439876235'),
            ('1.50',  '4.48168907033806482260205546011927581900574986836967'),
            ('1.75',  '5.75460267600573043686649970484269237092292230833653'),
            ('2.00',  '7.38905609893065022723042746057500781318031557055185'),
            ('2.25',  '9.48773583635852572055036904451173842377022496766239'),
            ('2.50',  '12.18249396070347343807017595116796618318276779006316'),
            ('2.75',  '15.64263188418817161021269804615665884503803503410762'),
            ('3.00',  '20.08553692318766774092852965458171789698790783855415')
        ]

        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(50)
        for n in list_numbers:
            e = str(DecimalNumber(n[0]).exp())
            if not self.assertEqual(e, n[1], "Error calculating exp({0})".format(n[0])):
                failed = True
        DecimalNumber.set_scale(current_scale)

        return failed

    def test_ln(self) -> bool:
        """Tests ln()
        It tests a list of numbers calculating ln(number)
        and checking the expected result.
        """
        self.test_counter += 1
        failed: bool = False

        list_numbers = [
            ('0.25', '-1.38629436111989061883446424291635313615100026872051'),
            ('0.50', '-0.69314718055994530941723212145817656807550013436026'),
            ('0.75', '-0.28768207245178092743921900599382743150350971089776'),
            ('1.00',  '0'),
            ('1.25',  '0.22314355131420975576629509030983450337460108554801'),
            ('1.50',  '0.40546510810816438197801311546434913657199042346249'),
            ('1.75',  '0.55961578793542268627088850052682659348608446086135'),
            ('2.00',  '0.69314718055994530941723212145817656807550013436026'),
            ('2.25',  '0.81093021621632876395602623092869827314398084692499'),
            ('2.50',  '0.91629073187415506518352721176801107145010121990826'),
            ('2.75',  '1.01160091167847992522747933504877616367070658521691'),
            ('3.00',  '1.09861228866810969139524523692252570464749055782275')
        ]

        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(50)
        for n in list_numbers:
            e = str(DecimalNumber(n[0]).ln())
            if not self.assertEqual(e, n[1], "Error calculating ln({0})".format(n[0])):
                failed = True
        DecimalNumber.set_scale(current_scale)

        # Check for ln(0)
        if not self.assertRaises(DecimalNumberExceptionMathDomainError, lambda: DecimalNumber(0).ln()):
            failed = True
        # Check for ln() of a negative number
        if not self.assertRaises(DecimalNumberExceptionMathDomainError, lambda: DecimalNumber(-1).ln()):
            failed = True

        return failed

    def test_e(self) -> bool:
        """Tests that method e() works correctly.
        It tests it with scale = 100, meaning 100 decimals.
        'e' with up to 100 decimals is precalculated. It tests that is returned correctly.
        'e' with 200 decimals is calculated and checked.
        """
        self.test_counter += 1
        failed: bool = False
        # 'e' with 100 decimals is already calculated. It is checked and the it is calculated with 200 decimals
        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(100)
        if not self.assertEqual(
            str(DecimalNumber.e()),
            "2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274",
            "Value of 'e' with one hundred decimals is incorrect"
        ):
            failed = True
        DecimalNumber.set_scale(200)
        if not self.assertEqual(
            str(DecimalNumber.e()),
            "2.71828182845904523536028747135266249775724709369995957496696762772407663035354759457138217852516642742746639193200305992181741359662904357290033429526059563073813232862794349076323382988075319525101901",
            "Value of 'e' with two hundred decimals is incorrect"
        ):
            failed = True
        DecimalNumber.set_scale(current_scale)
        return failed

    def test_ln2(self) -> bool:
        """Tests that method ln(2) works correctly.
        It tests it with scale = 100, meaning 100 decimals.
        ln(2) with up to 100 decimals is precalculated. It tests that is returned correctly.
        ln(2) with 200 decimals is calculated and checked.
        """
        self.test_counter += 1
        failed: bool = False
        # ln(2) with 100 decimals is already calculated. It is checked and the it is calculated with 200 decimals
        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(100)
        if not self.assertEqual(
            str(DecimalNumber.ln2()),
            "0.6931471805599453094172321214581765680755001343602552541206800094933936219696947156058633269964186875",
            "Value of ln(2) with one hundred decimals is incorrect"
        ):
            failed = True
        DecimalNumber.set_scale(200)
        if not self.assertEqual(
            str(DecimalNumber.ln2()),
            "0.69314718055994530941723212145817656807550013436025525412068000949339362196969471560586332699641868754200148102057068573368552023575813055703267075163507596193072757082837143519030703862389167347112335",
            "Value of ln(2) with two hundred decimals is incorrect"
        ):
            failed = True
        DecimalNumber.set_scale(current_scale)
        return failed

    def test_sin(self) -> bool:
        """Tests sin()
        It tests a list of numbers calculating sin(number)
        and checking the expected result.
        """
        self.test_counter += 1
        failed: bool = False

        list_numbers = [
            ('0',    '0'),
            ('0.2',  '0.19866933079506121545941262711838975037020672954021'),
            ('0.4',  '0.38941834230865049166631175679570526459306018344396'),
            ('0.6',  '0.56464247339503535720094544565865790710988808499415'),
            ('0.8',  '0.71735609089952276162717461058138536619278523779142'),
            ('1.0',  '0.84147098480789650665250232163029899962256306079837'),
            ('1.2',  '0.93203908596722634967013443549482599541507058820873'),
            ('1.4',  '0.98544972998846018065947457880609751735626167234737'),
            ('1.6',  '0.99957360304150516434211382554623417197949791475492'),
            ('1.8',  '0.97384763087819518653237317884335760670293947136523'),
            ('2.0',  '0.90929742682568169539601986591174484270225497144789'),
            ('2.2',  '0.80849640381959018430403691041611906515855960597558'),
            ('2.4',  '0.67546318055115092656577152534128337425336495789353'),
            ('2.6',  '0.51550137182146423525772693520936824389387858775426'),
            ('2.8',  '0.33498815015590491954385375271242210603030652888359'),
            ('3.0',  '0.14112000805986722210074480280811027984693326425227'),
            ('3.2', '-0.05837414342757990913721741461909518512512509908293'),
            ('3.4', '-0.25554110202683131924990242936373907581092037943434'),
            ('3.6', '-0.44252044329485238426672734749269391091848782847472'),
            ('3.8', '-0.61185789094271907573358608611888243771607580529324'),
            ('4.0', '-0.75680249530792825137263909451182909413591288733647'),
            ('4.2', '-0.87157577241358806001857709790882123480771186014449'),
            ('4.4', '-0.95160207388951595403539233338038768420517733027774'),
            ('4.6', '-0.99369100363346445613810465990882952642152580067382'),
            ('4.8', '-0.99616460883584067178159646650363455682194459993781'),
            ('5.0', '-0.9589242746631384688931544061559939733524615439646'),
            ('5.2', '-0.88345465572015326467308444042180321999386557565688'),
            ('5.4', '-0.77276448755598736235846978273423230445709536392994'),
            ('5.6', '-0.6312666378723213114636691537166711930720248256872'),
            ('5.8', '-0.46460217941375721141822652670258931885263532874474'),
            ('6.0', '-0.2794154981989258728115554466118947596279948643182'),
            ('6.2', '-0.08308940281749657800057928909836718528109967293846')
        ]

        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(50)
        for n in list_numbers:
            s = str(DecimalNumber(n[0]).sin())
            if not self.assertEqual(s, n[1], "Error calculating sin({0})".format(n[0])):
                failed = True
        DecimalNumber.set_scale(current_scale)

        return failed

    def test_cos(self) -> bool:
        """Tests cos()
        It tests a list of numbers calculating cos(number)
        and checking the expected result.
        """
        self.test_counter += 1
        failed: bool = False

        list_numbers = [
            ('0',    '1'),
            ('0.2',  '0.98006657784124163112419651674816887739352436080657'),
            ('0.4',  '0.92106099400288508279852673205180161402585956931985'),
            ('0.6',  '0.82533561490967829724095249895537603887809103918847'),
            ('0.8',  '0.69670670934716542092074998164232492610178601370806'),
            ('1.0',  '0.54030230586813971740093660744297660373231042061792'),
            ('1.2',  '0.36235775447667357763837335562307602033994778557665'),
            ('1.4',  '0.16996714290024093861674803520364980292818392102853'),
            ('1.6', '-0.02919952230128872620577046294649852444486472109385'),
            ('1.8', '-0.22720209469308705531667430653058073247695158653826'),
            ('2.0', '-0.41614683654714238699756822950076218976600077107554'),
            ('2.2', '-0.58850111725534570852414261265492841629376036669873'),
            ('2.4', '-0.73739371554124549960882222733478290843301289199228'),
            ('2.6', '-0.85688875336894723379770215164520111235392263823324'),
            ('2.8', '-0.94222234066865815258678811736615401246341423446825'),
            ('3.0', '-0.98999249660044545727157279473126130239367909661559'),
            ('3.2', '-0.99829477579475308466166072228358269144701258595166'),
            ('3.4', '-0.96679819257946101428220153976569391119594442684891'),
            ('3.6', '-0.89675841633414700587029172526593922995037606912552'),
            ('3.8', '-0.7909677119144166999965681743507251864017333039176'),
            ('4.0', '-0.65364362086361191463916818309775038142413359664622'),
            ('4.2', '-0.49026082134069957765554488137713364673125516102182'),
            ('4.4', '-0.30733286997841968311913974221771237118950331487701'),
            ('4.6', '-0.11215252693505451742990782122918964248775134505344'),
            ('4.8',  '0.0874989834394465693202152576494876339574498905961'),
            ('5.0',  '0.28366218546322626446663917151355730833442259225222'),
            ('5.2',  '0.46851667130037695863909392660864570409989349454139'),
            ('5.4',  '0.63469287594263436240675183898074094918956609491144'),
            ('5.6',  '0.77556587851024979765580966215728192307775648420884'),
            ('5.8',  '0.88551951694131900416465810176148620005410899252792'),
            ('6.0',  '0.96017028665036602054565229792292440545193767921101'),
            ('6.2',  '0.99654209702321747513940262386926395252788462409872')
        ]

        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(50)
        for n in list_numbers:
            c = str(DecimalNumber(n[0]).cos())
            if not self.assertEqual(c, n[1], "Error calculating cos({0})".format(n[0])):
                failed = True
        DecimalNumber.set_scale(current_scale)

        return failed

    def test_tan(self) -> bool:
        """Tests tan()
        It tests a list of numbers calculating tan(number)
        and checking the expected result.
        """
        self.test_counter += 1
        failed: bool = False

        list_numbers = [
            ('0',     '0'),
            ('0.2',   '0.20271003550867248332135827164753448262687566965163'),
            ('0.4',   '0.42279321873816176198163542716529033394198977271569'),
            ('0.6',   '0.68413680834169231707092541746333574524265408075678'),
            ('0.8',   '1.02963855705036401274636117282036528416821960677231'),
            ('1.0',   '1.55740772465490223050697480745836017308725077238152'),
            ('1.2',   '2.57215162212631893540999423603336395652940930604339'),
            ('1.4',   '5.79788371548288964370772024360369904599369751893968'),
            ('1.6', '-34.23253273555741705801487543047619090177569941115324'),
            ('1.8',  '-4.28626167462806352545188895228026668020736003385825'),
            ('2.0',  '-2.18503986326151899164330610231368254343201774622766'),
            ('2.2',  '-1.3738230567687951601400367633334698743026332922337'),
            ('2.4',  '-0.916014289673410512730863247508105793993645549977'),
            ('2.6',  '-0.60159661308975872273608189269127978293417758666969'),
            ('2.8',  '-0.35552983165117587757735260363543503816953711960914'),
            ('3.0',  '-0.1425465430742778052956354105339134932260922849018'),
            ('3.2',   '0.05847385445957846762586774167681370216472247958237'),
            ('3.4',   '0.26431690086742526694892295392026530372697129599275'),
            ('3.6',   '0.49346672998490370894458164319649608827513552026627'),
            ('3.8',   '0.77355609050312607285870726589496034494206180873258'),
            ('4.0',   '1.15782128234957758313734241826732392311976276736714'),
            ('4.2',   '1.77777977450884096177623210090516337260894048546837'),
            ('4.4',   '3.0963237806497417682253024535177360615032120910449'),
            ('4.6',   '8.86017489564807389842749537123019978456538862298282'),
            ('4.8', '-11.38487065424289926455670693026324154897067456117154'),
            ('5.0',  '-3.38051500624658563698270587944734390870956920828546'),
            ('5.2',  '-1.88564187751976469674264091289219213894792190226543'),
            ('5.4',  '-1.21754082462055611296736395481594505143979759288247'),
            ('5.6',  '-0.81394328368970213470079115394423478782654579724762'),
            ('5.8',  '-0.52466622194680001367291294422548426757702824110572'),
            ('6.0',  '-0.29100619138474915705369958886817554283115557091234'),
            ('6.2',  '-0.0833777148659287977660811118347761394190004557363')
        ]

        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(50)
        for n in list_numbers:
            t = str(DecimalNumber(n[0]).tan())
            if not self.assertEqual(t, n[1], "Error calculating tan({0})".format(n[0])):
                failed = True
        DecimalNumber.set_scale(current_scale)

        return failed

    def test_asin(self) -> bool:
        """Tests asin()
        It tests a list of numbers calculating asin(number)
        and checking the expected result.
        """
        self.test_counter += 1
        failed: bool = False

        list_numbers = [
            ('-1',   '-1.57079632679489661923132169163975144209858469968756'),
            ('-0.9', '-1.1197695149986341866866770558453996158951621864033'),
            ('-0.8', '-0.92729521800161223242851246292242880405707410857224'),
            ('-0.7', '-0.77539749661075306374035335271498711355578873864116'),
            ('-0.6', '-0.64350110879328438680280922871732263804151059111531'),
            ('-0.5', '-0.52359877559829887307710723054658381403286156656252'),
            ('-0.4', '-0.41151684606748801938473789761733560485570113512703'),
            ('-0.3', '-0.30469265401539750797200296122752916695456003170678'),
            ('-0.2', '-0.20135792079033079145512555221762341024003808140223'),
            ('-0.1', '-0.10016742116155979634552317945269331856867597222963'),
            ( '0',    '0'),
            ( '0.1',  '0.10016742116155979634552317945269331856867597222963'),
            ( '0.2',  '0.20135792079033079145512555221762341024003808140223'),
            ( '0.3',  '0.30469265401539750797200296122752916695456003170678'),
            ( '0.4',  '0.41151684606748801938473789761733560485570113512703'),
            ( '0.5',  '0.52359877559829887307710723054658381403286156656252'),
            ( '0.6',  '0.64350110879328438680280922871732263804151059111531'),
            ( '0.7',  '0.77539749661075306374035335271498711355578873864116'),
            ( '0.8',  '0.92729521800161223242851246292242880405707410857224'),
            ( '0.9',  '1.1197695149986341866866770558453996158951621864033'),
            ( '1',    '1.57079632679489661923132169163975144209858469968756')
        ]

        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(50)
        for n in list_numbers:
            a = str(DecimalNumber(n[0]).asin())
            if not self.assertEqual(a, n[1], "Error calculating asin({0})".format(n[0])):
                failed = True
        DecimalNumber.set_scale(current_scale)

        return failed

    def test_acos(self) -> bool:
        """Tests acos()
        It tests a list of numbers calculating acos(number)
        and checking the expected result.
        """
        self.test_counter += 1
        failed: bool = False

        list_numbers = [
            ('-1',   '3.14159265358979323846264338327950288419716939937511'),
            ('-0.9', '2.69056584179353080591799874748515105799374688609086'),
            ('-0.8', '2.49809154479650885165983415456218024615565880825979'),
            ('-0.7', '2.34619382340564968297167504435473855565437343832871'),
            ('-0.6', '2.21429743558818100603413092035707408014009529080287'),
            ('-0.5', '2.09439510239319549230842892218633525613144626625007'),
            ('-0.4', '1.98231317286238463861605958925708704695428583481458'),
            ('-0.3', '1.87548898081029412720332465286728060905314473139433'),
            ('-0.2', '1.77215424758522741068644724385737485233862278108978'),
            ('-0.1', '1.67096374795645641557684487109244476066726067191718'),
            ('0',    '1.57079632679489661923132169163975144209858469968755'),
            ('0.1',  '1.47062890563333682288579851218705812352990872745792'),
            ('0.2',  '1.36943840600456582777619613942212803185854661828532'),
            ('0.3',  '1.26610367277949911125931873041222227514402466798078'),
            ('0.4',  '1.15927948072740859984658379402241583724288356456053'),
            ('0.5',  '1.04719755119659774615421446109316762806572313312504'),
            ('0.6',  '0.92729521800161223242851246292242880405707410857224'),
            ('0.7',  '0.79539883018414355549096833892476432854279596104639'),
            ('0.8',  '0.64350110879328438680280922871732263804151059111531'),
            ('0.9',  '0.45102681179626243254464463579435182620342251328425'),
            ('1.0',  '0')
        ]

        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(50)
        for n in list_numbers:
            a = str(DecimalNumber(n[0]).acos())
            if not self.assertEqual(a, n[1], "Error calculating acos({0})".format(n[0])):
                failed = True
        DecimalNumber.set_scale(current_scale)

        return failed

    def test_atan(self) -> bool:
        """Tests atan()
        It tests a list of numbers calculating acos(number)
        and checking the expected result.
        """
        self.test_counter += 1
        failed: bool = False

        list_numbers = [
            ('-1',   '-0.78539816339744830961566084581987572104929234984378'),
            ('-0.9', '-0.73281510178650659164079207273428025198575567935826'),
            ('-0.8', '-0.67474094222355266305652097360981361507400625484071'),
            ('-0.7', '-0.61072596438920861654375887649023609381850306612883'),
            ('-0.6', '-0.54041950027058415544357836460859991013514825146259'),
            ('-0.5', '-0.46364760900080611621425623146121440202853705428612'),
            ('-0.4', '-0.3805063771123648863035879168104331044974057136581'),
            ('-0.3', '-0.29145679447786709199560462143289119350316759901207'),
            ('-0.2', '-0.19739555984988075837004976519479029344758510378785'),
            ('-0.1', '-0.09966865249116202737844611987802059024327832250431'),
            ('0',     '0'),
            ('0.1',   '0.09966865249116202737844611987802059024327832250431'),
            ('0.2',   '0.19739555984988075837004976519479029344758510378785'),
            ('0.3',   '0.29145679447786709199560462143289119350316759901207'),
            ('0.4',   '0.3805063771123648863035879168104331044974057136581'),
            ('0.5',   '0.46364760900080611621425623146121440202853705428612'),
            ('0.6',   '0.54041950027058415544357836460859991013514825146259'),
            ('0.7',   '0.61072596438920861654375887649023609381850306612883'),
            ('0.8',   '0.67474094222355266305652097360981361507400625484071'),
            ('0.9',   '0.73281510178650659164079207273428025198575567935826'),
            ('1.0',   '0.78539816339744830961566084581987572104929234984378')
        ]

        current_scale: int = DecimalNumber.get_scale()
        DecimalNumber.set_scale(50)
        for n in list_numbers:
            a = str(DecimalNumber(n[0]).atan())
            if not self.assertEqual(a, n[1], "Error calculating acos({0})".format(n[0])):
                failed = True
        DecimalNumber.set_scale(current_scale)

        return failed



# def print_exception(exc: Exception) -> None:
#     if sys.implementation.name == "cpython":
#         traceback.print_exc()
#     else:
#         sys.print_exception(exc)


if __name__ == "__main__":
    print("Testing the module 'decimal_number':")

    # Creates an object of the class for tests
    test = TestDecimalNumber()
    # Counts the number of tests that fail
    failed_counter: int = 0
    # Iterates through the items to find methods 'test_...'
    for k, v in TestDecimalNumber.__dict__.items():
        if k.startswith("test_") and callable(v):
            print("Testing: ", k)
            failed: bool = TestDecimalNumber.__dict__[k](test)  # Executes the test
            if failed:
                failed_counter += 1

    print("Tests ran:", test.test_counter)
    if failed_counter == 0:
        print("Result:", "OK")
    elif failed_counter == 1:
        print("Result: 1 test failed")
    else:
        print("Result: {0} tests failed".format(failed_counter))
