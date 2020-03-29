#!/usr/bin/env python3
# manager.py   SQLサーバーへの接続を行う

from urllib.parse import urlparse
import mysql.connector
import json
import random
import traceback


class Manager:
    # 読み込んだ設定
    setting = None

    #　初期化
    def __init__(self, setting_path):
        # ここ設定ファイルの読み込み
        setting_text = open(setting_path, "r")
        self.setting = json.load(setting_text)

    # sqlカーソル取得
    def get_connection(self):
        # 'mysql://user:pass@localhost:3306/dbname'
        u = "mysql://" \
            + self.setting["user"] + ":" \
            + self.setting["password"] + "@" \
            + self.setting["host"] + ":" \
            + str(self.setting["port"]) + "/" \
            + self.setting["dbname"]
        url = urlparse(u)

        conn = mysql.connector.connect(
            host=url.hostname or 'localhost',
            port=url.port or 3306,
            user=url.username or 'root',
            password=url.password or '',
            database=url.path[1:],
        )
        return conn

    # あるユーザーのフォロワーのupsertを実行する
    def upsert_follows(self, to_id, from_ids):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            sql = 'insert into follow values(%s, %s, now()) ' \
                  'on duplicate key update modified = now()'
            for from_id in from_ids:
                cur.execute(sql, (from_id, to_id))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()

        conn.close()

    # あるユーザのフォローしている人をupsertする
    def upsert_followings(self, to_ids, from_id):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            sql = 'insert into follow values(%s, %s, now()) ' \
                  'on duplicate key update modified = now()'
            for to_id in to_ids:
                cur.execute(sql, (from_id, to_id))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()

        conn.close()

    # ユーザ情報のUpsert
    def upsert_user(self, users=None):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            sql = 'insert into user values(%s, %s, %s, %s, now(), %s, %s) ' \
                  'on duplicate key update ' \
                  'name = %s, ' \
                  'screen_name = %s, ' \
                  'language_code = %s, ' \
                  'modified = now(), ' \
                  'follower_next_cursor = %s, ' \
                  'friends_next_cursor = %s'
            for user in users:
                # print(user.name)
                cur.execute(sql, (
                    user.id,
                    user.name,
                    user.screen_name,
                    user.language_code.value,
                    user.follower_next_cursor,
                    user.friends_next_cursor,
                    user.name,
                    user.screen_name,
                    user.language_code.value,
                    user.follower_next_cursor,
                    user.friends_next_cursor
                ))
            conn.commit()
        except Exception:
            print(traceback.format_exc())
            conn.rollback()
        conn.close()

    def update_next_cursor(self, id, follower_next_cursor, friends_next_cursor):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            sql = 'update user set ' \
                  'follower_next_cursor = %s, ' \
                  'friends_next_cursor = %s ' \
                  'where id = %s '
            cur.execute(sql, (follower_next_cursor, friends_next_cursor, id))
            conn.commit()
        except Exception as e:
            print(traceback.format_exc())
            conn.rollback()
        conn.close()

    def insert_id_only(self, user_ids):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            sql = 'insert ignore into user (id) values(%s)'
            for user_id in user_ids:
                cur.execute(sql, [user_id])
            conn.commit()
        except Exception:
            print(traceback.format_exc())
            conn.rollback()
        conn.close()

    def get_random_user(self, count=15, lang=None):
        conn = self.get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            # 検索条件
            where_str = ""
            params = []
            if lang is not None:
                where_str += " where language_code = %s"
                params.append(lang)

            # ユーザーの数を取得
            # select count(*) as count from user {where 検索条件}
            count_sql = 'select count(*) as count from user'
            count_sql += where_str

            cur.execute(count_sql, params)
            max_num = cur.fetchone()["count"]
            print(str(max_num))

            # ユーザーテーブルからランダムに取得
            user_list = []
            # select * from user {where 検索条件} limit 1 offset %s
            random_sql = "select * from user"
            random_sql += where_str

            # 検索場所の指定 パラメータはfor文の中で指定する
            random_sql += " limit 1 offset %s"

            for i in range(count):
                # offset位置の指定
                params.append(random.randint(0, max_num - 1))
                cur.execute(random_sql, params)
                user_list.append(cur.fetchone())
                # 次のループのためにoffsetを削除して、全体のパラメータ数を戻しておく
                params.pop()        # 末尾のoffset位置を削除
            conn.close()
            return user_list
        except Exception as e:
            print(traceback.format_exc())
            conn.rollback()
            conn.close()
            return None


    def get_none_detail_user(self, count=1):
        conn = self.get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            # ID以外を持たないユーザーを取得
            sql = 'select * from user where name is null limit %s'
            cur.execute(sql, [count])
            id_dics = cur.fetchall()

            # 取得結果をIDのリストにして取得
            user_ids = []
            for id in id_dics:
                user_ids.append(id["id"])
            return user_ids
        except Exception as e:
            print(traceback.format_exc())
            conn.rollback()
            conn.close()
            return None


def test():
    m = Manager("sql_manager/mysql_setting.json")

    follow_ids = (1, 2, 3, 4, 5)
    m.upsert_follows(100, follow_ids)


if __name__ == "__main__":
    test()
