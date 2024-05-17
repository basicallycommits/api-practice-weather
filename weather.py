import tkinter as tk
from tkinter import ttk, messagebox
import requests

def get_weather():
    city = city_entry.get()
    api_key = 'd1d04105b9586d36eaa8c5c095925bb0'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        temperature_celsius = temperature - 273.15
        
        result = f"The weather in {city} is currently {weather} with a temperature of {temperature_celsius:.1f}°C."
        result_label.config(text=result)
    except requests.exceptions.HTTPError as errh:
        messagebox.showerror("HTTP Error", f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        messagebox.showerror("Connection Error", f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        messagebox.showerror("Timeout Error", f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Error", f"An error occurred: {err}")

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Set the style
style = ttk.Style()
style.theme_use('clam')  # You can choose 'clam', 'alt', 'default', 'classic'

# Create and place the city entry widget
city_label = ttk.Label(root, text="Enter city:")
city_label.pack(pady=5)

city_entry = ttk.Entry(root)
city_entry.pack(pady=5)

# Create and place the "Get Weather" button
get_weather_button = ttk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack(pady=5)

# Create and place the result label
result_label = ttk.Label(root, text="", wraplength=300)
result_label.pack(pady=10)

# Add some padding to all widgets
for widget in root.winfo_children():
    widget.pack_configure(padx=10, pady=5)

# Set minimum window size
root.minsize(400, 200)

# Start the main event loop
root.mainloop()
