from pydantic import BaseModel
from typing import Optional, Callable, Awaitable, Union



class AnimeRes(BaseModel):
    """动漫资源"""

    title: str  # 标题
    tag: str  # 用于分类的标签
    size: Optional[str] = None  # 大小
    link: Optional[str] = None  # 跳转链接
    magnet: str = ""  # 种子链接


class Tag(BaseModel):
    """动漫资源类型"""

    id: int  # 类型id
    name: str  # 类型名称

    def __repr__(self) -> str:
        return f"<{self.id}: {self.name}>"

    def __eq__(self, value: Union["Tag", int, str]) -> bool:
        if isinstance(value, Tag):
            return self.name == value.name
        elif isinstance(value, int):
            return self.id == value
        elif isinstance(value, str):
            return self.name == value
