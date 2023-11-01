import csv
import tkinter as tk
from tkinter import ttk
import functools
from tkinter import filedialog
import os

# Define global dictionaries
country_count_dict = {} # Contains {"country", "number of instances of this country"}
country_select_dict = {} # Contains {"country", "True|False"} - True if selected

def clear_frame(frame):
    ## This should clear the frame when selecting a new input file,
    ## but it doesn't work
    for child in frame.winfo_children():
        child.destroy()
        
def count_selected():
    ## Count how many entries are against the selected countries
    # and update the displayed total
    select_count=0
    for country in country_count_dict:
        if country_select_dict[country] == True:
            select_count = select_count + country_count_dict[country]
    status.set("Number of entries selected is "+ str(select_count))
    
def on_checkbox_click(country):
    country_select_dict[country] = not country_select_dict[country]  # Toggle the selection status
    count_selected()

def create_long_scrollable_list():    
    frame=ttk.Frame(country_select_frame)
    clear_frame(frame)
    frame.pack(side=tk.LEFT, anchor='nw', expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame, height=570)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill='y')

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    country_select_dict.clear() #Clear the list before starting a new one

    # Create a colored background frame inside checkbox_frame
    background_frame = tk.Frame(canvas, background="white")
    canvas.create_window((0, 0), window=background_frame, anchor="nw")
 
    for country in country_count_dict:
        # Output the country_list and country_count_list to the list box
        var = tk.IntVar()
        count=country_count_dict[country]
        output_string = (country + ' (' + str(count) + ')').ljust(50)
        country_select_dict[country] = False # All countries initially not selected
        callback = functools.partial(on_checkbox_click, country)
        checkbox = tk.Checkbutton(
            background_frame,
            text=output_string,
            command=callback,
            bg="white",
            variable=var
            )
        checkbox.pack(anchor="w", padx=5)

def open_input_file():
    ## Count number of lines in input file and display it in the status box
    csvFileName = returned_values.get('filename')
    base_name = returned_values.get('basename')
    csv_input_file = open (csvFileName , "r", encoding = "ISO-8859-1")
    rowcount = 0
    for row in csv_input_file:
        rowcount+=1
    status.set("Number of lines in "+base_name+" is "+ str(rowcount))

def country_count(country_list):
    ## Count the number of entries in the input file against each country name
    # Open the file and read it into a temporary file
    csvFileName = returned_values.get('filename')
    country_count_dict.clear() #Reset the country counts
    
    with open(csvFileName, encoding = "ISO-8859-1", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        tmp=[]
        for row in reader:
            tmp.append(row[6])
    for country in country_list:
        count=tmp.count(country)
        country_count_dict[country]=count

#    print (country_count_dict)
        
def build_country_list():
    ## Build a list of countries included in the input file
    try:
        # Open the file and read it into a temporary file
        csvFileName = returned_values.get('filename')    
        with open(csvFileName, encoding = "ISO-8859-1", newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            tmp=[]
            for row in reader:
                tmp.append(row)
        country_list=[]
        x=0
        for row in tmp:
            country= tmp[x][6]
            if country not in country_list:
                country_list.append(country)
            x = x+1
        # sort the list
        country_list.sort()
        # create_long_scrollable_list(country_list,country_count_list)
        return country_list

    except FileNotFoundError:
        status.set("File not found")
        return[]

    except Exception as e:
        status.set("Error: "+str(e))
        return[]

def process_input_file():
    # Reset the dictionaries
    country_count_dict.clear()
    country_select_dict.clear()
    # Choose and open the input file
    open_input_file()
    # Build the country list
    country_list=build_country_list()
    # Count the entries per country
    country_count(country_list)
    # Display the scrollable list of tick-boxes
    create_long_scrollable_list()

def write_output_file():
    csvFileName = returned_values.get('filename')
    base_name = returned_values.get('basename')
    csvFileOut = returned_values.get('out_filename')
    out_base_name = returned_values.get('out_base')
    
    with open(csvFileName, encoding = "ISO-8859-1", newline='') as csvfile:
        reader = csv.reader(csvfile)
        tmp=[]
        for row in reader:
            tmp.append(row)
            
    with open(csvFileOut,'w',encoding = "ISO-8859-1", newline='')as csvout:
        csv_writer=csv.writer(csvout)
        header = tmp[0]
        csv_writer.writerow(header)
        x = 0
        rows_written = 0
        for row in tmp:
            if x>0:
                country = tmp[x][6]
                if country_select_dict[country] == True:
                    csv_writer.writerow(row)
                    rows_written += 1
            x = x + 1
    csvout.close()
    status.set(out_base_name+" - "+str(rows_written)+" rows written ")
    
if __name__ == "__main__":
    
    csvFileName = "user.csv"
    csvFileOut="contacts.csv"

    returned_values = {} # Dictionary used for returning values from button press
    returned_values['filename']=csvFileName
    returned_values['basename']=csvFileName
    returned_values['out_filename']=csvFileOut
    returned_values['out_base']=csvFileOut

    root = tk.Tk()
    root.title("Trim contacts.csv")
    root.geometry("400x800")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    # Set the styles for ttk buttons
    style = ttk.Style()
    style.configure("Blue.TButton", font=("Courier New", 12), borderwidth=3)

    global status
    status = tk.StringVar()
    status_label = ttk.Label(root, textvariable=status)
    status_label.grid(sticky=tk.W + tk.E, row=99, padx=10, pady=2)
    status.set("Ready")
    
    input_text_frame = ttk.Frame(root)
    input_text_frame.grid(row=0, column=0, padx=10, sticky=(tk.E + tk.W)) 
 
    lbl1 = ttk.Label(master=input_text_frame, text="1. Choose input file and open it:")
    lbl1.pack(anchor='w', padx=10)

    input_field_frame = ttk.Frame(root)
    input_field_frame.grid(row = 1, column=0, padx=10, sticky=(tk.E + tk.W + tk.N))

    file_select_button = ttk.Button(text = csvFileName, style="Blue.TButton", width=20, master = input_field_frame)
    file_select_button.grid(row=0, column=0)

    def choose_file_dialog():
        ## When the input filename button is clicked,
        ## open a filename dialog box.
        ## Strip the path name before replacing the button text
        csvFileName = filedialog.askopenfilename(filetypes = (("CSV Files","*.csv"),),title="Select CSV input file")
        base_name = os.path.basename(csvFileName)
        file_select_button.config(text=base_name)
        returned_values['filename'] = csvFileName
        returned_values['basename'] = base_name

    def save_file_dialog():
        ## When the output filename button is clicked,
        ## open a filename dialog box.
        ## Strip the path name before replacing the button text
        csvFileOut = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes = (("CSV Files","*.csv *.CSV"),),
            title="Name the CSV output file"
        )
        base_name_out = os.path.basename(csvFileOut)
        output_file_button.config(text=base_name_out)
        returned_values['out_filename'] = csvFileOut
        returned_values['out_base'] = base_name_out
        write_output_file()
        
    file_select_button.config(command=choose_file_dialog)
    
    button1 = ttk.Button(text = "Open", command = process_input_file, master=input_field_frame)
    button1.grid(row=0, column=1, pady=2)

    country_select_frame = ttk.Frame(root)
    country_select_frame.grid(row=2, column=0, padx=10, sticky=(tk.E + tk.W))

    lbl2 = ttk.Label(master=country_select_frame, text="2. Select countries:")
    lbl2.pack(anchor='nw', padx=10, pady=2)

    output_frame = ttk.Frame(root)
    output_frame.grid(row=3, column=0, padx=10, pady=2, sticky=(tk.E + tk.W))
    
    lbl3 = ttk.Label(master=output_frame, text="3. Choose output file and save:")
    lbl3.pack(anchor='w', padx=10)

    output_field_frame = ttk.Frame(root)
    output_field_frame.grid(row=4, column=0, padx=10, sticky=(tk.E + tk.W))

    output_file_button = ttk.Button(text = csvFileOut, style="Blue.TButton", width=20, master = output_field_frame)
    output_file_button.grid(row=0, column=0)

    output_file_button.config(command=save_file_dialog)
    
    button2_text="Save"
    button2 = ttk.Button(text = button2_text, command = write_output_file, master=output_field_frame)
    button2.grid(row=0, column=1)
    
    root.mainloop()
    
