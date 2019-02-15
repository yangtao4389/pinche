"""
常量定义的地方
"""
from enum import Enum
STATUS = YES_OR_NO = (
    ("T", "有效"),
    ("F", "无效"),
)
STATUS2 = (
    ("T", "是"),
    ("F", "否"),
)
STATUS_T = 'T'
STATUS_F = 'F'




class ConstantCode(Enum):
    Error = -1
    Right = 0

class ConstantResolution(Enum):
    HD = "hd"  # 高清
    SD = "sd"  # 标清