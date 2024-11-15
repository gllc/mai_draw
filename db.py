# welcome to MAIMAI!
from enum import StrEnum

from pydantic import BaseModel


class StrEnumType(StrEnum):

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class RareTypeEnum(StrEnumType):
    Normal = 'Normal'
    Bronze = 'Bronze'
    Silver = 'Silver'
    Gold = 'Gold'
    Rainbow = 'Rainbow'


class Color(BaseModel):
    R: int
    G: int
    B: int

    def to_tuple(self):
        return self.R, self.G, self.B


class IDName(BaseModel):
    ID: int
    name: str

    def __hash__(self):
        return hash(self.ID)

    def __repr__(self):
        return f"{self.name}({self.ID})"


class BaseItem(BaseModel):
    name: IDName

    def __repr__(self):
        return repr(self.name)


class MapColor(BaseItem):
    ColorGroupId: IDName
    ColorDark: Color


class Item(BaseItem):
    normText: str


class Chara(BaseItem):
    color: IDName


class Frame(Item):
    pass


class Icon(Item):
    pass


class Plate(Item):
    pass


class Title(Item):
    rareType: RareTypeEnum
    disable: bool


class Manager(BaseModel):
    MapColorDict: dict[int, MapColor]
    FrameDict: dict[int, Frame]
    IconDict: dict[int, Icon]
    CharaDict: dict[int, Chara]
    PlateDict: dict[int, Plate]
    TitleDict: dict[int, Title]


with open('draw.json', 'r', encoding='utf-8') as f:
    manager = Manager.model_validate_json(f.read())


class UserChara(BaseModel):
    characterId: int | Chara
    level: int = 1
    awakening: int = 0

    def __init__(self, characterId: int | Chara, level: int = 1):
        super().__init__(characterId=characterId, level=level)
        levels = [9, 49, 99, 299, 999, 9999]
        for i in range(len(levels)):
            if level >= levels[i]:
                self.awakening = i + 1
        if isinstance(characterId, int):
            self.characterId = manager.CharaDict.get(characterId, characterId)
