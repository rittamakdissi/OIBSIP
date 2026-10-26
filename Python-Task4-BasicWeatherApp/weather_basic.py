import requests
from config import API_KEY


BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city_or_zip):
  params = {"q": city_or_zip, "appid": API_KEY, "units": "metric"}

  try:
    response = requests.get(BASE_URL, params=params, timeout=10)

    if response.status_code == 200:
      data = response.json()

      city = data["name"]
      temp_c = data["main"]["temp"]
      temp_f = (temp_c * 9 / 5) + 32
      humidity = data["main"]["humidity"]
      description = data["weather"][0]["description"]
      wind_speed = data["wind"]["speed"]

      print(f"\n   Weather in {city}")
      print(f"Temperature: {temp_c:.1f}°C ({temp_f:.1f}°F)")
      print(f"Condition: {description.capitalize()}")
      print(f"Humidity: {humidity}%")
      print(f"Wind Speed: {wind_speed} m/s\n")

    elif response.status_code == 404:
      print(
          "\n City or ZIP code not found."
      )
    elif response.status_code == 401:
      print("\nInvalid API Key.")
    else:
      print(
          f"\n An unexpected error occurred (Status code:"
          f" {response.status_code})"
      )

  except requests.exceptions.Timeout:
    print("\n Request timed out. Please check your internet connection.")
  except requests.exceptions.ConnectionError:
    print("\n Request failed due to a network connection error.")
  except Exception as e:
    print(f"\n[Unexpected Error]: {e}")


def main():
  print("Weather App")

  while True:
    user_input = input(
        "Enter city name or ZIP code :"
    ).strip()

    if not user_input:
      print("Please enter a valid city name or ZIP code.")
      continue

    get_weather(user_input)


if __name__ == "__main__":
  main()