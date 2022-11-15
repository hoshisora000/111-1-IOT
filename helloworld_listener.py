#!/usr/bin/env python3 # 告訴系統該檔案為 Python 檔。

import rospy  # 導入 rospy 這個 class。
from std_msgs.msg import String # 導入 String 這個 class。

def callback(data): # 自訂一個callback函數，參數為 data
	rospy.loginfo(rospy.get_caller_id() + ' I heard %s' % data.data)
    # 在 Terminal 上印出內容。
	
if __name__ == '__main__':
	rospy.init_node('user1_listener',anonymous=True)
    # 初始化一個名叫 user1_listener 的 node，並且其為匿名(問題討論2)
	sub = rospy.Subscriber('testtopic',String,callback)
    # rospy.Publisher 初始化，讓他可以對 testtopic 這個 topic 接收訊息
    # 當接收到訊息後呼叫 callback 處理收到的內容
	rospy.spin() # 讓python保持執行直到該node停止
