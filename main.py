import os
from pathlib import Path

import requests
from dotenv import load_dotenv


class Weather:
    def __init__(self, city, temperature, humidity, description):
        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.description = description

    def display(self):
        print("\n" + "=" * 35)
        print("         WEATHER SUMMARY")
        print("=" * 35)
        print(f"City        : {self.city}")
        print(f"Temperature : {self.temperature} C")
        print(f"Humidity    : {self.humidity}%")
        print(f"Description : {self.description}")
        print("=" * 35)


def main():
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()

    if not api_key:
        print("Please add your API key to the .env file.")
        return

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": 30.0444,
        "lon": 31.2357,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        weather = Weather(
            city=data["name"],
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            description=data["weather"][0]["description"],
        )

        weather.display()

    except requests.exceptions.HTTPError as error:
        status = error.response.status_code

        if status == 401:
            print("Check your API key and email verification.")
            print("A new key may take up to 2 hours to activate.")
        else:
            print(f"API error. Status code: {status}")

    except requests.exceptions.RequestException:
        print("Connection failed. Check your internet and try again.")

    except (ValueError, KeyError, IndexError, TypeError):
        print("Unexpected data received from the API.")


if __name__ == "__main__":
    main()