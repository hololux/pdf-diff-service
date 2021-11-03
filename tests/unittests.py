import unittest

class TestPdfCompareModule(unittest.TestCase):

  def always_true(self):
      self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()