# -*- coding: utf-8 -*-
import win32com.client	
import os

qi = win32com.client.Dispatch("MSMQ.MSMQQueueInfo")
computer_name = os.getenv('COMPUTERNAME')
qi.FormatName="direct=os:"+computer_name+"\\private$\\Tasks;journal"
strFind = "{report:9}"
strOutputPath = r"Output.txt"

from constants import *
queue = qi.Open(MQ_PEEK_ACCESS, MQ_DENY_NONE)

while True:     
     
     msg = queue.PeekCurrent(0,True,1000,0)
     if msg:          
             
         print( msg.Label )
         print( msg.Body )
         #test Body for search string and write it out to disk
         if strFind in msg.Body:
             with open(strOutputPath, "w") as text_file:
                text_file.write("{}\n{}".format(msg.SentTime, msg.Body))
                
         msg = queue.PeekNext(0,True,1000,0)               
     else:
         print("No More Messages in Queue")
         break
queue.Close()


