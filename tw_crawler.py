#!/usr/bin/env python3
#　ツイッタをクローリングする

import tw_manager.manager as tw_manager
import sql_manager.manager as sql_manager
import os
import traceback
from tw_manager.tw_object import LanguageType


tw = tw_manager.Manager(os.path.abspath(os.path.dirname(__file__)) + "/setting/tw_setting.json")
sql = sql_manager.Manager(os.path.abspath(os.path.dirname(__file__)) + "/setting/mysql_setting.json")


def get_follows():
    users = sql.get_random_user(count=1, lang=LanguageType.JA.value)
    for user in users:
        # 確認用
        print(str(user["id"]))
        print("randome user data -> user:" + user["name"] + ", screen_name:" + user["screen_name"] + ", lang:" + user["language_code"])
        user_id = user["id"]
        follower_ids = tw.get_follower_ids(user_id=user_id)
        # print(follower_ids)
        sql.upsert_follows(user_id, follower_ids)
        sql.insert_id_only(follower_ids)

        follow_ids = tw.get_friend_ids(user_id=user_id)
        # print(follow_ids)
        sql.upsert_followings(follow_ids, user_id)
        sql.insert_id_only(follow_ids)


def get_user_detail():
    # DB上でIDしか持たないユーザーの詳細を設定する
    # IDしか持たないユーザーを取得
    user_ids = sql.get_none_detail_user(count=100)
    users = tw.get_users(user_ids=user_ids)
    sql.upsert_user(users=users)


def set_user(user_names):
    users = tw.get_users(screen_names=user_names)
    sql.upsert_user(users)


def crawling(get_frollow_num=1, get_user_num=1):
    # set_user(["InokashiraZoo", "TamaZooPark"])

    for i in range(get_frollow_num):
        get_follows()

    for i in range(get_user_num):
        get_user_detail()


if __name__ == "__main__":
    try:
        crawling(get_frollow_num=1, get_user_num=1)
    except Exception as e:
        print(traceback.format_exc(()))


def test():
    sql = sql_manager.Manager(os.path.abspath(os.path.dirname(__file__)) + "/setting/test_mysql.json")
    users = tw.get_users(screen_names=["TamaZooPark" ,"InokashiraZoo"])
    sql.upsert_user(users)
    try:
        users = sql.get_random_user(count=1, lang="ja")
        for user in users:
            user_id = user["id"]
            follower_ids = tw.get_follower_ids(user_id=user_id)
            # print(follower_ids)
            sql.upsert_follows(user_id, follower_ids)
            sql.insert_id_only(follower_ids)

            follow_ids = tw.get_friend_ids(user_id=user_id)
            # print(follow_ids)
            sql.upsert_followings(follow_ids, user_id)
            sql.insert_id_only(follow_ids)

            # DB上でIDしか持たないユーザーの詳細を設定する
            # IDしか持たないユーザーを取得
            user_ids = sql.get_none_detail_user(count=100)
            users = tw.get_users(user_ids=user_ids)
            sql.upsert_user(users=users)
    except Exception as e:
        print(traceback.format_exc(()))