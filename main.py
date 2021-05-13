"""
This file will run all the visualizations and programs

Refrences:
- https://docs.python.org/3/library/tk.html
- https://www.tutorialspoint.com/python/tk_text.htm
- https://www.geeksforgeeks.org/python-grid-method-in-tkinter/
"""

from analyze_data import plot_top_10, plot_sentiments
import greenhousegases_project
import global_land_temp
import future_predict
import tkinter as tk


def run_greenhouse_visualizations() -> None:
    """
    Plots visualizations for Greenhouse gas emissions visualizations
    """
    Greenhouse_emissions_data = 'datasets/greenhouse_gas_inventory_data_data.csv'

    greenhousegases_project.plot_all_countries_peryear(Greenhouse_emissions_data)
    greenhousegases_project.plot_scatter_n2o(Greenhouse_emissions_data)
    greenhousegases_project.scatterboxplot_sparsely_pop(Greenhouse_emissions_data)
    greenhousegases_project.plot_scatter_boxplot_1990_2014(Greenhouse_emissions_data)

    Co2_per_capita_data = 'datasets/emissions_per_capita.csv'

    greenhousegases_project.plot_emission_per_gdp(Co2_per_capita_data)
    greenhousegases_project.dist_2016(Co2_per_capita_data)


def run_land_temp_visualizations() -> None:
    """
    Plots visualizations for Land temperature related visualizations
    """
    Land_temp_data = 'datasets/filtered_land_temp.csv'

    global_land_temp.plot_data_greater_average(Land_temp_data)
    global_land_temp.plot_data_usa_can_all(Land_temp_data)


def twitter_visualizations() -> None:
    """
    Plot the visualizations for twitter data
    """
    Twitter_data = 'datasets/climate-change-sentiment.csv'

    plot_sentiments(Twitter_data)
    plot_top_10(Twitter_data)


def predictions_visualizations() -> None:
    """
    Plot the best fit lines and cost function graphs
    for Co2 emissions and Land temperature from 1990
    to 2014 and 2013 respectively, and print the
    predictions for 2015 2016 and 2017
    """
    Land_temp_data = 'datasets/filtered_land_temp.csv'
    Greenhouse_emissions_data = 'datasets/greenhouse_gas_inventory_data_data.csv'
    future_predict.predict_temp_and_emissions(Land_temp_data, Greenhouse_emissions_data)


if __name__ == '__main__':
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    root.geometry("1200x200")

    txt = tk.Label(frame, text="Hi! welcome to our project. Select the type of visualizations"
                               " you want to see (more information on each type of visualizations"
                               " is in the pdf file chapter 3.)")
    txt.grid(row=0, column=1, pady=1)

    b1 = tk.Button(frame,
                   text="look at average land temperature data visualizations",
                   command=run_land_temp_visualizations,
                   borderwidth=6,
                   relief="solid")
    b1.grid(row=3, column=1, pady=6)
    b2 = tk.Button(frame,
                   text="look at Greenhouse gas data visualizations",
                   command=run_greenhouse_visualizations,
                   borderwidth=6,
                   relief="solid")
    b2.grid(row=5, column=1, pady=6)
    b3 = tk.Button(frame,
                   text="look at Twitter data visualizations",
                   command=twitter_visualizations,
                   borderwidth=6,
                   relief="solid")
    b3.grid(row=7, column=1, pady=6)
    b4 = tk.Button(frame,
                   text="look at the visualizations and predictions of Canada's Co2 emissions for 2015, 2016 and 2017 ",
                   command=predictions_visualizations,
                   borderwidth=6,
                   relief="solid")
    b4.grid(row=9, column=1, pady=6)

    button = tk.Button(frame,
                       text="QUIT",
                       fg="red",
                       command=quit,
                       borderwidth=6,
                       relief="solid")
    button.grid(row=11, column=1, pady=6)

    root.mainloop()
