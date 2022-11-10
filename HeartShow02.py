from tkinter import *
import math
import random

class HeartShow:
    def __init__(self):
        self.author=chr(65)+chr(105)+chr(107)+chr(107)+chr(111)
        self.heartSize_max = 80 #大心的最大大小 （可调，不可太大）
        self.heartSize_rate = 0.5 #边距比例 （可调：0.1-1）
        self.heartSize_deviation = -(self.heartSize_max - self.heartSize_max * self.heartSize_rate) / 1.5    #大心的大小值y轴偏移（不要调）
        self.rate = 1.15    #大心的长宽比例(不要调)
        self.size = 600     #画布大小 （可调，长宽相等）
        self.deviation = self.size / 2 - 2 * self.heartSize_max #大心偏移量（不要调）
        self.payback = 2 * self.heartSize_max + self.deviation  #大心的回调量(不要调)
        self.core_Pos = (self.size / 2, self.size / 2 - self.heartSize_deviation*1.5) #准星基础位置（不要调）
        self.MouseFollow = True     #鼠标跟随开关（可调：True，False）
        self.littleHeart_createRate = 0.5 #小心心的生成概率,用于控制星星数量 （可调：0.1-1）
        self.littleHeart_max = 7 #小心心的最大大小 （可调，不可太大）
        self.littleHeart_min = 2 #小心心的最小大小 （可调，不可太大）
        self.speed = 0.05   #小心心的移动速度 （可调，0.01-1）
        self.heart_Pos=self.getHeartPos()   #获取心形分布坐标（不要调）
    
    def show(self):
        #生成窗体
        self.root=Tk()
        self.root.title('小心心 BY 凡凡')
        self.root.geometry(str(self.size)+'x'+str(self.size))
        self.root.resizable(0,0)
        self.Board=Canvas(self.root,width=self.size,height=self.size,bg='black')
        self.Board.pack(fill=BOTH,expand=0)
        self.Board.bind('<Motion>',self.moveCore)    #如果想改为鼠标左键拖动而不是自动跟随，将Motion改为B1-Motion
        self.root.after(1,self.heartJump)
        self.root.mainloop()
    
    def moveCore(self,event):
        #准星跟随鼠标
        if self.MouseFollow:
            self.core_Pos=(event.x,event.y-self.heartSize_deviation*1.5)
    
    def drawLittleHeart(self,_pos,_size,_color,_num):
        #绘制小心心
        self.Board.create_arc(_pos[0] , _pos[1] , _pos[0] + _size , _pos[1] + _size ,start=0,extent=180,fill=_color,outline=_color,tags='heart_'+str(_num))
        self.Board.create_arc(_pos[0] - _size , _pos[1], _pos[0] + _size - _size , _pos[1] + _size ,start=0,extent=180,fill=_color,outline=_color,tags='heart_'+str(_num))
        self.Board.create_arc(_pos[0] - _size, _pos[1] - 0.5 * _size, _pos[0] + _size , _pos[1] + 1.44 * _size ,start=-180,extent=180,fill=_color,outline=_color,tags='heart_'+str(_num))
        self.Board.create_polygon(_pos[0],_pos[1]+1.80*_size , _pos[0] - 0.86*_size,_pos[1] + 0.9*_size, _pos[0] + 0.86*_size,_pos[1] + 0.9*_size,fill=_color,outline=_color,tags='heart_'+str(_num))
        
    def getHeartSize(self,distanceRate,max=8,min=2):
        #获取小心心渐变尺寸
        rate=1/distanceRate
        if rate>max:
            rate=max
        elif rate<min:
            rate=min
        return rate
        
    def getHeartColor(self,distanceRate):
        #获取小心心渐变颜色
        #可对色域进行调整
        if distanceRate>1:
            distanceRate=1
        elif distanceRate<0:
            distanceRate=0
        _R=255-distanceRate*100
        _G=0+distanceRate*51
        _B=50+distanceRate*51
        _color='#'+str(hex(int(_R)))[2:].zfill(2)+str(hex(int(_G)))[2:].zfill(2)+str(hex(int(_B)))[2:].zfill(2)
        return _color

    def heartJump(self):
        #跳动起来
        for i in range(len(self.heart_Pos)):
            self.Board.delete('heart_'+str(i))
            curPos=((self.heart_Pos[i][0]-self.core_Pos[0])-(self.heart_Pos[i][2]-self.core_Pos[0])*self.heart_Pos[i][4]/2+self.core_Pos[0] , (self.heart_Pos[i][1]-self.core_Pos[1])-(self.heart_Pos[i][3]-self.core_Pos[1])*self.heart_Pos[i][4]/2+self.core_Pos[1])
            # self.Board.create_line(curPos[0],curPos[1],curPos[0]+1,curPos[1]+1,fill='red',tags='heart_'+str(i))   #调试点
            self.drawLittleHeart(curPos,self.getHeartSize(self.heart_Pos[i][4],self.littleHeart_max,self.littleHeart_min),self.getHeartColor(self.heart_Pos[i][4]),i)
            self.heart_Pos[i][4]-=self.speed
            if self.heart_Pos[i][4]<=0:
                self.heart_Pos[i][4]=1
        self.Board.update()
        self.root.after(1,self.heartJump)
        
    def getHeartPos(self):
        #心形分布坐标
        posList=[]
        for x in range(-2 * self.heartSize_max,2 * self.heartSize_max):
            if random.random()<self.littleHeart_createRate:
                p1_x=self.payback+x
                p1_y=self.payback+self.getPosByX_1(x,self.heartSize_max)*self.heartSize_max*self.rate
                p1_x_min=self.payback+x*self.heartSize_rate
                p1_y_min=self.payback+self.getPosByX_1(x,self.heartSize_max)*self.heartSize_max*self.rate*self.heartSize_rate-self.heartSize_deviation
                
                p2_x=self.payback+x
                p2_y=self.payback+self.getPosByX_2(x,self.heartSize_max)*self.heartSize_max*self.rate
                
                p2_x_min=self.payback+x*self.heartSize_rate
                p2_y_min=self.payback+self.getPosByX_2(x,self.heartSize_max)*self.heartSize_max*self.rate*self.heartSize_rate-self.heartSize_deviation

                posList.append([p1_x,p1_y,p1_x_min,p1_y_min,random.random()])    #pos_x_max,pos_y_max,pos_x_min,pos_y_min,distanceRate
                posList.append([p2_x,p2_y,p2_x_min,p2_y_min,random.random()])
        random.shuffle(posList)
        return posList

    def getPosByX_1(self,x,heartSize):
        #心形生成函数part1
        x=x / heartSize
        y = - math.sqrt(1-(abs(x)-1)**2)
        return y
    def getPosByX_2(self,x,heartSize):
        #心形生成函数part2
        x=x / heartSize
        y= 2 * math.sqrt(1 - 0.5 * abs(x) )
        return y
        
if __name__=='__main__':
    heart=HeartShow()
    heart.show()