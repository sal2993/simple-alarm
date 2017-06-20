#!/usr/bin/env python

import sys
from datetime import datetime
from datetime import date
import subprocess

def main():
  print "Hello to uAlarm"

  wake_video_link = ""

  # If 0 command line arguments given
  if (len(sys.argv) == 1):
    print datetime.now()
    wake_hour = raw_input("enter the alarm hour [24-hour format, 07]: ")
    wake_min = raw_input("enter the alarm min [24-hour format, 30]: ")
    try: 
      wake_hour_int = int(wake_hour)
      wake_min_int = int(wake_min)
    except ValueError:
      print "Error: sorry you entered a wrong value"
      sys.exit(1)
      
    x = datetime.now()
    print x

  # If 1 command line argument is given
  # if you want to set the alarm from the a command line argument
  #   Ex. # ./alarm.py 7:25
  elif (len(sys.argv) == 2):
    # split 7:25 to time1 = [ 7 , 25 ]
    time1 = sys.argv[1].split(":")
    wake_hour_int = int(time1[0])
    wake_min_int = int(time1[1])
    wake_video_link = "https://www.youtube.com/feed/subscriptions"
    
    # Current time
    x = datetime.now()
    print x

  # Created for debugging/TESTING purposes ONLY!
  # if want to test some times then comment the last line of file. 
  elif (len(sys.argv) == 3) : 
    time1 = sys.argv[1].split(":")

    wake_video_link = sys.argv[2]

    wake_hour_int = int(time1[0])
    wake_min_int = int(time1[1])

    # current time
    x = datetime.now()

  # Alarm calculations actually begin below.
  else:
    print "Invalid command line number of arguments"
    print "Usage: alarm [WAKE_TIME]"

  alarmtime = 0
  print "Sleep time duration in Hours, Mins: "
  if (x.hour == wake_hour_int):
    if (x.minute == wake_min_int):
      print "Error: same hour and same mins for current time and alarm time"
      sys.exit(4)
    elif (x.minute < wake_min_int):
    #Example: Current time: 2:20, Wake time: 2:40
      print "0"
      print str(wake_min_int - x.minute)
      alarmtime = (wake_min_int - x.minute) * 60
    else:
    #Example: Current time: 2:20, Wake time: 2:01
      print "23"
      alarmtime = (23 * 60 * 60)
      print str(60 - (x.minute - wake_min_int))
      alarmtime = alarmtime + ((60 - (x.minute - wake_min_int)) * 60)
      
    
  elif (x.hour < wake_hour_int): 

    if (x.minute <= wake_min_int):
    #Example: Current time: 2:20, Wake time: 7:40
      print str(wake_hour_int - (x.hour + 1)) 
      alarmtime = ( (wake_hour_int - (x.hour + 1)) * 60 * 60)

      print str( 60 - x.minute + wake_min_int )
      alarmtime = alarmtime + ( ( 60 - x.minute + wake_min_int ) * 60)
    else:
    #Example: Current time: 2:52, Wake time: 7:35
      print str(wake_hour_int - (x.hour + 1)) 
      alarmtime = ( (wake_hour_int - (x.hour + 1)) * 60 * 60)

      print str( 60 - x.minute + wake_min_int )
      alarmtime = alarmtime + ( ( 60 - x.minute + wake_min_int ) * 60)

  else:
    print str((23 - x.hour) + wake_hour_int)
    alarmtime = (((23 - x.hour) + wake_hour_int) * 60 * 60)

    if (x.minute <= wake_min_int):
    #Example: Current time: 21:45, Wake time: 6:52
      print str(60 - x.minute + wake_min_int)
      alarmtime = alarmtime + ( (60 - x.minute + wake_min_int) * 60)
    else:
    #Example: Current time: 21:45, Wake time: 6:07
      print str(60 - x.minute + wake_min_int)
      alarmtime = alarmtime + ( (60 - x.minute + wake_min_int) * 60)
    
  # Get the number of hours and convert to second
  print ""
  print "alarm seconds:"
  print alarmtime
  print "Alarm set for " + str(wake_hour_int) + ":" + str(wake_min_int)
  print "/home/pi/Programs/alarm/turn.py " + str(alarmtime) + \
   " " + str(wake_video_link) + " &"

  # Message sent to turn.py
  output_time = "/home/pi/Programs/alarm/turn.py " + str(alarmtime) + \
   " " + str(wake_video_link) + " &"
  # /Message sent

  # JSON package
  meat = r'\{' +\
  fix_str(r"wakeup_time", str(wake_hour_int) + r':' + str(wake_min_int)) +\
  r', ' + fix_str(r"sleep_time", str(x.hour) +r':' + str(x.minute)) +\
  r', ' + fix_str(r"date_of_wake", x.isoformat()) +\
  r', ' + fix_str(r"wakeup_video", wake_video_link) +\
  r'}'
  
  json_info = r"ssh savior@104.131.178.67 \
  'echo " + meat + " >>\
 /home/savior/Applications/Kittenheads/llog_inputs/target.txt'"
  # /JSON package

  # Json sent
  subprocess.call(json_info, shell=True)

  # Delegate to turn.py
  #subprocess.call(output_time, shell=True)

# ("key", value) => {"key": "value=string"}
def fix_str(x, y):
  return r'\"' + str(x) + r'\"' + ":" + r'\"' + str(y) + r'\"'
if __name__ == "__main__":
  main()
