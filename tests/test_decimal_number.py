import sys
import random
from mpy_decimal.mpy_decimal import *

if sys.implementation.name == "cpython":
    import traceback
if sys.implementation.name == "micropython":
    pass


class TestDecimalNumber():

    def __init__(self) -> None:
        self.test_counter: int = 0

    def assertRaises(self, exc, function) -> None:
        try:
            function()
            return False
        except Exception as e:
            if isinstance(e, exc):
                return True
            else:
                return False

    def assertEqual(self, v1, v2, message: str) -> bool:
        if v1 == v2:
            return True
        else:
            print("\t" + message)
            return False

    def assertTrue(self, v, message: str) -> bool:
        if v:
            return True
        else:
            print("\t" + message)
            return False

    def assertFalse(self, v, message: str) -> bool:
        if not v:
            return True
        else:
            print("\t" + message)
            return False

    def test_init(self) -> bool:
        self.test_counter += 1
        failed: bool = False
        # Creation of a number with negative number of decimals
        if not self.assertRaises(DecimalNumberExceptionMathDomainError, lambda: DecimalNumber(1, -5)):
            failed = True
        return failed

    def test_parse_number(self) -> bool:
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
            if not self.assertRaises(DecimalNumberExceptionParseError, lambda: DecimalNumber.from_string(n)):
                failed = True
        for n in list_valid:
            number = DecimalNumber.from_string(n)
        return failed

    def test_set_scale(self) -> bool:
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
            sr = str(DecimalNumber.from_string(n[1]).square_root())
            if not self.assertEqual(sr, n[2], "Error calculating square_root({0})".format(n[1])):
                failed = True
            DecimalNumber.set_scale(current_scale)

        if not self.assertRaises(DecimalNumberExceptionMathDomainError, lambda: DecimalNumber(-1).square_root()):
            failed = True
        return failed

    def test_pi(self) -> bool:
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
        list_numbers = [
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
            ("-38046.6", "242.139", "-37804.461"),
            ("703.094", "505.603", "1208.697"),
            ("-5142.17", "7103.99", "1961.82"),
            ("9518.7", "-91.967", "9426.733"),
            ("-19963.2", "6037.19", "-13926.01"),
            ("-4730.85", "34402.7", "29671.85"),
            ("-7877.74", "-6375.13", "-14252.87"),
            ("1555.64", "-2198.51", "-642.87"),
            ("2449.8", "6830.9", "9280.7"),
            ("17087.7", "5718.11", "22805.81"),
            ("-144.512", "-6693.8", "-6838.312"),
            ("-73.293", "40779.5", "40706.207"),
            ("-284.752", "91034.4", "90749.648"),
            ("-2598.06", "-48982.5", "-51580.56"),
            ("6477.48", "-493.168", "5984.312"),
            ("-75738.3", "-97330", "-173068.3"),
            ("877.087", "-50314.6", "-49437.513"),
            ("9863.45", "113.618", "9977.068"),
            ("1502.24", "-44865.9", "-43363.66"),
            ("2824.44", "6714.55", "9538.99"),
            ("-2232.98", "95691.5", "93458.52"),
            ("-4176.3", "2734.73", "-1441.57"),
            ("-739.079", "3897.22", "3158.141"),
            ("2347.59", "-233.081", "2114.509"),
            ("401.84", "-374.7", "27.14"),
            ("-1486.23", "-4860.73", "-6346.96"),
            ("71333.3", "-8461.26", "62872.04"),
            ("5451.84", "-8923.02", "-3471.18"),
            ("-1281.39", "792.936", "-488.454"),
            ("9996.1", "-187.13", "9808.97"),
            ("13192.6", "316.788", "13509.388"),
            ("5340.51", "8154.78", "13495.29"),
            ("24342.8", "78667.8", "103010.6"),
            ("8749.12", "9990.3", "18739.42"),
            ("67209.9", "98214.4", "165424.3"),
            ("-6405.35", "-6985.81", "-13391.16"),
            ("-14830.9", "-67201.7", "-82032.6"),
            ("-923.155", "-161.626", "-1084.781"),
            ("3.743", "3639.74", "3643.483"),
            ("91631.2", "836.776", "92467.976"),
            ("1174.79", "-989.79", "185"),
            ("7650.11", "-95807.8", "-88157.69"),
            ("-24848.5", "46739.4", "21890.9"),
            ("-12464.7", "-6575.74", "-19040.44"),
            ("54089.7", "-744.401", "53345.299"),
            ("-5570.04", "-884.52", "-6454.56"),
            ("-298.725", "7487.96", "7189.235"),
            ("245.577", "743.8", "989.377"),
            ("-900.911", "-38917", "-39817.911"),
            ("56701.2", "832.257", "57533.457"),
            ("3930.76", "829.749", "4760.509"),
            ("71341.9", "36815.4", "108157.3"),
            ("-183.081", "3094.77", "2911.689"),
            ("-5409.72", "-2671.11", "-8080.83"),
            ("9824.36", "-49918.7", "-40094.34"),
            ("606.225", "-9381.2", "-8774.975"),
            ("-52.731", "-3457.49", "-3510.221"),
            ("-455.367", "567.046", "111.679"),
            ("-480.198", "151.322", "-328.876"),
            ("-294.097", "-627.192", "-921.289"),
            ("-20863.1", "7254.18", "-13608.92"),
            ("-3717.26", "-9067.9", "-12785.16"),
            ("-6905.26", "5918.99", "-986.27"),
            ("716.089", "-1461.06", "-744.971"),
            ("-536.811", "3871.68", "3334.869"),
            ("-45461.6", "-2998.23", "-48459.83"),
            ("-9337.58", "-633.028", "-9970.608"),
            ("78304.9", "16746.7", "95051.6"),
            ("-1186.78", "-62862.5", "-64049.28"),
            ("-777.973", "5473.55", "4695.577"),
            ("6852.21", "-1432.92", "5419.29"),
            ("-505.653", "-8844.6", "-9350.253"),
            ("-3138.92", "-22303.2", "-25442.12"),
            ("-7928.34", "801.698", "-7126.642"),
            ("-733.8", "576.324", "-157.476"),
            ("7298.57", "810.431", "8109.001"),
            ("-793.282", "1887.1", "1093.818"),
            ("3616.56", "-7958.94", "-4342.38"),
            ("-27633.5", "17373.7", "-10259.8"),
            ("80546.2", "-5510.44", "75035.76"),
            ("-82.321", "-40936.2", "-41018.521"),
            ("6761.93", "-2496.96", "4264.97"),
            ("-80811.8", "-3851.03", "-84662.83"),
            ("-31293.2", "47.457", "-31245.743"),
            ("-5901.9", "-557.528", "-6459.428"),
            ("-834.12", "4119.74", "3285.62")
        ]
        self.test_counter += 1
        failed: bool = False
        for n in list_numbers:
            a = DecimalNumber.from_string(n[0])
            b = DecimalNumber.from_string(n[1])
            c = DecimalNumber.from_string(n[2])
            cc = a + b
            aa = DecimalNumber.from_string(n[0])
            aa += b

            if not self.assertEqual(c, cc, "Incorrect addition for ({0} + {1})".format(str(a), str(b))):
                failed = True
            if not self.assertEqual(aa, cc, "Incorrect addition to itself for ({0} + {1})".format(str(a), str(b))):
                failed = True
        return failed

    def test_sub_iub(self) -> bool:
        list_numbers = [
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
            ("-38046.6", "242.139", "-38288.739"),
            ("703.094", "505.603", "197.491"),
            ("-5142.17", "7103.99", "-12246.16"),
            ("9518.7", "-91.967", "9610.667"),
            ("-19963.2", "6037.19", "-26000.39"),
            ("-4730.85", "34402.7", "-39133.55"),
            ("-7877.74", "-6375.13", "-1502.61"),
            ("1555.64", "-2198.51", "3754.15"),
            ("2449.8", "6830.9", "-4381.1"),
            ("17087.7", "5718.11", "11369.59"),
            ("-144.512", "-6693.8", "6549.288"),
            ("-73.293", "40779.5", "-40852.793"),
            ("-284.752", "91034.4", "-91319.152"),
            ("-2598.06", "-48982.5", "46384.44"),
            ("6477.48", "-493.168", "6970.648"),
            ("-75738.3", "-97330", "21591.7"),
            ("877.087", "-50314.6", "51191.687"),
            ("9863.45", "113.618", "9749.832"),
            ("1502.24", "-44865.9", "46368.14"),
            ("2824.44", "6714.55", "-3890.11"),
            ("-2232.98", "95691.5", "-97924.48"),
            ("-4176.3", "2734.73", "-6911.03"),
            ("-739.079", "3897.22", "-4636.299"),
            ("2347.59", "-233.081", "2580.671"),
            ("401.84", "-374.7", "776.54"),
            ("-1486.23", "-4860.73", "3374.5"),
            ("71333.3", "-8461.26", "79794.56"),
            ("5451.84", "-8923.02", "14374.86"),
            ("-1281.39", "792.936", "-2074.326"),
            ("9996.1", "-187.13", "10183.23"),
            ("13192.6", "316.788", "12875.812"),
            ("5340.51", "8154.78", "-2814.27"),
            ("24342.8", "78667.8", "-54325"),
            ("8749.12", "9990.3", "-1241.18"),
            ("67209.9", "98214.4", "-31004.5"),
            ("-6405.35", "-6985.81", "580.46"),
            ("-14830.9", "-67201.7", "52370.8"),
            ("-923.155", "-161.626", "-761.529"),
            ("3.743", "3639.74", "-3635.997"),
            ("91631.2", "836.776", "90794.424"),
            ("1174.79", "-989.79", "2164.58"),
            ("7650.11", "-95807.8", "103457.91"),
            ("-24848.5", "46739.4", "-71587.9"),
            ("-12464.7", "-6575.74", "-5888.96"),
            ("54089.7", "-744.401", "54834.101"),
            ("-5570.04", "-884.52", "-4685.52"),
            ("-298.725", "7487.96", "-7786.685"),
            ("245.577", "743.8", "-498.223"),
            ("-900.911", "-38917", "38016.089"),
            ("56701.2", "832.257", "55868.943"),
            ("3930.76", "829.749", "3101.011"),
            ("71341.9", "36815.4", "34526.5"),
            ("-183.081", "3094.77", "-3277.851"),
            ("-5409.72", "-2671.11", "-2738.61"),
            ("9824.36", "-49918.7", "59743.06"),
            ("606.225", "-9381.2", "9987.425"),
            ("-52.731", "-3457.49", "3404.759"),
            ("-455.367", "567.046", "-1022.413"),
            ("-480.198", "151.322", "-631.52"),
            ("-294.097", "-627.192", "333.095"),
            ("-20863.1", "7254.18", "-28117.28"),
            ("-3717.26", "-9067.9", "5350.64"),
            ("-6905.26", "5918.99", "-12824.25"),
            ("716.089", "-1461.06", "2177.149"),
            ("-536.811", "3871.68", "-4408.491"),
            ("-45461.6", "-2998.23", "-42463.37"),
            ("-9337.58", "-633.028", "-8704.552"),
            ("78304.9", "16746.7", "61558.2"),
            ("-1186.78", "-62862.5", "61675.72"),
            ("-777.973", "5473.55", "-6251.523"),
            ("6852.21", "-1432.92", "8285.13"),
            ("-505.653", "-8844.6", "8338.947"),
            ("-3138.92", "-22303.2", "19164.28"),
            ("-7928.34", "801.698", "-8730.038"),
            ("-733.8", "576.324", "-1310.124"),
            ("7298.57", "810.431", "6488.139"),
            ("-793.282", "1887.1", "-2680.382"),
            ("3616.56", "-7958.94", "11575.5"),
            ("-27633.5", "17373.7", "-45007.2"),
            ("80546.2", "-5510.44", "86056.64"),
            ("-82.321", "-40936.2", "40853.879"),
            ("6761.93", "-2496.96", "9258.89"),
            ("-80811.8", "-3851.03", "-76960.77"),
            ("-31293.2", "47.457", "-31340.657"),
            ("-5901.9", "-557.528", "-5344.372"),
            ("-834.12", "4119.74", "-4953.86")
        ]
        self.test_counter += 1
        failed: bool = False
        for n in list_numbers:
            a = DecimalNumber.from_string(n[0])
            b = DecimalNumber.from_string(n[1])
            c = DecimalNumber.from_string(n[2])
            cc = a - b
            aa = DecimalNumber.from_string(n[0])
            aa -= b

            if not self.assertEqual(c, cc, "Incorrect subtruction for ({0} - {1})".format(str(a), str(b))):
                failed = True
            if not self.assertEqual(aa, cc, "Incorrect subtruction from itself for ({0} - {1})".format(str(a), str(b))):
                failed = True
        return failed

    def test_mul_imul(self) -> bool:
        list_numbers = [
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
            ("-38046.6", "242.139", "-9212565.6774"),
            ("703.094", "505.603", "355486.435682"),
            ("-5142.17", "7103.99", "-36529924.2583"),
            ("9518.7", "-91.967", "-875406.2829"),
            ("-19963.2", "6037.19", "-120521631.408"),
            ("-4730.85", "34402.7", "-162754013.295"),
            ("-7877.74", "-6375.13", "50221616.6062"),
            ("1555.64", "-2198.51", "-3420090.0964"),
            ("2449.8", "6830.9", "16734338.82"),
            ("17087.7", "5718.11", "97709348.247"),
            ("-144.512", "-6693.8", "967334.4256"),
            ("-73.293", "40779.5", "-2988851.8935"),
            ("-284.752", "91034.4", "-25922227.4688"),
            ("-2598.06", "-48982.5", "127259473.95"),
            ("6477.48", "-493.168", "-3194485.85664"),
            ("-75738.3", "-97330", "7371608739"),
            ("877.087", "-50314.6", "-44130281.5702"),
            ("9863.45", "113.618", "1120665.4621"),
            ("1502.24", "-44865.9", "-67399349.616"),
            ("2824.44", "6714.55", "18964843.602"),
            ("-2232.98", "95691.5", "-213677205.67"),
            ("-4176.3", "2734.73", "-11421052.899"),
            ("-739.079", "3897.22", "-2880353.46038"),
            ("2347.59", "-233.081", "-547178.62479"),
            ("401.84", "-374.7", "-150569.448"),
            ("-1486.23", "-4860.73", "7224162.7479"),
            ("71333.3", "-8461.26", "-603569597.958"),
            ("5451.84", "-8923.02", "-48646877.3568"),
            ("-1281.39", "792.936", "-1016060.26104"),
            ("9996.1", "-187.13", "-1870570.193"),
            ("13192.6", "316.788", "4179257.3688"),
            ("5340.51", "8154.78", "43550684.1378"),
            ("24342.8", "78667.8", "1914994521.84"),
            ("8749.12", "9990.3", "87406333.536"),
            ("67209.9", "98214.4", "6600980002.56"),
            ("-6405.35", "-6985.81", "44746558.0835"),
            ("-14830.9", "-67201.7", "996661692.53"),
            ("-923.155", "-161.626", "149205.85003"),
            ("3.743", "3639.74", "13623.54682"),
            ("91631.2", "836.776", "76674789.0112"),
            ("1174.79", "-989.79", "-1162795.3941"),
            ("7650.11", "-95807.8", "-732940208.858"),
            ("-24848.5", "46739.4", "-1161403980.9"),
            ("-12464.7", "-6575.74", "81964626.378"),
            ("54089.7", "-744.401", "-40264426.7697"),
            ("-5570.04", "-884.52", "4926811.7808"),
            ("-298.725", "7487.96", "-2236840.851"),
            ("245.577", "743.8", "182660.1726"),
            ("-900.911", "-38917", "35060753.387"),
            ("56701.2", "832.257", "47189970.6084"),
            ("3930.76", "829.749", "3261544.17924"),
            ("71341.9", "36815.4", "2626480585.26"),
            ("-183.081", "3094.77", "-566593.58637"),
            ("-5409.72", "-2671.11", "14449957.1892"),
            ("9824.36", "-49918.7", "-490419279.532"),
            ("606.225", "-9381.2", "-5687117.97"),
            ("-52.731", "-3457.49", "182316.90519"),
            ("-455.367", "567.046", "-258214.035882"),
            ("-480.198", "151.322", "-72664.521756"),
            ("-294.097", "-627.192", "184455.285624"),
            ("-20863.1", "7254.18", "-151344682.758"),
            ("-3717.26", "-9067.9", "33707741.954"),
            ("-6905.26", "5918.99", "-40872164.8874"),
            ("716.089", "-1461.06", "-1046248.99434"),
            ("-536.811", "3871.68", "-2078360.41248"),
            ("-45461.6", "-2998.23", "136304332.968"),
            ("-9337.58", "-633.028", "5910949.59224"),
            ("78304.9", "16746.7", "1311348668.83"),
            ("-1186.78", "-62862.5", "74603957.75"),
            ("-777.973", "5473.55", "-4258274.11415"),
            ("6852.21", "-1432.92", "-9818668.7532"),
            ("-505.653", "-8844.6", "4472298.5238"),
            ("-3138.92", "-22303.2", "70007960.544"),
            ("-7928.34", "801.698", "-6356134.32132"),
            ("-733.8", "576.324", "-422906.5512"),
            ("7298.57", "810.431", "5914987.38367"),
            ("-793.282", "1887.1", "-1497002.4622"),
            ("3616.56", "-7958.94", "-28783984.0464"),
            ("-27633.5", "17373.7", "-480096138.95"),
            ("80546.2", "-5510.44", "-443845002.328"),
            ("-82.321", "-40936.2", "3369908.9202"),
            ("6761.93", "-2496.96", "-16884268.7328"),
            ("-80811.8", "-3851.03", "311208666.154"),
            ("-31293.2", "47.457", "-1485081.3924"),
            ("-5901.9", "-557.528", "3290474.5032"),
            ("-834.12", "4119.74", "-3436357.5288")
        ]
        self.test_counter += 1
        failed: bool = False
        for n in list_numbers:
            a = DecimalNumber.from_string(n[0])
            b = DecimalNumber.from_string(n[1])
            c = DecimalNumber.from_string(n[2])
            cc = a * b
            aa = DecimalNumber.from_string(n[0])
            aa *= b

            if not self.assertEqual(c, cc, "Incorrect multiplication for ({0} - {1})".format(str(a), str(b))):
                failed = True
            if not self.assertEqual(aa, cc, "Incorrect multiplication by itself for ({0} - {1})".format(str(a), str(b))):
                failed = True
        return failed

    def test_truediv(self) -> bool:
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

            aa = DecimalNumber.from_string(str(a))
            bb = DecimalNumber.from_string(str(b))
            cc = aa * bb

            aa2 = cc / bb

            if not self.assertEqual(aa, aa2, "Incorrect division for ({0} / {1})".format(str(a), str(b))):
                failed = True
        return failed

    def test_itruediv(self) -> bool:
        self.test_counter += 1
        failed: bool = False
        # Creates 10000 random divisions to itself and checks them
        for _ in range(0, 100):
            a = (random.randrange(0, 990) * 1000 +
                 random.randrange(0, 1000)) / 1000
            if random.randrange(0, 2) == 0:
                a = -a

            b = (random.randrange(0, 990) * 1000 +
                 random.randrange(0, 1000)) / 1000
            if random.randrange(0, 2) == 0:
                b = -b

            aa = DecimalNumber.from_string(str(a))
            bb = DecimalNumber.from_string(str(b))
            cc = aa * bb
            aa2 = cc.clone()
            aa2 /= bb

            if not self.assertEqual(aa2, aa, "Incorrect division of itself for ({0} /= {1})".format(str(a), str(b))):
                failed = True
        return failed

    def test_neg(self) -> bool:
        self.test_counter += 1
        failed: bool = False
        n = DecimalNumber(12345)
        n2 = -n
        if not self.assertTrue((n._number == n2._number and n._is_positive and not n2._is_positive), "Error on __neg__ method"):
            failed = True
        return failed

    def test_pos(self) -> bool:
        self.test_counter += 1
        failed: bool = False
        n = DecimalNumber(-12345)
        n2 = +n
        if not self.assertTrue((n._number == n2._number and n._is_positive == n2._is_positive), "Error on __pos__ method"):
            failed = True
        return failed

    def test_abs(self) -> bool:
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
        self.test_counter += 1
        failed: bool = False
        n1 = DecimalNumber.from_string("12.3")
        n2 = DecimalNumber.from_string("0.98765")

        if not self.assertFalse(n1 < n2, "Error evaluating {0} < {1}".format(n1, n2)):
            failed = True
        if not self.assertTrue(n2 < n1, "Error evaluating {0} < {1}".format(n2, n1)):
            failed = True

        if not self.assertFalse(n1 <= n2, "Error evaluating {0} <= {1}".format(n1, n2)):
            failed = True
        if not self.assertTrue(n2 <= n1, "Error evaluating {0} <= {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n1 <= n1, "Error evaluating {0} <= {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n2 <= n2, "Error evaluating {0} <= {1}".format(n2, n2)):
            failed = True

        if not self.assertFalse(n1 == n2, "Error evaluating {0} == {1}".format(n1, n2)):
            failed = True
        if not self.assertFalse(n2 == n1, "Error evaluating {0} == {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n1 == n1, "Error evaluating {0} == {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n2 == n2, "Error evaluating {0} == {1}".format(n2, n2)):
            failed = True

        if not self.assertTrue(n1 != n2, "Error evaluating {0} != {1}".format(n1, n2)):
            failed = True
        if not self.assertTrue(n2 != n1, "Error evaluating {0} != {1}".format(n1, n1)):
            failed = True
        if not self.assertFalse(n1 != n1, "Error evaluating {0} != {1}".format(n1, n1)):
            failed = True
        if not self.assertFalse(n2 != n2, "Error evaluating {0} != {1}".format(n2, n2)):
            failed = True

        if not self.assertTrue(n1 >= n2, "Error evaluating {0} >= {1}".format(n1, n2)):
            failed = True
        if not self.assertFalse(n2 >= n1, "Error evaluating {0} >= {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n1 >= n1, "Error evaluating {0} >= {1}".format(n1, n1)):
            failed = True
        if not self.assertTrue(n2 >= n2, "Error evaluating {0} >= {1}".format(n2, n2)):
            failed = True

        if not self.assertTrue(n1 > n2, "Error evaluating {0} > {1}".format(n1, n2)):
            failed = True
        if not self.assertFalse(n2 > n1, "Error evaluating {0} > {1}".format(n2, n1)):
            failed = True
        return failed

    def test_to_string_thousands(self) -> bool:
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
            number = DecimalNumber.from_string(n[0])
            if not self.assertEqual(n[1], number.to_string_thousands(), "Error in to_string_thousands"):
                failed = True
        return failed

    def test_to_string_max_length(self) -> bool:
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
            number = DecimalNumber.from_string(n[0])
            if not self.assertEqual(n[1], number.to_string_max_length(8), "Error in to_string_max_length"):
                failed = True
        for n in list_numbers:
            number = DecimalNumber.from_string('-'+n[0])
            result: str = n[1]
            if result != "0" and result != "Overflow":
                result = '-' + result
            if not self.assertEqual(result, number.to_string_max_length(9), "Error in to_string_max_length"):
                failed = True
        return failed

    def test_make_integer_comparable(self) -> bool:
        self.test_counter += 1
        failed: bool = False
        list_numbers = [
            ("123", "123", 123, 123),
            ("123", "123.45", 12300, 12345),
            ("123.45", "123", 12345, 12300)
        ]
        for n in list_numbers:
            n1 = DecimalNumber.from_string(n[0])
            n2 = DecimalNumber.from_string(n[1])
            a, b = n1._make_integer_comparable(n1, n2)
            if not self.assertTrue(
                n[2] == a and n[3] == b,
                "Error in _make_integer_comparable for numbers {0} and {1}, {2} != {3} or {4} != {5}".format(
                    n1, n2, n[2], a, n[3], b)
            ):
                failed = True
        return failed

    def test_reduce_to_scale(self) -> bool:
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

        ]
        current_scale = DecimalNumber.get_scale()
        for n in list_numbers:
            s: int = n[0]
            DecimalNumber.set_scale(s)
            n1 = DecimalNumber.from_string(n[1])
            if not self.assertTrue(
                str(n1) == n[2],
                "Error in _reduce_to_scale for numbers {0} and {1}; {2} != {3}".format(n[1], n[2], n1, n[2])
            ):
                failed = True
        DecimalNumber.set_scale(current_scale)

        return failed

    def test_pow(self) -> bool:
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
            n1 = DecimalNumber.from_string(n[0])
            e: int = n[1]
            r = n1 ** e
            if not self.assertTrue(
                n[2] == str(r),
                "Error in power (n ** e) for n = {0} and e = {1}; {2} != {3}".format(n1, e, r, n[2])
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

# def print_exception(exc: Exception) -> None:
#     if sys.implementation.name == "cpython":
#         traceback.print_exc()
#     else:
#         sys.print_exception(exc)


if __name__ == "__main__":
    print("Testing the module 'decimal_number':")

    test = TestDecimalNumber()
    failed_counter: int = 0
    for k, v in TestDecimalNumber.__dict__.items():
        if k.startswith("test_") and callable(v):
            print("Testing: ", k)
            failed: bool = TestDecimalNumber.__dict__[k](test)
            if failed:
                failed_counter += 1

    print("Tests ran:", test.test_counter)
    if failed_counter == 0:
        print("Result:", "OK")
    elif failed_counter == 1:
        print("Result: 1 test failed")
    else:
        print("Result: {0} tests failed".format(failed_counter))

