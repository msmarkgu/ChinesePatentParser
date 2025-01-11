import json, os

from typing import Dict, List, Tuple, Optional

from .patent_template import PatentTemplate

class PatentInstance:
    """
    Represent a concrete patent document.
    """
    
    def __init__(self):
        self.__ocr_text = ''   # OCR result

        self.PubNumber = ''    # (10)申请公布号
        self.PubDate = ''      # (43)申请公布日
        self.AppNumber = ''    # (21)申请号
        self.AppDate = ''      # (22)申请日
        self.Applicant = ''    # (71)申请人
        self.Inventor = ''     # (72)发明人
        self.Agent = ''        # (74)专利代理机构
        self.IntCI = ''        # (51) Int.CI. International Classification Id
        self.Title = ''        # (54)发明名称
        self.Abstract = ''     # (57)摘要

        self.ClaimItems = []   # 权利要求书
        self.DescItems  = []   # 说明书
        self.TechDomain = []   # 说明书 -- 技术领域
        self.Background = []   # 说明书 -- 背景技术
        self.InvContent = []   # 说明书 -- 发明内容
        self.DrawingDes = []   # 说明书 -- 附图说明
        self.ImplMethod = []   # 说明书 -- 具体实施方式
        self.ApxDrawing = []   # 说明书附图

    def set_ocr_text(self, text):
        self.__ocr_text = text
        
    def get_orc_text(self):
        return self.__ocr_text

    def __repr__(self):
        data = [
            f"Pub No.: {self.PubNumber}",
            f"Pub Date.: {self.PubDate}",
            f"App No.: {self.AppNumber}",
            f"App Date.: {self.AppDate}",

            f"Title: {self.Title}", 
            f"Applicant: {self.Applicant}",
            f"Inventor: {self.Inventor}",
            f"Agent: {self.Agent}",
            f"INT.CI: {self.IntCI}",

            f"Abstract: {self.Abstract}",
            f"Claims: {len(self.ClaimItems)} items", 
            f"Description: {len(self.DescItems)} items",
            f"TechDomain: {len(self.TechDomain)}", 
            f"Background: {len(self.Background)} items", 
            f"InvContent: {len(self.InvContent)} items", 
            f"DrawingDes: {len(self.DrawingDes)} items", 
            f"ImplMethod: {len(self.ImplMethod)} items" 
        ]
        return '\n'.join(data)
    
    def to_json(self) -> str:
        data = {}

        data[PatentTemplate.SecTitle_PubNumber] = self.PubNumber   # "申请公布号"
        data[PatentTemplate.SecTitle_PubDate] = self.PubDate       # "申请公布日"
        data[PatentTemplate.SecTitle_AppNumber] = self.AppNumber   # "申请号"
        data[PatentTemplate.SecTitle_AppDate] = self.AppDate       # "申请日"
        data[PatentTemplate.SecTitle_Applicant] = self.Applicant   # "申请人"
        data[PatentTemplate.SecTitle_Inventor] = self.Inventor     # "发明人"
        data[PatentTemplate.SecTitle_Agent] = self.Agent           # "代理机构"
        data[PatentTemplate.SecTitle_IntCI] = self.IntCI           # "国际分类号"

        data[PatentTemplate.SecTitle_InvTitle] = self.Title        # "发明名称"
        data[PatentTemplate.SecTitle_Abstract] = self.Abstract     # "摘要"

        data[PatentTemplate.SecTitle_Claims] = self.ClaimItems     # "权利要求书"

        # subsections in "说明书"
        data[PatentTemplate.SubsecTitle_TechDomain] = self.TechDomain  # "技术领域"
        data[PatentTemplate.SubsecTitle_Background] = self.Background  # "背景技术"
        data[PatentTemplate.SubsecTitle_InvContent] = self.InvContent  # "发明内容"
        data[PatentTemplate.SubsecTitle_DrawingDes] = self.DrawingDes  # "附图说明"
        data[PatentTemplate.SubsecTitle_ImplMethod] = self.ImplMethod  # "具体实施方式"

        return json.dumps(data, ensure_ascii=False, indent=2)
