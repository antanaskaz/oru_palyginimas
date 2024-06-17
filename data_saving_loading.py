import csv
import os
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


def save_to_csv(data):
    file_path = "city_weather_data.csv"

    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as csvfile:
            field_names = ['city', 'date_current', 'date_for', 'temperature', 'wind', 'precipitation']
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    else:
        existing_rows = []
        not_existing = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            existing_rows = list(reader)

        for row in data:
            if not row_exists(row, existing_rows):
                not_existing.append(row)

        with open(file_path, 'a', newline='') as csvfile:
            field_names = ['city', 'date_current', 'date_for', 'temperature', 'wind', 'precipitation']
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            for row in not_existing:
                writer.writerow(row)


def pandas_graph(city, date, parameter):
    df = pd.read_csv("city_weather_data.csv")
    if city in df["city"].values:
        if date in df["date_for"].values:

            filtered_df = df[df["date_for"] == date].copy()
            filtered_df = filtered_df.sort_values(by='date_current')

            sb.set(style="whitegrid")

            if parameter == "Temperature":
                fig, ax = plt.subplots(1, 1, figsize=(10, 15))
                sb.lineplot(ax=ax, x='date_current', y='temperature', data=filtered_df, marker='o')
                ax.set_title('Temperature forecast comparison')
                ax.set_xlabel('Date of forecast')
                ax.set_ylabel('Temperature (°C)')
                ax.tick_params(axis='x')

            if parameter == "Wind":
                fig, ax = plt.subplots(1, 1, figsize=(10, 15))
                sb.lineplot(ax=ax, x='date_current', y='wind', data=filtered_df, marker='o')
                ax.set_title('Wind forecast comparison')
                ax.set_xlabel('Date of forecast')
                ax.set_ylabel('Wind speed (m/s)')
                ax.tick_params(axis='x')

            if parameter == "Precipitation":
                fig, ax = plt.subplots(1, 1, figsize=(10, 15))
                sb.lineplot(ax=ax, x='date_current', y='precipitation', data=filtered_df, marker='o')
                ax.set_title('Precipitation forecast comparison')
                ax.set_xlabel('Date of forecast')
                ax.set_ylabel('Precipitation (mm)')
                ax.tick_params(axis='x')

            plt.tight_layout()
            plt.show()
        else:
            return -2
    else:
        return -1


def row_exists(new_row, existing_rows):
    return new_row in existing_rows
