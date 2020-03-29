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

    def __init__(self):
        pass

    @classmethod
    def create_user_from_tw(cls, tw_params_dic):
        user = User()
        user.id = tw_params_dic["id"]
        user.name = tw_params_dic["name"]
        user.screen_name = tw_params_dic["screen_name"]
        user.location = tw_params_dic["location"]
        # user.derived = tw_params_dic["derived"]
        # user.url = tw_params_dic["url"]
        # user.description = tw_params_dic["description"]
        user.protected = tw_params_dic["protected"]
        user.verified = tw_params_dic["verified"]
        # user.follower_count = tw_params_dic["follower_count"]
        # user.friends_count = tw_params_dic["friends_count"]
        # user.listed_count = tw_params_dic["listed_count"]
        # user.favourites_count = tw_params_dic["favourites_count"]
        # user.statuses_count = tw_params_dic["statuses_count"]
        # user.created_at = tw_params_dic["created_at"]
        # user.profile_banner_url = tw_params_dic["profile_banner_url"]
        # user.profile_image_url_https = tw_params_dic["profile_image_url_https"]
        # user.default_profile = tw_params_dic["default_profile"]
        # user.default_profile_image = tw_params_dic["default_profile_image"]
        # user.withheld_in_countries = tw_params_dic["withheld_in_countries"]
        # user.withheld_scope = tw_params_dic["withheld_scope"]
        user.language_code = User.lang_detect(tw_params_dic["description"])
        return user

    @classmethod
    def create_user_from_sql(cls, param):
        user = User()
        user.id = param["id"]
        user.name = param["name"]
        user.screen_name = param["screen_name"]
        user.language_code = LanguageType.value_of(param["language_code"])
        user.modified = param["modified"]
        user.follower_next_cursor = param["follower_next_cursor"]
        user.friends_next_cursor = param["friends_next_cursor"]
        return user

    @classmethod
    def lang_detect(cls, text):
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