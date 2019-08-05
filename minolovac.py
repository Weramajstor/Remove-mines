from tkinter import *
from random import*
from tkinter import messagebox
import time

bio = [[0] * 20 for i in range(20)]

xD=[1,1,1,0,-1,-1,-1,0]
yD=[-1,0,1,1,1,0,-1,-1]
        
def klikdesni(event):
    global brojMina
    pritisnutiGumb = event.widget
    for i in range(9):
        kraj = False
        for j in range(9):
            if pritisnutiGumb == polje[i][j]:
                kraj = True
                break
        if kraj:
            break
    if zastave[i][j] == 0:
        if brojMina > 0:
            brojMina -= 1
            tekst.config(text='Broj mina: '+str(brojMina))
            polje[i][j].config(image=zastava)
            zastave[i][j] = 1
            bio[i][j]=1
    else:
        brojMina += 1
        tekst.config(text='Broj mina: '+str(brojMina))
        polje[i][j].config(image=prazno)
        zastave[i][j] = 0
        bio[i][j]=0
    return

def check( r , s ):
    if r>=0 and r<9 and s>=0 and s<9:
        return True
    return False

def bfs( ky , kx ):
    global brojPolja
    qy = []
    qx = []
    qy+= {ky}
    qx += {kx}
    bio[ky][kx]=1
    sz=1

    while sz:
        d=0
        py=[]
        px=[]
        while d<sz:

            Y=qy[d]
            X=qx[d]
            broj = Label(prozor, image=slike[Y][X],width=15,height=15 ,bg='light blue')
            broj.grid(row = Y+1,column=X)
            brojPolja -= 1
            polje[Y][X].destroy()
            
            for g in range(8):
                if bombe[Y][X] != 0:
                    break
                iy=Y+yD[g]
                ix=X+xD[g]
                if check( iy , ix ) ==False:
                    continue
                if bio[iy][ix] or bombe[iy][ix]=='B' :
                    continue
                
                bio[iy][ix]=1
                py+={iy}
                px+={ix}
            d+=1
        qy , qx = py , px
        sz=len(qy)
    return True
    

def kliklijevi(event):
    pritisnutiGumb = event.widget
    global brojPolja
    for i in range(9):
        kraj = False
        for j in range(9):
            if pritisnutiGumb == polje[i][j]:
                kraj = True
                break
        if kraj:
            break
    if zastave[i][j] == 0 and bombe[i][j] == 'B':
        for x in range(9):
            for z in range(9):
                if bombe[x][z] == 'B':
                    broj = Label(prozor, image=slike[x][z],width=15,height=15,bg='white')
                    broj.grid(row = x+1,column=z)
        messagebox.showerror('Bomba','Žao nam je ali pogodili ste bombu!')
    elif zastave[i][j] == 0:
        bfs(i,j)
        if brojPolja < 1:
            messagebox.showinfo('Čestitamo!','Čestitamo! Pobijedili ste!')
    return

prozor = Tk()
prozor.title('Minolovac')
prozor.geometry('190x210+300+200')
prozor.resizable(False,False)
prazno = PhotoImage()
zastava = PhotoImage(file='zastava2.png')
zastave = []
bombe = []
slike = []
brojMina = 10
brojPolja = 71
Tekst = 'Broj mina: '+str(brojMina)
tekst = Label(prozor, text = Tekst)
tekst.grid(row = 0, column = 0,columnspan = 9)

prsten = [[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]

polje = []
for i in range(9):
    polje += [[]]
    zastave += [[]]
    bombe += [[]]
    slike += [[]]
    for j in range(9):
        polje[i] += [Button(prozor, image = prazno,width = 15,height = 15)]
        polje[i][j].grid(row = i+1,column= j)
        polje[i][j].bind('<Button-3>',klikdesni)
        polje[i][j].bind('<Button-1>',kliklijevi)
        zastave[i] += [0]
        bombe[i] += [0]
        slike[i] += [0]

n = 10
while n>0:
    red = randint(0,8)
    stupac = randint(0,8)
    if bombe[red][stupac] == 0:
        bombe[red][stupac] = 'B'
        n -= 1

for i in range(9):
    for j in range(9):
        if bombe[i][j] != 'B':
            for z in range(8):
                try:
                    if bombe[i+prsten[z][0]][j+prsten[z][1]] == 'B' and i+prsten[z][0]>=0 and j+prsten[z][1]>=0:
                        bombe[i][j] += 1
                except IndexError:
                    pass
            slike[i][j] = PhotoImage(file = str(bombe[i][j])+'.png')
        else:
            slike[i][j] = PhotoImage(file = 'bomba.png')

prozor.mainloop()
