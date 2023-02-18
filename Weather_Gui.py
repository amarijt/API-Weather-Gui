import tkinter as tk
import requests
import time
from tkinter import messagebox, Toplevel, Label
from tkinter import *
from PIL import Image, ImageTk

#Function that uses the city from the city_entry as a parameter to get the temperature
def get_weather(city):
    api_key = "d2a4a6ae82bc2f30306b9c9c27f17b5a"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    #using json to grab the temperature from the api (in celsius) and converting it to fahrenheit to display 
    temp_celsius = data["main"]["temp"]
    temp_fahrenheit = (temp_celsius * 9/5) + 32
    return f"{temp_fahrenheit:.1f}°F ({temp_celsius:.1f}°C)."

#Function that uses the city from the city_entry as a parameter to get the weather condition(clear, rain, etc.)
def get_weather_condition(city):
    api_key = "d2a4a6ae82bc2f30306b9c9c27f17b5a"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    weather_conditions = data["weather"][0]["main"]
    return weather_conditions

#Function that uses the city from the city_entry as a parameter to get the time of day so that we can display a picture if its day or night
def get_timeofday(city):
    api_key = "d2a4a6ae82bc2f30306b9c9c27f17b5a"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    sunrise_timestamp = data["sys"]["sunrise"]
    sunset_timestamp = data["sys"]["sunset"]

    # Convert the Unix timestamps to datetime objects in the local timezone
    sunrise_datetime = time.localtime(sunrise_timestamp)
    sunset_datetime = time.localtime(sunset_timestamp)

    # Get the current time in the local timezone
    current_datetime = time.localtime()

    # Determine if it's currently daytime based on the current time and the sunrise/sunset times
    if sunrise_datetime <= current_datetime < sunset_datetime:
        return True
    else:
        return False

#Function to clear the user input
def reset():
    city_entry.delete(0, tk.END)

# Function to handle button click event
def get_city_weather():
    #Grabs the user data from the entry
    city = city_entry.get()
    #Exception handling to manage the user input
    try:
        #Create variables calling the function and inserting the user input into the functions
        result = get_weather(city)
        weather_condition= get_weather_condition(city)
        timeofday = get_timeofday(city)
        #Creating messages to relay the results
        message1 = f"The current temperature in {city} is {result}"
        message2 = f"The current weather condition is {weather_condition}."
        
        # Create a new Toplevel window for the custom dialog
        dialog = Toplevel(window)
        dialog.title("Weather Info")

        #Using if statements to declare whcih image the image_file variable will represent
        if weather_condition == "Snow":
            image_file = r"C:\Users\amari\Downloads\SnowCloud.png.png"
        elif weather_condition == "Clouds":
            image_file = r"C:\Users\amari\Downloads\PartlyCloudy.png.png"
        elif weather_condition == "Rain":
            image_file = r"C:\Users\amari\Downloads\RainyCloud.png.png"
        elif weather_condition == "Windy":
            image_file = r"C:\Users\amari\Downloads\Windy.png.png"
        else:
            #nested if-else statement to display day or night if the weather is clear
            if timeofday == True:
                image_file = r"C:\Users\amari\Downloads\Sunny.png.png"
            else:
                image_file = r"C:\Users\amari\Downloads\Night.png"

        #Displaying the Image 
        image = Image.open(image_file)
        photo = ImageTk.PhotoImage(image)
        image_label = Label(dialog, image=photo)
        image_label.image = photo
        image_label.pack()
        

        # Display the weather information in the dialog
        message_label1 = Label(dialog, text=message1)
        message_label1.pack()

        message_label2 = Label(dialog, text=message2)
        message_label2.pack()

        #Nested function to close the toplevel as well as clear the user input
        def toplevelclose():
            dialog.destroy()
            city_entry.delete(0, tk.END)
            
        #OK button to close the toplevel as well as clear the user entry
        ok_button = tk.Button(dialog, text="OK", command=toplevelclose)
        ok_button.pack()
        
        #Center the dialog on the screen
        dialog.update_idletasks()
        w = dialog.winfo_screenwidth()
        h = dialog.winfo_screenheight()
        size = tuple(int(_) for _ in dialog.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        dialog.geometry("%dx%d+%d+%d" % (size + (x, y)))

        #Make the dialog modal to prevent interactions with the main window
        dialog.transient(window)
        dialog.grab_set()

    #Throw an exception if invalid entry 
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "An error occurred. Try again :).")

    
#Create the tkinter window
window = tk.Tk()
window.title("Weather App")

buttonframe = Frame(window)

#Center the window 
width = 300
height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

#Set the window position and size
window.geometry(f"{width}x{height}+{x}+{y}")


#Create the city input label and entry field
city_label = tk.Label(window, text="Enter a city:")
city_label.pack()
city_entry = tk.Entry(window)
city_entry.pack()

#Set the colors 
window['bg']='light blue'
buttonframe['bg'] = 'light blue'

#Set the font and size of label
city_label.config(font=('Helvetica', 15), bg= 'light blue',  )

#Creating buttons on the main window to reset the entry, find the weather or close the gui
reset_button = tk.Button(buttonframe, text="Reset", command = reset, width=10, height=1)
reset_button.pack(side = LEFT, padx=10, pady=10 )

get_weather_button = tk.Button(buttonframe, text="Get Weather", command=get_city_weather, width=10, height=1)
get_weather_button.pack(side = LEFT, padx=10, pady=10)

exit_button = tk.Button(buttonframe, text="Exit", command = window.destroy, width=10, height=1)
exit_button.pack(side = RIGHT, padx=10, pady=10)
buttonframe.pack()

# Start the tkinter event loop
window.mainloop()

