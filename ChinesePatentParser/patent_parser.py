import os, re, sys

import pdfplumber

from typing import Dict, List, Tuple, Optional

from .general_parser import GeneralParser
from .patent_instance import PatentInstance
from .patent_template import PatentTemplate

class PatentParser(GeneralParser):
    def __init__(self, isDebug=False):
        self.isDebug = isDebug

    def can_ignore(self, label_regex: str, line: str) -> bool:
        # ignore page headers, like '权利要求书', '说明书'
        if (PatentTemplate.SecTitle_Claims in label_regex or \
            PatentTemplate.SecTitle_Description in label_regex ) \
            and \
            (line == PatentTemplate.SecTitle_Claims or \
                re.search("^\d+$", line) or \
                re.search("^CN\s*\d+.*\d+/\d+\s*页$", line)):  # CN 115757739 A 1/2页
            return True
        else:
            return False

    def extract_abstract(self, abstract_text: str) -> str:
        abstract_lines = []

        lines = abstract_text.split('\n')
        # look for 1st line starts with "本发明"
        abstract_begin = False
        for line in lines:
            if not abstract_begin and ( \
                line.startswith('本发明') or \
                line.startswith('本说明书') or \
                line.startswith('本申请')
            ):
                abstract_begin = True

            if abstract_begin:
                if len(line) < 6 and (re.search("^\d+", line) or re.search("\d+$", line)):
                    pass
                else:
                    abstract_lines.append(line)

        abstract = "".join(abstract_lines) 

        return abstract

    def extract_claims(self, claim_text: str) -> List[str]:
        claims = self.extract_items_by_regex(claim_text, PatentTemplate.Regex_Claim_Item)

        if self.isDebug:
            print(f"\nlen(claims) = {len(claims)} items\n")
            for claim in claims:
                print(f"{claim}")

        return claims

    def extract_description(self, description_text: str) -> List[str]:
        desc_items = self.extract_items_by_regex(description_text, PatentTemplate.Regex_Desc_Item)

        if self.isDebug:
            print(f"len(desc_items) = {len(desc_items)}\n")
            for item in desc_items:
                print(f"{item}")

        return desc_items
    
    def parse_description_subsections(self, 
                                      description_text: str, 
                                      data: PatentInstance, 
                                        max_lines: int) -> None:
        subsec_regex_map = PatentTemplate.get_subsection_regex_mapping()

        subsections = self.split_sections(description_text, subsec_regex_map, max_lines)

        if self.isDebug:
            print(f"len(subsections) = {len(subsections)}")

        key = PatentTemplate.SubsecTitle_TechDomain
        if key in subsections.keys():
            techdomain_text = subsections[key].replace(key, "").strip()

            data.TechDomain = self.extract_items_by_regex(techdomain_text, PatentTemplate.Regex_Desc_Item)

        key = PatentTemplate.SubsecTitle_Background
        if key in subsections.keys():
            data.Background = self.extract_items_by_regex(
                subsections[key].replace(key, "").strip(), 
                PatentTemplate.Regex_Desc_Item
            )
        
        key = PatentTemplate.SubsecTitle_InvContent
        if key in subsections.keys():
            data.InvContent = self.extract_items_by_regex(
                subsections[key].replace(key, "").strip(), 
                PatentTemplate.Regex_Desc_Item
            )

        key = PatentTemplate.SubsecTitle_DrawingDes
        if key in subsections.keys():
            data.DrawingDes = self.extract_items_by_regex(
                subsections[key].replace(key, "").strip(), 
                PatentTemplate.Regex_Desc_Item
            )

        key = PatentTemplate.SubsecTitle_ImplMethod
        if key in subsections.keys():
            data.ImplMethod = self.extract_items_by_regex(
                subsections[key].replace(key, "").strip(), 
                PatentTemplate.Regex_Desc_Item
            )

        return
    
    def parse_content(self, text: str, maxlines: int) -> PatentInstance:
        section_regex_map = PatentTemplate.get_section_regex_mapping()

        sections = self.split_sections(text, section_regex_map, maxlines)

        if self.isDebug:
            print(f"len(text) = {len(text)}")
            print(f"len(sections) = {len(sections.keys())}")

        data = PatentInstance()
        
        data.Title = sections.get(PatentTemplate.SecTitle_InvTitle, '').replace('\n', ' ')

        data.PubNumber = sections.get(PatentTemplate.SecTitle_PubNumber, '').replace('\n', ' ')
        data.PubDate = sections.get(PatentTemplate.SecTitle_PubDate, '').replace('\n', ' ')

        data.AppNumber = sections.get(PatentTemplate.SecTitle_AppNumber, '').replace('\n', ' ')
        data.AppDate = sections.get(PatentTemplate.SecTitle_AppDate, '').replace('\n', ' ')

        data.Applicant = sections.get(PatentTemplate.SecTitle_Applicant, '')
        data.Inventor = sections.get(PatentTemplate.SecTitle_Inventor, '')
        data.Agent = sections.get(PatentTemplate.SecTitle_Agent, '')
        data.IntCI = sections.get(PatentTemplate.SecTitle_IntCI, '')

        data.Abstract = self.extract_abstract(sections.get(PatentTemplate.SecTitle_Abstract, ''))

        data.ClaimItems = self.extract_claims(sections.get(PatentTemplate.SecTitle_Claims, ''))

        if PatentTemplate.SecTitle_Description in sections.keys():
            description_text = sections[PatentTemplate.SecTitle_Description]

            data.DescItems = self.extract_description(description_text)

            self.parse_description_subsections(description_text, data, maxlines)

        return data
    
    def parse_pdf_file(self, pdf_path: str, maxlines: int=10000) -> PatentInstance:
        text = self.extract_text_from_pdf(pdf_path)
        data = self.parse_content(text, maxlines)
        return data

def main(argv):
    pdf_path = sys.argv[1]  # 'your_file.pdf'
    maxlines = int(sys.argv[2]) if len(argv)>2 else 5000 # process up to max lines
    isDebug = False

    pp = PatentParser(isDebug)

    data = pp.parse_pdf_file(pdf_path, maxlines)

    # print(f"\n{data}\n")

    data_json = data.to_json()

    print(f"\n{data_json}")

if __name__ == "__main__":
    main(sys.argv)
