from io import BytesIO
import os
import base64
import unittest

from pdfcompare import pdfcompare_module

class TestPdfCompareModule(unittest.TestCase):

  def setUp(self):
    script_dir = os.path.dirname(__file__)
    self.pdf_path_old = os.path.join(script_dir, 'test_pdfs' ,"test_old.pdf")
    self.pdf_path_new = os.path.join(script_dir, 'test_pdfs' ,'test_new.pdf')

  def test_compare_pdfs_base(self):
    (output, hits) = pdfcompare_module.compare_pdfs(self.pdf_path_old, self.pdf_path_new)
    out = BytesIO()
    output.write(out)
    base64String = base64.b64encode(out.getvalue()).decode()
    self.assertNotEqual(base64String, "")
    self.assertGreater(hits, 0)

  def test_same_pdf(self):
    (output, hits) = pdfcompare_module.compare_pdfs(self.pdf_path_old, self.pdf_path_old)
    out = BytesIO()
    output.write(out)
    base64String = base64.b64encode(out.getvalue()).decode()
    self.assertNotEqual(base64String, "")
    self.assertEqual(hits, 0)

if __name__ == '__main__':
  unittest.main()