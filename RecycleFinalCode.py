import time
import random
import sys
sys.path.append('../')

from Common_Libraries.p3b_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim():
  try:
    my_table.ping()
  except Expection as error_update_sim:
    print (error_update_sim)
    
### Constants
speed = 0.2 #Qbots speed

### Initialize the QuanserSim Environment
my_table = servo_table()
arm = qarm()
arm.home()
bot = qbot(speed)

#function created to dispense container
def dispense(bottle_ID):
  #makes the local variable "mat_info" global so it can be used in other functions
  global mat_info
  #assigns container properties to variable "mat_info"
  mat_info = my_table.container_properties(bottle_ID)
  #dispenses container called in mat_info
  my_table.dispense_container()
  print(mat_info)
  return(mat_info)

#function created to load containers onto hopper
def load(bottle_ID):
  num_container = 1
  #initial angle for bottle placement
  angle = -110
  #makes the local variable "binID" gloabel so it can be used in other functions
  global binID
  binID = 0
  
  #assigns mass of container to variable
  container_mass = mat_info[1]
  print(container_mass)
  total_mass = container_mass
  new_bin_ID = binID
  
  while binID == new_bin_ID nd num_container <= 3 and total_mass <= 90:
    #checks if new container has the same binID as the previous container, number of containers on hopper is less than or equal to 3 and total mass of containers is less than or equal to 90
    
    #assigns bin nmber to variable
    binID = mat_info[2]
    print(binID)
    #increments number of containers by one
    num_container += 1
    #functions to pick up and transfer container from table to hopper start here
    arm.move_arm(0.65,0,0.25)
    time.sleep(0.2)
    arm.control_gripper(45)
    time.sleep(0.2)
    arm.move_arm(0.4064,0,0.4826)
    time.sleep(0.2)
    arm.rotate_base(angle)
    time.sleep(0.2)
    arm.rotate_elbow(17)
    time.sleep(0.2)
    arm.control_gripper(-25)
    time.sleep(0.2)
    arm.rotate_elbow(-47)
    time.sleep(0.2)
    arm.home()
    #increments angle at which bottle is placed by 20 deg
    angle += 20
    #functions to pick up and transfer container from table to hopper end here
    
    #picks random container from "bottles"
    bottle_ID = random.choice(bottles)
    #dispenses randomly chosen container
    dispense(bottle_ID)
    #assigns binID of new container to variable
    new_bin_ID = my_table.container_properties(bottle_ID) [2]
    #assigns mass of new container to variable
    container_mass = my_table.container_properties(bottle_ID) [1]
    #increments total mass by the mass of the newly dispensed container
    total_mass += container_mass
    
    print(total_mass)
return binID

#function created to transfer containers to appropriate bins
def transfer_container(binID):
  i = 0
  
  #assigns current time in environment to variable
  start = time.time()
  #checks if difference between current time in environment and start time is less than 4.6 seconds
  while time.time() - start<9.2:
    bot.forward_velocity(bot.follow_line(0.1)[1])
  while i < 4:
    i += 1
    bot.activate_color_sensor("Red")
    red = bot.read_red_color_sensor("Bin01",0.6)
    bot.deactivate_color_sensor()
    bot.activate_color_sensor("Green")
    red = bot.read_green_color_sensor("Bin02",0.6)
    bot.deactivate_color_sensor()    
    bot.activate_color_sensor("Blue")
    red = bot.read_blue_color_sensor("Bin03",0.6)
    bot.deactivate_color_sensor()
    if binID == "Bin01":
      if red[1] >= 4:
        break
      elif binID == "Bin02":
        if green[1] >= 4:
      elif binID == "Bin03":
        if blue[1] >= 4:
      elif binID == "Bin04":
        if blue[1] <= 0.5 and red[1] <= 0.5 and green[1] <= 0.5:
          break
      bot.forward_time(4.59)
      
#function created to dump container
def bot_dump():
  bot.deactivate_actuator()
  bot.dump()
  bot.deactivate_actuator()
  
def return home():
while bot.follow_line(0.1)[0] < 3:
  bot.forward_velocity(bot.follow_line(0.4)[1])
bot.stop
time.sleep(0.2)
bot.rotate(180)

#function to allow all functions to run
def main():
  i = 0
  while True:
    global bottles
    bottles = [1,2,3,4,5,6]
    bottle_ID = random.choice(bottles)
    while i<1:
      i += 1
      dispense(bottle_ID)
    load(bottle_ID)
    transfer_container(binID)
    bot_dump()
    return_home()
main()
