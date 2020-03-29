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
        print("id" + str(user.id))
        print("random user data -> user:" + user.name + ", screen_name:" + user.screen_name + ", lang:" + user.language_code.value)
        print("follower_next:" + str(user.follower_next_cursor) + " friends_next:" + str(user.friends_next_cursor))

        # フォロワーを取得してDBに登録
        follower_data = tw.get_follower_ids(user_id=user.id, next_cursor=user.follower_next_cursor)
        print(follower_data)
        follower_ids = follower_data["ids"]
        user.follower_next_cursor = follower_data["next_cursor"]
        # print(follower_ids)
        sql.upsert_follows(user.id, follower_ids)
        sql.insert_id_only(follower_ids)

        # フォローを取得してDBに登録
        follow_data = tw.get_friend_ids(user_id=user.id, next_cursor=user.friends_next_cursor)
        friends_ids = follow_data["ids"]
        user.friends_next_cursor = follow_data["next_cursor"]
        # print(follow_ids)
        sql.upsert_followings(friends_ids, user.id)
        sql.insert_id_only(friends_ids)

        print("update cursor -> "
              "id:" + str(user.id) +
              "  follower_next:" + str(user.follower_next_cursor) +
              " frineds_next:" + str(user.friends_next_cursor))
        sql.update_next_cursor(user)


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

    # users = tw.get_users(screen_names=["TamaZooPark" ,"InokashiraZoo"])
    # sql.upsert_user(users)
    try:
        users = sql.get_random_user(count=1, lang=LanguageType.JA.value)
        for user in users:
            # 確認用
            print("id" + str(user.id))
            print(
                "random user data -> user:" + user.name + ", screen_name:" + user.screen_name + ", lang:" + user.language_code.value)
            print("follower_next:" + str(user.follower_next_cursor) + " friends_next:" + str(user.friends_next_cursor))

            # フォロワーを取得してDBに登録
            follower_data = tw.get_follower_ids(user_id=user.id, next_cursor=user.follower_next_cursor)
            print(follower_data)
            follower_ids = follower_data["ids"]
            user.follower_next_cursor = follower_data["next_cursor"]
            # print(follower_ids)
            sql.upsert_follows(user.id, follower_ids)
            sql.insert_id_only(follower_ids)

            # フォローを取得してDBに登録
            follow_data = tw.get_friend_ids(user_id=user.id, next_cursor=user.friends_next_cursor)
            friends_ids = follow_data["ids"]
            user.friends_next_cursor = follow_data["next_cursor"]
            # print(follow_ids)
            sql.upsert_followings(friends_ids, user.id)
            sql.insert_id_only(friends_ids)

            print("update cursor -> "
                  "id:" + str(user.id) +
                  "  follower_next:" + str(user.follower_next_cursor) +
                  " frineds_next:" + str(user.friends_next_cursor))
            sql.update_next_cursor(user)
    except Exception as e:
        print(traceback.format_exc(()))