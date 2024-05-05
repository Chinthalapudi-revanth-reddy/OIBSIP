import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime

class BMIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")
        self.master.geometry("400x400")

        self.weight_label = tk.Label(master, text="Weight (kg):")
        self.weight_label.pack()

        self.weight_entry = tk.Entry(master)
        self.weight_entry.pack()

        self.height_label = tk.Label(master, text="Height (m):")
        self.height_label.pack()

        self.height_entry = tk.Entry(master)
        self.height_entry.pack()

        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.save_button = tk.Button(master, text="Save Data", command=self.save_data)
        self.save_button.pack()

        self.view_history_button = tk.Button(master, text="View History", command=self.view_history)
        self.view_history_button.pack()

        self.plot_button = tk.Button(master, text="Plot BMI Trend", command=self.plot_bmi_trend)
        self.plot_button.pack()

        # Load existing data
        try:
            with open("bmi_data.json", "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Invalid input. Please enter positive values for weight and height.")
                return

            bmi = weight / (height ** 2)
            category = self.classify_bmi(bmi)

            result_text = f"\nYour BMI is: {bmi:.2f}\nCategory: {category}"
            self.result_label.config(text=result_text)

            # Save data
            self.data.append({"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "bmi": bmi})

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values for weight and height.")

    def classify_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def save_data(self):
        with open("bmi_data.json", "w") as file:
            json.dump(self.data, file)
        messagebox.showinfo("Data Saved", "BMI data saved successfully.")

    def view_history(self):
        history_window = tk.Toplevel(self.master)     #new window
        history_window.title("BMI History")

        history_text = tk.Text(history_window)       #to display BMI history entries
        history_text.pack()

        for entry in self.data:
            history_text.insert(tk.END, f"Date: {entry['date']}, BMI: {entry['bmi']:.2f}\n\n")

        history_text.config(state=tk.DISABLED)      #cannot edit BMI values

    def plot_bmi_trend(self):
        # Check if there are at least two entries to plot a trend
        if len(self.data) < 2:
            messagebox.showinfo("Not Enough Data", "Insufficient data to plot BMI trend.")
            return

        # Extract dates and BMI values from the data
        dates = [entry["date"] for entry in self.data]
        bmis = [entry["bmi"] for entry in self.data]

        # Create a new figure and axes for plotting
        fig, ax = plt.subplots()

        # Plot BMI trend over time with circular markers
        ax.plot(dates, bmis, marker='o')

        # Set labels for x-axis, y-axis, and the title of the plot
        ax.set_xlabel('Date')
        ax.set_ylabel('BMI')
        ax.set_title('BMI Trend Over Time')

        # Create a new window to display the BMI trend plot
        plot_window = tk.Toplevel(self.master)
        plot_window.title("BMI Trend") 

        # Create a Tkinter canvas for displaying the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()

        canvas.get_tk_widget().pack()

        # Create a frame for potential toolbar options
        toolbar = tk.Frame(plot_window)
        # Pack the frame at the bottom of the window
        toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar.update()

        # Pack the canvas at the top of the window
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Pack the Tkinter canvas to make it visible
        canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



if __name__ == "__main__":
    # Create a Tkinter root window
    root = tk.Tk()
    app = BMIApp(root)
    # Start the Tkinter main event loop, allowing the GUI to run
    root.mainloop()
