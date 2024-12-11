import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta

class Patient:
    def __init__(self, first_name, last_name, contact, age_group, previous_medical_condition, appointment_type, patient_id, arrival_time, burst_time):
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.age_group = age_group
        self.previous_medical_condition = previous_medical_condition
        self.appointment_type = appointment_type
        self.id = patient_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0
        self.finish_time = arrival_time + timedelta(minutes=burst_time)

appointments = []
next_normal_check_id = 1
next_emergency_id = 1

def create_appointment():
    global next_normal_check_id, next_emergency_id

    # Validate inputs
    if not entry_first_name.get() or not entry_last_name.get() or not entry_contact.get() or not entry_previous_medical_condition.get():
        messagebox.showerror("Input Error", "Please fill all the fields")
        return
    
    if not entry_contact.get().isdigit():
        messagebox.showerror("Input Error", "Contact number must be numeric")
        return

    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    contact = entry_contact.get()
    age_group = age_group_var.get()
    previous_medical_condition = entry_previous_medical_condition.get()
    appointment_type = appointment_type_var.get()

    if appointment_type == "Normal Check":
        burst_time = 5
        patient_id = next_normal_check_id
        next_normal_check_id += 1
    else:
        burst_time = 60
        patient_id = next_emergency_id
        next_emergency_id += 1

    arrival_time = datetime.now()
    patient = Patient(first_name, last_name, contact, age_group, previous_medical_condition, appointment_type, patient_id, arrival_time, burst_time)

    if appointments:
        last_patient = appointments[-1]
        patient.wait_time = (last_patient.finish_time - arrival_time).seconds // 60
        patient.finish_time = arrival_time + timedelta(minutes=patient.wait_time + burst_time)

    if appointment_type == "Emergency":
        appointments.insert(0, patient)
    else:
        appointments.append(patient)

    messagebox.showinfo("Success", f"Appointment created successfully! Your appointment ID is: {patient_id}")
    clear_form()

def clear_form():
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_previous_medical_condition.delete(0, tk.END)

def list_appointments():
    list_window = tk.Toplevel(root)
    list_window.title("All Appointments")
    list_window.geometry("800x400")

    if not appointments:
        tk.Label(list_window, text="No appointments yet.", font=("Arial", 12), fg="black").pack()
        return

    # Create a Treeview (Table-like environment)
    tree = ttk.Treeview(list_window, columns=("ID", "Name", "Contact", "Type", "Arrival", "Finish"), show="headings")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Define the column headings
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Contact", text="Contact")
    tree.heading("Type", text="Type")
    tree.heading("Arrival", text="Arrival")
    tree.heading("Finish", text="Finish")

    # Define column width
    tree.column("ID", width=50, anchor="center")
    tree.column("Name", width=150, anchor="w")
    tree.column("Contact", width=100, anchor="center")
    tree.column("Type", width=100, anchor="center")
    tree.column("Arrival", width=150, anchor="center")
    tree.column("Finish", width=150, anchor="center")

    # Insert rows for appointments
    for patient in appointments:
        arrival_time_str = patient.arrival_time.strftime("%Y-%m-%d %H:%M:%S")
        finish_time_str = patient.finish_time.strftime("%Y-%m-%d %H:%M:%S")
        name = f"{patient.first_name} {patient.last_name}"
        tree.insert("", "end", values=(patient.id, name, patient.contact, patient.appointment_type, arrival_time_str, finish_time_str))

        # Add a "Delete" button for each row (Postpone/Remove appointment)
        tree.bind("<Delete>", lambda event, tree=tree: delete_appointment(tree))

def delete_appointment(tree):
    selected_item = tree.selection()
    if selected_item:
        item = selected_item[0]
        appointment_id = tree.item(item)["values"][0]
        appointment_to_remove = next((appt for appt in appointments if appt.id == appointment_id), None)
        if appointment_to_remove:
            appointments.remove(appointment_to_remove)
            tree.delete(item)
            messagebox.showinfo("Success", f"Appointment with ID {appointment_id} has been postponed (removed).")
        else:
            messagebox.showerror("Error", "Appointment not found!")
    else:
        messagebox.showerror("Error", "No appointment selected!")

# Main Window
root = tk.Tk()
root.title("Doctor's Appointment System")
root.geometry("600x400")
root.resizable(False, False)

# Colors
background_color = "#add8e6"
frame_color = "#d1e7f0"
button_color = "#6495ed"
button_hover_color = "#4169e1"
label_color = "#2f4f4f"
entry_color = "#ffffff"

# Create main frame
main_frame = tk.Frame(root, bg=background_color)
main_frame.pack(pady=20)

# Input Section (Left-align text fields and labels)
tk.Label(main_frame, text="First name:", font=("Arial", 12), fg=label_color, bg=background_color, anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_first_name = tk.Entry(main_frame, font=("Arial", 12), bg=entry_color)
entry_first_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Last name:", font=("Arial", 12), fg=label_color, bg=background_color, anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_last_name = tk.Entry(main_frame, font=("Arial", 12), bg=entry_color)
entry_last_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Contact number:", font=("Arial", 12), fg=label_color, bg=background_color, anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_contact = tk.Entry(main_frame, font=("Arial", 12), bg=entry_color)
entry_contact.grid(row=2, column=1, padx=10, pady=5)

# Age Group
age_group_label = tk.LabelFrame(main_frame, text="Select Age Group", font=("Arial", 12), padx=10, pady=10, bg=frame_color)
age_group_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
age_group_var = tk.IntVar()

age_groups = ["3 to 10", "11 to 15", "16 to 24", "25 to 35", "36 and above"]
for idx, group in enumerate(age_groups, start=1):
    tk.Radiobutton(age_group_label, text=group, variable=age_group_var, value=idx, font=("Arial", 10), bg=frame_color).grid(row=0, column=idx-1, padx=5)

# Medical Condition
tk.Label(main_frame, text="Previous medical condition:", font=("Arial", 12), fg=label_color, bg=background_color, anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_previous_medical_condition = tk.Entry(main_frame, font=("Arial", 12), bg=entry_color)
entry_previous_medical_condition.grid(row=4, column=1, padx=10, pady=5)

# Appointment Type
appointment_type_label = tk.LabelFrame(main_frame, text="Select Appointment Type", font=("Arial", 12), padx=10, pady=10, bg=frame_color)
appointment_type_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
appointment_type_var = tk.StringVar()

tk.Radiobutton(appointment_type_label, text="Normal Check", variable=appointment_type_var, value="Normal Check", font=("Arial", 10), bg=frame_color).grid(row=0, column=0, padx=5)
tk.Radiobutton(appointment_type_label, text="Emergency", variable=appointment_type_var, value="Emergency", font=("Arial", 10), bg=frame_color).grid(row=0, column=1, padx=5)

# Buttons
button_frame = tk.Frame(root, bg=background_color)
button_frame.pack(pady=20)

create_button = tk.Button(button_frame, text="Create Appointment", font=("Arial", 12), bg=button_color, fg="white", activebackground=button_hover_color, command=create_appointment)
create_button.grid(row=0, column=0, padx=10)

list_button = tk.Button(button_frame, text="List Appointments", font=("Arial", 12), bg=button_color, fg="white", activebackground=button_hover_color, command=list_appointments)
list_button.grid(row=0, column=1, padx=10)

# Key binding for Enter to shift focus to the next field
def focus_next(event):
    event.widget.tk_focusNext().focus()
    return "break"

entry_first_name.bind("<Return>", focus_next)
entry_last_name.bind("<Return>", focus_next)
entry_contact.bind("<Return>", focus_next)
entry_previous_medical_condition.bind("<Return>", focus_next)

root.mainloop()
