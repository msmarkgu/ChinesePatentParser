import unittest
from ChinesePatentParser import patent_parser  # Absolute import

class TestA(unittest.TestCase):
    def test_parser(self):
        pdf_path = './example/Alibaba.pdf'

        parser = patent_parser.PatentParser()

        data = parser.parse_pdf_file(pdf_path)

        data_json = data.to_json()

        print(f"\n{data_json}")

        self.assertIsNotNone(data)  # Example assertion

if __name__ == '__main__':
    unittest.main()

# in command line, run:
# python -m unittest discover -s tests
