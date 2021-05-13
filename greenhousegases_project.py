"""This file is used for the visualization of the trends in Greenhouse Gases
and carbon emissions.
Resources:
- https://www.geeksforgeeks.org/box-plot-in-python-using-matplotlib/
- https://www.kite.com/python/answers/how-to-color-a-scatter-plot-by-category-using-matplotlib-in-python
- https://plotly.com/python/box-plots/
- https://towardsdatascience.com/how-to-create-an-animated-choropleth-map-with-less-than-15-lines-of-code-2ff04921c60b
"""
from typing import List

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

from data_manager import Dataset, group_by_values


def data_by_tags_country_year(filepath: str,
                              tags: List[str],
                              countries_or_years: list,
                              country_or_year: int) -> List[List[float]]:
    """The function would take in the filepath of the dataset from which it would extract the data
    convert every variable in the row into its appropriate datatype and then filter out the data
    containing only the tags we want, and only for the countries or years we want, and then return
    emission values separately for all the countries or years.

    @param filepath: the path of the dataset
    @param tags: list of all the categories of emissions we want in the data
    @param countries_or_years: The countries or years for which we want the data
    @param country_or_year: 0 or 1 based on if we want to categorise by country or year
    @return: Return a list containing lists for every countries emission value
    """

    # extract dataset and covert all variables into their respective datatype
    dataset = Dataset(filepath=filepath, types=[str, int, float, str])

    # keeping rows with tags we want
    dataset.filter_by_value(3, tags)

    # splitting by countries
    grouped_data = group_by_values(dataset, country_or_year)

    # Extracting emission values for the countries we want to analyze
    countries_so_far = []

    for county in countries_or_years:
        county_data = grouped_data[county]
        countries_so_far.append(county_data.extract_column(2))

    return countries_so_far


def data_by_tags(filepath: str,
                 tags: List[str],
                 country_filter: List[str] = None,
                 year_filter: List[int] = None) -> List[List]:
    """The function would take in the filepath of the dataset from which it would extract the data
    convert every variable in the row into its appropriate datatype and then filter out the data
    containing only the tags we want, and return the emission values along side the respective
    country and year.

    We can pass in optional lists to only get rows with specific country or year

    @param filepath: the path of the dataset
    @param tags: list of all the categories of emissions we want in the data
    @param country_filter: list of countries we want data for
    @param year_filter: list of years we want data for
    @return: Return a list with emission value alongside the respective country and year
    """

    # extract dataset and covert all variables into thir respective datatype
    dataset = Dataset(filepath=filepath, types=[str, int, float, str])

    # keeping rows with tags we want
    dataset.filter_by_value(3, tags)

    # filtering countries and years
    if country_filter:
        dataset.filter_by_value(0, country_filter)
    if year_filter:
        dataset.filter_by_value(1, year_filter)

    # extract the values, countries and years
    values = dataset.extract_column(2)
    countries = dataset.extract_column(0)
    year = dataset.extract_column(1)

    return [values, countries, year]


def tidy_gdp_data(filepath: str) -> Dataset:
    """Transform the data for plotting purposes. It will remove all the columns with year before 1990 and
    after 2016, and convert columns to their respective data type.

    :param filepath: path of the dataset
    :return: transformed dataset object
    """
    # loading data
    raw_data = Dataset(filepath)

    # creating new dataset object
    data = Dataset(dataset=[])

    # making the data tidy
    for row in raw_data.get():
        for element_index in range(4, len(row)):

            value = row[element_index]
            year = 1960 + element_index - 4

            if 1990 <= year <= 2016:
                data.push([row[0], row[1], row[2], row[3], year, value])

    data.remove_na()

    data.transform([str, str, str, str, int, float])

    return data


# Plot1
def plot_all_countries_peryear(filepath: str) -> None:
    """ Plots 5 boxplots showing amount of nitrogen triflouride (NF3) emissions (kilotonnes) in all
    countries taken together over the years 2010, 2011, 2012, 2013 and 2014.

    Through this visualization, it is easier to understand correlation of how increased development
    has affected Nitrogen Triflouride emissions in recent years.

    @param filepath: the path of the dataset
    """

    years = [2010, 2011, 2012, 2013, 2014]

    tags = ['nitrogen_trifluoride_nf3_emissions_in_kilotonne_co2_equivalent']

    data = data_by_tags_country_year(filepath, tags, years, 1)
    x1 = np.array(data[0])  # NF3 emissions for all countries in 2010
    x2 = np.array(data[1])  # NF3 emissions for all countries in 2011
    x3 = np.array(data[2])  # NF3 emissions for all countries in 2012
    x4 = np.array(data[3])  # NF3 emissions for all countries in 2013
    x5 = np.array(data[4])  # NF3 emissions for all countries in 2014

    plt.boxplot((x1, x2, x3, x4, x5), notch=False, sym="o", labels=["2010",
                                                                    "2011",
                                                                    "2012",
                                                                    "2013",
                                                                    "2014"])
    plt.xlabel("Region/Country", fontsize=15)
    plt.ylabel("Aggregated Emissions of Gases (in kilotonnes) ", fontsize=9)

    plt.title("Aggregated Nitrogen Triflouride emissions for 5 years (from all countries) ",
              fontsize=10,
              fontweight="bold")

    plt.show()


# Plot2
def plot_scatter_n2o(filepath: str) -> None:
    """Plots a scatterplot showing amount of nitrous oxide (N2O) emissions (kilotonnes) in USA,
    Canada and the European Union each year (between 1990 and 2014).

    This helps us to understand trends of nitrous oxide emissions in 3 countries with very
    different demographics. (Canada - Low population Density, EU - Higher Population Density,
    USA - Large scale industrialization)

    @param filepath: the path of the dataset
    """

    countries = ['Canada', 'United States of America', 'European Union']

    tags = [
        'nitrous_oxide_n2o_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent']

    data = data_by_tags(filepath, tags, country_filter=countries)

    y = data[0]  # emission data
    labels = data[1]  # list of countries
    x = data[2]  # list of years

    data = pd.DataFrame({"X Value": x, "Y Value": y, "Category": labels})

    groups = data.groupby("Category")  # to group the data by region/country

    for name, group in groups:
        plt.plot(group["X Value"], group["Y Value"], marker="o", linestyle="-", label=name)

    plt.xlabel("Years", fontsize=15)
    plt.ylabel("Emissions of Gases (in kilotonnes)", fontsize=15)
    plt.title("Nitrous Oxide emissions each year")
    plt.legend()
    plt.show()


# Plot3
def scatterboxplot_sparsely_pop(filepath: str) -> None:
    """ Plots a scatterplot and a box plot together showing distribution of amount of carbon
    dioxide (CO2) emissions (kilotonnes) in Austria, Belarus and Bulgaria in the 24 year period
    (between 1990 and 2014).

    This plot studies and visualizes details of total carbon dioxide emissions in sparsely
    populated countries. The scatterplot shows each year's emissions data for the 3 aforementioned
    countries and the boxplot aggregates and visualizes this data.

    @param filepath: the path of the dataset
    """
    countries = ['Austria', 'Belarus', 'Bulgaria']

    tags = [
        'carbon_dioxide_co2_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent']

    data = data_by_tags_country_year(filepath, tags, countries, 0)

    y0 = data[0]
    y1 = data[1]
    y2 = data[2]

    emission_values = [y0, y1, y2]

    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)',
              'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']

    fig = go.Figure()

    for xd, yd, cls in zip(countries, emission_values, colors):
        fig.add_trace(go.Box(
            y=yd,
            name=xd,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=cls))

    fig.update_layout(
        title='Carbon Dioxide (CO2) Emissions in kilotonnes for 3 sparsely populated countries (from 1990 - 2014)',
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )

    fig.show()


# Plot4
def plot_scatter_boxplot_1990_2014(filepath: str) -> None:
    """Plots a scatterplot and a box plot together showing distribution of hydrofluorocarbon (hfcs)
    emissions in 1990, 2002 and 2014 (in all countries taken together).

    This tells us about trends of changes in hydroflourocarbon emissions in 1990, 2002 and 2014.
    This helps to correlate increased industrialization over the years with release of more
    pollutants. The scatterplot shows each country's emissions data for the 3 aforementioned years
    and the boxplot aggregates and visualizes this data.

    @param filepath: the path of the dataset
    """
    years = [1990, 2002, 2014]

    tags = ['hydrofluorocarbons_hfcs_emissions_in_kilotonne_co2_equivalent']

    data = data_by_tags_country_year(filepath, tags, years, 1)

    y0 = data[0]
    y1 = data[1]
    y2 = data[2]

    emission_values = [y0, y1, y2]

    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)',
              'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']

    fig = go.Figure()

    for xd, yd, cls in zip(years, emission_values, colors):
        fig.add_trace(go.Box(
            y=yd,
            name=xd,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=cls))

    fig.update_layout(
        title='Hydrofluorocarbon (hfcs) Emissions in kilotonnes by all countries (aggregated together) '
              'for 1990, 2002, 2014 ',
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )

    fig.show()


def plot_emission_per_gdp(filepath: str) -> None:
    """Plots a Choropleth map showing the distribution of CO2 emissions (kg per PPP $ of GDP)
    for all countries in the dataset.

    @param filepath:the path of the dataset
    """
    data = tidy_gdp_data(filepath)

    df = pd.DataFrame({'country': data.extract_column(0),
                       'code': data.extract_column(1),
                       'year': data.extract_column(4),
                       'CO2 emissions (kg per PPP $ of GDP)': data.extract_column(5)})

    fig = px.choropleth(df,
                        locations='country',
                        color='CO2 emissions (kg per PPP $ of GDP)',
                        animation_frame='year',
                        locationmode='country names',
                        scope='world',
                        range_color=(min(data.extract_column(5)), max(data.extract_column(5))),
                        title='CO2 emissions (kg per PPP $ of GDP) by country',
                        height=600
                        )

    fig.show()


def dist_2016(filepath: str) -> None:
    """The function plots a pie chart for percentage contribution of different
    countries for CO2 emissions (kg per PPP $ of GDP) for 2016.

    @param filepath: path of teh dataset
    """
    data = tidy_gdp_data(filepath)

    data.filter_by_value(4, [2016])

    total_in_world = sum(data.extract_column(5))

    values = [value / total_in_world for value in data.extract_column(5)]

    df = pd.DataFrame({'country': data.extract_column(0),
                       'code': data.extract_column(1),
                       'year': data.extract_column(4),
                       'CO2 emissions (kg per PPP $ of GDP)': values})

    fig = px.pie(df,
                 values='CO2 emissions (kg per PPP $ of GDP)',
                 names='country'
                 )

    fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['plotly.express',
                          'plotly.graph_objects',
                          'matplotlib.pyplot',
                          'typing',
                          'data_manager',
                          'numpy',
                          'pandas'],
        'allowed-io': [],
        'max-line-length': 150,
        'disable': ['R1705', 'C0200']
    })
