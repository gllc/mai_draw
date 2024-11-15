from pathlib import Path
from typing import List, Tuple

from PIL.Image import Image, new
from PIL.Image import open as iopen
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
from unicodedata import normalize

from db import Icon, Chara, Frame, Plate, manager, Title, UserChara


class ResourceManager:
    def __init__(self, path: str | Path):
        self.path = path if isinstance(path, Path) else Path(path)

        if not self.path.exists():
            raise FileNotFoundError(self.path)

    def get_icon(self, icon: Icon) -> Image:
        return iopen(self.path / "icon" / f"Icon_{str(icon.name.ID).zfill(6)}.png")

    def get_chara(self, chara: Chara) -> Image:
        return iopen(self.path / "chara" / f"Chara_{str(chara.name.ID).zfill(6)}.png")

    def get_frame(self, frame: Frame) -> Image:
        return iopen(self.path / "frame" / f"Frame_{str(frame.name.ID).zfill(6)}.png")

    def get_plate(self, plate: Plate) -> Image:
        return iopen(self.path / "nameplate" / f"Plate_{str(plate.name.ID).zfill(6)}.png")

    def get_chara_frame_base(self, chara: Chara) -> Image:
        try:
            return iopen(self.path / "map" / f"csl_frame_base_{str(chara.color.ID).zfill(6)}.png")
        except FileNotFoundError:
            return iopen(self.need_path / "chara" / "UI_Chara_RBase.png")

    def get_chara_frame(self, chara: Chara) -> Image:
        try:
            return iopen(self.path / "map" / f"csl_frame_{str(chara.color.ID).zfill(6)}.png")
        except FileNotFoundError:
            return iopen(self.need_path / "chara" / "UI_Chara_RFrame.png")

    def get_chara_star(self, chara: Chara) -> Image:
        try:
            return iopen(self.path / "map" / f"c_star_{str(chara.color.ID).zfill(6)}.png")
        except FileNotFoundError:
            return iopen(self.need_path / "chara" / "UI_Chara_Star.png")

    def get_chara_leve_frame(self, chara: Chara) -> Image:
        try:
            return iopen(self.path / "map" / f"clv_frame_{str(chara.color.ID).zfill(6)}.png")
        except FileNotFoundError:
            return iopen(self.need_path / "chara" / "UI_Chara_LFrame.png")

    def get_color(self, chara: Chara) -> tuple:
        return manager.MapColorDict[chara.color.ID].ColorDark.to_tuple()

    def get_fonts_path(self, name: str) -> Path:
        return self.path / "fonts" / name

    @property
    def need_path(self) -> Path:
        return self.path / "need"


Res_Manager = ResourceManager(Path(__file__).parent / "out")


class CardDraw:
    def __init__(self, name: str, icon: Icon | int, plate: Plate | int, frame: Frame | int, title: Title | int, chara: List[UserChara], resm: ResourceManager = Res_Manager):
        self.name = normalize("NFKC", name)
        self.icon: Icon = icon if isinstance(icon, Icon) else manager.IconDict[icon]
        self.plate: Plate = plate if isinstance(plate, Plate) else manager.PlateDict[plate]
        self.frame: Frame = frame if isinstance(frame, Frame) else manager.FrameDict[frame]
        self.title: Title = title if isinstance(title, Title) else manager.TitleDict[title]
        self.chara = chara
        self.resm = resm
        self.iframe = None
        self.ifd = None

    def draw_rating(self, rating: int):
        ratings = [15000, 14500, 14000, 13000, 12000, 10000, 7000, 4000, 2000, 1000, 0]
        for i in range(11):
            if rating >= ratings[i]:
                num = 11 - i
                break
        irating = iopen(self.resm.need_path / "rating" / f"UI_CMN_DXRating_{num:02}.png").resize((166, 32))
        rating = list(str(rating))
        rating.reverse()
        for i, v in enumerate(rating):
            inum = iopen(self.resm.path / "nums" / f"Drating_{v}.png").resize((16, 22))
            irating.alpha_composite(inum, (129 - i * 13, 5))
        self.iframe.alpha_composite(irating, (142, 32))

    def draw_class(self, classId: int):
        iclass = iopen(self.resm.need_path / "class" / f"UI_CMN_Class_S_{classId:02}.png").resize((110, 65))
        self.iframe.alpha_composite(iclass, (32 + 102 + 185, 6))

    def draw_dan(self, danId: int):
        idan = iopen(self.resm.need_path / "course" / f"UI_CMN_DaniPlate_{danId:02}.png").resize((84, 39))
        self.iframe.alpha_composite(idan, (32 + 102 + 197, 66))

    def get_stars(self, uchara: UserChara) -> Tuple[Image, Image]:
        cstar = self.resm.get_chara_star(uchara.characterId)
        starBig = cstar.copy().resize((44, 44))
        starSmail = cstar.resize((70, 70))
        if uchara.awakening == 5:
            starBig.alpha_composite(iopen(self.resm.need_path / "chara" / "UI_CMN_Chara_Star_Big.png").resize((44, 44)))
            starSmail.alpha_composite(iopen(self.resm.need_path / "chara" / "UI_CMN_Chara_Star_Small.png"), (-3, -3))
        elif uchara.awakening == 6:
            starBig.alpha_composite(iopen(self.resm.need_path / "chara" / "UI_CMN_Chara_star_big_MAX.png").resize((44, 44)))
            starSmail.alpha_composite(iopen(self.resm.need_path / "chara" / "UI_CMN_Chara_star_small_MAX.png"), (-3, -3))
        else:
            starSmail.alpha_composite(iopen(self.resm.need_path / "chara" / "UI_CMN_Chara_Star_Small.png"), (-3, -3))
            levels = [1, 9, 49, 99, 299, 999, 9999]
            pixels = 0
            for i in range(7):
                if uchara.level < levels[i]:
                    pixels = int((levels[i] - uchara.level) / (levels[i] - levels[i - 1]) * 106) + 12
                    break
            if pixels == 0:
                raise ValueError("Level error")
            starU = iopen(self.resm.need_path / "chara" / "UI_CMN_Chara_Star_Big_Gauge01.png")
            ssd = Draw(starU)
            ssd.rectangle((0, 12, starU.width, pixels), fill=(255, 255, 255, 0))

            starB = iopen(self.resm.need_path / "chara" / "UI_CMN_Chara_Star_Big_Gauge02.png").resize((44, 44))
            starB.alpha_composite(starU.resize((44, 44)))
            starBig.alpha_composite(starB)
        return starBig, starSmail

    def generate(self, uchara: UserChara) -> Image:
        chara = uchara.characterId
        c = self.resm.get_chara(chara).resize((200, 200))
        clf = self.resm.get_chara_frame(chara)
        clfb = self.resm.get_chara_frame_base(chara)
        color = self.resm.get_color(chara)

        bc = new(c.mode, c.size, color)
        calpha = c.split()[-1]
        bc.putalpha(calpha)
        bc.alpha_composite(c, (-10, 5))

        back_c = clfb.copy()
        back_c.alpha_composite(bc, (-13, 35))
        back_c.putalpha(iopen(self.resm.path / "mask.png").convert("L"))

        clfb.alpha_composite(back_c)
        clfb.alpha_composite(clf)

        starBig, starSmail = self.get_stars(uchara)
        clfb.alpha_composite(starBig, (52, 222))

        if uchara.awakening > 0:
            clfb.alpha_composite(starSmail.resize((26, 26)), (29, 223))
        if uchara.awakening > 1:
            clfb.alpha_composite(starSmail.resize((26, 26)), (93, 223))
        if uchara.awakening > 2:
            clfb.alpha_composite(starSmail.resize((22, 22)), (11, 213))
        if uchara.awakening > 3:
            clfb.alpha_composite(starSmail.resize((22, 22)), (115, 213))
        font_s = truetype(self.resm.get_fonts_path("FOT-RodinNTLGPro-EB.otf"), size=16)
        font_l = truetype(self.resm.get_fonts_path("FOT-RodinNTLGPro-EB.otf"), size=25)
        mcd = Draw(clfb)
        mcd.text((25 + (60 - len(str(uchara.level)) * 15) / 2, 16), "LV", fill=(255, 255, 255, 255), font=font_s)
        mcd.text((55 + (80 - len(str(uchara.level)) * 18) / 2, 9), str(uchara.level), fill=(255, 255, 255, 255), font=font_l)
        return clfb

    def draw_version(self, version1: str, version2: str):
        font = truetype(self.resm.get_fonts_path("GenSenMaruGothicTW-Regular.ttf"), size=20)

        def write_text(text: str, x: int, y: int, k: int = 0):
            fix = 0
            for i in range(len(text)):
                self.ifd.text((x + i * k + fix, y), text[i], fill=(255, 255, 255, 255), font=font, stroke_width=1, stroke_fill=0)
                if text[i] == ".":
                    fix -= 5

        write_text("Ver.CN", 910, 68, 13)
        write_text(version1, 988, 68, 13)
        write_text(f"-{version2}", 1036, 68, 8)

    def draw(self):
        white = (255, 255, 255, 255)
        black = (0, 0, 0, 255)
        # init frame
        self.iframe = self.resm.get_frame(self.frame)
        self.ifd = Draw(self.iframe)
        # plate
        self.iframe.alpha_composite(self.resm.get_plate(self.plate), (32, 26))
        # icon
        self.iframe.alpha_composite(self.resm.get_icon(self.icon).resize((102, 102)), (39, 33))
        # name
        name_font = truetype(self.resm.get_fonts_path("MO-UDShinGoSCGb4-Reg.otf"), size=20)
        self.iframe.alpha_composite(iopen(self.resm.path / "name_frame.png"), (144, 66))
        for i, c in enumerate(self.name):
            self.ifd.text((32 + 102 + 23 + i * 20, 26 + 40 + 10), c, fill=black, font=name_font)
        # title
        ititle_frame = iopen(self.resm.need_path / "title" / f"UI_CMN_Shougou_{self.title.rareType.name}.png")
        title_text = self.title.name.name if len(self.title.name.name.encode()) <= 19 else self.title.name.name[:19]
        title_font = truetype(self.resm.get_fonts_path("MO-UDShinGoSCGb4-DeB.otf"), size=14)
        self.iframe.alpha_composite(ititle_frame, (32 + 102 + 7, 26 + 76))
        self.ifd.text((32 + 102 + (276 - 10 - 14 * len(title_text) + 7 * len([i for i in title_text if len(i.encode()) == 1])) / 2, 26 + 86),
                      title_text, fill=white, font=title_font, stroke_width=1, stroke_fill=black)
        # draw main chara
        main_chara = self.chara[0]
        ichara = self.resm.get_chara(main_chara.characterId).resize((306, 306))
        self.iframe.alpha_composite(ichara, (-46, 146))
        mclf = self.resm.get_chara_leve_frame(main_chara.characterId)
        # chara level
        font_s = truetype(self.resm.get_fonts_path("FOT-RodinNTLGPro-EB.otf"), size=16)
        font_l = truetype(self.resm.get_fonts_path("FOT-RodinNTLGPro-EB.otf"), size=24)
        mcd = Draw(mclf)
        mcd.text((21, 12), "LV", fill=(255, 255, 255, 255), font=font_s)
        mcd.text((53 + (100 - 8 - len(str(main_chara.level)) * 18) / 2, 9), str(main_chara.level), fill=(255, 255, 255, 255), font=font_l)
        self.iframe.alpha_composite(mclf, (35, 364))

        starBig, starSmail = self.get_stars(main_chara)
        self.iframe.alpha_composite(starBig, (85, 399))
        if main_chara.awakening > 0:
            self.iframe.alpha_composite(starSmail.resize((26, 26)), (61, 403))
        if main_chara.awakening > 1:
            self.iframe.alpha_composite(starSmail.resize((26, 26)), (127, 403))
        if main_chara.awakening > 2:
            self.iframe.alpha_composite(starSmail.resize((22, 22)), (42, 400))
        if main_chara.awakening > 3:
            self.iframe.alpha_composite(starSmail.resize((22, 22)), (151, 400))

        for i, c in enumerate(self.chara[1:]):
            self.iframe.alpha_composite(self.generate(c), (205 + 139 * i, 178))

        # on icon
        ion = iopen(self.resm.need_path / "On.png")
        self.iframe.alpha_composite(ion, (1016, 25))

    def get_image(self) -> Image:
        return self.iframe
