"""Here we would use Linear regression to predict the future average
land temperature and Co2 emissions.
"""
from typing import Any
import numpy as np
from greenhousegases_project import data_by_tags
from linear_regression import train, predict_values, plot_statistics
from global_land_temp import get_avg_by_year


def train_emissions(emissions_path: str) -> Any:
    """The function trains a model for the emissions dataset

    @param emissions_path: path to the dataset
    @return: Return the trained model
    """
    tags = [
        'carbon_dioxide_co2_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_'
        'kilotonne_co2_equivalent']

    countries = ['Canada']

    emissions_data = data_by_tags(emissions_path, tags, country_filter=countries)

    y_axis_data = emissions_data[0]
    data_y = np.array(y_axis_data)

    x_axis_data_emissions = np.array(range(data_y.shape[0]))

    iterations = 2000
    learning_rate = 0.01

    # converting list data to numpy
    input_x_emissions = x_axis_data_emissions.reshape(x_axis_data_emissions.shape[0], 1)
    input_y_emissions = data_y.reshape(data_y.shape[0], 1)
    input_y_emissions = np.flip(input_y_emissions)

    # train model
    weights, history = train(input_x_emissions, input_y_emissions, iterations, learning_rate)

    return input_x_emissions, input_y_emissions, weights, history


def train_land_temp(temp_path: str) -> Any:
    """The function trains a model for the Land temp dataset

    @param temp_path: path to the dataset
    @return: trained model
    """

    countries = ['Canada']

    iterations = 2000
    learning_rate = 0.01

    # converting list data to numpy
    x_data_land_temp = np.array(range(24))

    input_x_land_temp = x_data_land_temp.reshape(x_data_land_temp.shape[0], 1)
    input_y_land_temp = np.array(get_avg_by_year(temp_path, countries)[0]).reshape(24, 1)

    # train model
    weights1, history1 = train(input_x_land_temp, input_y_land_temp, iterations, learning_rate)

    return input_x_land_temp, input_y_land_temp, weights1, history1


def predict_temp_and_emissions(temp_path: str, emissions_path: str) -> None:
    """Plot a scatter plot predicting the the future values for average land temperature
    and co2 emissions for 2015, 2016, and 2017 given the data we have from 1990 to 2014.

    @param temp_path: path for land temperature dataset
    @param emissions_path: path for Co2 emissions dataset
    """

    model_emissions = train_emissions(emissions_path)
    model_land_temp = train_land_temp(temp_path)

    # plotting fitted line and loss graph
    plot_statistics(model_emissions[0],
                    model_emissions[1],
                    model_emissions[2],
                    model_emissions[3],
                    True)

    # plotting fitted line and loss graph
    plot_statistics(model_land_temp[0],
                    model_land_temp[1],
                    model_land_temp[2],
                    model_land_temp[3],
                    True)

    # emissions predictions
    # predicting values for 2015, 2016 and 1017
    years = np.array([25, 26, 27])  # predictions of year 2015, 2016, 2017 (1990 + 25, 1990 + 26, 1990 + 27)
    input_years = years.reshape(years.shape[0], 1)
    prediction_emissions = predict_values(input_years, model_emissions[2])  # predicted values

    # Land Temp predictions
    # predicting values for 2015, 2016 and 1017
    predicted_temp = predict_values(input_years, model_land_temp[2])
    # printing the predictions
    print(' ')
    print(f'Canadas Predicted Co2 emissions for 2015, 2016 and 2017 are '
          f'{prediction_emissions[0][0]}, {prediction_emissions[1][0]}, {prediction_emissions[2][0]}')
    print(f'Canadas Predicted Land Temperature for 2015, 2016 and 2017 are '
          f'{predicted_temp[0][0]}, {predicted_temp[1][0]}, {predicted_temp[2][0]}')
    print(' ')


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['numpy',
                          'linear_regression',
                          'greenhousegases_project',
                          'global_land_temp',
                          'typing'],
        'allowed-io': ['predict_temp_and_emissions'],
        'max-line-length': 150,
        'disable': ['R1705', 'C0200']
    })
