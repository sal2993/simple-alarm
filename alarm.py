#!/usr/bin/env python

import sys
from datetime import datetime
import subprocess

def main():
  print "Hello to uAlarm"

  if (len(sys.argv) != 3):
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
  
  # for testing purposes only
  # if want to test some times then comment the last line of file. 
  else: 
    time1 = sys.argv[1].split(":")
    time2 = sys.argv[2].split(":")

    wake_hour_int = int(time2[0])
    wake_min_int = int(time2[1])

    x = datetime(2006,1,1,int(time1[0]),int(time1[1]))

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
  output_time = "./turn.py " + str(alarmtime) 
  subprocess.call(output_time, shell=True)



if __name__ == "__main__":
  main()
