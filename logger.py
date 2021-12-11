from logging import DEBUG, getLogger
import logging.handlers
import sys



"""
ログを初期化する\n
実行ファイルでは、このモジュールとloggingをインポートし、その他のファイルではloggingをインポートし,\n
logger=logging.getLogger(__name__)で使用する
"""


# ルートロガーの作成
logger = getLogger('')
logger.setLevel(DEBUG)


# ログの出力形式の設定
formatter = logging.Formatter(
    '[%(levelname)6s] %(message)s')

# ログのコンソール出力の設定
sh = logging.StreamHandler(sys.stderr)
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)

# ログのファイル出力の作成


# ルートロガーに追加

logger.addHandler(sh)
