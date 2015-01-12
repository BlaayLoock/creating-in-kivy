from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock

import json
import random


class WeatherRoot(BoxLayout):
    current_weather = ObjectProperty()

    def show_current_weather(self, location):
        self.clear_widgets()

        if self.current_weather is None:
            self.current_weather = CurrentWeather()

        if location is not None:
            self.current_weather.location = location

        self.current_weather.update_weather()
        self.add_widget(self.current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())


class LocationButton(ListItemButton):
    location = ListProperty()


class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()

    def search_location(self):
        search_template = "http://api.openweathermap.org/data/2.5/"
        search_template += "find?q={}&type=like"
        search_url = search_template.format(self.search_input.text)
        return UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        cities = [(item['name'], item['sys']['country']) for item in data['list']]

        self.search_results.adapter.data = cities
        self.search_results._trigger_reset_populate()

    def convert_arguments(self, index, item):
        name, country = item
        return {
            'location': (name, country)
        }


class CurrentWeather(BoxLayout):
    location = ListProperty(['New York', 'US'])
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()
    condition_box = ObjectProperty()
    condition_desc = StringProperty()
    condition_image = StringProperty()

    def update_weather(self):
        weather_template = "http://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric"
        weather_url = weather_template.format(*self.location)
        request = UrlRequest(weather_url, self.weather_retrieved)

    def weather_retrieved(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.temp = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']
        self.condition_desc = data['weather'][0]['description']
        self.condition_image = "http://openweathermap.org/img/w/{}.png".format(data['weather'][0]['icon'])


class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()
