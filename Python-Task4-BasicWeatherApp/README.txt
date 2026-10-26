# Weather App - Advanced Python GUI

An advanced weather application built in Python, providing a modern graphical user interface with hourly and daily forecasts, and automatic location detection.

## 🛠️ Technologies Used
* **Python**
* **OpenWeatherMap API** (for fetching current weather and forecasts)
* **ipinfo.io API** (for automatic location detection via IP)
* **Tkinter & Pillow (PIL)** (used to build the advanced GUI and display icons)
* **Requests** (for handling HTTP requests)

---

## ✨ Features

* **Flexible Search:** Manually enter a city name or ZIP code to search for weather.
* **Current Weather:** Detailed display including current temperature, humidity percentage, wind speed, and weather condition description.
* **Weather Icons:** Fetch and display real weather icons corresponding to the current condition.
* **Hourly Forecast Table:** organized display of upcoming hourly weather forecasts accompanied by expressive emojis.
* **5-Day Forecast Table:** Structured table showing weather predictions for the next 5 days with day names and conditions.
* **Unit Toggle (°C / °F):** Dedicated button to instantly switch between metric and imperial measurement systems and update all data automatically.
* **Automatic Location Detection (Bonus):** Automatically detects the user's location upon startup using IP via the `ipinfo.io` service.
* **GUI Error Handling:** Gracefully handles errors (such as leaving the search field empty, city not found, invalid API key, or network disconnection) and displays messages exclusively within the graphical interface.