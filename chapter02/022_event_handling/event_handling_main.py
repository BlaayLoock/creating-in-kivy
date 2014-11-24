from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class AddLocationForm(BoxLayout):

    @staticmethod
    def search_location():
        print("Explicit is better than Implicit")


class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()
