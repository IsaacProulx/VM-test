import re
import math
import tkinter as tk
import tkinter.filedialog

root = tk.Tk()
frame = tk.Frame(root)
frame.grid(row="0",column="0",sticky="w")
text = tk.Text(root, width=50, bg="#243957", fg="white", insertbackground="white")
text.grid(row="1",column="0")
display = tk.Canvas(root, bg="white", height=385, width=385)
display.grid(row="1",column="1")
y1=2
y2=14
x1=2
x2=14
#display.create_rectangle(0,0,10,10, fill="black")
#display.create_rectangle(10,0,20,10, fill="black")
#display.create_rectangle(10,0,20,10, fill="black")
    

print("-----------------------------------------")
print("Enter Instructions")
print("Enter \"help\" For a List of Instructions")
print("Enter \"run\" to Execute")
def process(command, debug):
    print("-----------------------------------------")
    reg = []
    labels = {}
    for i in range(16):
        reg.append(0)
    mem = []
    for i in range(4096):
        mem.append(0)
    acc = None
    pc = 0
    pcOld = 0
    while(pc < len(command)):
        line = command[pc]
        line = line.replace(" ","")
        line = line.replace("\n","")
        if(not line):
            del command[pc]
            pc-=1
        if(len(line)>1):
            if(line[-1]==":"):
                #print(line)
                labels[line[0:-1]] = pc
            elif(line[0]==":"):
                #print(line)   
                pass
        pc+=1
    
    pc=0
    #print(labels)
    while(pc < len(command)):
        line = command[pc]
        print(line)
        line = line.replace(" ","")
        #line = line.replace("ari","1")
        #line = line.replace("movi","2")
        #line = line.replace("prt","3")
        #line = line.replace("cmpv","2")
        #line = line.replace("cmpr","2")
        #line = line.replace("jmp",":")
        #line = line.replace("r","")      
        op = line[0:4]     
        def err(error):
            """Print error message (dependent on var error)"""
            if(error==0):
                print("ERROR: Unsupported OPCode \"{}\"".format(line))
            elif(error==1):
                print("ERROR: Unsupported Operator")            
            elif(error==2):
                print("ERROR: Invalid Label Name")
            elif(error==3):
                print("ERROR: Label Not Defined")                
            return None
        
        def boot():
            for i in range(32):
                l=i
                pixels = "0"*32
                pixels = [char for char in pixels]
                pixelSize = 384/32
                x1 = 2
                x2 = pixelSize + 2
                y2 = pixelSize*l + pixelSize+2
                y1 = y2 - pixelSize
                for pixel in pixels:
                    #text.insert(tk.INSERT,pixel)
                    if(pixel=='1'):
                        #print('1')
                        display.create_rectangle(x1,y1,x2,y2, fill="black")
                        #text.insert(tk.INSERT,"\n({},{}),({},{})".format(x1,y1,x2,y2))
                    else:
                        display.create_rectangle(x1,y1,x2,y2, fill="#74d481")
                        #text.insert(tk.INSERT,"\n({},{}),({},{})".format(x1,y1,x2,y2))
                    x1+=pixelSize
                    x2+=pixelSize            
        
        def arith(com,debug):
            op = int(com[0],16)
            r = int(com[1],16)
            value = int(com[3:11],16)
            if(debug):
                print("operation: "+com[0])
                print("register: "+com[1])
                print("value: "+com[3:11])
            if(op==0):
                #addition
                reg[r] += value
            elif(op==1):
                #subtraction
                reg[r] -= value
            elif(op==2):
                #multiplication
                reg[r] *= value
            elif(op==3):
                #division
                reg[r] /= value
            elif(op==4):
                #exponent
                reg[r] **= value
                #print(reg[r])
            elif(op==5):
                #logarithm
                reg[r] = math.log(reg[r],value)
                #print(reg[r])
            else:
                err(1)
            return None
        
        def movi(com, debug):
            #print(com)
            r = int(com[0],16)  
            value = int(com[3:11],16)
            reg[r] = value
            return None
        
        def prt(com, debug):
            #print(com)
            d = reg[int(com[0],16)] #pixels to display
            l = reg[int(com[1],16)] #line to display on (0-15)
            pixels = bin(d).replace("0b","")
            while(len(pixels)<32):
                pixels = "0"+pixels
            pixels = [char for char in pixels]
            pixelSize = 384/32 #pxiel size = screen width/pixels per line
            if(len(pixels)==32):
                #text.insert(tk.INSERT,"\n")
                x1 = 2
                x2 = pixelSize + 2
                y2 = pixelSize*l + pixelSize+2
                y1 = y2 - pixelSize
                for pixel in pixels:
                    #text.insert(tk.INSERT,pixel)
                    if(pixel=='1'):
                        display.create_rectangle(x1,y1,x2,y2, fill="black")
                        #text.insert(tk.INSERT,"\n({},{}),({},{})".format(x1,y1,x2,y2))
                    else:
                        display.create_rectangle(x1,y1,x2,y2, fill="#74d481")
                        #text.insert(tk.INSERT,"\n({},{}),({},{})".format(x1,y1,x2,y2))
                    x1+=pixelSize
                    x2+=pixelSize
                #text.insert(tk.INSERT,reg[r])
                #print(reg[r])
            return None
        
        def cmpv(com, debug):
            op = int(com[0],16)
            r = int(com[1],16)
            value = int(com[3:11],16)
            if(op==0):
                #eq
                if(reg[r] == value):
                    return 1
                return 0
            elif(op==1):
                #neq
                if(reg[r] != value):
                    return 1
                return 0
            elif(op==2):
                #le
                if(reg[r] <= value):
                    return 1
                return 0
            elif(op==3):
                #ge
                if(reg[r] >= value):
                    return 1
                return 0
            else:
                err(1)         
            return None
        
        def cmpr(com, debug):
            op = int(com[0],16)
            r1 = int(com[1],16)
            r2 = int(com[2],16)
            if(op==0):
                #eq
                if(reg[r1] == reg[r2]):
                    return 1
                return 0
            elif(op==1):
                #neq
                if(reg[r1] != reg[r2]):
                    return 1
                return 0
            elif(op==2):
                #le
                if(reg[r1] <= reg[r2]):
                    return 1
                return 0
            elif(op==3):
                #ge
                if(reg[r1] >= reg[r2]):
                    return 1
                return 0
            else:
                err(1) 
            return None
        
        if(op=="0000"):
            print("NOP")
        elif(re.search("^1.*.*0$", op)):  
            arith(line[1:],debug)
        elif(re.search("^2.*.*.*$", op)):
            movi(line[1:],debug)
        elif(re.search("^3.*.*0$", op)):
            prt(line[1:],debug)
        elif(re.search("^4.*.*0$", op)):
            pc += cmpv(line[1:],debug)         
        elif(re.search("^5.*.*.*$", op)):
            pc += cmpr(line[1:],debug)
        elif(re.search("^6.*00$", op)):
            pc += reg[int(line[1],16)]            
        elif(re.search("^FFFF$", op)):
            boot()
        elif(re.search("^<-$", op)):
            pc = pcOld      
        elif(line[-1]==":"):
            if(len(line.replace(":","")) == 0):
                err(2)
            else:
                pass
                #labels[line[0:-1]] = pc
        elif(line[0]==":"):
            if(line[1:] in labels):
                pcOld = pc
                pc = labels[line[1:]]
            else:
                err(3)
        else:
            err(0)   
            
        pc+=1
    #main()
    return None

def main():
    command = []
    debug = False
    print("-----------------------------------------")
    while(True):
        line = input(">>>")
        if(re.search("^(run)",line.lower())):
            if(not line[4:]):
                process(command, debug)
            else:
                print("Executing {}...".format(line[4:]))
                file = open("./vm scripts/"+line[4:], 'r')
                for l in file.readlines():
                    command.append(l[0:-1])
                file.close()
                process(command, debug)
            break
        elif(line.lower() == "help"):
            print("----------")
            print("gui")
            print("view")
            print("debug")
            print("stop")
            print("run")
            print("help")
            print("help op")
            print("save")
            print("----------")
        elif(line.lower() == "help"):
            print("place holder")
        elif(line.lower() == "debug"):
            if(debug):
                debug=False
                print("Debug Disabled")
            else:
                debug=True
                print("Debug Enabled")
        elif(line.lower() == "stop"):
            break
        elif(re.search("^(view)",line.lower())):
            if(not line[5:]):
                for i in command:
                    print(i)
            else:
                print("Reading {}...".format(line[5:]))
                print("--------------")
                file = open("./vm scripts/"+line[5:], 'r')
                lines = file.readlines()
                for l in lines:
                    print(l[0:-1]) 
                file.close()
                print("--------------")
        elif(line.lower() == "save"):
            file = open("./vm scripts/"+input("Enter a Name:\n"), 'w')
            commandLines = []
            for com in command:
                commandLines.append(com+"\n")
            file.writelines(commandLines)
            file.close()
        elif(line.lower() == "gui"):
            root.mainloop()
        elif(line):
            command.append(line)
    return None

def start():
    #text.delete(1.0, tk.END)
    main()
    
def save():
    lines = []
    for line in text.get('1.0', 'end').split("\n"):
        lines.append(line+"\n")    
    file = tkinter.filedialog.asksaveasfile()
    file.writelines(lines)
    file.close()    

def openFile():
    text.delete(1.0, tk.END)
    file = tkinter.filedialog.askopenfile()
    lines = file.readlines()
    for l in lines:
        text.insert(tk.INSERT,l[0:-1]+"\n")
    file.close()

def run():
    process(["FFFF"],False)    
    process(text.get('1.0', 'end').split("\n"), False)


fileMenu = tk.Menubutton(frame, text="File", relief="raised")
fileMenu.menu =  tk.Menu(fileMenu, tearoff = 0 )
fileMenu["menu"] = fileMenu.menu
fileMenu.menu.add_command(label="Save", command=save)
fileMenu.menu.add_command(label="Open", command=openFile )

runButton = tk.Button(frame, text="Run", command=run)
helpButton = tk.Button(frame, text="Help")
debugButton = tk.Button(frame, text="Debug")
fileMenu.grid(row=0,column=0)
runButton.grid(row=0,column=1)
helpButton.grid(row=0,column=2)
debugButton.grid(row=0,column=3)
process(["FFFF"],False)
root.mainloop()