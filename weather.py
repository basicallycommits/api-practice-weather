import requests

# Define the API endpoint and your API key
api_key = 'd1d04105b9586d36eaa8c5c095925bb0'
city = 'Auckland'
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

try:
    # Make the GET request to the API
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

    # Parse the JSON response
    data = response.json()

    # Extract and print relevant information
    weather = data['weather'][0]['description']
    temperature = data['main']['temp']
    print("The weather in {} is currently {} with a temperature of {:.1f}°C.".format(city, weather, temperature-273.15))

except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"An error occurred: {err}")
