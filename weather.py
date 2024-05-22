import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
from dotenv import load_dotenv
from customtkinter import *
from tkinter.simpledialog import askstring

# Load environment variables from .env file
load_dotenv()

def get_weather():
    city = city_entry.get()
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')

    if not api_key:
        messagebox.showerror("API Key Missing", "Please enter your OpenWeatherMap API key.")
        return

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        temperature_celsius = temperature - 273.15

        result = f"The weather in {city} is currently {weather} with a temperature of {temperature_celsius:.1f}°C."
        result_label.configure(text=result)
    except requests.exceptions.HTTPError as errh:
        messagebox.showerror("HTTP Error", f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        messagebox.showerror("Connection Error", f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        messagebox.showerror("Timeout Error", f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Error", f"An error occurred: {err}")

def save_api_key():
    api_key = askstring("API Key", "Enter your OpenWeatherMap API key:")
    if api_key:
        with open(".env", "w") as env_file:
            env_file.write(f"OPENWEATHERMAP_API_KEY={api_key}")
        load_dotenv()  # Reload the .env file to update the API key in the environment
        messagebox.showinfo("API Key Saved", "Your API key has been saved.")

# Create the main window
root = CTk()
root.title("Weather App")

# Set the style
set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Create and place the city entry widget
city_label = CTkLabel(root, text="Enter city:")
city_label.pack(pady=5)

city_entry = CTkEntry(root)
city_entry.pack(pady=5)

# Create and place the "Get Weather" button
get_weather_button = CTkButton(root, text="Get Weather", command=get_weather)
get_weather_button.pack(pady=5)

# Create and place the result label
result_label = CTkLabel(root, text="", wraplength=300)
result_label.pack(pady=10)

# Create and place the "Save API Key" button
save_api_key_button = CTkButton(root, text="Save API Key", command=save_api_key)
save_api_key_button.pack(pady=5)

# Add some padding to all widgets
for widget in root.winfo_children():
    widget.pack_configure(padx=10, pady=5)

# Set minimum window size
root.minsize(400, 200)

# Add icon to the application
root.iconbitmap("images/logo-black.png")

# Start the main event loop
root.mainloop()
