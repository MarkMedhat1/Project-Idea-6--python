from tkinter import *
from tkinter import messagebox
import webbrowser
import time

def calculate_bmi():
    weight = float(weight_entry.get())
    height_cm = float(height_entry.get())
    height_m = height_cm / 100
    bmi = weight / (height_m * height_m)

    if bmi <= 18.4:
        result_label.config(text="Underweight")
        messagebox.showinfo("BMI Result", "Your BMI is: {:.2f}\nYou are Underweight".format(bmi))
    elif 18.5 <= bmi <= 24.9:
        result_label.config(text="Normal")
        messagebox.showinfo("BMI Result", "Your BMI is: {:.2f}\nYou are Normal")
    elif 25 <= bmi <= 29.9:
        result_label.config(text="Overweight")
        messagebox.showinfo("BMI Result", "Your BMI is: {:.2f}\nYou are Overweight")
    else:
        result_label.config(text="Obese")
        messagebox.showinfo("BMI Result", "Your BMI is: {:.2f}\nYou are Obese")

def update_time():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text="Current Time: " + current_time)
    window.after(1000, update_time)  # Update time every 1 second (1000 ms)

def open_instagram_profile():
    url = "https://instagram.com/abdelrahman_1607?igshid=YTQwZjQ0NmI0OA%3D%3D&utm_source=qr"
    webbrowser.open(url)

window = Tk()
window.title("BMI Calculator")
window.geometry("400x250")

weight_label = Label(window, text="Enter Weight (kg):")
weight_label.pack()
weight_entry = Entry(window)
weight_entry.pack()

height_label = Label(window, text="Enter Height (cm):")
height_label.pack()
height_entry = Entry(window)
height_entry.pack()

calculate_button = Button(window, text="Calculate BMI", command=calculate_bmi)
calculate_button.pack()

result_label = Label(window, text="")
result_label.pack()

time_label = Label(window, text="Current Time: ")
time_label.pack()

instagram_button = Button(window, text="DM for online training", command=open_instagram_profile)
instagram_button.pack()

update_time()  # Start the live time display

window.mainloop()
