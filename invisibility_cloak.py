import cv2
import time
import numpy as np

#XVID is a format like jpeg, mp4. We are saying to save it in XVID format
fourcc=cv2.VideoWriter_fourcc(*'XVID')
#Output should format be in output.avi. 648, 480 is the size of the video
#cv2.VideoWriter( filename, fourcc, fps, frameSize )
output_file=cv2.VideoWriter('output.jpeg', fourcc, 20.0, (640, 480))

#read the video from the web cam
cap=cv2.VideoCapture(0)
#allow the camera to start
time.sleep(2)#2 seconds to start
bg=0#background 0

#capture the background in 60 frames
for i in range():
    #ret checks if we get a frame while reading the frame.
    ret,bg=cap.read()

#mirroring. Camera captures the object inverted so we are flipping the background
bg=np.flip(bg,axis=1)

#as long as the camera if reading the frame, it will store the image in "img". If we don't get any frame, it will break. 
#we are also flipping the image. 
while(cap.isOpened()):
    ret,img = cap.read()
    if not ret:
        break
    img=np.flip(img,axis=1)
#we need to convert the images from BGR (Blue Green Red) to HSV (Hue(0 is red, 120 is green, 240 is blue. They are degress), Saturation(purtity/intensity of the color), Value(brightness of the color)).
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# we are going to find the red color and going to mask it. 
#array([red, green, blue])
#the picture is big so we give 2 masks. 
    lower_red=np.array([0,120,50])
    upper_red=np.array([10,255,255])
    #1st mask
    mask_1=cv2.inRange(hsv, lower_red, upper_red)

    lower_red=np.array([170,120,70])
    upper_red=np.array([180,255,255])
    #2nd mask
    mask_2=cv2.inRange(hsv, lower_red, upper_red)
    #combining both the masks
    mask_1=mask_1+mask_2

    #dilating the image
    #morphologyEx(src(image), dst(how the output shoud be), op(integer which says what kind of msrphology you want in this case is dilating), kernel(pixels))
    mask_1=cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask_1=cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    #we are saving image which is not hidden in mask_2
    #bitwise checks each pixels in the image. 
    mask_2=cv2.bitwise_not(mask_1)
    #part of the image which are not red color is saved
    res_1=cv2.bitwise_and(img,img,mask=mask_2)
    #part of the image which arre red color is saved
    res_2=cv2.bitwise_and(bg,bg,mask=mask_1)
    
    final_output=cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)
    #displaying the output to the user
    cv2.imshow("magic", final_output)
    #loading
    cv2.waitKey(1)

cap.release()
#out.release()
cv2.destroyAllWindows()