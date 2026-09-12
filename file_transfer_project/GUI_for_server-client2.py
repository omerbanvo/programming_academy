from tkinter import *
import os
import socket
from client import upload_file
from client import download_file

#class for the gui 
class FileTransferGUI:
    def __init__(self, client_folder, server_folder):
        self.client_folder = client_folder
        self.server_folder = server_folder
        adress = ('127.0.0.1', 2345)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(adress)

        # create a window root
        self.root = Tk()
        self.root.geometry("800x300")

        # Make both columns expand equally
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Only the listbox row (row 1) should stretch — the label row (row 0) stays fixed
        self.root.grid_rowconfigure(1, weight=1)

        # Colors and font
        self.BG_COLOR = "#fafafa"
        self.TEXT_COLOR = "#222222"
        self.SELECT_COLOR = "#cfe8ff"
        self.FONT = ("Helvetica", 15)

        self.listbox_client = Listbox(self.root,
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            font=self.FONT,
            activestyle='dotbox',
            selectbackground=self.SELECT_COLOR,
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#dddddd"
        )
        self.add_all_files_to_listbox(self.listbox_client, self.client_folder)

        self.listbox_server = Listbox(self.root,
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            font=self.FONT,
            activestyle='dotbox',
            selectbackground=self.SELECT_COLOR,
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#dddddd"
        )
        self.add_all_files_to_listbox(self.listbox_server, self.server_folder)

        self.listbox_client.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.listbox_server.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        Label(self.root, text="My Files", font=("Helvetica", 13, "bold"), bg="white", fg=self.TEXT_COLOR).grid(row=0, column=0, sticky="w", padx=5)
        Label(self.root, text="Server Files", font=("Helvetica", 13, "bold"), bg="white", fg=self.TEXT_COLOR).grid(row=0, column=1, sticky="w", padx=5)

        # adding the buttons
        self.upload_button = Button(self.root, text="upload file", state="disabled", command=self.upload)
        self.download_button = Button(self.root, text="download file", state="disabled", command=self.download)

        # placing the buttons
        self.upload_button.grid(row=2, column=0)
        self.download_button.grid(row=2, column=1)

        # store the currently selected file/index from each listbox
        self.selected_client_file = None
        self.selected_server_file = None

        # bind selection events
        self.listbox_client.bind("<<ListboxSelect>>", self.on_client_select)
        self.listbox_server.bind("<<ListboxSelect>>", self.on_server_select)

        self.root.mainloop()

    # function that adds to the listbox all the files from a folder
    def add_all_files_to_listbox(self, listbox, folderpath):
        i = 1
        for file in os.listdir(folderpath):
            full_path = os.path.join(folderpath, file)
            if os.path.isdir(full_path):
                self.add_all_files_to_listbox(listbox, full_path)
            else:
                if not file[0] == '.':
                    listbox.insert(i, file)
                    i += 1

    # function that gives the selected file
    def get_selected_file(self, listbox):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            file_name = listbox.get(index)
            return (file_name, index)
        return None

    def on_client_select(self, event):
        result = self.get_selected_file(self.listbox_client)
        if result:
            self.selected_client_file = result
            self.upload_button.config(state="normal")

    def on_server_select(self, event):
        result = self.get_selected_file(self.listbox_server)
        if result:
            self.selected_server_file = result
            self.download_button.config(state="normal")

    #upload button
    def upload(self):
        flag = "upload".encode('utf-8')
        self.client_socket.sendall(flag)
        file_name = self.selected_client_file[0]
  
        full_path = os.path.join(self.client_folder, file_name)
        upload_file(self.client_socket, full_path)
        self.client_socket.close()

        

    #download button
    def download(self):
        
        flag = "download".encode('utf-8')
        self.client_socket.send(flag)
        file_name = self.selected_server_file[0]
        self.client_socket.send(file_name.encode('utf-8'))
        download_file(self.client_socket, server_folder, file_name)
        self.client_socket.close()


client_folder = '/Users/omerbanvolgyi/Documents/Temp'
server_folder = '/Users/omerbanvolgyi/Documents/programming_academy/UPLOAD_FILES_TO_SERVER'
app = FileTransferGUI(client_folder, server_folder)