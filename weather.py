import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
from cryptography.fernet import Fernet
from customtkinter import *
from tkinter.simpledialog import askstring

# Function to load the encryption key or create one if it doesn't exist
def load_or_create_key():
    key_file = 'key.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as file:
            file.write(key)
    return key

# Function to encrypt the API key
def encrypt_api_key(api_key, key):
    cipher_suite = Fernet(key)
    encrypted_key = cipher_suite.encrypt(api_key.encode())
    with open(".apikey", "wb") as file:
        file.write(encrypted_key)

# Function to decrypt the API key
def decrypt_api_key(key):
    try:
        with open(".apikey", "rb") as file:
            encrypted_key = file.read()
        cipher_suite = Fernet(key)
        api_key = cipher_suite.decrypt(encrypted_key).decode()
        return api_key
    except Exception as e:
        return None

# Function to get the weather information
def get_weather(event=None):
    city = city_entry.get()
    api_key = decrypt_api_key(encryption_key)

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

# Function to save the API key and clear the entry
def save_api_key(event=None):
    api_key = api_key_entry.get()
    if api_key:
        encrypt_api_key(api_key, encryption_key)
        api_key_entry.delete(0, tk.END)
        messagebox.showinfo("API Key Saved", "Your API key has been saved.")

# Create the main window
root = CTk()
root.title("Weather App")

# Set the style
set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Define the font
font = ("Helvetica", 16)

# Create and place the API key entry widget
api_key_label = CTkLabel(root, text="Enter API Key:", font=font)
api_key_label.pack(pady=5)

api_key_entry = CTkEntry(root, font=font)
api_key_entry.pack(pady=5)
api_key_entry.bind("<Return>", save_api_key)

# Create and place the city entry widget
city_label = CTkLabel(root, text="Enter city:", font=font)
city_label.pack(pady=5)

city_entry = CTkEntry(root, font=font)
city_entry.pack(pady=5)
city_entry.bind("<Return>", get_weather)

# Create and place the "Get Weather" button
get_weather_button = CTkButton(root, text="Get Weather", command=get_weather, font=font)
get_weather_button.pack(pady=5)

# Create and place the result label
result_label = CTkLabel(root, text="", wraplength=300, font=font)
result_label.pack(pady=10)

# Add some padding to all widgets
for widget in root.winfo_children():
    widget.pack_configure(padx=10, pady=5)

# Set minimum window size
root.minsize(400, 300)

# Add icon to the application
root.iconbitmap("../images/logo-black.ico")

# Load or create encryption key
encryption_key = load_or_create_key()

# Start the main event loop
root.mainloop()
