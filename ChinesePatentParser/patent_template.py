import json, os

from typing import Dict, List, Tuple, Optional

from .simple_bidict import SimpleBiDict

class PatentTemplate:
    """
    Define common sections and subsections in a patent, and regex patterns used to identify them.
    """

    DocStart = "document_start"
    DocEnd = "document_end"

    # section titles
    SecTitle_PubNumber = "申请公布号"
    SecTitle_PubDate = "申请公布日"
    SecTitle_AppNumber = "申请号"
    SecTitle_AppDate = "申请日"
    SecTitle_Applicant = "申请人"
    SecTitle_Inventor = "发明人"
    SecTitle_Agent = "代理机构"
    SecTitle_IntCI = "国际分类号"

    SecTitle_InvTitle = "发明名称"
    SecTitle_Abstract = "摘要"

    SecTitle_Claims = "权利要求书"
    SecTitle_Description = '说明书'
    SecTitle_Drawings = '说明书附图'

    # subsection titles in "权利要求书"
    SubsecTitle_TechDomain = "技术领域"
    SubsecTitle_Background = "背景技术"
    SubsecTitle_InvContent = "发明内容"
    SubsecTitle_DrawingDes = "附图说明"
    SubsecTitle_ImplMethod = "具体实施方式"

    # class/static/global variable.
    Section_Regex_Map = None     # mapping btw a section and the regex identifying it.
    Subsection_Regex_Map = None  # mapping btw a subsection and the regex identifying it.

    # items in Claims look like "1. xxx", "2. xxx", etc.
    Regex_Claim_Item = "^\d{1,2}\."

    # items in Description look like "[0001] xxx", "[0005] xxx", etc.
    """
    OCR can recognize square brackets as the following 6 defined in Unicode:
        Square Bracket Left: U+005B ( [ )
        Square Bracket Right: U+005D ( ] )
        Left Square Bracket: U+3010 ( 【 )
        Right Square Bracket: U+3011 ( 】 )
        Left Black Square Bracket: U+FF3B ( ［ )
        Right Black Square Bracket: U+FF3D ( ］ )
    """
    Regex_Desc_Item = "^[\[\u3010\uff3b]\d+[\]\u3011\uff3d]"

    @staticmethod
    def get_section_regex_mapping() -> SimpleBiDict[str, str]:
        """
        Use a bidirection dictionary to map between section title and regex pattern.
        Make sure the key/value pairs follow the order they appear in content text.
        """
        if PatentTemplate.Section_Regex_Map is None:
            mapping = SimpleBiDict[str, str]()

            mapping.add(PatentTemplate.DocStart, "(19)国家知识产权局")
            mapping.add(PatentTemplate.SecTitle_PubNumber, "^\(10\)\s*申请公布号") # (10)申请公布号
            mapping.add(PatentTemplate.SecTitle_PubDate, "^\(43\)\s*申请公布日")   # (43)申请公布日
            mapping.add(PatentTemplate.SecTitle_AppNumber, "^\(21\)\s*申请号")    # (21)申请号
            mapping.add(PatentTemplate.SecTitle_AppDate, "^\(22\)\s*申请日")      # (22)申请日
            mapping.add(PatentTemplate.SecTitle_Applicant, "^\(71\)\s*申请人")    # (71)申请人
            mapping.add(PatentTemplate.SecTitle_Inventor, "^\(72\)\s*发明人")     # (72)发明人
            mapping.add(PatentTemplate.SecTitle_Agent, "^\(74\)\s*专利代理机构")   # (74)专利代理机构
            mapping.add(PatentTemplate.SecTitle_IntCI, "^\(51\)\s*Int\.C")       # (51)Int.C, OCR output can be "Int.CI." or "Int.Cl"
            mapping.add(PatentTemplate.SecTitle_InvTitle, "^\(54\)\s*发明名称")        # (54)发明名称
            mapping.add(PatentTemplate.SecTitle_Abstract, "^\(57\)\s*摘要")           # (57)摘要
            mapping.add(PatentTemplate.SecTitle_Claims, "^权\s*利\s*要\s*求\s*书$")    # 权利要求书
            mapping.add(PatentTemplate.SecTitle_Description, "^说\s*明\s*书$")        # 说明书
            mapping.add(PatentTemplate.SecTitle_Drawings, "^说\s*明\s*书\s*附\s*图$")  # 说明书附图
            mapping.add(PatentTemplate.DocEnd, "9876501234")

            PatentTemplate.Section_Regex_Map = mapping

        return PatentTemplate.Section_Regex_Map

    @staticmethod
    def get_subsection_regex_mapping() -> SimpleBiDict[str, str]:
        """
        Use a bidirection dictionary to map between subsections in "说明书" section and the regex patterns identifying them.
        """
        if PatentTemplate.Subsection_Regex_Map is None:
            mapping = SimpleBiDict[str, str]()

            # subsection titles in the description section.
            mapping.add(PatentTemplate.SubsecTitle_TechDomain, "^技术领域$")     # '技术领域'
            mapping.add(PatentTemplate.SubsecTitle_Background, "^背景技术$")     # '背景技术'
            mapping.add(PatentTemplate.SubsecTitle_InvContent, "^发明内容$")     # '发明内容'
            mapping.add(PatentTemplate.SubsecTitle_DrawingDes, "^附图说明$")     # '附图说明'
            mapping.add(PatentTemplate.SubsecTitle_ImplMethod, "^具体实施方式$")  # '具体实施方式'

            PatentTemplate.Subsection_Regex_Map = mapping

        return PatentTemplate.Subsection_Regex_Map
