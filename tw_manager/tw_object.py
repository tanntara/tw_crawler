#!/usr/bin/env python3
# ツイッターの戻り値オブジェクト

from enum import Enum, auto
import datetime
from langdetect import detect


class LanguageType(Enum):
    NONE = ""
    AR = "ar"
    BG = "bg"
    BN = "bn"
    CA = "ca"
    CS = "cs"
    CY = "cy"
    DA = "da"
    DE = "de"
    EL = "el"
    EN = "en"
    ES = "es"
    ET = "et"
    FA = "fa"
    FI = "fi"
    FR = "fr"
    GU = "gu"
    HE = "he"
    HI = "hi"
    HR = "hr"
    HU = "hu"
    ID = "id"
    IT = "it"
    JA = "ja"
    KN = "kn"
    KO = "ko"
    LT = "lt"
    LV = "lv"
    MK = "mk"
    ML = "ml"
    MR = "mr"
    NE = "ne"
    NL = "nl"
    NO = "no"
    PA = "pa"
    PL = "pl"
    PT = "pt"
    RO = "ro"
    RU = "ru"
    SK = "sk"
    SL = "sl"
    SO = "so"
    SQ = "sq"
    SV = "sv"
    SW = "sw"
    TA = "ta"
    TE = "te"
    TH = "th"
    TL = "tl"
    TR = "tr"
    UK = "uk"
    UR = "ur"
    VI = "vi"
    ZHCN = "zh - cn"
    ZHTW = "zh - tw"

    @classmethod
    def value_of(cls, target_value):
        for e in LanguageType:
            if e.value == target_value:
                return e
        raise ValueError('{} は有効な値ではありません'.format(target_value))


class User:
    id = 0
    name = ""
    screen_name = ""
    location = ""
    # derived = ()
    # url = ""
    # description = ""
    protected = False
    verified = True
    # follower_count = 0
    # friends_count = 0
    # listed_count = 0
    # favourites_count = 0
    # statuses_count = 0
    # created_at = datetime.datetime.now()
    # profile_banner_url = ""
    # profile_image_url_https = ""
    # default_profile = False
    # default_profile_image = False
    # withheld_in_countries = ()
    # withheld_scope = ""
    modified = datetime.datetime.now()
    follower_next_cursor = 0
    friends_next_cursor = 0
    language_code = LanguageType.NONE

    def __init__(self, tw_params_dic=None, lang="en"):
        self.id = tw_params_dic["id"]
        self.name = tw_params_dic["name"]
        self.screen_name = tw_params_dic["screen_name"]
        self.location = tw_params_dic["location"]
        # self.derived = tw_params_dic["derived"]
        # self.url = tw_params_dic["url"]
        # self.description = tw_params_dic["description"]
        self.protected = tw_params_dic["protected"]
        self.verified = tw_params_dic["verified"]
        # self.follower_count = tw_params_dic["follower_count"]
        # self.friends_count = tw_params_dic["friends_count"]
        # self.listed_count = tw_params_dic["listed_count"]
        # self.favourites_count = tw_params_dic["favourites_count"]
        # self.statuses_count = tw_params_dic["statuses_count"]
        # self.created_at = tw_params_dic["created_at"]
        # self.profile_banner_url = tw_params_dic["profile_banner_url"]
        # self.profile_image_url_https = tw_params_dic["profile_image_url_https"]
        # self.default_profile = tw_params_dic["default_profile"]
        # self.default_profile_image = tw_params_dic["default_profile_image"]
        # self.withheld_in_countries = tw_params_dic["withheld_in_countries"]
        # self.withheld_scope = tw_params_dic["withheld_scope"]
        self.language_code = self.lang_detect(tw_params_dic["description"])

        print()

    def lang_detect(self, text):
        # 変換できない文字列--空白や絵文字のみ--で構成される場合は例外が発生する模様
        try:
            code = detect(text)
            l = LanguageType.value_of(code)
            return l
        except:
            ValueError('{} は有効な値ではありません'.format(text))
            return LanguageType.NONE

    def get_str(self):
        return "name:" + self.name + "  screen_name:" + self.screen_name + "  lang:" + self.language_code.value