from  tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import json 
class WelcomeWindow(Tk):
    def __init__(self):
        '''
        Function: Opens json file to load data and then runs the welcome screen function
        Args: nothing 
        Returns: nothing
        '''

        super().__init__()
        self.geometry("750x450")
        self.title("Rocket Hire")
        
        style = Style(self)
        style.configure('welcome.TButton',font= (None,60,'bold'),background = "SystemButtonFace" ) 
       # Loads json file data into variables for program to use 
        with open("storage.json") as file: 
            self.json_file = json.load(file)
            self.rocket_avalibility =self.json_file['avalibility'] 
            self.info_list = self.json_file['data']
        
        # Set rocket hire costs
        self.rocket_hire_cost = {"Rocket Lab Photon": 10000, "SpaceX Falcon 9": 5000, "Blue Origin New Shepard": 8000}
        
        self.welcome_screen()
        self.mainloop()

    def welcome_screen(self): 
        '''
        Function: Loads welcome screen UI 
        Args: Nothing 
        Returns: Nothing
        '''
        img = PhotoImage(file='emoji2.png')
        Label(self, text= "Welcome to the Spacecraft Hire Store!",font= ("Arial", 20, 'bold') , foreground= "Orange"). pack()
        a =Button(self, image= img,command= lambda: self.close_welcome_screen()) # Welcome button 
        a.pack(fill= BOTH,expand=True, padx=20, pady=20)
        a.image_names = img
        
        #Button(self, image= img, text="Enter Store", command= lambda: self.close_welcome_screen(), style='welcome.TButton').pack(fill= BOTH,expand=True, padx=20, pady=20)
    def close_welcome_screen(self): 
        '''
        Function: Closes welcome screen
        Args: Nothing
        Returns: self.load_main_page() 
        '''
        for widget in self.winfo_children():
            widget.destroy()
        
        return self.load_main_page()
    def load_main_page(self): 
        '''
        Function: Displays rocket select UI with receipt table 
        Args: Nothing 
        Returns: nothing
        '''
        
        # Creates UI frames to put things in 
        self.user_interface_frame = Frame(self)
        self.user_interface_frame.pack()

        self.treeview_frame = Frame(self)
        self.treeview_frame.pack(pady=10)
        
        self.geometry("600x350")
        # Loads all rockets that are avalible into dropdown tab
        self.dropdown_list = []
        for key in self.rocket_avalibility: 
            if self.rocket_avalibility[key] != 0:
                self.dropdown_list.append(f'{str(key)}: {self.rocket_avalibility[key]}')
        if self.dropdown_list == []: 
            self.dropdown_list.append("All rockets are hired!")
        
        Label(self.user_interface_frame, text= "Please select the rocket you would like to hire:").pack( padx= 5 , pady= 5)
        
        self.rocket_dropdown = Combobox(self.user_interface_frame, values=self.dropdown_list, state= "readonly",width= 25)
        self.rocket_dropdown.pack( padx= 5 , pady= 5)
        # UI buttons
        Button(self.user_interface_frame, text= "Return Selected", command= lambda: self.return_rocket(self.receipt_table.item(self.receipt_table.selection()))).pack(side=LEFT, padx= 5 , pady= 5)
        Button(self.user_interface_frame, text= "Open Receipt", command=lambda : self.display_receipt(self.receipt_table.item(self.receipt_table.selection()))).pack(side=LEFT, padx= 5 , pady= 5)
        Button(self.user_interface_frame, text="Select", command=lambda: self.rocket_select(self.rocket_dropdown.get())).pack(side=LEFT, padx= 5 , pady= 5)
        # Scrollbar for receipt table 
        scrollbar = Scrollbar(self.treeview_frame, command=lambda: self.receipt_table.yview)
        # Receipt table to display receipt data and also let user open and return receipts 
        self.receipt_table = Treeview(self.treeview_frame, columns = ('receipt', "rocket","hire period","passengers", "pilot", "cost"), show= "headings",yscrollcommand = scrollbar.set)
        self.receipt_table.pack(side= "left")
        scrollbar.pack(fill=Y,expand=TRUE)
    
        self.receipt_table.heading('receipt', text = "Receipt")
        self.receipt_table.column('receipt', anchor='center', stretch= NO,width= 75)
  
        self.receipt_table.heading('rocket', text = "Rocket")
        self.receipt_table.column('rocket', anchor='center', stretch= NO,width= 150)
    
        self.receipt_table.heading('hire period', text = "Hire Period")
        self.receipt_table.column('hire period', anchor='center', stretch= NO,width= 75)

        self.receipt_table.heading('passengers', text = "Passengers")
        self.receipt_table.column('passengers', anchor='center', stretch= NO,width= 75)

        self.receipt_table.heading('pilot', text = "Pilot Needed")
        self.receipt_table.column('pilot', anchor='center', stretch= NO,width= 75)
        
        self.receipt_table.heading('cost', text = "Cost ($)")
        self.receipt_table.column('cost', anchor='center', stretch= NO,width= 75)
        
        for items in self.info_list:
            self.receipt_table.insert ( "", END,values=(items[0],items[1],items[2],items[3],items[4],items[5]) )


    def display_receipt (self, selected_receipt): 
        '''
        Function: Displays the selected receipt in a info window 
        Args: selected_receipt - The receipt that the user has selected on the receipt table
        Returns: nothing
        '''
        if selected_receipt['values'] == "":
            messagebox.showerror('Error', "Please select receipt to open first!")
            return
        data = selected_receipt['values']
        # Selected receipt data displayed in a info popup 
        messagebox.showinfo("receipt",f"Receipt: {data[0]}\nRocket: {data[1]}\nHire Period: {data[2]} Days\nPassengers: {data[3]}\nPilot needed: {data[4]}\nCost: ${data[5]}")
  
    
    def return_rocket(self,selected_receipt): 
        '''
        Function: Returns the rocket/receipt user has selected 
        Args: selected_receipt - The receipt that the user has selected on the receipt table
        Returns: Nothing
        '''
        # Error checking to see if user has selected anything 
        if selected_receipt['values'] == "":
            messagebox.showerror('error','Please select a rocket first!')
            return
            
        data = selected_receipt['values'] 
        # Confirm user input
        confirm = messagebox.askyesno("Confirm", 'Are you sure you want to return this?')
        if confirm:
            self.info_list.remove(data)
            
            self.rocket_avalibility[data[1]] += 1 
            self.dropdown_list.append(f"{data[1]}: {self.rocket_avalibility[data[1]]}") 
            
            self.clear_screen()
            self.update_json()
    

    def rocket_select(self,rocket): 
        '''
        Function: Checks what rocket the user has selected and updates the UI to other user inputs
        Args: rocket - the rocket the user selected
        Returns: Nothing
        '''
        if not rocket: 
            messagebox.showerror("Error", f"select rocket.")
            return
        elif rocket == "All rockets are hired!": 
            messagebox.showerror("Error", f"Sorry, but all rockets are hired!")
            return
        for widget in self.user_interface_frame.winfo_children():
            widget.destroy()
        self.rocket = rocket[:-3]

        # Loading all UI buttons and labels
        Label(self.user_interface_frame, text= "How many days are you hiring the rocket for: ").grid(column=0, row=0, pady=5, sticky= W)
        self.hire_period = Entry(self.user_interface_frame)
        self.hire_period.grid(column=1, row=0, pady=5)

        Label(self.user_interface_frame, text= "How many passengers are going on the rocket: ").grid(column=0, row=1, pady=5, sticky= W)
        self.passengers  = Entry(self.user_interface_frame)
        self.passengers.grid(column=1, row=1, pady=5)

        Label(self.user_interface_frame, text= "Do you need a pilot to pilot the rocket: ").grid(column=0, row=2, pady=5, sticky= W)
        self.pilot_hire = Combobox(self.user_interface_frame, values= ["Yes", "No"], state="readonly", width= 18)
        self.pilot_hire.grid(column=1, row=2, pady=5)
        
        button_frame = Frame(self.user_interface_frame)
        button_frame.grid(column= 0, row=3,columnspan=2)
        Button(button_frame, text= "Cancel", command= lambda: self.clear_screen()).pack(side=LEFT,padx= 10, pady=5)
        self.select_button= Button(button_frame, text="Hire", command=lambda: self.calculate(self.hire_period.get().strip().lower(),
        self.passengers.get().strip().lower(), self.pilot_hire.get().strip()))
        self.select_button.pack(padx=10, pady=5)


    def calculate (self, hire_period, passengers,pilot_hire):
        '''
        Function: Error checks users inputs and if everything is correct then calculates costs then adds it to the receipt display
        Args: hire_period - hire period input, passengers - passenger amound input, pilot_hire - if the user needs a pilot
        Returns: Nothing 
        
        '''
        error =[]
        # Error checking user inputs 
        if not hire_period or not hire_period.isdigit() or int(hire_period) > 30:
            error.append("hire period (between 1 and 30 days)" ) 
        if not passengers or not passengers.isdigit() or int(passengers) >10:
            error.append( "passenger amount (between 1 and 10 passengers)")
        
        if not pilot_hire: 
            error.append( "pilot response (select Yes or No)")

        if error: # If there is error then display error message
            messagebox.showerror("Error", f'Invalid ' + ", ".join(error) + '. ')
            return

        counter = 0 
        # Adding user data to receipt list
        self.rocket_avalibility[self.rocket] -= 1
        if self.rocket_avalibility[self.rocket] == 0: 
            for key in self.dropdown_list:
                if key[:-3] == self.rocket: self.dropdown_list.pop(counter)
                counter += 1

        cost = (int(hire_period) * self.rocket_hire_cost[self.rocket]) + (int(passengers) * 500*int(hire_period)) + (500 * int(hire_period) if pilot_hire == "Yes" else 0)
        self.json_file['counter'] += 1
        self.info_list.append([self.json_file['counter'] , self.rocket, int(hire_period),int(passengers),pilot_hire,cost])
       
        # Updates json 
        self.update_json()
        self.clear_screen()
    
    
    def update_json(self):
        '''
        Function: Updates json file with new data
        '''
        with open('storage.json','w') as file: json.dump(self.json_file, file, indent= 5)
        
 
    def clear_screen(self):
        # Refreshes all UI items on screen 
        for widget in self.winfo_children():
            widget.destroy()
        self.load_main_page()
        return
        
        
WelcomeWindow()
