import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk

class Passenger:
    def __init__(self, name, passport_number):
        self.name = name
        self.passport_number = passport_number

    def __str__(self):
        return f"{self.name} ({self.passport_number})"

    def __eq__(self, other):
        if isinstance(other, Passenger):
            return self.name == other.name and self.passport_number == other.passport_number
        return False
    
    def __hash__(self):
        return hash((self.name, self.passport_number))

class Flight:
    def __init__(self, flight_number, origin, destination, total_seats):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.total_seats = total_seats
        self.available_seat = total_seats
        self.Passengers = []

    def book_seat(self, passenger):
        if self.available_seat > 0:
            self.Passengers.append(passenger)
            self.available_seat -= 1
            return True
        return False

    def cancle_seat(self, passenger):
        if passenger in self.Passengers:
            self.Passengers.remove(passenger)
            self.available_seat += 1
            return True
        return False


class ReservationSystem:
    def __init__(self):
        self.flights = []

    def add_flight(self, flight):
        self.flights.append(flight)

    def book_flight(self, flight_number, passenger):
        for flight in self.flights:
            if flight.flight_number == flight_number:
                return flight.book_seat(passenger)
        return False

    def cancle_reservation(self, flight_number, passenger):
        for flight in self.flights:
            if flight.flight_number == flight_number:
                return flight.cancle_seat(passenger)
        return False

    def display_flight(self):
        return [
            f"{flight.flight_number}: {flight.origin} to {flight.destination}, Seats: {flight.available_seat}"
            for flight in self.flights
        ]

    def display_passenger(self, flight_number):
        for flight in self.flights:
            if flight.flight_number == flight_number:
                return [str(passenger) for passenger in flight.Passengers]
        return None


def main():
    system = ReservationSystem()

    # Add sample flights
    flight1 = Flight("F001", "Pune", "Mumbai", 50)
    flight2 = Flight("F002", "Mumbai", "Delhi", 40)
    flight3 = Flight("F003", "Bangalore", "Chennai", 60)
    flight4 = Flight("F004", "Hyderabad", "Pune", 70)

    system.add_flight(flight1)
    system.add_flight(flight2)
    system.add_flight(flight3)
    system.add_flight(flight4)

    root = tk.Tk()
    root.title("AIRLINE RESERVATION SYSTEM")
    root.geometry("800x600")

    bg_image = Image.open("airline.png")
    bg_image = bg_image.resize((1000,1000),Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)

    background_label = tk.Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = tk.Label(
        root,
        text= "RESERVATION FORM",
        font=("Helevetica",24,"bold"),
        bg="lightblue",
        fg="black"
    )

    title_label.place(relx=0.5,rely=0.03,anchor="center")



    # Configure rows and columns
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_rowconfigure(6, weight=1)
    root.grid_rowconfigure(7, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    def book_ticket():
        flight_number = entry_flight_number.get()
        passenger_name = entry_passenger_name.get()
        passport_number = entry_passport_number.get()

        if not flight_number or not passenger_name or not passport_number:
            messagebox.showerror("Error", "All fields are required!")
            return

        passenger = Passenger(passenger_name, passport_number)
        if system.book_flight(flight_number, passenger):
            messagebox.showinfo("Success", "Booking successful!")
        else:
            messagebox.showerror("Error", "Booking failed. No available seats.")

    def cancel_ticket():
        flight_number = entry_flight_number.get()
        passenger_name = entry_passenger_name.get()
        passport_number = entry_passport_number.get()

        if not flight_number or not passenger_name or not passport_number:
            messagebox.showerror("Error", "All fields are required!")
            return

        passenger = Passenger(passenger_name, passport_number)
        if system.cancle_reservation(flight_number, passenger):
            messagebox.showinfo("Success", "Cancellation successful!")
        else:
            messagebox.showerror("Error", "Cancellation failed. Passenger not found or flight not found.")

    def view_flights():
        flights = system.display_flight()
        flight_list.delete(0, tk.END)
        for flight in flights:
            flight_list.insert(tk.END, flight)

    def view_passengers():
        flight_number = entry_flight_number.get()
        passengers = system.display_passenger(flight_number)
        passenger_list.delete(0, tk.END)
        if passengers:
            for passenger in passengers:
                passenger_list.insert(tk.END, passenger)
        else:
            messagebox.showinfo("Info", "No passengers found for this flight.")

    tk.Label(root, text="Flight Number").grid(row=0, column=0, padx=10, pady=10)
    entry_flight_number = tk.Entry(root)
    entry_flight_number.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Passenger Name").grid(row=1, column=0, padx=10, pady=10)
    entry_passenger_name = tk.Entry(root)
    entry_passenger_name.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Passport Number").grid(row=2, column=0, padx=10, pady=10)
    entry_passport_number = tk.Entry(root)
    entry_passport_number.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(root, text="Book Ticket", command=book_ticket).grid(row=3, column=0, padx=10, pady=10)
    tk.Button(root, text="Cancel Ticket", command=cancel_ticket).grid(row=3, column=1, padx=10, pady=10)

    tk.Button(root, text="View Flights", command=view_flights).grid(row=4, column=0, padx=10, pady=10)
    tk.Button(root, text="View Passengers", command=view_passengers).grid(row=4, column=1, padx=10, pady=10)

    tk.Label(root, text="Flight List").grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    flight_list = tk.Listbox(root, width=50, height=5)
    flight_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    tk.Label(root, text="Passenger List").grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    passenger_list = tk.Listbox(root, width=50, height=5)
    passenger_list.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()