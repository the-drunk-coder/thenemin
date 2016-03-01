#!/usr/bin/env python
import skywriter
import signal
import thenemin_sound_functions as sound
import time
#some_value = 5000

block_flag = False;

base_speed = 0.5

def block(length):
  block_flag = True
  time.sleep(length)

  
@skywriter.move()
def move(x, y, z):
  if(not block_flag):
    print( x, y, z )
    grainlength=80+(y*200)
    sound.sampl("thenemin","sample", gain=max(0, 1.0-z), start=min(0.1 + x, 1), a=30, r=30, speed=base_speed, length=grainlength )
    block(grainlength/2000)
    
#@skywriter.flick()
#def flick(start,finish):
#  print('Got a flick!', start, finish)

#@skywriter.airwheel()
#def spinny(delta):
#  global some_value
#  some_value += delta
#  if some_value < 0:
#  	some_value = 0
#  if some_value > 10000:
#    some_value = 10000
#  print('Airwheel:', some_value/100)

#@skywriter.double_tap()
#def doubletap(position):
#  print('Double tap!', position)

#@skywriter.tap()
#def tap(position):

"""  
@skywriter.touch()
def touch(position):
  print(position)
  global base_speed
  if(position == "north"):
    print('Bassdrum!')
    #base_speed = base_speed - 0.02
    sound.sampl("bd","2")
  elif(position == "east"):
    print('Snare!')
    #base_speed = base_speed + 0.02
    sound.sampl("sn","4", speed=0.5)
"""  
signal.pause()
