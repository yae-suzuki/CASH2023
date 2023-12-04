import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import datetime
from sensor_msgs.msg import Image
import time
import requests
from playsound import playsound
import requests
from playsound import playsound

#from timeout_decorator import timeout, TimeoutError


# Sring型メッセージをサブスクライブして端末に表示するだけの簡単なクラス
class HscrSub(Node):
    def __init__(self): # コンストラクタ
        super().__init__('HSCR_Robot_sub_node')
        # サブスクライバの生成
        self.sub = self.create_subscription(String,'topic', self.callback, 10)#topicっていう名前の箱のサブスクライブ、Stringは形　受け取る
        self.publisher = self.create_publisher(Image,'result',10)#大事！resultっていう名前の箱にパブリッシュしてる。送ってる。rqtは通信を見えるようにする。動画をresultに送ってrqtでみてる。

    def callback(self, msg):  # コールバック関数 送られたときに起動
        self.get_logger().info(f'サブスクライブ: {msg.data}')
        VOICEVOX_URL = "http://localhost:50021"# VOICEVOX EngineのURL
        text = "かつおぶしが好きにゃ。"
        # 音声合成のためのクエリを生成
        response = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={
                "text": text,
                "speaker": 58,
                },
            )

        audio_query = response.json()

	    # 音声合成を行う
        response = requests.post(
            f"{VOICEVOX_URL}/synthesis",
		headers={
		    "Content-Type": "application/json",
		},
		params={
		    "speaker": 58,
		},
		json=audio_query,
            )
            
	    # ステータスコードが200以外の場合はエラーメッセージを表示
        if response.status_code != 200:
            print("エラーが発生しました。ステータスコード: {}".format(response.status_code))
            print(response.text)
        else:
	# 音声データを取得
            audio = response.content
	# 音声データをファイルに保存
            with open("output.wav", "wb") as f:
                f.write(audio)
	# 音声データを再生
            playsound("output.wav")

            
def main(args=None): # main¢p

    try:
        rclpy.init()#初期化
        node = HscrSub()#nodeにHscrを
        msg=String()#stringは文字列いれれる 
        while True:           
            rclpy.spin_once(node)#一回ノードを起動する　終わったらノード（プログラム）を終了
            node.text_to_speech()#movie_startを実行する
    except KeyboardInterrupt:
        pass#ctl+C(KeyboardInterrupt) node finish

#変更点の解説
#３１行目　movieに関するいらないもの削除
#３５行目　タブ追加→callbackないで作用するようにした
#３７行目　def削除　        ➘
#７４〜７９　削除（７６除く）  →→　defを実行しているところがない、if=__name__使用しないため
#７６行目→voicevox_urlの下に移動　

#rosでif = __name__は使わない（setup.pyでどのプログラムの何をノードとして実行するか記述されている。
#例えば"sub = hscr.20231016_sub_test:main'"の場合、
# hscrの中にある20231016_sub_testという名前のプログラムのmain部分を走らせてねって記述している
# if = __name__ はそのプログラムを実行させたときに if = __name__以下を実行させるもの　予め指定してあげてるから不要

#VOICEVOX_URL　voiceアプリに接続（裏で起動）
#これを文字が送られてきたらつながるようにした（最初からつなげておいても良いかも）

