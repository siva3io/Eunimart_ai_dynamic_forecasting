# -*- coding: utf-8 -*-
from odoo import http
import json


class Forecasting(http.Controller):
    @http.route('/forecasting/forecasting', type="json", auth="public", cors="*", method=["POST"])
    def get_dynamic_forecast(self, **kw):
        payload = http.request.jsonrequest
        dynamic_forecast_data = http.request.env["forecasting.foreasting"].sudo().forecast(payload)
        response = {"data": dynamic_forecast_data,
                    "query_id": payload['data']['query_id']
                    }
        return response
