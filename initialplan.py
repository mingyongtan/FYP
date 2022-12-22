# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 16:27:41 2022

@author: admin
"""
import sim as vrep
import imageprocessin2 as ip
import numpy as np
import imutils
import cv2
import time

vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999, True, True, 5000, 5)
red_lower = np.array([-10, 50, 50])
red_upper = np.array([10, 255, 255])
stop = vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
time.sleep(4)
print("!!")
start = vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)

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
              if cv2.waitKey(1) & 0xFF == ord('q'):
                  break
          elif err == vrep.simx_return_novalue_flag:
              print("no image yet")
              pass
          else:
              print(err)
cv2.destroyAllWindows()

if __name__ == '__main__':
      
    visions()
        