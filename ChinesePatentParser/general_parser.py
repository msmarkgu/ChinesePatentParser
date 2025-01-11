import os, re, sys
import pdfplumber

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional

from .simple_bidict import SimpleBiDict
from .patent_template import PatentTemplate

class GeneralParser:
    Doc_Ending_Label = '9876501234'  # dummy label to flag end of document.

    """ A general parser to parse general patent pdf """
    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ''
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        return text

    @abstractmethod
    def can_ignore(label_regex: str, line: str) -> bool:
        return False

    def get_clean_text(self, label_regex: str, lines: List[str]) -> str:
        cleaned_lines = []
        
        for line in lines:
            if self.can_ignore(label_regex, line):
                pass
            else:
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def add_section(self, section_regex: str, section_title: str,
                    lines: List[str], sections: Dict[str, str]) -> None:
        text = self.get_clean_text(section_regex, lines)

        result = re.sub(section_regex, "", text).strip()

        if section_title in sections.keys():
            sections[section_title] = sections[section_title] + "\n" + result
        else:
            sections[section_title] = result

        return

    def split_sections(self, text: str, 
                       segment_regex_map: SimpleBiDict[str, str], 
                       max_lines: int=10000) -> Dict[str, str]:
        """ 
        Split the input text lines by using the given regex labels (e.g. section title). 
        """
        text_lines = text.split('\n')
        total_lines = len(text_lines)

        title_list = segment_regex_map.keys()
        regex_list = segment_regex_map.values()
        
        # use dictionary to carry result: key is section title (aka, regex label).
        sections = {}

        buffer = []
        line_count = 0
        title_idx = 0
        while line_count < min(total_lines, max_lines):
            curr_regex = regex_list[title_idx]
            curr_title = title_list[title_idx]

            next_regex = regex_list[title_idx+1] if title_idx<len(regex_list)-1 else PatentTemplate.DocEnd

            line = text_lines[line_count]

            if re.search(curr_regex, line):
                # current section starts

                buffer.append(line)

            elif re.search(next_regex, line):
                # current section ends
                if len(buffer)>0:
                    self.add_section(curr_regex, curr_title, buffer, sections)

                # move on to next section
                buffer = [line]
                title_idx += 1

            else:
                # inside current section
                buffer.append(line)

            line_count += 1

        # handle the last section
        if len(buffer) > 0:
            self.add_section(curr_regex, curr_title, buffer, sections)

        #if self.isDebug:
        #    for key, value in sections.items():
        #        print(f"key: {key}\nvalue: {value}\n")

        return sections

    def extract_items_by_regex(self, text: str, item_regex: str) -> Dict[str, str]:
        items = []   # each claim starts with sequence number like "1.", "2.", etc.
        lines = text.split('\n')
        buffer = []
        line_count = 0
        match_count = 0
        while line_count < len(lines):
            line = lines[line_count]

            if re.search(item_regex, line):   # e.g., "^\d{1,2}\."
                
                if len(buffer) > 0 and match_count > 0:
                    items.append("\n".join(buffer))
                
                match_count += 1
                buffer = [line]
            else:
                buffer.append(line)

            line_count += 1

        # add the last one in buffer
        if len(buffer) > 0:
            items.append("\n".join(buffer))

        return items
