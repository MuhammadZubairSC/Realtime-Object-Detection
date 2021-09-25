import cv2
import pandas
from datetime import datetime as dt

firstFrame=None

video=cv2.VideoCapture(0)
statusList=[None, None]
timeD=[]
dataF=pandas.DataFrame(columns=["Start", "Stop"])
while True:

    check, frame=video.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (21,21), 0)

    if firstFrame is None:
        firstFrame=gray
        continue

    deltaFrame=cv2.absdiff(firstFrame, gray)

    thresholdFrame=cv2.threshold(deltaFrame, 35,255, cv2.THRESH_BINARY) [1]
    thresholdFrame=cv2.dilate(thresholdFrame, None, iterations=2)
    (cnts,_)=cv2.findContours(thresholdFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    statusFlag=0
    for contour in cnts:
        if cv2.contourArea(contour)<15000:
            continue
        statusFlag=1
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (w+x, y+h), (0,255,0), 3)
    
    statusList=statusList[-2:] 
    if statusList[-1]==1 and statusList[-2]==0:
        timeD.append(dt.now())
    if statusList[-1]==0 and statusList[-2]==1:
        timeD.append(dt.now())

    statusList.append(statusFlag)

    cv2.imshow("Color Frame", frame)


    key=cv2.waitKey(1)
    if key==ord('q'):
        if statusFlag==1:
            timeD.append(dt.now())
        break

for i in range(0, len(timeD), 2):
    dataF=dataF.append({"Start":timeD[i],"Stop":timeD[i+1]}, ignore_index=True)
dataF.to_csv("MotionDetect.csv")

video.release()

cv2.destroyAllWindows()
