import numpy
import os,sys
from PIL import Image,ImageFont,ImageDraw
import cv2
import os,time,pygame;
from moviepy.editor import*
from ctypes import *
import _thread
from threading import Thread
from multiprocessing import cpu_count,Process
class config:
    txtheight=120
    videRate=16/9;
    videoPath=''
    cutframePath=''
    fontwidth=2
    fontheight=4
    fontPath="c:/windows/fonts/consola.ttf"
    txtwidth=180*16/9*2
    fps=8;
    frameNumber=0
    interval=3



def toImgStr(imgPath,savePath,outputHeight):
    img=Image.open(imgPath)
    imgWidth,imgHeight=img.size
    config.videorate=imgWidth /imgHeight
    outputWidth = 2*outputHeight * imgWidth // imgHeight
    img=img.resize((outputWidth,outputHeight),Image.ANTIALIAS)
    imgMatrix=numpy.array(img.convert('L'))
    chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    N = len(chars)
    strImg=''
    for i in range(outputHeight):
        for j in range (outputWidth):
            strImg+=chars[int(imgMatrix[i][j]/256*N)]
        strImg+='\n'
    with open(savePath, mode='w') as f:
        f.write(strImg)


def cutFrame(path,savePath):
    video=cv2.VideoCapture(path)
    video_clip=VideoFileClip(path)
    audio=video_clip.audio
    audio.write_audiofile("1.mp3")
    video_clip.reader.close()
    video_clip.audio.reader.close_proc()    
    nowFrame=0;
    if video.isOpened():
        retval,frame=video.read()
    else:
        
        return False
    FrameNumber=video.get(7)-1
    fileNumber=0
    for root,dirs,file in os.walk(savePath):
        for item in file:
            if item.endswith('jpg'):
                fileNumber+=1
    print(fileNumber)

    if(FrameNumber//config.interval+1==fileNumber):
        print('缓存已存在')
        config.frameNumber=fileNumber
        return fileNumber
    else:
        for item in os.listdir(savePath):
            os.remove(savePath+item)
    print("cutting Video frame please waiting")
    while retval:
        if nowFrame%config.interval==0:
            cv2.imwrite(savePath+"%d.jpg"%nowFrame,frame)
            #cv2.waitKey(1)
        retval,frame=video.read()
        nowFrame+=1
    config.frameNumber=nowFrame//config.interval+1
    print("finished,frameNumber: %d"% (config.frameNumber))
    
    return config.frameNumber;

def translate(height,inFolder,outFolder):
    if(config.frameNumber):
        if len(os.listdir(outFolder))==config.frameNumber:
            print("txt cache exist")
            return config.frameNumber;
        else:
            for item in os.listdir(outFolder):
                os.remove(outFolder+item)
        #for item in os.listdir(inFolder):
        #    imgPath=inFolder+item; 
        #    savePath=outFolder+"%s.txt"%item;
        #    toImgStr(imgPath,savePath,height)
        current=0;
        print(cpu_count())
        threads=cpu_count()
        step=config.frameNumber//threads+1
        for i in range(threads):
            t=Process(target=translateRange,args=(current,current+step,height,inFolder,outFolder,i))
            t.start()
            #th=_thread.start_new_thread ( translateRange, (current,current+step,height,inFolder,outFolder))
            #th.run()
            current=current+step
        while  config.frameNumber!=len(os.listdir(outFolder)):
            time.sleep(3)
    else:
         print('error')
         return False
def translateRange(start,end,height,inFolder,outFolder,processIndex):
    print("进程开启")
    fileList=os.listdir(inFolder)
    if(end>len(fileList)):
        end=len(fileList)
    if(start<0):
        start=0
    print(start,end)
    while (start<end):
        imgPath=inFolder+fileList[start]
        savePath=outFolder+"%s.txt"%fileList[start]
        toImgStr(imgPath,savePath,height)
        start+=1


def str_to_img(inPath,outPath,imgWidth,imgHeight):
    result=[]
    x,y=0,0
    with open(inPath,'r') as f:
        result=f.readLines()
    
    font=ImageFont.truetype(config.fontPath,3);
    img=Image.new('RGB',(imgWidth,imgHeight),(255,255,255))
    dr=ImageDraw.Draw(img)
  
    for line in result:
        for char in line:
            dr.text((x,y),char,font=font,fill=0)
            x+=2;
        x=0
        y+=4;
    img.save(outPath)
def imageToVideo(inputPath,outPath):
    #image=Image.open(inputPath)
    size=(1280,720)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video=cv2.VideoWriter(outPath+"11.mp4v",fourcc,config.fps,size)
    for i in range(710):
        path=inputPath+'%d'%(i*3)+".jpg.txt.jpg";
        print(path)
        img=cv2.imread(path)
        video.write(img)
    video.release()


def shellOutput(path):
        time.sleep(1)
        Path=os.getcwd()
        dllPath=Path+"\\dll1.dll"
        libe=CDLL(dllPath)
        pygame.mixer.init()
        src=pygame.display.set_mode([30,30])
        pygame.mixer.music.load(Path+"\\1.mp3")
        txtList={}
        print("loaging")
        for i in range (config.frameNumber):
            with open(path+"%d.jpg.txt"%(i*config.interval)) as f:
                result=f.read()
            txtList[i]=result
        pygame.mixer.music.play()
        for i in range(config.frameNumber):
            time1=time.time()
            libe.gotoXY(0,0)
            print(txtList[i])
            time2=time.time()
            time.sleep(1/config.fps-(time2-time1))

            #stdsrc=curses.initscr()
           
            #curses.setsyx(0,0)
            #curses.endwin()
            #os.system("cls")

           

      

def main():
    path=os.getcwd()
    imgSavePath=path+"\\img\\"
    txtSavePath=path+"\\txt\\"
    textImageSavePath=path+"\\strimg\\"
    path+="\\1.mp4"
    
    height=180;
    #try:
    #    _thread.start_new_thread(cutFrame,(path,imgSavePath))
    #    _thread.start_new_thread(cutFrame,(path,imgSavePath))
    #except:
    #    print("error")

    number=cutFrame(path,imgSavePath)
    translate(height,imgSavePath,txtSavePath)
    #_thread.start_new_thread(translate,(height,imgSavePath,txtSavePath))
    #_thread.start_new_thread(translate,(height,imgSavePath,txtSavePath))

    shellOutput(txtSavePath)
    #strList=os.listdir(txtSavePath)
    #width=int(config.txtheight*config.videRate*config.fontheight);
    #height=int(config.txtheight*config.fontheight)
    #for i in strList:
    #    str_to_img(txtSavePath+i,textImageSavePath+i+".jpg",width,height)
    #imageToVideo(textImageSavePath,imgSavePath)
   
if __name__=="__main__":
    main()