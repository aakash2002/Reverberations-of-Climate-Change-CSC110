"""
This file will be used to handle all the data
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pprint import pprint
import csv
import ast


class Dataset:
    """
    The class stores a dataset and has functions
    to transform the dataset.

    Representation Invariants:
    - self._filepath != ''
    - all(datatype in [int, float, str, datetime, list, bool] for datatype in self._types)

    Private Instance Attributes:
    - _dataset : consist of the dataset
    - _filepath: path to the dataset
    """

    _filepath: str
    _dataset: List[List]

    def __init__(self, filepath: Optional[str] = None,
                 types: Optional[list] = None,
                 dataset: Optional[List[list]] = None) -> None:
        """Initialize a new dataset

        @param filepath: path of the dataset
        @param dataset: if we do not want to load from filepath and already have a dataset
        @param types: data types to which columns of dataset need to be converted

        Preconditions:
        - (filepath or dataset) and not (filepath and dataset)
        """
        if filepath:
            self._filepath = filepath
            self.load_data()

            if types:
                self.transform(types)

        if isinstance(dataset, list):
            self._dataset = dataset

    def get(self) -> List[List]:
        """Return self._dataset"""
        return self._dataset

    def load_data(self) -> None:
        """
        Load the data as list of lists and store it in
        self._dataset
        """
        with open(self._filepath) as file:
            reader = csv.reader(file)

            next(reader)  # skip the header row

            self._dataset = [list(row) for row in reader]

    def transform(self,
                  types: list,
                  year_only: Optional[bool] = False,
                  day_only: Optional[bool] = False) -> None:
        """
        Convert the columns of self._dataset to respective data types.

        @param types: list of datatype objects
        @param year_only: if we just want the year from datetime object
        @param day_only: if we just want the day from datetime object
        """
        self._dataset = [convert_datatype_for_row(row, types, year_only, day_only)
                         for row in self._dataset]

    def filter_by_value(self,
                        column: int,
                        values: list) -> None:
        """
        Change self.dataset to a filtered dataset, with rows in which column <column>
        has a value in <value> list

        @param column: the column with which we want to filter
        @param values: the list of values with column could have
        """
        self._dataset = [row for row in self._dataset
                         if row[column] in values]

    def filter_by_function(self,
                           filter_function: Any) -> None:
        """
        Change self._dataset to a filtered dataset, with rows that satisfies the
        predicate function <filter_function>.

        @param filter_function: the predicate function used for filtering
        """

        self._dataset = [row for row in self._dataset
                         if filter_function(row)]

    def remove_na(self) -> None:
        """Change self._dataset to a dataset with all the rows with
        None values and empty strings removed
        """
        self.filter_by_function(has_na)

    def select(self, selected_columns: List[int]) -> None:
        """Change self._dataset to a dataset with only the columns in the
         <selected_columns> list

        @param selected_columns: the columns we want to keep
        """
        self._dataset = [[row[column] for column in selected_columns] for row in self._dataset]

    def delete(self, selected_columns: List[int]) -> None:
        """Change self._dataset to a dataset with all the columns
        in <selected_columns> removed

        @param selected_columns: the columns we want to delete
        """
        self._dataset = [[row[column] for column in range(len(row))
                          if column not in selected_columns] for row in self._dataset]

    def head(self, nrows: Optional[int] = 5) -> None:
        """Print the first <n> rows of  self._dataset"""
        print_data = []
        for i in range(nrows):
            print_data.append(self._dataset[i])
        pprint(print_data)

    def unique(self, column: int) -> set:
        """Return a list of unique values for the column <column> in self._dataset"""
        return {row[column] for row in self._dataset}

    def calc_avg_col(self, column: int) -> float:
        """Return the average for a column of self._dataset

        @param column: the column for which we want the average
        @return: average of the column <column>
        """
        return sum([row[column] for row in self._dataset]) / len(self._dataset)

    def extract_column(self, column: int) -> list:
        """Return a column of self._dataset"""
        return [row[column] for row in self._dataset]

    def push(self, row: list) -> None:
        """Add row to the dataset"""
        self._dataset.append(row)

    def calculate_average(self,
                          grouping_column: int,
                          avg_column: int,
                          grouping_column_modifier: Optional = None) -> List[List]:
        """The function groups the data by column <grouping column> of the dataset and then
        calculate the average of column <avg_column> for every group and return the list of
        those averages and list of values for grouping column

        @param grouping_column: column with which we would group
        @param avg_column: the column of which we want to compute average
        @param grouping_column_modifier: function to group by modified value of the
                                         grouping column

        @return: List containing the average of column <avg_column> for every group of column
                 <grouping_column>
        """
        values = []
        group = []

        if grouping_column_modifier:
            data = group_by_function(self, grouping_column, grouping_column_modifier)
        else:
            data = group_by_values(self, grouping_column)

        for i in data:
            values.append(data[i].calc_avg_col(avg_column))
            group.append(data[i].get()[0][grouping_column])

        return [group, values]


def group_by_values(dataset: Dataset, column: int, filter_values: Optional = None) -> Dict[str, Dataset]:
    """Group the data by different values of the column <column> and return a dict
    with dataset objects of observations for a specific value of the column.

    @param dataset: the dataset by which we want tp group
    @param column: the column number to group by
    @param filter_values: set of values for column we want to keep
    @return: dict containing datasets with different values for the column
    """
    values_to_keep = dataset.unique(column)

    if filter_values:
        values_to_keep = values_to_keep.intersection(filter_values)

    dict_so_far = {value: Dataset(dataset=[]) for value in values_to_keep}

    for row in dataset.get():
        if row[column] in dict_so_far:
            dict_so_far[row[column]].push(row)

    return dict_so_far


def group_by_function(dataset: Dataset,
                      column: int, filter_function: Any,
                      filter_values: Optional = None) -> Dict[str, Dataset]:
    """Group the data by different values of the column <column> applied to the filter_function
        and return an dict with Dataset objects of observations for a specific value of the column
        applied to the filter function.

        @param dataset: the dataset by which we want tp group
        @param column: the column number to group by
        @param filter_function: function to get values from column
        @param filter_values: set of values for column we want to keep
        @return: dict containing datasets with different values for the column
        """

    temp_data = []
    for row in dataset.get():
        temp_data.append(row + [filter_function(row[column])])

    all_values = Dataset(dataset=temp_data)

    values_to_keep = all_values.unique(len(all_values.get()[0]) - 1)

    if filter_values:
        values_to_keep = values_to_keep.intersection(filter_values)

    dict_so_far = {value: Dataset(dataset=[]) for value in values_to_keep}

    for row in all_values.get():
        if row[len(dataset.get()[0])] in dict_so_far:
            dict_so_far[row[len(dataset.get()[0])]].push(row)

    return dict_so_far


def has_na(values: list) -> bool:
    """Return False if there is even one None value or Empty string
     in the <values> list, and True otherwise"""
    return not any(element is None or element == '' for element in values)


def convert_to_datetime(dt: str) -> datetime:
    """Convert a string to datetime format and
    return datetime object

    Preconditions:
    - dt is in valid datetime format
    """
    return datetime.fromisoformat(dt)


def convert_datatype_for_row(values: list,
                             types: list,
                             only_year: Optional[bool] = False,
                             day_only: Optional[bool] = False) -> list:
    """
    Returns a list with every element of the list converted
    into the appropriate datatype passed in the types.

    Appropriate types:
    - str
    - int
    - float
    - datetime
    - bool
    - list

    @param values: single row of the dataset
    @param types: type to change each value in the row
    @param only_year: if we just want the year from datetime object
    @param day_only: if we just want the day from datetime object

    Preconditions:
    - len(values) == len(types)
    """

    list_so_far = []  # ACCUMULATOR: stores the new values

    for index in range(len(values)):
        if types[index] != datetime and types[index] != list:
            list_so_far.append(types[index](values[index]))

        elif types[index] == datetime:
            if only_year:
                list_so_far.append(convert_to_datetime(values[index]).year)
            elif day_only:
                list_so_far.append(convert_to_datetime(values[index]).day)
            else:
                list_so_far.append(convert_to_datetime(values[index]))
        elif types[index] == list:
            list_so_far.append(ast.literal_eval((values[index])))

    return list_so_far


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pprint',
                          'datetime',
                          'csv',
                          'ast',
                          'typing'],
        'allowed-io': ['load_data'],
        'max-line-length': 150,
        'disable': ['R1705', 'C0200']
    })
