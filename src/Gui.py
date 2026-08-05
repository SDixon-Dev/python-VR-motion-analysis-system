import tkinter as tk

def open_select_sport_screen():
    # Function to open the screen for selecting sport
    button_close.pack_forget()
    button_select_sport.pack_forget()
    button_back_sport.pack(side=tk.BOTTOM, pady=5)
    for sport_button in sport_buttons:
        sport_button.pack(pady=5)

def open_select_technique_screen(sport):
    # Function to open the screen for selecting technique
    global selected_sport
    selected_sport = sport
    label.config(text="Select a technique for " + sport)
    button_back_sport.pack_forget()
    for sport_button in sport_buttons:
        sport_button.pack_forget()
    button_back_technique.pack(side=tk.BOTTOM, pady=5)
    for technique_button in technique_buttons[sport]:
        technique_button.pack(pady=5)

def open_learn_technique_screen(technique):
    # Function to open the screen for learning the technique
    label.config(text="Starting stance of " + technique + " in " + selected_sport)
    additional_text.config(text=additional_info[selected_sport][technique])
    button_back_technique.pack_forget()
    for technique_button in technique_buttons[selected_sport]:
        technique_button.pack_forget()
    additional_text.pack(side=tk.BOTTOM, pady=10)
    button_learn.pack(side=tk.BOTTOM, pady=5)

def close_program():
    # Function to close the program
    root.destroy()

def back_to_main_screen():
    # Function to go back to the main screen
    label.config(text="Select an option")
    additional_text.pack_forget()
    button_back_sport.pack_forget()
    button_back_technique.pack_forget()
    button_learn.pack_forget()
    for sport_button in sport_buttons:
        sport_button.pack_forget()
    for technique_button in technique_buttons[selected_sport]:
        technique_button.pack_forget()
    button_close.pack(side=tk.BOTTOM, pady=5)
    button_select_sport.pack(side=tk.BOTTOM, pady=5)

# Create the main window
root = tk.Tk()
root.title("Prototype GUI")
root.geometry("300x250")

# Create label to display screen content
label = tk.Label(root, text="Prototype GUI")
label.pack(pady=5)

# Create additional label for extra information
additional_text = tk.Label(root, text="")
additional_text.pack(pady=5)

# Create buttons for Screen 1
button_close = tk.Button(root, text="Close Program", command=close_program)
button_close.pack(side=tk.BOTTOM, pady=5)

button_select_sport = tk.Button(root, text="Select Sport", command=open_select_sport_screen)
button_select_sport.pack(side=tk.BOTTOM, pady=5)

# Create buttons for Screen 2 (Select Sport)
button_back_sport = tk.Button(root, text="Back", command=back_to_main_screen)

sport_buttons = []
sports = ["Fencing", "Kendo", "Iaido"]
for sport in sports:
    button = tk.Button(root, text=sport, command=lambda sport=sport: open_select_technique_screen(sport))
    sport_buttons.append(button)

# Create buttons for Screen 3 (Select Technique)
button_back_technique = tk.Button(root, text="Back", command=back_to_main_screen)

technique_buttons = {
    "Fencing": [tk.Button(root, text="Lunge", command=lambda: open_learn_technique_screen("Lunge")),
                 tk.Button(root, text="Parry", command=lambda: open_learn_technique_screen("Parry")),
                 tk.Button(root, text="Feint", command=lambda: open_learn_technique_screen("Feint"))],
    "Kendo": [tk.Button(root, text="Kirikaeshi", command=lambda: open_learn_technique_screen("Kirikaeshi")),
                   tk.Button(root, text="Men-Uchi", command=lambda: open_learn_technique_screen("Men-Uchi")),
                   tk.Button(root, text="Tsuki", command=lambda: open_learn_technique_screen("Tsuki"))],
    "Iaido": [tk.Button(root, text="Nukitsuke", command=lambda: open_learn_technique_screen("Nukitsuke")),
               tk.Button(root, text="Kiritsuke", command=lambda: open_learn_technique_screen("Kiritsuke")),
               tk.Button(root, text="Chiburui", command=lambda: open_learn_technique_screen("Chiburui"))]
}

# Create buttons for Screen 4 (Learn`q  wa` Technique)
button_learn = tk.Button(root, text="Practice", command=lambda: print("Get Ready..."))

# Information about the sports techniques
additional_info = {
    "Fencing": {
        "Lunge": "Stand side on with back foot tipped against the marker \n Have your front foot perpendicular pointed towards the target \n Hold one controller in the dominant hand, grip with your thumb on one side and rest of your fingers on the other. Hold it in front of you at shoulder level. \n Hold the other controller at waist level slightly behind you \n Lean forward thrusting the dominant hand, adjusting the pitch and pointing towards the target \n Step forward with you front foot and stretch your back foot keeping it fixed",
        "Parry": "Additional information about ",
        "Feint": "Additional information about "
    },
    "Kendo": {
        "Kirikaeshi": "Additional information about ",
        "Men-Uchi": "Additional information about ",
        "Tsuki": "Additional information about "
    },
    "Iaido": {
        "Nukitsuke": "Additional information about ",
        "Kiritsuke": "Additional information about ",
        "Chiburui": "Additional information about "
    }
}

# Run the application
root.mainloop()