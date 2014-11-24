from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest


class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()

    def search_location(self):
        search_template = "http://api.openweathermap.org/data/2.5/"
        search_template += "find?q={}&type=like"
        search_url = search_template.format(self.search_input.text)
        return UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        cities = ["{} ({})".format(item['name'], item['sys']['country'])
                  for item in data['list']]
        print('\n'.join(cities))


class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()
