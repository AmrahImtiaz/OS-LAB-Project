import tkinter as tk
from tkinter import ttk, messagebox
import time


class Appointment:
    def __init__(self, first_name, last_name, contact, age_group, medical_condition, appointment_type, id_, burst_time):
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.age_group = age_group
        self.medical_condition = medical_condition
        self.appointment_type = appointment_type
        self.id = id_
        self.arrival_time = time.time()
        self.burst_time = burst_time
        self.wait_time = 0
        self.finish_time = self.arrival_time + self.burst_time


class AppointmentManager:
    def __init__(self):
        self.appointments = []
        self.next_normal_check_id = 1
        self.next_emergency_id = 1

    def add_appointment(self, first_name, last_name, contact, age_group, medical_condition, appointment_type):
        if appointment_type == "Normal Check":
            id_ = 1000 + self.next_normal_check_id
            self.next_normal_check_id += 1
            burst_time = 5 * 60  # in seconds
        elif appointment_type == "Emergency":
            id_ = 2000 + self.next_emergency_id
            self.next_emergency_id += 1
            burst_time = 60 * 60  # in seconds
        else:
            raise ValueError("Invalid appointment type")

        new_appointment = Appointment(first_name, last_name, contact, age_group, medical_condition, appointment_type, id_, burst_time)
        if appointment_type == "Emergency":
            self.appointments.insert(0, new_appointment)  # Prioritize emergencies
        else:
            self.appointments.append(new_appointment)
        return new_appointment

    def list_appointments(self):
        return self.appointments

    def delete_appointment(self, id_):
        for appointment in self.appointments:
            if appointment.id == id_:
                self.appointments.remove(appointment)
                return True
        return False

    def update_appointment(self, id_, updates):
        for appointment in self.appointments:
            if appointment.id == id_:
                appointment.first_name = updates.get("first_name", appointment.first_name)
                appointment.last_name = updates.get("last_name", appointment.last_name)
                appointment.contact = updates.get("contact", appointment.contact)
                appointment.age_group = updates.get("age_group", appointment.age_group)
                appointment.medical_condition = updates.get("medical_condition", appointment.medical_condition)
                return True
        return False


manager = AppointmentManager()


def create_gui():
    root = tk.Tk()
    root.title("Appointment Management System")
    root.geometry("600x500")

    # Frames
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill="both", expand=True)

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(side="top", fill="x")

    # Appointment list display
    tree = ttk.Treeview(main_frame, columns=("ID", "Name", "Type", "Contact"), show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Type", text="Type")
    tree.heading("Contact", text="Contact")
    tree.pack(side="top", fill="both", expand=True)

    def refresh_tree():
        for i in tree.get_children():
            tree.delete(i)
        for appointment in manager.list_appointments():
            tree.insert("", "end", values=(appointment.id, f"{appointment.first_name} {appointment.last_name}", appointment.appointment_type, appointment.contact))

    def add_appointment():
        def submit():
            try:
                first_name = entry_first_name.get()
                last_name = entry_last_name.get()
                contact = entry_contact.get()
                age_group = combo_age_group.get()
                medical_condition = entry_condition.get()
                appointment_type = combo_appointment_type.get()

                if not all([first_name, last_name, contact, age_group, appointment_type]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                new_appointment = manager.add_appointment(first_name, last_name, contact, age_group, medical_condition, appointment_type)
                messagebox.showinfo("Success", f"Appointment Created! ID: {new_appointment.id}")
                refresh_tree()
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        add_window = tk.Toplevel(root)
        add_window.title("Add Appointment")
        add_window.geometry("400x400")

        ttk.Label(add_window, text="First Name").pack(pady=5)
        entry_first_name = ttk.Entry(add_window)
        entry_first_name.pack()

        ttk.Label(add_window, text="Last Name").pack(pady=5)
        entry_last_name = ttk.Entry(add_window)
        entry_last_name.pack()

        ttk.Label(add_window, text="Contact").pack(pady=5)
        entry_contact = ttk.Entry(add_window)
        entry_contact.pack()

        ttk.Label(add_window, text="Age Group").pack(pady=5)
        combo_age_group = ttk.Combobox(add_window, values=["3 to 10", "11 to 15", "16 to 24", "25 to 35", "36 and above"])
        combo_age_group.pack()

        ttk.Label(add_window, text="Medical Condition").pack(pady=5)
        entry_condition = ttk.Entry(add_window)
        entry_condition.pack()

        ttk.Label(add_window, text="Appointment Type").pack(pady=5)
        combo_appointment_type = ttk.Combobox(add_window, values=["Normal Check", "Emergency"])
        combo_appointment_type.pack()

        ttk.Button(add_window, text="Submit", command=submit).pack(pady=20)

    def delete_appointment():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No appointment selected!")
            return

        item = tree.item(selected_item)
        id_ = item["values"][0]
        if manager.delete_appointment(id_):
            messagebox.showinfo("Success", f"Appointment ID {id_} deleted.")
            refresh_tree()
        else:
            messagebox.showerror("Error", "Failed to delete appointment.")

    ttk.Button(button_frame, text="Add Appointment", command=add_appointment).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Delete Appointment", command=delete_appointment).pack(side="left", padx=5)

    refresh_tree()
    root.mainloop()


if __name__ == "__main__":
    create_gui()
