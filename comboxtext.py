# from tkinter import *
 
# def MouseDown(event): # 不要忘记写参数event
#     global mousX  # 全局变量，鼠标在窗体内的x坐标
#     global mousY  # 全局变量，鼠标在窗体内的y坐标
 
#     mousX=event.x  # 获取鼠标相对于窗体左上角的X坐标
#     mousY=event.y  # 获取鼠标相对于窗左上角体的Y坐标
    
# def MouseMove(event):
#     w=la1.winfo_x() # w为标签的左边距
#     h=la1.winfo_y() # h为标签的上边距
#     root.geometry(f'+{event.x_root - mousX-w}+{event.y_root - mousY-h}') # 窗体移动代码
#     # event.x_root 为窗体相对于屏幕左上角的X坐标
#     # event.y_root 为窗体相对于屏幕左上角的Y坐标
# def exit(event):
#     root.destroy()
 
# root=Tk() # 源码来自wb98.com
# root.geometry('300x150+888+444')
# root.overrideredirect(True)  # 无标题栏窗体
 
# la1=Label(root,text='按着我，可以移动窗体\n双击退出',height=3,bg='red',cursor='fleur')
# la1.pack(padx=10,pady=40)
 
# la1.bind("<Button-1>",MouseDown)  # 按下鼠标左键绑定MouseDown函数
# la1.bind("<B1-Motion>",MouseMove)  # 鼠标左键按住拖曳事件,3个函数都不要忘记函数写参数
# la1.bind("<Double-Button-1>",exit)  # 双击鼠标左键，关闭窗体
 
# root.mainloop()

print([1,2,3] == [1,3,2])