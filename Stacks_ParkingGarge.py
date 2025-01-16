import customtkinter as ctk
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from datetime import datetime
import pytz

# Set Philippine timezone (PHT)
PH_TIMEZONE = pytz.timezone('Asia/Manila')

class PupCeaParkingGarage:
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self.garage = []  # Stack to store cars in the parking garage (LIFO)
        self.car_counts = {}  # Dictionary to track car arrival and departure counts
        self.history = []  # History of parking events

    def car_park(self, car):
        if len(self.garage) < self.max_capacity:
            if car in self.garage:
                return f"Car {car} is already parked."
            self.garage.append(car)  # Add car to the top of the stack
            self.car_counts[car] = self.car_counts.get(car, [0, 0])  # Initialize count if not present
            self.car_counts[car][0] += 1  # Increment arrival count
            self.history.append((car, "Arrival", len(self.garage), datetime.now(PH_TIMEZONE).strftime("%B %d, %Y %I:%M %p")))
            return f"Car {car} parked successfully."
        else:
            return "Garage is full."

    def remove_car(self, car):
        if car not in self.garage:
            return f"Car {car} is not in the garage."

        # Temporarily remove cars above the desired car (if not on top)
        temp_stack = []
        while self.garage and self.garage[-1] != car:
            temp_stack.append(self.garage.pop())

        # Remove the desired car (top of the stack)
        if self.garage and self.garage[-1] == car:
            self.garage.pop()
            self.car_counts[car][1] += 1  # Increment departure count
            self.history.append((car, "Departure", len(self.garage) + 1, datetime.now(PH_TIMEZONE).strftime("%B %d, %Y %I:%M %p")))
        else:
            return f"Car {car} not found in the garage."

        # Re-park the temporarily removed cars (stack them back)
        while temp_stack:
            self.garage.append(temp_stack.pop())

        return f"Car {car} removed successfully."

    def view_garage(self):
        return self.garage if self.garage else []

    def get_car_info(self, car):
        if car not in self.car_counts:
            return f"No record for car {car}."
        arrivals, departures = self.car_counts[car]
        return f"Car {car} - Arrivals: {arrivals}, Departures: {departures}"

    def get_parking_history(self):
        return self.history

class ParkingApp:
    def __init__(self, win, garage):
        self.win = win
        self.garage = garage
        self.car_slots = []  # Keep track of car images and plate numbers in canvas
        self.car_photos = []  # List to store 10 car images

        self.win.title("PUP-CEA Parking Garage")
        self.win.geometry("1390x700")
        self.win.resizable(False,False)

        # Main Frame
        main_frame2 = ctk.CTkFrame(win, width=1400, height=700)
        main_frame2.pack(expand=True, fill="both", padx=0, pady=0)
         # Add an image
        image_path = "main_frame2.png"  # Replace with the path to your image
        try:
                image = Image.open(image_path)
                image = image.resize((1750, 900), Image.Resampling.LANCZOS)  # Resize the image
                photo = ImageTk.PhotoImage(image)
                image_label = ctk.CTkLabel(main_frame2, image=photo, text="")  # Use image in a label
                image_label.pack(pady=20)
        except FileNotFoundError:
                print("Image file not found. Please check the path.")

        # Entry Frame
        entry_frame = ctk.CTkFrame(main_frame2, height=500, width=520, border_color="#fffff0", border_width=7, fg_color="#fadadd",corner_radius=5)
        entry_frame.place(relx=0.3, rely=0.5, anchor="center")

        # Canvas for garage display
        self.canvas = tk.Canvas(main_frame2, width=620, height=600, bg="#fadadd", bd=8, highlightthickness=6, highlightcolor="#fffff0")
        self.canvas.place(relx=0.7, rely=0.5, anchor="center")

        # font
        custom_font1 = ctk.CTkFont(family="Tahoma", size=20, weight="bold")
        custom_font2 = ctk.CTkFont(family = "Verdana", size = 15, weight= "normal", slant="roman")
        custom_font3 = ctk.CTkFont(family = "Verdana", size = 19, weight = "normal", slant = "roman")
        custom_font4 = ctk.CTkFont(family= "Poppins", size = 17, weight = "normal", slant= "roman")

        # Entry Fields
        plate_label = ctk.CTkLabel(entry_frame, text="Plate Number:", text_color="#333333", fg_color="#fadadd", font=custom_font1)
        plate_label.place(relx=0.2, rely=0.2, anchor="center")

        self.plate_num_entry = ctk.CTkEntry(entry_frame, width=280,height = 45,text_color="#333333",font= custom_font2, placeholder_text="Enter Plate Number",
                                            placeholder_text_color="#333333", fg_color="#ffafa4",
                                            border_color="black", border_width=2)
        self.plate_num_entry.place(relx=0.9, rely=0.2, anchor="e")

        # Buttons
        arrival_button = ctk.CTkButton(entry_frame, height = 50, width= 170,
                                       text="Arrival ", text_color="#333333", font=custom_font3,
                                       border_color="black",border_width=2, hover_color="#ffffff",fg_color="#ffafa4",
                                       command=self.arrival)
        arrival_button.place(relx=0.3, rely=0.4, anchor="center")

        departure_button = ctk.CTkButton(entry_frame, height = 50, width= 180,
                                         text="Departure ", text_color="#333333", font=custom_font3,
                                       border_color="black",border_width=2,hover_color="#ffffff",  fg_color="#ffafa4", command=self.departure)
        departure_button.place(relx=0.7, rely=0.4, anchor="center")

        view_parking_button = ctk.CTkButton(entry_frame, width = 390, height = 50, text = "View Parking History", text_color="#333333", font=custom_font3,
                                       border_color="black",border_width=2, fg_color="#ffafa4", hover_color= "#ffffff", command=self.view_parking_history)
        view_parking_button.place(relx = 0.5, rely = 0.9, anchor = "center")

        
        # Parking Status Label
        self.status_label = ctk.CTkLabel(entry_frame, text="", text_color="black", fg_color="#fadadd", font =custom_font4, justify = "center")
        self.status_label.place(relx=0.5, rely=0.6, anchor="center")

        # Car info below status
        self.car_info_label = ctk.CTkLabel(entry_frame, text="", text_color="black", fg_color="#fadadd", font =custom_font4,justify= "right" )
        self.car_info_label.place(relx=0.5, rely=0.8, anchor="center")

        # Load 10 Car Images
        self.load_car_images()

        # Draw parking garage layout
        self.draw_garage_layout()

    def load_car_images(self):
        """Load 10 different car images."""
        for i in range(1, 11):  # Load car1.png to car10.png
            try:
                car_image = Image.open(f"car{i}.png")  # Replace with your car image filenames
                car_image = car_image.resize((50, 30), Image.Resampling.LANCZOS)
                car_photo = ImageTk.PhotoImage(car_image)
                self.car_photos.append(car_photo)
            except FileNotFoundError:
                print(f"Image car{i}.png not found. Please check the path.")

    def draw_garage_layout(self):
        """Draw parking slots on the canvas with descending slots and add a centered header."""
        # Add a header to the canvas
        self.canvas.create_text(
            310, 30,  # Centered horizontally within the canvas (width 620)
            text="ENTRANCE/EXIT", 
            font=("Arial", 18, "bold"), 
            fill="black"
        )

        # Centered parking layout
        x_start = 160  # Adjusted X position for centering (canvas width 620)
        y_start = 600  # Slot 1 should be lower to prevent overlap
        row_height = 55  # Adjusted height to fit 10 rows
        row_width = 300

        for i in range(10):  # 10 rows for 10 slots
            # Calculate the Y coordinates for the current slot
            y_top = y_start - (i + 1) * row_height
            y_bottom = y_start - i * row_height

            # Skip the top border for Slot 10 (topmost slot)
            if i != 9:  # Draw the top border for all slots except Slot 10
                self.canvas.create_line(
                    x_start, y_top,  # Top border line
                    x_start + row_width, y_top,
                    fill="black", width=2
                )

            # Draw the left, right, and bottom borders for all slots
            self.canvas.create_line(
                x_start, y_top,  # Left side
                x_start, y_bottom,
                fill="black", width=2
            )
            self.canvas.create_line(
                x_start + row_width, y_top,  # Right side
                x_start + row_width, y_bottom,
                fill="black", width=2
            )
            self.canvas.create_line(
                x_start, y_bottom,  # Bottom border
                x_start + row_width, y_bottom,
                fill="black", width=2
            )

            # Add text for slot number (Slot 1 at the bottom and Slot 10 at the top)
            self.canvas.create_text(
                x_start + 20, y_bottom - row_height // 2,
                text=f"Slot {i + 1}", anchor="w", font=("Arial", 14), fill="black"
            )
            self.car_slots.append(None)  # Reserve space for car images and plate numbers





    def get_current_time(self):
        """Get the current date and time in Philippine Time Zone with 12-hour format."""
        current_time = datetime.now(PH_TIMEZONE)
        return current_time.strftime("%B %d, %Y %I:%M %p")  # Date and 12-hour format with AM/PM

    def arrival(self):
        plate_number = self.plate_num_entry.get()
        if not plate_number:
            self.show_error_window("Error", "Please enter a plate number.")
            return

        result = self.garage.car_park(plate_number)
        if result == "Garage is full.":
            self.show_error_window("Garage Full", f"The garage is full. No parking slots are available.")
            return

        if "already parked" in result:
            self.show_error_window("Duplicate Entry", f"Car {plate_number} is already parked.")
            return

        # Find the first available slot and add the car
        slot_index = len(self.garage.garage) - 1
        x_slot = 250
        y_slot = 600 - (slot_index + 1) * 55 + 25

        if slot_index < len(self.car_photos):
            car_image = self.canvas.create_image(x_slot, y_slot, image=self.car_photos[slot_index], anchor="w")
            plate_text = self.canvas.create_text(
                x_slot + 60, y_slot, text=plate_number, fill="black", font=("Verdana", 15, "bold"), anchor="w"
            )
            self.car_slots[slot_index] = (car_image, plate_text)

        current_time = self.get_current_time()
        arrivals, _ = self.garage.car_counts[plate_number]
        self.status_label.configure(
            text=f"Car parked successfully!\n"
                f"Plate Number: {plate_number}\n"
                f"Arrival Count: {arrivals}\n"
                f"Departure Count: {self.garage.car_counts[plate_number][1]}\n"
                f"Time and Date: {current_time}\n"
                f"Available Parking Slots: {self.garage.max_capacity - len(self.garage.garage)}"
        )
    def departure(self):
        car_plate = self.plate_num_entry.get()
        if not car_plate:
            self.show_error_window("Error", "Please enter a plate number.")
            return

        if car_plate not in self.garage.garage:
            self.show_error_window("Car Not Found", f"Car {car_plate} is not in the garage.")
            return

        result = self.garage.remove_car(car_plate)
        if "removed successfully" in result:
            self.refresh_canvas()

        current_time = self.get_current_time()
        arrivals, departures = self.garage.car_counts.get(car_plate, (0, 0))
        self.status_label.configure(
            text=f"Car departed successfully!\n"
                f"Plate Number: {car_plate}\n"
                f"Arrival Count: {arrivals}\n"
                f"Departure Count: {departures}\n"
                f"Time and Date: {current_time}\n"
                f"Available Parking Slots: {self.garage.max_capacity - len(self.garage.garage)}"
        )


    
    
    def show_error_window(self, title, message):
        # Create a Toplevel window
        error_window = ctk.CTkToplevel(self.win)
        error_window.title(title)
        error_window.geometry("400x200")
        error_window.resizable(False, False)

        # Set the window's background color
        error_window.configure(fg_color="#fadadd")  

        # Title Label
        title_label = ctk.CTkLabel(
            error_window,
            text=title,
            font=ctk.CTkFont(family="Tahoma", size=18, weight="bold"),
            text_color="#333333",  
        )
        title_label.pack(pady=(20, 10))  # Padding for spacing

        # Message Label
        message_label = ctk.CTkLabel(
            error_window,
            text=message,
            font=ctk.CTkFont(family="Verdana", size=14, weight="normal"),
            text_color="#333333",
            wraplength=360, 
            justify="center",
        )
        message_label.pack(pady=(0, 20))  

        # Close Button
        close_button = ctk.CTkButton(
            error_window,
            text="Close",
            font=ctk.CTkFont(family="Verdana", size=14),
            fg_color="#ffafa4",  
            text_color="#333333", hover_color="#ffffff",  
            command=error_window.destroy,  # Close the window
        )
        close_button.pack(pady=10)  # Spacing below the button

        # Ensure the window stays on top and blocks interaction with the main window
        error_window.lift()
        error_window.grab_set()


    

    def refresh_canvas(self):
        self.canvas.delete("all")  # Clear the canvas
        self.draw_garage_layout()  # Redraw the layout
        for i, car in enumerate(self.garage.view_garage()):
            x_slot = 250  # Aligned with slot center
            y_slot = 600 - (i + 1) * 55 + 25  # Centered in the slot vertically index
            if i < len(self.car_photos):  # Ensure there is a corresponding image
                car_image = self.canvas.create_image(x_slot, y_slot, image=self.car_photos[i], anchor="w")
                plate_text = self.canvas.create_text(
                    x_slot + 60, y_slot, text=car, fill="black", font=("Arial", 12), anchor="w"
                )
                self.car_slots[i] = (car_image, plate_text)

    def update_canvas(self, message):
        # Display message at the bottom of the canvas
        self.canvas.delete("message")
        self.canvas.create_text(270, 490, text=message, fill="red", font=("Arial", 12), tags="message")
    def view_parking_history(self):
        # Create a new window to show parking history
        history_window = ctk.CTkToplevel(self.win)
        history_window.title("Parking History")
        history_window.geometry("680x700")

        # Set the background color of the history window to black
        history_window.configure(bg="black")

        # Ensure the history window appears above the main frame
        history_window.lift()  # Bring the history window to the front
        history_window.grab_set()  # Prevent interaction with the main window
        history_window.focus_set()  # Set focus to the history window

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(history_window, bg="black")  # Set the canvas background to black
        scrollbar = tk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame within the canvas to hold all the widgets
        history_frame = ctk.CTkFrame(canvas, fg_color="black")  # Set the frame background color to black
        
        # Scrollable Frame Configuration
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=history_frame, anchor="nw")

        history_frame.bind(
            "<Configure>", 
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )  # Update the scroll region when the frame size changes

        history_label = ctk.CTkLabel(history_frame, text="Parking History", font=("Arial", 18, "bold"), text_color="white")
        history_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Column headers
        headers = ["PLATE NUMBER", "ARRIVAL/DEPARTURE", "PARKING SLOT #", "TIMESTAMP"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(history_frame, text=header, font=("Arial", 12, "bold"), text_color="white")
            header_label.grid(row=1, column=col, padx=10, pady=5)

        # Set column weights to ensure consistent column width
        for col in range(len(headers)):
            history_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        # Display history data
        for idx, (plate, event_type, slot, timestamp) in enumerate(self.garage.get_parking_history()):
            ctk.CTkLabel(history_frame, text=plate, font=("Arial", 12), text_color="white").grid(row=idx+2, column=0, padx=10, pady=5)
            ctk.CTkLabel(history_frame, text=event_type, font=("Arial", 12), text_color="white").grid(row=idx+2, column=1, padx=10, pady=5)
            ctk.CTkLabel(history_frame, text=slot, font=("Arial", 12), text_color="white").grid(row=idx+2, column=2, padx=10, pady=5)
            ctk.CTkLabel(history_frame, text=timestamp, font=("Arial", 12), text_color="white").grid(row=idx+2, column=3, padx=10, pady=5)


if __name__ == "__main__":
    # Initialize the garage with a maximum capacity of 10
    garage = PupCeaParkingGarage(max_capacity=10)
    root = ctk.CTk()
    app = ParkingApp(root, garage)
    root.mainloop()
