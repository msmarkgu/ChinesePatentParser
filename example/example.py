from ChinesePatentParser import patent_parser  # Absolute import

pdf_path = './Alibaba.pdf'

parser = patent_parser.PatentParser()

data = parser.parse_pdf_file(pdf_path)

data_json = data.to_json()

print(f"\n{data_json}")
