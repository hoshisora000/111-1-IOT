#!/usr/bin/env python3 # 告訴系統該檔案為 Python 檔。

import rospy  # 導入 rospy 這個 class。
from std_msgs.msg import String # 導入 String 這個 class。

if __name__ == '__main__':   # 當本程式被直接執行才有以下動作(問題討論1)
	rospy.init_node('user1',anonymous=True)  
    # 初始化一個名叫 user1 的 node，並且其為匿名(問題討論2)
	pub=rospy.Publisher('testtopic',String,queue_size=10) 
    # rospy.Publisher 初始化，讓他可以對 testtopic 這個 topic 發布訊息
	rate = rospy.Rate(10) # 設定保持迴圈循環是10hz (換句話說一秒執行10次)
	
	while not rospy.is_shutdown(): # 利用迴圈檢查程式是否被關閉、退出
		hello = 'hello world ! %s' % rospy.get_time() 
		pub.publish(hello)   # 將 hello 的內容發佈到 topic 上
		rospy.loginfo(hello)  # 在 Terminal 上印出 hello 的內容。
		rate.sleep() #等待能夠保持迴圈循環 10hz 的時間
