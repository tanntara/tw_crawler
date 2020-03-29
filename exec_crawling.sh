#!/bin/sh

# クローリングを実行するスクリプト
# cron等で自動実行できるようにすればOK

# シェルスクリプトのあるディレクトリを取得
PROG_DIR=`dirname ${0}`

# 仮想環境に入る
source $PROG_DIR/venv/bin/activate

# pythonの実行
python $PROG_DIR/tw_crawler.py > $PROG_DIR/exec.log
