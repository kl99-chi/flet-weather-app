"""Flet Weather App.

Search any city and see its current weather (temperature, conditions,
humidity and wind) using the OpenWeatherMap API.

Built as the capstone for the FNB App Academy 2026 (app development module).
"""

import os

import flet as ft
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
ICON_URL = "https://openweathermap.org/img/wn/{icon}@4x.png"
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather_data(city: str) -> dict:
    """Fetch current weather for `city`.

    Always returns a dictionary with a "success" key, so the UI never has to
    deal with raw exceptions:
      success -> {"success": True, "city", "temp", "description", "icon",
                  "humidity", "wind"}
      failure -> {"success": False, "error": "<message>"}
    """
    if not API_KEY:
        return {
            "success": False,
            "error": "Missing API key. Add OPENWEATHER_API_KEY to your .env file.",
        }

    try:
        response = requests.get(
            BASE_URL,
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10,
        )
        data = response.json()

        if response.status_code == 200:
            return {
                "success": True,
                "city": f"{data['name']}, {data['sys'].get('country', '')}",
                "temp": f"{round(data['main']['temp'])}°C",
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
                "humidity": f"{data['main']['humidity']}%",
                # The API returns wind in m/s; convert to km/h for South Africa.
                "wind": f"{round(data['wind']['speed'] * 3.6)} km/h",
            }

        if response.status_code == 404:
            return {"success": False, "error": "CITY NOT FOUND"}
        if response.status_code == 401:
            return {"success": False, "error": "Invalid API key."}
        return {"success": False, "error": data.get("message", "Something went wrong.")}

    except requests.exceptions.RequestException:
        return {"success": False, "error": "Network error. Please check your connection."}
    except (KeyError, ValueError):
        return {"success": False, "error": "Unexpected response from the weather service."}


def main(page: ft.Page):
    # ---- Page: a phone-sized dark canvas ----
    page.title = "Flet Weather App"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 420
    page.window.height = 650
    page.padding = 24
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---- Controls ----
    city_input = ft.TextField(
        label="Weather forecast",
        hint_text="e.g. Johannesburg",
        border_radius=12,
        expand=True,
    )
    search_button = ft.IconButton(
        icon=ft.Icons.SEARCH,
        icon_color=ft.Colors.BLUE_400,
        icon_size=28,
    )

    # ---- Display elements (empty until a search succeeds) ----
    city_display = ft.Text(size=24, weight=ft.FontWeight.W_600)
    weather_icon = ft.Image(src=ICON_URL.format(icon="01d"), width=120, height=120, visible=False)
    temperature_text = ft.Text(size=42, weight=ft.FontWeight.BOLD)
    description_text = ft.Text(size=16, color=ft.Colors.GREY_400)
    humidity_text = ft.Text(size=18, weight=ft.FontWeight.W_600)
    wind_text = ft.Text(size=18, weight=ft.FontWeight.W_600)
    error_text = ft.Text(color=ft.Colors.RED, visible=False)

    def stat(icon, label, value_control):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, color=ft.Colors.BLUE_400),
                    value_control,
                    ft.Text(label, size=12, color=ft.Colors.GREY_500),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=16,
            border=ft.OutlineInputBorder(border_radius=12),
            bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
            expand=True,
        )

    stats_row = ft.Row(
        [
            stat(ft.Icons.WATER_DROP, "Humidity", humidity_text),
            stat(ft.Icons.AIR, "Wind", wind_text),
        ],
        spacing=12,
        visible=False,
    )

    # ---- State helpers ----
    def reset_weather():
        city_display.value = ""
        temperature_text.value = ""
        description_text.value = ""
        weather_icon.visible = False
        stats_row.visible = False

    def handle_search(e):
        city = (city_input.value or "").strip()

        if not city:
            reset_weather()
            error_text.value = "Please enter a valid city."
            error_text.visible = True
            page.update()
            return

        result = get_weather_data(city)

        if result["success"]:
            city_display.value = result["city"]
            temperature_text.value = result["temp"]
            description_text.value = result["description"]
            humidity_text.value = result["humidity"]
            wind_text.value = result["wind"]
            weather_icon.src = ICON_URL.format(icon=result["icon"])
            weather_icon.visible = True
            stats_row.visible = True
            error_text.visible = False
        else:
            reset_weather()
            error_text.value = result["error"]
            error_text.visible = True

        page.update()

    # ---- Bind events: Enter key and the search button do the same thing ----
    city_input.on_submit = handle_search
    search_button.on_click = handle_search

    # ---- Layout ----
    page.add(
        ft.Row(
            [city_input, search_button],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        error_text,
        city_display,
        weather_icon,
        temperature_text,
        description_text,
        stats_row,
    )


if __name__ == "__main__":
    port = os.getenv("PORT")
    if port:  # Render sets PORT, so run as a website
        ft.run(main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(port))
    else:     # on your laptop, open the desktop window as before
        ft.run(main)