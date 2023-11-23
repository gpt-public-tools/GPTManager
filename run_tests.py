
import unittest

if __name__ == '__main__':
    # This will discover and run all the tests in the 'tests' directory
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
