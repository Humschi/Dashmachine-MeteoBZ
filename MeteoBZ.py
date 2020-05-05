# http://daten.buergernetz.bz.it/de/dataset/southtyrolean-weatherservice-weatherdistricts
# http://daten.buergernetz.bz.it/services/weather/district?format=json&lang=de
# http://daten.buergernetz.bz.it/services/weather/district/2/bulletin?format=json&lang=de

import requests
from flask import render_template_string


class Platform:
    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        # set defaults for omitted options
        if not hasattr(self, "regionid"):
            self.regionid = 1

    def process(self):
        html_template = """
                        <div class="row">
                            <div class="col s6">
                                <span class="mt-0 mb-0 theme-primary-text font-weight-700" style="font-size: 36px">{{ maxTemp }}&deg;</span>
                            </div>
                            <div class="col s6 right-align">
                                <img height="48px" src="{{ image }}">
                            </div>
                        </div>
                        <div class="row">
                            <h6 class="font-weight-900 center theme-muted-text"></h6>
                        </div>
                        <div class="row">
                            <h6 class="font-weight-900 center theme-muted-text">{{ region }}</h6>
                        </div>
                        """

        icon_array = ["a", "c", "b", "c", "c", "lc", "d", "lc", "e", "hc", "f", "s", "g", "s", "h", "lr", "i",
                      "hr", "j", "lr", "k", "hc", "l", "sn", "m", "sn", "n", "sn", "o", "sn", "p", "sn", "q",
                      "sl", "r", "sl", "s", "none", "t", "none", "u", "t", "v", "t", "w", "t", "x", "t", "y",
                      "t", "z", "t"]

        # Get forecast for the given region
        jsonRequest = requests.get(
            f'http://daten.buergernetz.bz.it/services/weather/district/{self.regionid}/bulletin?format=json&lang=de') \
            .json()
        # Select the first forecast (today)
        forecast = jsonRequest["forecasts"][0]

        # Get regions
        regions = requests.get(
            'http://daten.buergernetz.bz.it/services/weather/district?format=json&lang=de').json()["rows"]

        # Set variable if can't find the correct name
        regionName = "Unknown"

        # Find region name by given regionId
        for i in regions:
            if i["id"] == int(self.regionid):
                regionName = i['name']

        # Replace ugly icon with meta-weather icon
        iconId = icon_array[icon_array.index(forecast["symbol"]["code"]) + 1]
        forecast["symbol"]["imageUrl"] = f"https://www.metaweather.com/static/img/weather/{iconId}.svg"

        # Return Template
        return_template = render_template_string(
            html_template,
            region=regionName,
            image=forecast["symbol"]["imageUrl"],
            maxTemp=forecast["temperatureMax"],
        )

        return return_template
