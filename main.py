# Bellevue University
# DSC510-T301
# Week 12: Assignment 12.1
#   Weather forcast application.
#   Gets GEO location info and weather/forcast using Open Weather Map API.
#
# Author: Garth Scheck
# Revision: 1.0
# Date: 3/3/2023
import requests
import datetime


def get_api_key():
    return "xxxxxxxxxxxxxxxxxxxxxxx"


# Weather Station Class
class WeatherStation:
    fmt = ''
    api_key = ''

    # Constructor
    def __init__(self, api_key):
        self.api_key = api_key

    def set_units(self, fmt):
        self.fmt = fmt

    # Get location depending on information passed in
    # first parameter is used for City or Zip Code
    # Second parameter is for state, left empty for zip
    def __get_location(self,
                       city_or_zip,
                       state=None):
        # base url
        geo_url = "http://api.openweathermap.org/geo/1.0/"
        loc_info = None

        if state is None:
            if len(city_or_zip) != 5:
                print('zip code must be 5 digits')
            else:
                zip_url = geo_url + "zip?zip=" + city_or_zip + ",us&appid=" + self.api_key
                try:
                    response = requests.get(zip_url)

                    if response.ok:
                        loc_info = response.json()
                    else:
                        print('Error code: ' + str(response.status_code) + ' - Could not locate ' + zip_url)
                        return None
                except requests.exceptions.ConnectionError:
                    print('Can not connect to ' + geo_url)
                    return None
                except requests.exceptions.ConnectTimeout:
                    print('Timed out trying to connect to ' + geo_url)
                    return None
                except requests.exceptions.TooManyRedirects:
                    print('Too many re-directs connecting to ' + geo_url)
                    return None
                except requests.exceptions.RequestException:
                    print('General request exception for ' + geo_url)
                    return None
        else:
            st_url = geo_url + "direct?q=" + city_or_zip + "," + state + ",us&appid=" + self.api_key

            try:
                response = requests.get(st_url)
                if response.ok:
                    loc_info = response.json()
                    data = requests.get(st_url).json()
                    if len(data) > 0:
                        loc_info = requests.get(st_url).json()[0]
                    else:
                        return None
                else:
                    if response.status_code == 404:
                        print('Could not locate : ' + st_url)
                        return None
                    else:
                        print('Error code: ' + str(response.status_code))
                        return None
            except requests.exceptions.ConnectionError:
                print('Can not connect to ' + st_url)
                return None
            except requests.exceptions.ConnectTimeout:
                print('Timed out trying to connect to ' + st_url)
                return None
            except requests.exceptions.TooManyRedirects:
                print('Too many re-directs connecting to ' + st_url)
                return None
            except requests.exceptions.RequestException:
                print('General request exception for ' + st_url)
                return None

        return loc_info

    # Gets current weather depending on information passed in
    # first parameter is used for City or Zip Code
    # Second parameter is for state, left empty for zip
    # This function calls the get_location function.
    def get_current_weather(self,
                            city_or_zip,
                            state=None):

        weather_url = ''
        loc_info = self.__get_location(city_or_zip, state)

        if self.fmt.lower() == 'c':
            units = '&units=metric'
        elif self.fmt.lower() == 'f':
            units = '&units=imperial'
        else:
            units = '&units=standard'

        if loc_info is not None:

            weather_url = "https://api.openweathermap.org/data/2.5/weather?lat=" + \
                          str(loc_info['lat']) + "&lon=" + str(loc_info['lon']) + \
                          "&appid=" + self.api_key + units
        else:
            print('Location not available.')

        if weather_url != '':
            try:
                response = requests.get(weather_url)
                if response.ok:
                    weather_info = response.json()
                else:
                    if response.status_code == 404:
                        print('Could not locate : ' + weather_url)
                    else:
                        print('Error code: ' + str(response.status_code))
            except requests.exceptions.ConnectionError:
                print('Can not connect to ' + weather_url)
                return None
            except requests.exceptions.ConnectTimeout:
                print('Timed out trying to connect to ' + weather_url)
                return None
            except requests.exceptions.TooManyRedirects:
                print('Too many re-directs to ' + weather_url)
                return None
            except requests.exceptions.RequestException:
                print('General requests exception for ' + weather_url)
                return None
            return weather_info

    # Gets five-day forecast depending on information passed in
    # first parameter is used for City or Zip Code
    # Second parameter is for state, left empty for zip
    # This function calls the get_location function.
    def get_five_day_forecast(self,
                              city_or_zip,
                              state=None):

        weather_url = ''
        loc_info = self.__get_location(city_or_zip, state)

        if self.fmt.lower() == 'c':
            units = '&units=metric'
        elif self.fmt.lower() == 'f':
            units = '&units=imperial'
        else:
            units = '&units=standard'

        if loc_info is not None:
            weather_url = "https://api.openweathermap.org/data/2.5/forecast?lat=" + \
                          str(loc_info['lat']) + "&lon=" + str(loc_info['lon']) + \
                          "&appid=" + self.api_key + units
        else:
            print('Location not available.')

        if weather_url != '':
            try:
                response = requests.get(weather_url)

                if response.ok:
                    weather_info = response.json()
                    return weather_info
                else:
                    if response.status_code == 404:
                        print('Could not locate : ' + weather_url)
                        return None
                    else:
                        print('Error code: ' + str(response.status_code))
                        return None
            except requests.exceptions.ConnectionError:
                print('Can not connect to ' + weather_url)
                return None
            except requests.exceptions.ConnectTimeout:
                print('Timed out trying to connect to ' + weather_url)
                return None
            except requests.exceptions.TooManyRedirects:
                print('Too many re-directs to ' + weather_url)
                return None
            except requests.exceptions.RequestException:
                print('General requests exception for ' + weather_url)
                return None

    # Displays the five-day forecast in a nice format
    def display_five_day(self, weather_data):
        if weather_data is not None:
            try:
                last_dt = None
                print('')

                print('Five day forcast for ' + weather_data['city']['name'] + '.')
                forcast = weather_data['list']

                for entry in forcast:
                    dt_format = '%Y-%m-%d %H:%M:%S'

                    dt_object = datetime.datetime.strptime(entry['dt_txt'], dt_format)

                    if last_dt is None or last_dt.day != dt_object.day:
                        print(str(str(dt_object.month) + '/' + str(dt_object.day) + '/' + str(dt_object.year)))

                    print('\t' + 'time: ' + dt_object.time().__format__('%I:%M %p'))
                    self.__display_record(entry)

                    last_dt = dt_object

            except KeyError:
                print('No data available. Check to make sure input is valid.')

    # Displays the current weather in a nice format
    def display_current(self, weather_data):
        if weather_data is not None:
            try:
                last_dt = None
                print()
                print('Current weather for ' + weather_data['name'] + '.')
                self.__display_record(weather_data)

            except KeyError:
                print('No data available. Check to make sure input is valid.')

    # print single temperature record
    # called by display_current and display_five_day
    def __display_record(self, record):
        print('\t\tCondition: ' + record['weather'][0]['description'])
        print('\t\tTemperature: ' + str(float(record['main']['temp'])) + '\u00b0' + ' ' + self.fmt)
        print('\t\tLow Temperature: ' + str(float(record['main']['temp_min'])) + '\u00b0' + ' ' + self.fmt)
        print('\t\tHigh Temperature: ' + str(float(record['main']['temp_max'])) + '\u00b0' + ' ' + self.fmt)
        print('\t\tHumidity: ' + str(record['main']['humidity']) + '%')
        print('\t\tPressure: ' + str(record['main']['pressure']) + 'hPa')
        print('')


# determines if zip code is valid
def valid_zip(zip_code):
    if len(zip_code) != 5:
        return False
    elif int(zip_code) < 0:
        return False
    else:
        return True


# determines if value is a number
def is_number(value):
    try:
        i_val = int(value)
    except ValueError:
        return False

    return True


def main():
    api_key = get_api_key()

    close_message = 'Thank you for using the weather forcast application.'

    print('Welcome to the weather forcast application.')
    print('')
    response = ''

    station = WeatherStation(api_key)
    forecast_types = ['c', 'f']
    temperature_units = ['C', 'F', 'K']

    while True:
        try:
            fmt = ''

            while response.lower() != 'n' and response.lower() != 'y':
                response = input('Would you like to get another weather forecast? (Y/N) ')

            # exit while loop if user responded with no
            if response.lower() == 'n':
                print('\n' + close_message)
                break

            forecast_type = ''
            while forecast_type.lower() not in forecast_types:
                forecast_type = input('Would you like the (C)urrent weather or a (F)ive day forecast? ')

            response = input("Enter the city or zip code of the region you "
                             "want the weather: ")

            # determine if user input was a zip code
            if is_number(response):
                if not valid_zip(response):
                    weather_data = None
                    print('If this is a Zip code, it must be 5 digits with no special characters.')
                else:
                    fmt = ''
                    while fmt.upper() not in temperature_units:
                        fmt = input('Would you like temperature in (K)elvin, (C)elsius or (F)ahrenheit? ')

                    station.set_units(fmt.upper())
                    if forecast_type.upper() == 'F':
                        weather_data = station.get_five_day_forecast(response)
                    else:
                        weather_data = station.get_current_weather(response)
            # else assume input was a City
            else:
                city = response

                state = ''
                while len(state) != 2:
                    if len(state) > 2 or len(state) == 1:
                        print('State code must be two characters, like "WA".')
                    state = input("Enter state code: ")

                fmt = ''
                while fmt.upper() not in temperature_units:
                    fmt = input('Would you like temperature in (K)elvin, (C)elsius or (F)ahrenheit? ')

                station.set_units(fmt.upper())

                if forecast_type.upper() == 'F':
                    weather_data = station.get_five_day_forecast(city, state.upper())
                else:
                    weather_data = station.get_current_weather(city, state.upper())

            # Check if data was returned
            if weather_data is not None:
                if forecast_type.upper() == 'F':
                    station.display_five_day(weather_data)
                else:
                    station.display_current(weather_data)
            else:
                print('No data found.')
                print('')
        except KeyboardInterrupt:
            print('\n' + close_message)
            break


# start of application
if __name__ == '__main__':
    main()
