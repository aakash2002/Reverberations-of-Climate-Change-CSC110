"""
This file will act as a library to train a liner model
to our data for future predictions.

Resources:
- https://towardsdatascience.com/linear-regression-using-python-b136c91bf0a2
- https://matplotlib.org/devdocs/contents.html
"""

import matplotlib.pyplot as plt
import numpy as np


# for only this files use
def predict(x: np.array, weights: np.array) -> np.array:
    """Returns the prediction made by the line, by passing
    in the value of x in equation y = theta_1*x + theta_0"""
    return np.dot(x, weights)


# for public use
def predict_values(x: np.array, weights: np.array) -> np.array:
    """Returns the prediction made by the line, by passing
    in the value of x in equation y = theta_1*x + theta_0"""
    x = np.insert(x, 0, np.array([1]), axis=1)
    return np.dot(x, weights)


def cost(x: np.array, y: np.array, weights: np.array) -> np.array:
    """Return the cost of the model by calculating the average squared difference in the
    predicted and actual values

    @param x: array of values of predictor variable of our model
    @param y: array of values of dependent variable corresponding to the values in x
    @param weights: array of slope and intercept of the line
    @return: the cost of the model
    """
    m = x.shape[0]  # total samples in the array

    y_hat = predict(x, weights)  # predicted values

    residual = y_hat - y  # difference in the actual and predicted values

    return np.sum(np.square(residual)) / (2 * m)


def train(x: np.array, y: np.array, iterations: int, learning_rate: float) -> list:
    """The function would calculate the gradients of the randomly initialized weight and bias
    and change them according to the gradient and the learning rate. This process is repeated
    <iterations> times, and return the trained weights. The aim is to reduce the cost of these
    parameters.

    @param x: array of values of predictor variable of our model
    @param y: array of values of dependent variable corresponding to the values in x
    @param iterations: number of times we want to train the model on our dataset
    @param learning_rate: the learning  rate of the model
    @return: list containing weights and cost_history

    Preconditions:
    - x.shape = [no. of rows, no. o columns]
    - y.shape = [no. of rows, 1]
    - iterations >= 0
    - learning rate >= 0
    """

    x = np.insert(x, 0, np.array([1]), axis=1)

    m = x.shape[0]  # total samples in the array

    weights = np.zeros((x.shape[1], 1))  # initialize weights

    cost_history = []  # will store cost after every epoch

    for _ in range(iterations):
        y_hat = predict(x, weights)  # predicted values

        residual = y_hat - y  # difference in the actual and predicted values

        gradient = np.dot(x.T, residual)

        weights -= (learning_rate / m) * gradient

        cost_history.append(cost(x, y, weights))

    return [weights, np.array(cost_history)]


def plot_statistics(x: np.array, y: np.array, weights: np.array, cost_history: np.array, reg_line: bool = False) -> None:
    """
    Plot the line and the data-points in one plot and cost on another plot

    @param x: array of values of predictor variable of our model
    @param y: array of values of dependent variable corresponding to the values in x
    @param weights: array of slope and intercept of line
    @param cost_history: array of costs of the model after each iteration of training the model
    @param reg_line: if we want to draw a regression line
    """

    if reg_line:
        plt.figure(1)
        plt.scatter(x, y)

        xs = np.insert(x, 0, np.array([1]), axis=1)

        y_hat = np.dot(xs, weights)  # predicted values

        plt.plot(x, y_hat, color='r')

    plt.figure(2)
    plt.plot(range(cost_history.shape[0]), cost_history)
    plt.title("Cost graph",
              fontsize=10,
              fontweight="bold")

    plt.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['matplotlib.pyplot',
                          'numpy'],
        'allowed-io': [],
        'max-line-length': 150,
        'disable': ['R1705', 'C0200']
    })
