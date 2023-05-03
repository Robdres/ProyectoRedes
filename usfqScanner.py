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
def create_buttons(container, item_data, output_label):
    actions = [
        ("ID", lambda data=item_data: output_label.config(text=f"ID: {data[0]}")),
        ("Name", lambda data=item_data: output_label.config(text=f"Name: {data[1]}")),
        ("MAC", lambda data=item_data: output_label.config(text=f"MAC: {data[2]}")),
        ("Status", lambda data=item_data: output_label.config(text=f"Status: {data[3]}")),
    ]
    for i, (text, action) in enumerate(actions):
        input_limiter = customtkinter.CTkInputDialog(container)
        input_limiter.grid(row = 1,column = i, padx = 5, pady=5)
        button = customtkinter.CTkButton(container, text=text, command=action)
        button.grid(row=1, column=i, padx=5, pady=5)

def slider_value(value):
        print("con el value: ", value)

        return value

def label_value(container, value):
    #value = slider_value
    print("Este es el value -> ", value)
    labelSlider = customtkinter.CTkLabel(container, text=value)
    labelSlider.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    
# Function to create item container
def create_item_container(parent, data, output_label):
    for i, item_id in enumerate(data):
        #create slider
        
        #slider.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        item_data = data[item_id]  # Get the item data using the item_id
        item_container = customtkinter.CTkFrame(parent, width=300, height=100, corner_radius=10)
        item_container.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="nsew")

        label_text = f"{item_data[0]} {item_data[1]} {item_data[2]} {item_data[3]}"
        label = customtkinter.CTkLabel(item_container, text=label_text)
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        button_container = customtkinter.CTkFrame(item_container, width=300, height=40, corner_radius=10)
        button_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        

        button_definitions = [
            ("Limit", partial(output_label.configure, text=f"ID: {item_data[0]}")),
            ("Block", partial(output_label.configure, text=f"Name: {item_data[1]}")),
            ("Info", partial(output_label.configure, text=f"Status: {item_data[3]}")),
        ]

        for j, (button_text, button_command) in enumerate(button_definitions):
            button = customtkinter.CTkButton(button_container, text=button_text, command=button_command)
            button.grid(row=0, column=j, padx=(0, 10), pady=(0, 10), sticky="nsew")
            #Slider en cada item
            slider = customtkinter.CTkSlider(button_container, from_=0, to=100, number_of_steps=10, command=slider_value)
            slider.grid(row=3, column=0, padx=(2, 10), pady=(10, 10), sticky="ew")
            #Label para el value del slider
            value = slider.get()
            label_value(button_container,value)
            
            #Radios Buttons
            #radio_var = tkinter.IntVar(value=0)
            radio_var = tkinter.StringVar(value="")
            radio_button_bit = customtkinter.CTkRadioButton(button_container,text="bit" ,variable=radio_var, value="bit")
            radio_button_bit.grid(row=5, column=0, pady=10, padx=20, sticky="n")
            
            radio_button_kbit = customtkinter.CTkRadioButton(button_container,text="kbit" ,variable=radio_var, value="kbit")
            radio_button_kbit.grid(row=6, column=0, pady=10, padx=20, sticky="n")
            
            radio_button_mbit = customtkinter.CTkRadioButton(button_container,text="mbit" ,variable=radio_var, value="mbit")
            radio_button_mbit.grid(row=7, column=0, pady=10, padx=20, sticky="n")
            
            radio_button_gbit = customtkinter.CTkRadioButton(button_container,text="gbit" ,variable=radio_var, value="gbit")
            radio_button_gbit.grid(row=8, column=0, pady=10, padx=20, sticky="n")
            
            print("radiobutton toggled, current value:", radio_var.get())
            
            
       
            

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
    

if __name__ == "__main__":
    app = App()
    app.mainloop()