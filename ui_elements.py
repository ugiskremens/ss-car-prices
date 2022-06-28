import tkinter as tk
from tkinter import filedialog
from generate_prices import GeneratePrices

class UIElements():
    def_submit_text = 'Ģenerēt'
    
    def generate_ui(self):
        # Canvas which will contain elements
        canvas = tk.Canvas(highlightthickness=0)
        
        # App title
        title = tk.Label(canvas, text='Auto cenu Ģenerācija')
        title.configure(font=('', 20))
        title.grid(row=0, column=0, columnspan=6, pady=20)
        
        # Make input label
        make_label = tk.Label(canvas, text='Auto marka:')
        make_label.grid(row=2, column=0, columnspan=6)
        
        # Make input entry
        self.make_entry = tk.Entry(canvas)
        self.make_entry.grid(row=3, column=0, columnspan=6)
        
        # Model input label
        model_label = tk.Label(canvas, text='Auto modelis:')
        model_label.grid(row=4, column=0, pady=(10,0), columnspan=6)
        
        # Model input entry
        self.model_entry = tk.Entry(canvas)
        self.model_entry.grid(row=5, column=0, columnspan=6)
        
        # Submit btn
        self.submit_btn = tk.Button(canvas, text=self.def_submit_text, command=self.generate_prices)
        self.submit_btn.grid(row=6, column=0, pady=10, columnspan=6)
        
        # Status label
        self.status_label = tk.Label(canvas, text='')
        self.status_label.grid(row=7, column=0, columnspan=6)
        
        # File path label
        self.file_path_label = tk.Label(canvas, text='...')
        self.file_path_label.grid(row=8, column=0, pady=(30,0))
        
        # File path btn
        self.file_path_btn = tk.Button(canvas, text='Izvēlēties..', command=self.browsefunc)
        self.file_path_btn.grid(row=8, column=1, pady=(30,0))
        
        canvas.pack()
    
    # Opens filedialog for user to choose file folder
    def browsefunc(self):
        filename = filedialog.askdirectory()
        if len(filename) > 32: filename = '...' + filename[-32:]
        
        self.file_path_label.config(text=filename)
        
    # Starts price generation with UI changes
    def generate_prices(self):
        self.submit_btn.configure(text='Ģenerē cenas..')
        status_label = ''
        
        # Get and check car make
        make = self.make_entry.get()
        if make == '':
            status_label = 'Nav norādīta marka'
        
        # Get and check car model
        model = self.model_entry.get()
        if model == '':
            status_label = 'Nav norādīts modelis'
        
        # Get and check file path
        file_path = self.file_path_label.cget('text')
        if file_path == '...':
            status_label = 'Nav norādīta izvades mapīte'
        
        # Generate prices
        if status_label == '':
            GeneratePrices().run(make, model, file_path)
            self.status_label.configure(text='Cenas noģenerētas!')
        else:
            self.status_label.configure(text=status_label)
        
        # Change button text
        self.submit_btn.configure(text=self.def_submit_text)
        