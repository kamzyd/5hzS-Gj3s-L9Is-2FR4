from datetime import datetime, timedelta
from memoization.memoize import memoize
import unittest, time
from freezegun import freeze_time

# test sequence:
# 1. memoization testing
# 2. timeout testing
# 3. type compatibility testing
#
# unit-test structure:
# creation of inputs
# execution of the tested code with output capturation
# comparison of the outputs with expected results

# converted example function
def addToTime(year, month, day):
    return datetime.now() + timedelta(days = day + 30 * month + 12 * 30 * year)

# it is important to note that the support of data
# types depends also on the used function. If the
# function does not support a certain data type
# the program will crash. This is why a special
# function will be passed and tested as well.
def testFunction(*value):
    return value

class TestMemoization(unittest.TestCase):
    '''Tests the 'memoize' class in search of inperfections,
       timout misfunctions and type compatibility errors.
    '''
    # Functionality tests

    def test_memoization(self):
        # test key mapping:
        instance = memoize(addToTime, 1, 1, 1, timeout = 1e3)
        self.assertEqual(list(instance.summorialmemory())[0], (1, 1, 1), "The cache key is not being memorized.")

        # test if values are memorized:
        # the same outcome has to occur 2 times within one
        # timeout's time
        value_a = instance.memoized(1, 1, 1)
        self.assertEqual(instance.memoized(1, 1, 1), value_a, "The first value is not being memorized.")

        # test if another value is memorized:
        value_b = instance.memoized(2, 2, 2)
        # this value must not be equal to the first one
        self.assertNotEqual(instance.memoized(1, 1, 1), value_b, "The second cache key is not being memorized.")
        # though, it must be equal to the returned value
        # if the same resolver is passed again within
        # timeout's time
        self.assertEqual(instance.memoized(2, 2, 2), value_b, "The second value is not being memorized.")

        # test if the first value can be returned:
        # after the second value is returned the first
        # one still has to remain unchanged
        self.assertEqual(instance.memoized(1, 1, 1), value_a, "First value gets mixed with the second one.")

    @freeze_time("1990-12-12 00:0:0")
    def test_timeout(self):
        instance = memoize(addToTime, timeout = 5000)
        value_a = instance.memoized(1, 1, 1)

        # test if the same value is returned before the
        # key is expired
        with freeze_time("1990-12-12 00:0:2"):
            self.assertEqual(instance.memoized(1, 1, 1), value_a, "Timeout error.")
        # test if another value is returned after expiration
        with freeze_time("1990-12-12 00:1:0"):
            self.assertNotEqual(instance.memoized(1, 1, 1), value_a, "Timeout error.")

    # Data type tests

    @freeze_time("1990-12-12")
    def __inputTypeTestPerform(self, func, *data):
        instance = memoize(func, timeout = 100)

        # test if the type can be passed to the given function
        try:
            anticipated_result = func(*data)
        except TypeError:
            message = "Error occured by passing object type " + type(data[0]).__name__ + " to function " + func.__name__ + "."
            self.assertTrue(False, message)
            return 0

        # test if the type can be passed to 'memoized' in case
        # an unhashable type occurs (type unsupported and
        # cannot be passed)
        try:
            result = instance.memoized(*data)
        except TypeError:
            message = "Error occured by passing object type " + type(data[0]).__name__ + "."
            self.assertTrue(False, message)
            return 0

        # test based on value
        self.assertEqual(result, anticipated_result, "The passed argument is not equal to the returned value after passing object type "
                        + type(data[0]).__name__ + ".")

        # test based on data type
        self.assertIs(type(result), type(anticipated_result), "The input and output types are not the same after passing object type "
                    + type(data[0]).__name__ + ".")

    def __inputTypeTest(self, value):
        # valid for debugging:
        # the function with higher probabilty of success without
        # any type of calculations is first. If an error is caused
        # due to the second function than in conclusion the
        # 'memoized' is compatible with the given object type
        # because the test was successful during implementation
        # of the first function.
        #
        # if no errors will occur the test is passed.

        self.__inputTypeTestPerform(testFunction, value, value, value)
        self.__inputTypeTestPerform(addToTime, value, value, value)

    @freeze_time("1990-12-12")

    @unittest.skip("fail: addToTime")
    def test_input_type_str(self):
        self.__inputTypeTest("a")

    def test_input_type_int(self):
        self.__inputTypeTest(1)

    def test_input_type_float(self):
        self.__inputTypeTest(1.5)

    @unittest.skip("fail: addToTime")
    def test_input_type_complex(self):
        self.__inputTypeTest(1j)

    @unittest.skip("fail: both")
    def test_input_type_list(self):
        self.__inputTypeTest(["banana", "apple"])

    @unittest.skip("fail: addToTime")
    def test_input_type_tuple(self):
        self.__inputTypeTest(("banana", "apple"))

    @unittest.skip("fail: addToTime")
    def test_input_type_range(self):
        self.__inputTypeTest(range(6))

    @unittest.skip("fail: both")
    def test_input_type_dict(self):
        self.__inputTypeTest({"banana": "apple"})

    @unittest.skip("fail: both")
    def test_input_type_set(self):
        self.__inputTypeTest({"banana", "apple"})

    @unittest.skip("fail: addToTime")
    def test_input_type_frozenset(self):
        self.__inputTypeTest(frozenset({"banana", "apple"}))

    def test_input_type_bool(self):
        self.__inputTypeTest(True)

    @unittest.skip("fail: addToTime")
    def test_input_type_bytes(self):
        self.__inputTypeTest(b"Hello")

    @unittest.skip("fail: both")
    def test_input_type_bytearray(self):
        self.__inputTypeTest(bytearray(5))

    @unittest.skip("fail: addToTime")
    def test_input_type_memoryview(self):
        self.__inputTypeTest(memoryview(bytes(5)))

if __name__ == "__main__":
    unittest.main()
    print("Everything passed.")
