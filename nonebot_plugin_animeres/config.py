from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Generator, overload
from pydantic import BaseModel
from nonebot import get_driver


try:
    from nonebot.adapters.onebot.v11 import Message
except Exception:
    ...


class Config(BaseModel):
    cartoon_proxy: Optional[str] = None
    cartoon_forward: bool = False
    cartoon_length: int = 3
    cartoon_formant: str = "{title}\n{magnet}"

global_config = Config(**get_driver().config.dict())


@dataclass
class Cartoon:
    """资源"""
    title: str
    tag: str
    size: Optional[str] = None
    link: Optional[str] = None
    magnet: str = ""

    def to_string(self) -> str:
        return global_config.cartoon_formant.format(self.__dict__)


class Cartoons:
    """多个资源"""
    _keys: Optional[List[str]] = None

    def __init__(self, cartoons: List[Cartoon]):
        self.cartoons: List[Cartoon] = []
        self.sort: Dict[str, List[Cartoon]] = {}    # 分类
        self.add(*cartoons)
    
    def __repr__(self) -> str:
        return str(self.cartoons)
    
    @property
    def keys(self) -> List[str]:
        """资源的全部类型

        Returns:
            List[str]: 资源类型
        """
        if self._keys is None:
            self._keys = list(self.sort.keys())
        return self._keys
    
    def add(self, *cartoons: Cartoon):
        """添加资源"""
        for cartoon in cartoons:
            self.cartoons.append(cartoon)
            sort = self.sort.get(cartoon.tag)
            if sort is None:    # 当该资源类型不存在时刷新keys
                self._keys = None
                self.sort[cartoon.tag] = []
            self.sort[cartoon.tag].append(cartoon)
    
    @overload
    def __getitem__(self, value: int) -> Cartoon: ...
    @overload
    def __getitem__(self, value: slice) -> "Cartoons": ...
    def __getitem__(self, value: Union[int, slice]) -> Union[Cartoon, "Cartoons"]:
        if isinstance(value, int):
            return self.cartoons[value]
        return Cartoons(self.cartoons[value])

    def get(self, 
            key: Union[int, str]
            ) -> Optional["Cartoons"]:
        """获取资源

        Returns:
            Cartoons: 多个资源
        """
        try:
            key = self.keys[key] if isinstance(key, int) else key
            return Cartoons(self.sort[key])
        except IndexError:
            return None

    def __iter__(self) -> Generator[Cartoon, None, None]:
        yield from self.cartoons
    
    def forward_msg(self, 
                    uin: int, 
                    anime: Optional["Cartoons"] = None,
                    ) -> List[dict]:
        """合并转发

        Args:
            uin (int): 用户QQ
            anime (Optional[&quot;Cartoons&quot;], optional): 多个资源. Defaults to None.

        Returns:
            List[dict]: 合并转发内容
        """
        return [{
            "type": "node",
            "data": {
                "name": "使用迅雷等bit软件下载",
                "uin": uin,
                "content": Message(i.to_string())
                }
            } for i in anime or self]
    
    def __bool__(self) -> bool:
        return bool(self.cartoons)
