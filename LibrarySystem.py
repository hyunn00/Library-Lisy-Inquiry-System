import os
from tkinter import *
import csv

# 도서 목록을 조회하고자 하는 파일 선택
def fileClick() :
    global fname
    num = list(listbox.curselection())[0]
    fname = str(file[num])

    fopen(fname)
    
    listBox.delete(0, END)
    textBox.delete('1.0', 'end')
    
    canvasDraw()
    canvas.bind("<Configure>", config)

# 선택한 리스트의 파일을 오픈
def fopen(fname) :
    global booklist, header
    
    booklist = []
    for i in range(0, 10) :
        f = open('%s' % fname, 'r', encoding='cp949')
        data = csv.reader(f)
        header = next(data)

        line = []
        counter = 20

        for row in data :
            # 처음으로 시작하는 문자가 i에 해당하는 숫자이면 line list에 넣기
            if row[1].startswith(str(i)) :
                
                line.append(row) 
                # 파일을 읽는 과정에서 속도를 높이기 위해 도서 목록 갯수 자정
                counter -= 1
                if counter == 0 :
                    break
        
        booklist.append(line)

# 화면 조정에 따른 config
def config(event) :
    canvas.delete("all")
    canvasDraw()

# canvas에 도형 그림
def canvasDraw() :
    global fname

    canvas.delete("all")

    cWidth = canvas.winfo_width()
    cHeight = canvas.winfo_height()

    x = int(cWidth / 10)
    y = int(cHeight / 9)
    num = 0
    canvas.create_text(cWidth/2, y/2, text = "%s 파일" % fname, font = ("맑은 고딕", 10))
    for i in range(0, 9) :
        for j in range(0, 10) :
            if j % 3 == 1 and i % 2 != 0 :
                x1, y1 = j * x, i * y
                x2, y2 = (j + 2) * x, (i + 1) * y

                canvas.create_rectangle(x1, y1, x2, y2, width = 0, fill = colors[num])
                canvas.create_text((x1+x2)/2, (y1+y2)/2, text = texts[num], font = ("맑은 고딕", 10))
                num += 1
            
            if num == 10 :
                break

# 도형 선택에 따른 list 출력
def rectClick(event) :
    global listnum

    cWidth = canvas.winfo_width()
    cHeight = canvas.winfo_height()

    x = int(cWidth / 10)
    y = int(cHeight / 9)

    mouseCanvasX, mouseCanvasY = canvas.canvasx(event.x), canvas.canvasy(event.y)
    listnum = 3 * (int(mouseCanvasY / (2 * y)) if mouseCanvasY % (2 * y) > y else -10) + (int(mouseCanvasX / (3 * x)) if mouseCanvasX % (3 * x) > x else -10)
    
    if listnum >= 0 and listnum < 10 :
        listInsert(listnum)
        textBox.delete('1.0', 'end')
        label_list.config(text = "%s 도서 목록" % texts[listnum][4:])

# 도서 목록 리스트 출력
def listInsert(num) :
    listBox.delete(0, END)

    global booklist

    order = 0
    for book in booklist[num] :
        listBox.insert(order, book[2].strip('/'))
        order += 1

# 선택 도서 정보 출력
def textInsert(num) :
    global listnum

    textBox.delete('1.0', 'end')

    data, Tdata = [], []

    data = booklist[listnum]
    Tdata = data[num]

    for i in range(0, len(header)) :
        textBox.insert(END, header[i] + " : " + Tdata[i].strip('/') + '\n')
    textBox.configure(font = ("Malgun Gothic", 9))

def btnClick() :
    num = list(listBox.curselection())[0]
    
    textInsert(num)

# 전역 변수
file = [f for f in os.listdir() if '.csv' in f]
booklist, header = [], []
colors = ["limegreen", "red", "lightgrey", "orange", "peru", "lightskyblue", "gold", "palegreen", "dodgerblue", "mediumorchid"]
texts = ["000 총류", "100 철학", "200 종교", "300 사회과학", "400 순수과학", "500 기술과학", "600 예술", "700 언어", "800 문학", "900 역사"]
listnum = 0
fname = ''

# Tkinter
root = Tk()
root.geometry("800x600")

# frame_top
frame_top = Frame(root)
frame_top.pack(side = 'top', fill = 'both', expand = True)

# frame_file
frame_file = Frame(frame_top)
frame_file.pack(side = 'left', fill = 'both', expand = True)

label_file = Label(frame_file, text = "CSV 파일 선택")
label_file.pack(side = "top", fill = 'x')

listbox = Listbox(frame_file, selectmode='single', height = 5, width = int(root.winfo_width() / 2))
for f in file :
    listbox.insert(END, f)
listbox.pack(fill = 'both', expand = True)

btn_file = Button(frame_file, text = '선택', command = fileClick)
btn_file.pack(side = 'bottom', fill = 'x')

#frame_cav
frame_cav = Frame(frame_top)
frame_cav.pack(side = 'right', fill = 'both', expand = True)

label_cav = Label(frame_cav, text = '도서 분류 코드 선택')
label_cav.pack(side = "top", fill = 'x')

canvas = Canvas(frame_cav, bg = 'white')
canvas.pack(side = 'left', fill = 'both', expand = True)

canvas.bind("<Button-1>", rectClick)

# frame_bottom
frame_bottom = Frame(root)
frame_bottom.pack(side = 'top', fill = 'both', expand = True)

# frame_list
frame_list = Frame(frame_bottom)
frame_list.pack(side = "left", fill = 'both', expand = True, ipady = 10)

label_list = Label(frame_list, text = "도서 목록")
label_list.pack(side = "top", fill = "x")

btn_choice = Button(frame_list, text = "선택", command = btnClick)
btn_choice.pack(side = "bottom", fill = "x")

scroll_list = Scrollbar(frame_list)
scroll_list.pack(side = "right", fill = "y", pady = 10)

listBox = Listbox(frame_list, selectmode = "single", height = 5, yscrollcommand = scroll_list.set)
listBox.pack(side = 'left', fill = 'both', expand = True)

scroll_list.config(command = listBox.yview)

# frame_text
frame_text = Frame(frame_bottom)
frame_text.pack(side = "right", fill = "both", expand = True, ipadx = 10)

label_text = Label(frame_text, text = "해당 도서 상세 정보")
label_text.pack(side = "top", fill = "x")

scroll_text = Scrollbar(frame_text)
scroll_text.pack(side = "right", fill = "y", pady = 10)

textBox = Text(frame_text, height = 5, width = 15, yscrollcommand = scroll_text.set)
textBox.pack(side = "left", fill = "both", expand = True)

scroll_text.config(command = textBox.yview)

root.mainloop()