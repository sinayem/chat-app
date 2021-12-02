import socket
from sys import flags
import threading
import tkinter as tk
from tkinter import Widget, scrolledtext
from tkinter import font
from tkinter.constants import LEFT
from PIL import Image,ImageTk
from tkinter import messagebox
HOST = "127.0.0.1"
PORT = 1234

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END,message+"\n")
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST,PORT))
        print("successfully connect to the server")
        add_message("[SERVER] Successfully Connected to the Server")
    except:
        messagebox.showerror("Unable to connect to the server", f"unable to connect to server host {HOST} and port {PORT}")
    
    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username","Username can't be empty")
    threading.Thread(target=listen_for_message_from_server,args=(client,)).start()
    #send_message_to_server(client)

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def send_message():
    message = message_textbox.get()
    if message != "":
        client.sendall(message.encode())
        message_textbox.delete(0,len(message))
    else:
        messagebox.showerror("Empty message","Message can't be empty")


root = tk.Tk()
root.geometry("600x600")
root.title("Chat Application")
root.resizable(False,False)

root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=4)
root.grid_rowconfigure(2,weight=2)

top_frame = tk.Frame(root,width=600,height=100,bg="#00cdac")
top_frame.grid(row=0,column=0,sticky=tk.NSEW)

middle_frame = tk.Frame(root,width=600,height=400,bg="#ffdde1")
middle_frame.grid(row=1,column=0,sticky=tk.NSEW)

bottom_frame = tk.Frame(root,width=600,height=100,bg="#19547b")
bottom_frame.grid(row=2,column=0,sticky=tk.NSEW)

username_label = tk.Label(top_frame,text="Enter Username: ",font=("Arial", "24", "bold italic"),bg="#00cdac",fg="white")
username_label.pack(side=tk.LEFT)
username_textbox = tk.Entry(top_frame,font=("Helvetica", "17"),bg="#004e92",fg="white")
username_textbox.pack(side=tk.LEFT)
username_button = tk.Button(top_frame,text="Join",font=("Times", "15", "bold italic"),bg="#a8e063",fg="black",command=connect)
username_button.pack(side=tk.LEFT,padx=7)


message_textbox = tk.Entry(bottom_frame,font=("Helvetica", "17"),bg="#c4e0e5",fg="black",width=35)
message_textbox.pack(side=tk.LEFT,padx=7)
img = Image.open("C:/Users/nayem/Desktop/django-projects/python projects/chatapp/1.gif") 
res_img = img.resize((100,75), Image.ANTIALIAS)
new_img= ImageTk.PhotoImage(res_img)
message_button = tk.Button(bottom_frame,image = new_img ,text="send",width=40,height=30,command=send_message)
message_button.pack(side=tk.RIGHT,padx=12) 


message_box = scrolledtext.ScrolledText(middle_frame,font=("Helvetica", "12"),bg="#ffdde1",fg="black", width=62,height=27)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)



def listen_for_message_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != "":
            username = message.split("~")[0]
            content =  message.split("~")[1]
            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error","Message received from client is empty")

    

def main():
    root.mainloop()



if __name__ == '__main__':
    main()