from datetime import datetime
from io import BytesIO
import time
from PIL import Image, ImageTk
import requests
import tkinter as tk
from config import API_KEY

current_units = "metric"
last_query = "Damascus"
icon_image = None


def get_icon(icon_code):
  global icon_image
  try:
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(icon_url, timeout=5)
    if response.status_code == 200:
      img_data = BytesIO(response.content)
      img = Image.open(img_data)
      icon_image = ImageTk.PhotoImage(img)
      return icon_image
  except Exception:
    pass
  return None


def get_weather_emoji(condition):
  cond = condition.lower()
  if "clear" in cond:
    return "☀️"
  elif "cloud" in cond:
    return "☁️"
  elif "rain" in cond or "drizzle" in cond:
    return "🌧️"
  elif "thunder" in cond:
    return "⛈️"
  elif "snow" in cond:
    return "❄️"
  elif "mist" in cond or "fog" in cond or "haze" in cond:
    return "🌫️"
  else:
    return "🌤️"


def fetch_weather(query=None):
  global last_query
  if not query:
    query = city_entry.get().strip()

  if not query:
    show_error("Please enter a city name or ZIP code!")
    return

  last_query = query
  error_label.config(text="")

  current_url = "http://api.openweathermap.org/data/2.5/weather"
  params = {"q": query, "appid": API_KEY, "units": current_units}

  try:
    res = requests.get(current_url, params=params, timeout=10)
    if res.status_code == 404:
      show_error("City or ZIP code not found!")
      return
    elif res.status_code == 401:
      show_error("Invalid API Key ")
      return
    elif res.status_code != 200:
      show_error(f"Error: Status code {res.status_code}")
      return

    data = res.json()
    city = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"]
    wind = data["wind"]["speed"]
    icon_code = data["weather"][0]["icon"]

    unit_symbol = "°C" if current_units == "metric" else "°F"
    speed_symbol = "m/s" if current_units == "metric" else "mph"

    city_title_label.config(text=city)
    temp_label.config(text=f"{temp:.1f}{unit_symbol}")
    desc_label.config(text=desc.capitalize())
    humidity_val.config(text=f"{humidity}%")
    wind_val.config(text=f"{wind} {speed_symbol}")

    img = get_icon(icon_code)
    if img:
      icon_label.config(image=img)
    else:
      icon_label.config(image="")

    fetch_forecast(query)

  except requests.exceptions.Timeout:
    show_error("Request timed out. Check connection.")
  except requests.exceptions.ConnectionError:
    show_error("Network connection error.")
  except Exception as e:
    show_error(f"Unexpected error: {e}")


def fetch_forecast(query):
  forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
  params = {"q": query, "appid": API_KEY, "units": current_units}

  try:
    res = requests.get(forecast_url, params=params, timeout=10)
    if res.status_code == 200:
      forecast_data = res.json()
      list_items = forecast_data.get("list", [])
      current_timestamp = time.time()

      # تفريغ الجدول القديم للساعات
      for widget in hourly_items_frame.winfo_children():
        widget.destroy()

      hourly_count = 0
      for item in list_items:
        if item["dt"] >= current_timestamp:
          time_str = datetime.fromtimestamp(item["dt"]).strftime("%H:%M")
          t = item["main"]["temp"]
          d = item["weather"][0]["main"]
          emoji = get_weather_emoji(d)
          unit_sym = "°C" if current_units == "metric" else "°F"

          row_frame = tk.Frame(hourly_items_frame, bg="#1e293b")
          row_frame.pack(fill=tk.X, pady=4)

          tk.Label(
              row_frame,
              text=f"🕒  {time_str}",
              font=("Consolas", 11, "bold"),
              bg="#1e293b",
              fg="#38bdf8",
              width=15,
              anchor="w",
          ).pack(side=tk.LEFT, padx=15)
          tk.Label(
              row_frame,
              text=f"{t:.1f} {unit_sym}",
              font=("Consolas", 11, "bold"),
              bg="#1e293b",
              fg="white",
              width=15,
              anchor="w",
          ).pack(side=tk.LEFT, padx=15)
          tk.Label(
              row_frame,
              text=f"{emoji}   {d}",
              font=("Segoe UI", 11),
              bg="#1e293b",
              fg="#94a3b8",
              anchor="w",
          ).pack(side=tk.LEFT, padx=15)

          hourly_count += 1
          if hourly_count >= 3:
            break

      # تفريغ الجدول القديم للأيام
      for widget in daily_items_frame.winfo_children():
        widget.destroy()

      for i in range(0, min(40, len(list_items)), 8):
        item = list_items[i]
        date_str = item["dt_txt"].split(" ")[0]
        day_name = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
        t = item["main"]["temp"]
        d = item["weather"][0]["main"]
        emoji = get_weather_emoji(d)
        unit_sym = "°C" if current_units == "metric" else "°F"

        row_frame = tk.Frame(daily_items_frame, bg="#1e293b")
        row_frame.pack(fill=tk.X, pady=4)

        tk.Label(
            row_frame,
            text=f"📅  {day_name}",
            font=("Consolas", 11, "bold"),
            bg="#1e293b",
            fg="#38bdf8",
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT, padx=15)
        tk.Label(
            row_frame,
            text=f"{t:.1f} {unit_sym}",
            font=("Consolas", 11, "bold"),
            bg="#1e293b",
            fg="white",
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT, padx=15)
        tk.Label(
            row_frame,
            text=f"{emoji}   {d}",
            font=("Segoe UI", 11),
            bg="#1e293b",
            fg="#94a3b8",
            anchor="w",
        ).pack(side=tk.LEFT, padx=15)

  except Exception:
    pass


def auto_detect_location():
  try:
    res = requests.get("https://ipinfo.io/json", timeout=5)
    if res.status_code == 200:
      ip_data = res.json()
      city = ip_data.get("city")
      if city:
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)
        fetch_weather(city)
        return
  except Exception:
    pass
  fetch_weather("Damascus")


def toggle_units():
  global current_units
  if current_units == "metric":
    current_units = "imperial"
    unit_btn.config(text="Switch to °C")
  else:
    current_units = "metric"
    unit_btn.config(text="Switch to °F")
  fetch_weather(last_query)


def show_error(message):
  error_label.config(text=message)
  city_title_label.config(text="---")
  temp_label.config(text="--")
  desc_label.config(text="No data")
  humidity_val.config(text="--%")
  wind_val.config(text="--")
  for widget in hourly_items_frame.winfo_children():
    widget.destroy()
  for widget in daily_items_frame.winfo_children():
    widget.destroy()
  icon_label.config(image="")


# ==================== بناء واجهة اللابتوب مع سكرول ناعم وسلس ====================
root = tk.Tk()
root.title("Weather App - Advanced")
root.geometry("1000x800")
root.config(bg="#0f172a")
root.resizable(True, True)
root.state("zoomed")

main_container = tk.Frame(root, bg="#0f172a")
main_container.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(
    main_container, bg="#0f172a", highlightthickness=0, yscrollincrement=6
)
scrollbar = tk.Scrollbar(
    main_container, orient="vertical", command=canvas.yview
)
scrollable_frame = tk.Frame(canvas, bg="#0f172a")


def on_frame_configure(event):
  canvas.configure(scrollregion=canvas.bbox("all"))


scrollable_frame.bind("<Configure>", on_frame_configure)

canvas_window = canvas.create_window(
    (0, 0), window=scrollable_frame, anchor="nw"
)


def on_canvas_configure(event):
  canvas.itemconfig(canvas_window, width=event.width)


canvas.bind("<Configure>", on_canvas_configure)
canvas.configure(yscrollcommand=scrollbar.set)


def _on_mousewheel(event):
  canvas.yview_scroll(int(-1 * (event.delta / 30)), "units")


canvas.bind_all("<MouseWheel>", _on_mousewheel)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# --- محتويات التطبيق ---

header_frame = tk.Frame(scrollable_frame, bg="#0f172a")
header_frame.pack(pady=(20, 10), fill=tk.X, padx=50)

tk.Label(
    header_frame,
    text="Weather App",
    font=("Segoe UI", 22, "bold"),
    bg="#0f172a",
    fg="#38bdf8",
).pack(side=tk.LEFT)

unit_btn = tk.Button(
    header_frame,
    text="Switch to °F",
    font=("Segoe UI", 11, "bold"),
    bg="#334155",
    fg="white",
    bd=0,
    padx=16,
    pady=8,
    cursor="hand2",
    command=toggle_units,
)
unit_btn.pack(side=tk.RIGHT)

search_frame = tk.Frame(scrollable_frame, bg="#1e293b", bd=0)
search_frame.pack(pady=10, padx=50, fill=tk.X)

city_entry = tk.Entry(
    search_frame,
    font=("Segoe UI", 14),
    bg="#1e293b",
    fg="white",
    bd=0,
    insertbackground="white",
    justify="center",
)
city_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, ipady=10)

search_btn = tk.Button(
    search_frame,
    text="🔍",
    font=("Segoe UI", 14),
    bg="#3b82f6",
    fg="white",
    bd=0,
    cursor="hand2",
    command=lambda: fetch_weather(),
)
search_btn.pack(side=tk.RIGHT, ipadx=18, ipady=6)

error_label = tk.Label(
    scrollable_frame, text="", font=("Segoe UI", 11), bg="#0f172a", fg="#ef4444"
)
error_label.pack(pady=3)

# لوحة الطقس الحالي
current_card = tk.Frame(scrollable_frame, bg="#1e293b")
current_card.pack(pady=8, padx=50, fill=tk.X)

top_card_frame = tk.Frame(current_card, bg="#1e293b")
top_card_frame.pack(fill=tk.X, padx=25, pady=(20, 10))

city_title_label = tk.Label(
    top_card_frame,
    text="Loading...",
    font=("Segoe UI", 26, "bold"),
    bg="#1e293b",
    fg="#f8fafc",
)
city_title_label.pack(side=tk.LEFT)

# تم تعديل مكان الأيقونة هنا وإنزالها قليلاً نحو الأسفل عبر pady=(12, 0)
icon_label = tk.Label(top_card_frame, bg="#1e293b")
icon_label.pack(side=tk.RIGHT, pady=(12, 0))

mid_card_frame = tk.Frame(current_card, bg="#1e293b")
mid_card_frame.pack(fill=tk.X, padx=25, pady=8)

temp_label = tk.Label(
    mid_card_frame,
    text="--",
    font=("Segoe UI", 42, "bold"),
    bg="#1e293b",
    fg="#38bdf8",
)
temp_label.pack(side=tk.LEFT)

desc_label = tk.Label(
    mid_card_frame,
    text="--",
    font=("Segoe UI", 14),
    bg="#1e293b",
    fg="#94a3b8",
)
desc_label.pack(side=tk.RIGHT, anchor="s", pady=8)

details_frame = tk.Frame(current_card, bg="#1e293b")
details_frame.pack(fill=tk.X, padx=25, pady=(15, 20))

hum_box = tk.Frame(details_frame, bg="#1e293b")
hum_box.pack(side=tk.LEFT, expand=True)
tk.Label(
    hum_box, text="💧 Humidity", font=("Segoe UI", 11), bg="#1e293b", fg="#94a3b8"
).pack()
humidity_val = tk.Label(
    hum_box, text="--%", font=("Segoe UI", 12, "bold"), bg="#1e293b", fg="white"
)
humidity_val.pack()

wind_box = tk.Frame(details_frame, bg="#1e293b")
wind_box.pack(side=tk.RIGHT, expand=True)
tk.Label(
    wind_box,
    text="💨 Wind Speed",
    font=("Segoe UI", 11),
    bg="#1e293b",
    fg="#94a3b8",
).pack()
wind_val = tk.Label(
    wind_box, text="--", font=("Segoe UI", 12, "bold"), bg="#1e293b", fg="white"
)
wind_val.pack()

# --- جدول توقعات الساعات ---
hourly_card = tk.Frame(scrollable_frame, bg="#1e293b")
hourly_card.pack(pady=10, padx=50, fill=tk.X)

tk.Label(
    hourly_card,
    text="Hourly Forecast (Next Hours)",
    font=("Segoe UI", 12, "bold"),
    bg="#1e293b",
    fg="#38bdf8",
).pack(anchor="w", padx=25, pady=(15, 8))

hourly_items_frame = tk.Frame(hourly_card, bg="#1e293b")
hourly_items_frame.pack(fill=tk.X, padx=25, pady=(0, 20))

# --- جدول توقعات الـ 5 أيام ---
daily_card = tk.Frame(scrollable_frame, bg="#1e293b")
daily_card.pack(pady=10, padx=50, fill=tk.X)

tk.Label(
    daily_card,
    text="5-Day Forecast",
    font=("Segoe UI", 12, "bold"),
    bg="#1e293b",
    fg="#38bdf8",
).pack(anchor="w", padx=25, pady=(15, 8))

daily_items_frame = tk.Frame(daily_card, bg="#1e293b")
daily_items_frame.pack(fill=tk.X, padx=25, pady=(0, 20))

tk.Label(scrollable_frame, text="", bg="#0f172a", height=3).pack()

root.after(100, auto_detect_location)
root.mainloop()