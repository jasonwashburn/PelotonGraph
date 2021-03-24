import requests
import os
from ride_data import calories_by_date, total_work_by_date, cycling_metric_by_date

PIXELA_ENDPOINT = f"https://pixe.la/v1/users/"
GRAPHS_ENDPOINT = f"{PIXELA_ENDPOINT}{os.getenv('PIXELA_USERNAME')}/graphs"

headers = {
    "X-USER-TOKEN": os.getenv("PIXELA_TOKEN")
}


def create_graph(graph_id, graph_name, graph_unit, value_type, color="momiji"):
    parameters = {"id": graph_id,
                  "name": graph_name,
                  "unit": graph_unit,
                  "type": value_type,
                  "color": color,
                  }

    response = requests.post(GRAPHS_ENDPOINT, json=parameters, headers=headers)
    print(response.text)


def update_ride_data(number_of_workouts=5):
    date_cals_dict = calories_by_date(number_of_workouts=number_of_workouts)
    for day, calories in date_cals_dict.items():
        ride_data = {
            "date": day,
            "quantity": str(calories)
        }
        response = requests.post(f"{GRAPHS_ENDPOINT}/peloton", json=ride_data, headers=headers)
        print(response.text)


def update_work_data(number_of_workouts=5):
    date_work_dict = total_work_by_date(number_of_workouts=number_of_workouts)
    for day, total_work in date_work_dict.items():
        ride_data = {
            "date": day,
            "quantity": str(total_work / 1000)  # Convert joules to KJ
        }
        response = requests.post(f"{GRAPHS_ENDPOINT}/cycling-work", json=ride_data, headers=headers)
        print(response.text)


def update_cycling_metric_data(graph_id, metric, number_of_workouts=5):
    date_metric_dict = cycling_metric_by_date(metric=metric, number_of_workouts=number_of_workouts)
    for day, metric in date_metric_dict.items():
        ride_data = {
            "date": day,
            "quantity": str(metric)
        }
        response = requests.post(f"{GRAPHS_ENDPOINT}/{graph_id}", json=ride_data, headers=headers)
        print(response.text)


def list_existing_graphs():
    response = requests.get(GRAPHS_ENDPOINT, headers=headers)
    data = response.json()
    existing_graphs = [graph['id'] for graph in data['graphs']]
    print(existing_graphs)


def delete_graph(graph_id):
    user_input = input(f"Delete '{id}'?\nAre you sure? (Y/N): ")
    if user_input.lower() == 'y':
        response = requests.delete(f"{GRAPHS_ENDPOINT}/{graph_id}", headers=headers)
        print(response.json())


def update_graph(graph_id, **kwargs):
    update_dict = kwargs
    response = requests.put(f"{GRAPHS_ENDPOINT}/{graph_id}", json=update_dict, headers=headers)
    print(response.json())

# create_graph(graph_id="avg-resistance", graph_name="Peloton Cycling - Average Resistance",
#             graph_unit="%", value_type="float")

# update_graph(graph_id="avg-resistance", timezone="US/Central")

# print(cycling_metric_by_date(metric='avg_resistance', number_of_workouts=10))
# update_cycling_metric_data(graph_id="avg-resistance", metric="avg_resistance", number_of_workouts=365)
