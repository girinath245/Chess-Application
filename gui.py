# This is the main Gui Program

import chess
import tkinter as tk
from PIL import Image, ImageTk
import time

button_list = []
chess_list = []

board = chess.Board()

x = True
#Even_clicks checker

def promotion_check(prev,k):
    if chess_list.index(prev,0,32) in range(8,24):
        if (board.turn==True and k in range(56,64)):
            return 1
        elif (board.turn==False and k in range(0,8)):
            return 2
    return False

def assign_new_piece(button,path):
    
    img=None
    img = Image.open(path)
    img = img.resize((45,45))
    ph = ImageTk.PhotoImage(img)
    button.config(image=ph)
    button.image = ph    

def reinstate_color(prev):
    if (prev//8 + prev %8)%2==0:
        button_list[prev].configure(bg = '#8af542')
    else:
        button_list[prev].configure(bg = 'white')


def sqr_notation(i):
    if i<=63:
        c = 'a'
        c = chr(ord(c) + i%8)
        c += str(i//8 +1)
        return c
    return None
    
def exchange_piece(button1,button2):
    if (button1["image"]!=''):
        button2["image"]=button1["image"]
        button1["image"]=''
        
def remove_piece(button1):
    button1["image"] = ''
    print("Removing")
        
def generate_uci(i,j):
   
    s1 = sqr_notation(i)
    s1+= sqr_notation(j)
    
    y = chess.Move.from_uci(s1)
    x = board.san(y)
    print(x)
    return s1

def move(k):
    
    global x
    global prev
    
    if x:
        if (k in chess_list):
            prev = k
            print(k)
            button_list[k].configure(bg = 'green')
            
            # for button in button_list:
            #     button_list[k].configure(activebackground = 'red')
            # try:
            #     index = chess_list.index(k, 0, len(chess_list)-1)
            #     button_list[k].configure(bg = 'green')
            # except ValueError:
            #     button_list[k].configure(activebackground = 'blue')
            #     x = not x
        else:
            x = not x


    else:
        print(k)
        # Handling the case when same square is clicked twice
        if k==prev and (k//8+k%8)%2==0:
            button_list[k].configure(bg = '#8af542')
        elif k==prev and (k//8+k%8)%2!=0:
            button_list[k].configure(bg = 'white')

        else:        
            # button_list[k].configure(bg = 'red')
            # time.sleep(0.075)
            # button_list[k].configure(bg = 'black')
            
            '''If the move is legal'''

            uci = generate_uci(prev,k)  
            yuci = chess.Move.from_uci(uci)
                        
            if promotion_check(prev,k)==1 or promotion_check(prev,k)==2:
                
                print("Inisde promotion check")
                
                valpcheck = promotion_check(prev,k)
                newp = input()
                if newp=='q' and valpcheck == 1:
                    assign_new_piece(button_list[prev],"alpha/wq.png")
                elif newp=='r' and valpcheck == 1:
                    assign_new_piece(button_list[prev],"alpha/wr.png")
                elif newp=='b' and valpcheck == 1:
                    assign_new_piece(button_list[prev],"alpha/wb.png")
                elif newp=='n' and valpcheck == 1:
                    assign_new_piece(button_list[prev],"alpha/wn.png")
                elif newp=='q' and valpcheck == 2:
                    assign_new_piece(button_list[prev],"alpha/wq.png")
                elif newp=='r' and valpcheck == 2:
                    assign_new_piece(button_list[prev],"alpha/wr.png")
                elif newp=='b' and valpcheck == 2:
                    assign_new_piece(button_list[prev],"alpha/wb.png")
                elif newp=='n' and valpcheck == 2:
                    assign_new_piece(button_list[prev],"alpha/wn.png")
                
                exchange_piece(button_list[prev],button_list[k])
                newp ='q'
                uci += newp
                
                board.push_san(uci)
                print(board)           
            
            elif yuci in board.legal_moves:
                    
                # First piece move
                
                print("Verifying move:")
                
                '''Standard algebraic notation san'''
                
                alpha = board.san(yuci)

                if (board.is_castling(yuci)):
                    # Works fine
                    # 4 cases white-black and short castle-long castle
                    # True indicates white's turn'
                    
                    # These two checks work to include the case when the rook is clicked for castling
                    if 	 (k == 0 or k==56):
                        k+=2

                    elif (k == 7 or k == 63): 	
                        k-=1  

                    exchange_piece(button_list[prev],button_list[k])
                    print("Inside castling")
                    
                    if alpha=="O-O" and board.turn==True:
                        exchange_piece(button_list[7],button_list[5])
                    elif alpha=="O-O" and board.turn==False:
                        exchange_piece(button_list[63],button_list[61])
                    elif alpha=="O-O-O" and board.turn==True:
                        exchange_piece(button_list[0],button_list[3])
                    elif alpha=="O-O-O" and board.turn==False:
                        exchange_piece(button_list[56],button_list[59])  
    
                elif board.is_en_passant(yuci):
                    # Works fine
                    exchange_piece(button_list[prev],button_list[k])
                    print("Inside en passant")
                    mod = (k-prev)%8
                    if mod==7:
                        mod = -1
                    
                    delpawn = prev + mod
                    ind_del = chess_list.index(delpawn,0,32)
                    print("Deleting")
                    remove_piece(button_list[delpawn])
                
                elif board.is_capture(yuci):
                    # Write code
                    exchange_piece(button_list[prev],button_list[k])
                    print("Okok")
                
                else:
                    exchange_piece(button_list[prev],button_list[k])
                    print("Xyz")
    
                board.push_san(uci)
                print(board)
                
                try:
                    # Index of capturing piece
                    ind1 = chess_list.index(prev, 0, len(chess_list)-1)
                    
                except ValueError:
                    print("No piece in initial index in move function")
                
                # Index of captured piece
                ind2 = chess_list.index(k, 0, len(chess_list)-1) if k in chess_list else -1
                chess_list[ind1] = k
                if ind2!=-1:
                    chess_list[ind2] = -1  #Making the captured piece -1 in chesslist
                
            reinstate_color(prev)
    
            reinstate_color(k)
    
            prev = -1

    x = not x    
    
def initialize_board(button_list,window):

    highest = 450
    k=0
    for i in range(8):
        
        left_most = 280
        for j in range(8):
            
            k = 8*i +j
            if (i+j)%2 == 0:
                button_list.append(tk.Button(window,bg='#8af542',text=str(8*i+j),command = lambda k =k :move(k)))
            else:
                button_list.append(tk.Button(window,bg='white',text=str(8*i+j),command = lambda k =k :move(k)))

            button_list[k].place(height=50,width=50, x=left_most, y=highest)
            left_most+=50

        highest-=50

def initialize_chess(chess_list,button_list,window):
    for i in range(16):
        chess_list.append(i)
    for i in range(48,64):
        chess_list.append(i)
    
    file_path = {      "wr":"merida_chess_set/wr.svg",
                       "wn":"merida_chess_set/wn.svg",
                       "wb":"merida_chess_set/wb.svg",
                       "wq":"merida_chess_set/wq.svg",
                       "wk":"merida_chess_set/wk.svg",
                       "wp":"merida_chess_set/wp.svg",
                       "br":"merida_chess_set/br.svg",
                       "bn":"merida_chess_set/bn.svg",
                       "bb":"merida_chess_set/bb.svg",
                       "bq":"merida_chess_set/bq.svg",
                       "bk":"merida_chess_set/bk.svg",
                       "bp":"merida_chess_set/bp.svg"}
    
    png_path = {       "wr":"alpha/wr.png",
                       "wn":"alpha/wn.png",
                       "wb":"alpha/wb.png",
                       "wq":"alpha/wq.png",
                       "wk":"alpha/wk.png",
                       "wp":"alpha/wp.png",
                       "br":"alpha/br.png",
                       "bn":"alpha/bn.png",
                       "bb":"alpha/bb.png",
                       "bq":"alpha/bq.png",
                       "bk":"alpha/bk.png",
                       "bpawn":"alpha/bp1.jpg"}
    
    assign_new_piece(button_list[0],png_path["wr"])
    assign_new_piece(button_list[1],png_path["wn"])
    assign_new_piece(button_list[2],png_path["wb"])
    assign_new_piece(button_list[3],png_path["wq"])
    assign_new_piece(button_list[4],png_path["wk"])
    assign_new_piece(button_list[5],png_path["wb"])
    assign_new_piece(button_list[6],png_path["wn"])
    assign_new_piece(button_list[7],png_path["wr"])

    for i in range(8):
        assign_new_piece(button_list[8+i],png_path["wp"])
        assign_new_piece(button_list[48+i],png_path["bpawn"])

    assign_new_piece(button_list[56],png_path["br"])
    assign_new_piece(button_list[57],png_path["bn"])
    assign_new_piece(button_list[58],png_path["bb"])
    assign_new_piece(button_list[59],png_path["bq"])
    assign_new_piece(button_list[60],png_path["bk"])
    assign_new_piece(button_list[61],png_path["bb"])
    assign_new_piece(button_list[62],png_path["bn"])
    assign_new_piece(button_list[63],png_path["br"])
    
def main():
    window = tk.Tk()
    window.title('Chess')
    window.geometry("960x540")
    window.resizable(False,False)
    print(sqr_notation(83))
    initialize_board(button_list,window)
    initialize_chess(chess_list,button_list,window)
    
    #game (button_list)
    
    window.mainloop()
    
if __name__ == "__main__":
    main()