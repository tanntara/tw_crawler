#!/usr/bin/env python3
# twitterへの接続、取得などを行う

import json
import tw_manager.tw_object as tw_object
from requests_oauthlib import OAuth1Session


class Manager:
    # OAuth1Session
    tw = None

    def __init__(self, setting_path):
        # ここ設定ファイルの読み込み
        setting_text = open(setting_path, "r")
        setting = json.load(setting_text)

        ck = setting["api_key"]
        cs = setting["api_key_secret"]
        at = setting["access_token"]
        ats = setting["access_token_secret"]

        self.tw = OAuth1Session(ck, cs, at, ats)

    def get_follower_ids(self, user_id=None, screen_name=None, count=5000):
        # パラメータ生成
        params = {
            'count': count
        }
        if id is not None:
            params.setdefault("user_id", user_id)
        elif screen_name is not None:
            params.setdefault("screen_name", screen_name)

        url = "https://api.twitter.com/1.1/followers/ids.json"  # ユーザリスト取得エンドポイント
        return self.inner_get_ids(url, params)

    def get_friend_ids(self, user_id=None, screen_name=None, count=5000):
        # パラメータ生成
        params = {
            'count': count
        }
        if id is not None:
            params.setdefault("user_id", user_id)
        elif screen_name is not None:
            params.setdefault("screen_name", screen_name)

        url = "https://api.twitter.com/1.1/friends/ids.json"  # ユーザリスト取得エンドポイント
        return self.inner_get_ids(url, params)

    # （プライベート）idリスト取得メソッド
    # url:　APIエンドポイント
    # params: パラメータ辞書
    def inner_get_ids(self, url, params):
        # APIから取得
        res = self.tw.get(url, params=params)

        if res.status_code == 200:  # 正常通信出来た場合
            j_ids = json.loads(res.text)  # レスポンスからタイムラインリストを取得
            # print("Success get ids. from %s", url)
            # print(j_ids)
            return j_ids["ids"]
        else:  # 正常通信出来なかった場合
            print("Failed: %d" % res.status_code)
            return None

    def get_users(self, user_ids=None, screen_names=None):
        params = { }
        if user_ids is not None:
            params.setdefault("user_id", user_ids)
        elif screen_names is not None:
            params.setdefault("screen_name", screen_names)

        url = "https://api.twitter.com/1.1/users/lookup.json"   #　ユーザー情報取得エンドポイント
        res = self.tw.get(url, params=params)

        if res.status_code == 200:  # Success
            j_users = json.loads(res.text)
            users = []
            for r in j_users:
                # print(r)
                users.append(tw_object.User(r))
            return users
        else:  # 正常通信出来なかった場合
            print("Failed: %d" % res.status_code)
            return None


def test():
    m = Manager("tw_manager/tw_setting.json")
    # ids = m.get_follower_ids(screen_name="TamaZooPark")
    ids = m.get_friend_ids(screen_name="TamaZooPark")
    for id in ids:
        print(str(id) + ",")


if __name__ == "__main__":
    test()