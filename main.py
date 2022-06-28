import tkinter as tk
from ui_elements import UIElements

app = tk.Tk()
app.geometry('400x400')
app.title('Auto cenas no ss.lv')


def start_app():
    # TODO save generated prices to file
    UIElements().generate_ui()
    
    # Run app
    app.mainloop() 
    
if __name__ == '__main__':
    start_app()