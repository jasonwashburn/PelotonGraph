import datetime as dt

import pylotoncycle
import os

username = os.getenv("PELOTON_USERNAME")
password = os.getenv("PELOTON_PASSWORD")
conn = pylotoncycle.PylotonCycle(username, password)


def calories_by_date(number_of_workouts=5):

    workouts = conn.GetRecentWorkouts(number_of_workouts)

    calories_by_date_dict = {}
    for workout in workouts:
        epoch_date = workout['device_time_created_at']
        calories = workout['overall_summary']['calories']
        formatted_date = dt.datetime.fromtimestamp(epoch_date).strftime("%Y%m%d")
        if formatted_date in calories_by_date_dict:
            total_calories = calories_by_date_dict.get(formatted_date) + calories
            calories_by_date_dict[formatted_date] = total_calories
        else:
            calories_by_date_dict[formatted_date] = calories

    return calories_by_date_dict


def total_work_by_date(number_of_workouts=5):

    workouts = conn.GetRecentWorkouts(number_of_workouts)

    total_work_by_date_dict = {}
    for workout in workouts:
        if workout['metrics_type'] == "cycling":
            epoch_date = workout['device_time_created_at']
            total_work = workout['overall_summary']['total_work']
            formatted_date = dt.datetime.fromtimestamp(epoch_date).strftime("%Y%m%d")
            if formatted_date in total_work_by_date_dict:
                total_work = total_work_by_date_dict.get(formatted_date) + total_work
                total_work_by_date_dict[formatted_date] = total_work
            else:
                total_work_by_date_dict[formatted_date] = total_work
        else:
            continue

    return total_work_by_date_dict


def cycling_metric_by_date(metric, number_of_workouts=5):

    workouts = conn.GetRecentWorkouts(number_of_workouts)

    cycling_metric_by_date_dict = {}
    for workout in workouts:
        if workout['metrics_type'] == "cycling":
            epoch_date = workout['device_time_created_at']
            workout_metric = workout['overall_summary'][metric]
            formatted_date = dt.datetime.fromtimestamp(epoch_date).strftime("%Y%m%d")
            if formatted_date in cycling_metric_by_date_dict:
                workout_metric = cycling_metric_by_date_dict.get(formatted_date) + workout_metric
                cycling_metric_by_date_dict[formatted_date] = workout_metric
            else:
                cycling_metric_by_date_dict[formatted_date] = workout_metric
        else:
            continue

    return cycling_metric_by_date_dict
