import requests
import os
import plotly.graph_objects as go
from collections import defaultdict
proxies = {
  "http": None,
  "https": None,
}
APIFY_URL= "https://api.apify.com/v2/key-value-stores/lDegAca820XgvjE0C/records/LATEST?disableRedirect=true"
HISTORICAL_DATA_URL= "https://api.apify.com/v2/datasets/jr5ogVGnyfMZJwpnB/items?format=json&clean=1"


def fetch_url(url):
    response = requests.get(url, proxies=proxies)
    if response.status_code == 200:
        return response.json()
    raise "Non 200 response from the {url}".format(url=url)



def generate_x_data(historic_data, x_axis_key):
    aggregated_map = defaultdict(int)
    for data in historic_data:
        x_val = data[x_axis_key]
        x_key = x_val.split("T")[0]
        aggregated_map[x_key] = 0
    return aggregated_map



def plot_infected_deceased(y_axis_keys, x_axis_key):
    historic_data = fetch_url(HISTORICAL_DATA_URL)
    fig = go.Figure()
    color = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
    x_data = [x[x_axis_key] for x in historic_data]

    for i  in range(len(y_axis_keys)):
        y_key = y_axis_keys[i]
        agg_map = defaultdict(int)
        for data in historic_data:
            if data[y_key] is not None:
                x_val = data[x_axis_key]
                agg_map[x_val.split("T")[0]] += int(data[y_key])
        fig.add_trace(go.Scatter(x=list(agg_map.keys()),y=list(agg_map.values()),name=y_key, line=dict(color=color[i], width=4)))
            
    fig.update_layout(title='Number of infections and death rates per day',
                   xaxis_title='Dates of month',
                   yaxis_title='Count of infection/deaths')


    fig.show()

if __name__ == "__main__":
    plot_infected_deceased(['deceased','infected'],'lastUpdatedAtApify')

