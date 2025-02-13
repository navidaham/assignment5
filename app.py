"""
strompris fastapi app entrypoint
"""
from __future__ import annotations

import datetime
import os
from typing import List, Optional

import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_item(request: Request,
              date: datetime.date = datetime.date.today(),
              locations: list[str] = Query(list(LOCATION_CODES.keys()))):
    """Render the 'strompris.html' template with given inputs """

    return templates.TemplateResponse("strompris.html", {"request": request,"locations": locations, "today": date})

@app.get("/plot_prices.json")
def get_plot_prices_json(locations: list[str] = Query(list(LOCATION_CODES.keys())),
                        end: datetime.date=datetime.date.today(), days: int = 7) -> dict:
    """Plot the result of given inputs from user. All inputs are optional"""

    prices_df = fetch_prices(end_date=end, days=days, locations=locations)
    Chart = plot_prices(prices_df)

    # Returns a vega-lite JSON chart
    return Chart.to_dict()


# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)


...

# Task 5.6 (bonus):
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date


...

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)


...


# mount your docs directory as static files at `/help`

...


def main():
    """Launches the application on port 5000 with uvicorn"""
    # use uvicorn to launch your application on port 5000
    import uvicorn
    uvicorn.run(app, port=5000)


if __name__ == "__main__":
    main()
