import tkinter as tk
import time
from tkinter import font, Menu, messagebox
from data_scraping import get_cities, get_weather_info
from data_saving_loading import save_to_csv, pandas_graph

days_info_values = [[]for _ in range(6)]
weather_info = None
frames = []
window_page = 0


def cascade_forecast():
    global window_page
    if window_page != 1:
        window_page = 1
        forecast_frame.grid()
        forecast_comparison_frame.grid_forget()


def cascade_forecast_comparison():
    global window_page
    if window_page != 2:
        window_page = 2
        forecast_frame.grid_forget()
        forecast_comparison_frame.grid()


def set_weather_info():
    global weather_info
    global frames
    global city_label
    weather_info = get_weather_info(listbox_1.get(listbox_1.curselection()))
    if weather_info is not None:
        for index in range(6):
            grid_row = 0
            grid_column = 1

            city_label.config(text=f"{listbox_1.get(listbox_1.curselection())}")

            label = tk.Label(frames[index], text=weather_info[index]["date_for"])
            label.grid(row=grid_row, column=grid_column)
            days_info_values[index].append(label)
            grid_row += 1

            label = tk.Label(frames[index], text=str(weather_info[index]["temperature"])+"C°")
            label.grid(row=grid_row, column=grid_column)
            days_info_values[index].append(label)
            grid_row += 1

            label = tk.Label(frames[index], text=str(weather_info[index]["wind"])+"m/s")
            label.grid(row=grid_row, column=grid_column)
            days_info_values[index].append(label)
            grid_row += 1

            label = tk.Label(frames[index], text=str(weather_info[index]["precipitation"])+"mm")
            label.grid(row=grid_row, column=grid_column)
            days_info_values[index].append(label)

            root.geometry("")
            time.sleep(0.2)
    else:
        messagebox.showerror("Error", "Failed to load forecast for selected city!")


def save_data():
    save_to_csv(weather_info)


def show_graph():
    if not listbox_entry.get(listbox_entry.curselection()):
        messagebox.showerror("Error", "Parameter (temperature, wind, precipitation for the graph was not selected!")
        return
    exists = pandas_graph(city_entry.get(), date_entry.get(), listbox_entry.get(listbox_entry.curselection()))
    if exists == -1:
        messagebox.showerror("Error", "Data does not exist for this city!")
        return
    elif exists == -2:
        messagebox.showerror("Error", "Data does not exist for that date!")
        return


root = tk.Tk()
root.title("Weather forecast")
root.iconbitmap("weather.ico")

menu = tk.Menu(root)
root.config(menu=menu)
submenu = Menu(menu, tearoff=0)

menu.add_cascade(label="Forecast", command=cascade_forecast)
menu.add_cascade(label="Forecast comparison", command=cascade_forecast_comparison)

# Forecast frame---------------------------------
forecast_frame = tk.Frame(root)
forecast_frame.grid(row=0, column=0)

frame_top_1 = tk.Frame(forecast_frame)
frame_top_1.grid(row=0, column=0)

frame_top_2 = tk.Frame(forecast_frame)
frame_top_2.grid(row=0, column=1)

label_1 = tk.Label(frame_top_1, text="City selection")
label_1.grid(row=0, column=0, sticky="s")

scrollbar = tk.Scrollbar(frame_top_1, orient="vertical")
listbox_1 = tk.Listbox(frame_top_1, width=20, height=10, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
scrollbar.config(command=listbox_1.yview)
cities = get_cities()
for index, city in enumerate(cities):
    listbox_1.insert(index, city)
listbox_1.grid(row=1, column=0)
scrollbar.grid(row=1, column=1, sticky="wns")

button_1 = tk.Button(frame_top_1, text="Show", command=set_weather_info)
button_1.grid(row=2, column=0)

button_2 = tk.Button(frame_top_2, text="Save to .csv file", command=save_data)
button_2.grid(row=1, column=1, columnspan=2)

city_frame = tk.Frame(frame_top_2)
city_frame.grid(row=0, column=1, columnspan=2)
city_font = font.Font(size=12, weight="bold")
city_label = tk.Label(city_frame, text="City", font=city_font)
city_label.grid(row=0, column=0)

frames = []
days_info = [[] for _ in range(6)]
for index in range(6):
    grid_row = 0
    grid_column = 0
    frame = tk.Frame(frame_top_2)
    frame.grid(row=2, column=index + 2)
    frames.append(frame)
    label = tk.Label(frames[index], text="Date:", borderwidth=1, relief="solid")
    label.grid(row=grid_row, column=grid_column, padx=5, pady=5)
    days_info[index].append(label)
    grid_row += 1

    label = tk.Label(frames[index], text="Temperature:", borderwidth=1, relief="solid")
    label.grid(row=grid_row, column=grid_column, padx=5, pady=5)
    days_info[index].append(label)
    grid_row += 1

    label = tk.Label(frames[index], text="Wind:", borderwidth=1, relief="solid")
    label.grid(row=grid_row, column=grid_column, padx=5, pady=5)
    days_info[index].append(label)
    grid_row += 1

    label = tk.Label(frames[index], text="Precipitation:", borderwidth=1, relief="solid")
    label.grid(row=grid_row, column=grid_column, padx=5, pady=5)
    days_info[index].append(label)
    grid_column += 2

# Forecast comparison frame----------------------
forecast_comparison_frame = tk.Frame(root)
forecast_comparison_frame.grid(row=0, column=0)

entries_frame = tk.Frame(forecast_comparison_frame)
entries_frame.grid(row=0, column=0)

form_label = tk.Label(entries_frame, text="Here you can check how the forecast changed for a certain date")
form_label.grid(row=0, column=0, sticky="we")

city_label_2 = tk.Label(entries_frame, text="City")
city_label_2.grid(row=1, column=0, sticky="we")

city_entry = tk.Entry(entries_frame)
city_entry.grid(row=2, column=0, sticky="we")

date_label = tk.Label(entries_frame, text="Date (yyyy-mm-dd)")
date_label.grid(row=3, column=0, sticky="we")

date_entry = tk.Entry(entries_frame)
date_entry.grid(row=4, column=0, sticky="we")

listbox_entry = tk.Listbox(entries_frame, selectmode=tk.SINGLE)
listbox_entry_height = min(listbox_entry.size(), 10) * listbox_entry.cget("height")
listbox_entry.config(height=listbox_entry_height)
listbox_entry.grid(row=5, column=0)
listbox_entry.insert(tk.END, "Temperature", "Wind", "Precipitation")

button_entry = tk.Button(entries_frame, text="Check", command=show_graph)
button_entry.grid(row=6, column=0)

cascade_forecast()

root.mainloop()
