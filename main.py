
"""
Created on Sun May  8 21:17:04 2022

@author: admin
"""

import cv2
import numpy as np
import time
import json
import sys
import sim as vrep
import imutils
import imageprocessin2 as ip
import keyboard
import threading
from keyboard import KeyboardEvent



command_list=[]
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999, True, True, 5000, 5)
red_lower = np.array([-10, 50, 50])
red_upper = np.array([10, 255, 255])
stop = vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
time.sleep(4)
print("!!")
start = vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)

        
    #while keyboard.read_key() != "q":
            
        
def init():
      cv2.startWindowThread()
      cv2.namedWindow("image")  
      visions()
      


def visions():
      print('Vision Sensor object handling')
      res, v1 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
      print('Getting first image')
      err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
      while vrep.simxGetConnectionId(clientID) != -1:
          err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
          if err == vrep.simx_return_ok:
              print("image OK!!!")
              img = np.array(image, dtype=np.uint8)
              img.resize([resolution[0], resolution[1], 3])
              img = imutils.rotate_bound(img, 180)
              gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
              canny_image = cv2.Canny(gray_image, 100, 200)
              cropped_image = ip.region_of_interest(canny_image,np.array([ip.region_of_interest_vertices], np.int32),)
              lines = cv2.HoughLinesP(canny_image,rho=6,theta=np.pi/180,threshold=160,lines=np.array([]), minLineLength=40,maxLineGap=25)
              print(lines)
              if ip.lines.any():
                  
                  #print(lines)
                  try:
                      image_with_lines = ip.drow_the_lines(img, lines)
                      #plt.imshow(image_with_lines)
                      #plt.show()
                  except:
                      image_with_lines = img
                    
                 
                  cv2.imshow('image', image_with_lines)
                  cv2.startWindowThread()
                  cv2.namedWindow("image")   
              if cv2.waitKey(1) & 0xFF == ord('e'):
                  break
          elif err == vrep.simx_return_novalue_flag:
              print("no image yet")
              pass
          else:
              print(err)
cv2.destroyAllWindows()

def detect_key():
    res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_blocking)
    err, target = vrep.simxGetObjectHandle(clientID, "Quadricopter_target", vrep.simx_opmode_blocking)
    err, arr = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_blocking)
    err, qrr = vrep.simxGetObjectOrientation(clientID, target, -1,  vrep.simx_opmode_blocking)
    
    while keyboard.read_key() != "q":
            if keyboard.is_pressed("w") :
                print('w KEY PRESSED')
                vrep.simxSetObjectPosition(clientID, target,-1,(arr[0] + 0.15,arr[1] ,arr[2]), vrep.simx_opmode_blocking)
                err, arr = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_blocking)
                print(arr)
                
            if keyboard.is_pressed("s") :
                print('s KEY PRESSED')
                vrep.simxSetObjectPosition(clientID, target,-1,(arr[0] - 0.15,arr[1] ,arr[2]), vrep.simx_opmode_blocking)
                err, arr = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_blocking)
                print(arr)
                
            if keyboard.is_pressed("a")  :
                print('a KEY PRESSED')
                vrep.simxSetObjectPosition(clientID, target,-1,(arr[0],arr[1] + 0.15,arr[2]), vrep.simx_opmode_blocking)
                err, arr = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_blocking)
                print(arr)
                 
            if keyboard.is_pressed("d")  :
                print('d KEY PRESSED')
                vrep.simxSetObjectPosition(clientID, target,-1,(arr[0],arr[1] - 0.15,arr[2]), vrep.simx_opmode_blocking)
                err, arr = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_blocking)
                print(arr)
                    
            if keyboard.is_pressed("left")  :
                print('left arrow KEY PRESSED')
                vrep.simxSetObjectOrientation(clientID, target,-1,(qrr[0] ,qrr[1] ,qrr[2] + 0.15), vrep.simx_opmode_blocking)
                err, qrr = vrep.simxGetObjectOrientation(clientID, target, -1, vrep.simx_opmode_blocking)
                print(qrr)
                    
            if keyboard.is_pressed("right")  :
                print('right arrow KEY PRESSED')
                vrep.simxSetObjectOrientation(clientID, target,-1,(qrr[0] ,qrr[1] ,qrr[2] - 0.15), vrep.simx_opmode_blocking)
                err, qrr = vrep.simxGetObjectOrientation(clientID, target, -1, vrep.simx_opmode_blocking)
                print(qrr)
        
            if keyboard.is_pressed( "up") :
                print('up arrow KEY PRESSED')
                vrep.simxSetObjectPosition(clientID, target,-1,(arr[0],arr[1] ,arr[2] + 0.15), vrep.simx_opmode_blocking)
                err, arr = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_blocking)
                print(arr)
                
            if keyboard.is_pressed("down")  :
                print('down arrow KEY PRESSED')
                vrep.simxSetObjectPosition(clientID, target,-1,(arr[0],arr[1] ,arr[2] - 0.15), vrep.simx_opmode_blocking)
                err, arr = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_blocking)
                print(arr)
            else:
                pass 
                
  
    
    
def record(file='path.txt'):    
    f = open(file, 'w+')
    
    keyboard_events = []
    keyboard.start_recording()
    detect_key()
    
    starttime = time.time()
    keyboard_events = keyboard.stop_recording()
    print(keyboard_events)
    print(starttime, file=f)

    for kevent in range(0, len(keyboard_events)):
        print(keyboard_events[kevent].to_json(), file = f)
    f.close()

      
def play(file="path.txt", speed = 1):
    f = open(file, 'r')
    rlines = f.readlines()
    f.close()
    keyboard_events = []
    print(keyboard_events)
    
    for index in range(2,len(rlines)):
        keyboard_events.append(keyboard.KeyboardEvent(**json.loads(rlines[index])))  
        
    print(keyboard_events)    
    
    starttime = float(rlines[0])
    starttime = starttime-120
    print(starttime)
    keyboard_time_interval = keyboard_events[0].time - starttime
    print(keyboard_time_interval)
    keyboard_time_interval /= speed
    print(keyboard_time_interval)
    k_thread = threading.Thread(target = lambda : time.sleep(keyboard_time_interval) == keyboard.play(keyboard_events, speed_factor=speed) )
    #m_thread = threading.Thread(target = lambda : time.sleep(keyboard_time_interval) == keyboard.play(movement, speed_factor=speed) )
    k_thread.start()
    detect_key()
    #m_thread.start()
    k_thread.join()
    #m_thread.join()
   
def main():  
    
    if clientID!= -1:
        print ('Connection establish')
        
        print ("1. New path \n")
        print ("2. Old path \n")
        print ("Enter number :")
        nums = 2
        
        if nums == 1:
            record()
        
    #v.join() 
        if nums == 2 :

            play()
    else:
        print("Failed to connect to remote API Server")
        vrep.simxFinish(clientID)  
        
if __name__ == '__main__':
      
    main()
        
    
            
 


