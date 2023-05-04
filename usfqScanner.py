import tkinter
import tkinter.messagebox
import customtkinter
import subprocess
import socket
import struct
import random
import string
from functools import partial



customtkinter.set_appearance_mode("dark")
#customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


# Function to generate a random MAC address
def random_mac_address():
    return ":".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)])

# Function to generate random data 
def generate_data(n=10):
    data = {}
    for i in range(n):
        _id = i + 1
        name = "".join(random.choices(string.ascii_letters, k=5))
        mac_address = random_mac_address()
        status = random.choice(["Online", "Offline"])
        data[_id] = (_id, name, mac_address, status)
    return data


# Function to create buttons and bind actions
def slider_value(value, labelSlider):
    labelSlider.configure(text=value)

  
# Function to create item container
def create_item_container(parent, data, output_label):
    for i, item_id in enumerate(data):
        item_data = data[item_id]  # Get the item data using the item_id
        item_container = customtkinter.CTkFrame(parent, width=300, height=100, corner_radius=10)
        item_container.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")

        label_text = f"{item_data[0]} {item_data[1]} {item_data[2]} {item_data[3]}"
        label = customtkinter.CTkLabel(item_container, text=label_text)
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        button_container = customtkinter.CTkFrame(item_container, width=300, height=40, corner_radius=10)
        button_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        button_definitions = [
            ("Limit Bandwidth", partial(output_label.configure, text=f"ID: {item_data[0]}")),
            ("Block", partial(output_label.configure, text=f"Name: {item_data[1]}")),
            ("Info", partial(output_label.configure, text=f"Status: {item_data[3]}")),
        ]

        for j, (button_text, button_command) in enumerate(button_definitions):
            button = customtkinter.CTkButton(button_container, text=button_text, command=button_command)
            button.grid(row=0, column=j, padx=(0, 10), pady=(0, 10), sticky="nsew")
            
            slider = customtkinter.CTkSlider(button_container, from_=0, to=100, number_of_steps=10)
            slider.grid(row=3, column=0, padx=(2, 10), pady=(10, 10), sticky="ew")
            
            labelSlider = customtkinter.CTkLabel(button_container, text="50")
            labelSlider.grid(row=4, column=0, padx=10, pady=10, sticky="w")
            
            #slider.configure(command=lambda value: slider_value(value, labelSlider)) /Previous Lambda not working for data requests
            slider.configure(command=lambda value, label=labelSlider: slider_value(value, label))
            
            

class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()
            
           
       
            

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("USFQ Red Scanner")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="USFQ Scanner", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
    #Entrada para limitar acceso a sitios web 
        
        self.entry = customtkinter.CTkEntry(self.sidebar_frame,placeholder_text="Limitar acceso a un sitio en especifico")
        self.entry.grid(row=1, column=0, columnspan=2, padx=(5, 0), pady=(5, 5), sticky="nsew")
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Limitar Acceso",command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        #self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create output label
        self.output_label = customtkinter.CTkLabel(self, text="")
        self.output_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # create main entry and button
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Connected Devices")
        self.scrollable_frame.grid(row=1, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=10)
        
        #RADIO BUTTON FRAME
        
        
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                                                                       item_list=["bit","kbit","mbit","gbit"],
                                                                       label_text="Arguments for limiting")
        self.scrollable_radiobutton_frame.grid(row=1, column=3, padx=5, pady=5, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=200)
        
        #Show blockled domains
        self.button_blocked_domains = customtkinter.CTkButton(self.sidebar_frame, text="Show Blocked Domains",command =self.action_showButton)
        self.button_blocked_domains.grid(row=3, column=0, padx=20, pady=10)
        
        
        #Free button
        self.button_free = customtkinter.CTkButton(self.sidebar_frame, text="Free")
        self.button_free.grid(row=5, column=0, padx=20, pady=10)
        
        #TextBox Domain List
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=250)
        self.textbox.grid(row=4, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        

        # Generate random data
        data = generate_data(10)

        # Display data in the scrollable frame
        create_item_container(self.scrollable_frame, data, self.output_label)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
   #RADIO BUTTON     
    def radiobutton_frame_event(self):
        print(f"radiobutton frame modified: {self.scrollable_radiobutton_frame.get_checked_item()}")
        
    def action_showButton(self):
        self.textbox.insert("0.0", "List Blocked Domains\n\n" + "Obtener nombres de los dominios bloqueados\n\n")
        
        
        
    
    
    
    

if __name__ == "__main__":
    app = App()
    app.mainloop()