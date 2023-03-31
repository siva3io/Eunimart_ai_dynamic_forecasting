# -*- coding: utf-8 -*-
from odoo import models
import statsmodels.api as sm
import pandas as pd
import json

pd.set_option('display.max_rows', None)


class Forecasting(models.Model):
    _name = 'forecasting.forecasting'
    _description = 'forecasting.forecasting'

    def forecast(self, request_data):
        datetime_field = ""
        y_field = ""
        for field_info in request_data["data"]["schema"]:
            if field_info["field_type"] in ["date", "datetime"]:
                datetime_field = field_info["field_label"]
            if field_info["is_y"]:
                y_field = field_info["field_label"]

        dynamic_df = pd.DataFrame(request_data["data"]["data"])
        dynamic_df[datetime_field] = pd.to_datetime(
            dynamic_df[datetime_field])  # converting the date/datetime as datetime object
        dynamic_df.set_index(datetime_field, inplace=True)  # Making datetime object as index
        lead = int(request_data["data"]["lead"])

        # SARIMAX Model
        sarima_model = sm.tsa.statespace.SARIMAX(dynamic_df[y_field], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        sarima_model = sarima_model.fit()

        # Forecast
        forecast = sarima_model.get_forecast(steps=lead)
        y_label_mean = forecast.predicted_mean
        confidence_interval = forecast.conf_int(alpha=float(request_data['data']['alpha']))
        model_forecast_data = {
            "datetime": list(y_label_mean.to_dict().keys()),
            "y_label_low": list(confidence_interval.to_dict()['lower ' + y_field].values()),
            "y_label_high": list(confidence_interval.to_dict()['upper ' + y_field].values()),
            "y_label_mean": list(y_label_mean.to_dict().values()),

        }

        return model_forecast_data
