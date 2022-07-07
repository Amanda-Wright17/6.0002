# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # x = pylab.array(x)
    # y = pylab.array(y)
    models = [pylab.polyfit(x, y, deg) for deg in degs]
    return models


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mean = pylab.mean(y)
    numerator = (y - estimated)**2
    denominator = (y - mean)**2
    r_squared = 1 - (pylab.sum(numerator) / pylab.sum(denominator))
    
    return r_squared
    

def predicted_values(x, coefficients):
    """"
    For each regression model, compute the expected values.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of the N sample points
        coefficients: a pylab array storing the coefficients of a polynomial
        
        Returns:
            a pylab array of predicted values for each x
    """
    predicted_values = 0
    for i, coef in enumerate(coefficients):
        print(i, coef)
        predicted_values += coef * x**(len(coefficients) - (i+1))
    return predicted_values


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    print(f"eval models, x values {x}")
    print(f"eval models, y values {y}")
    # iterate over each model in list of regression models
    for model in models:
        # create line of best fit using coefficients
        y_predicted = predicted_values(x, model)
        print(f"eval models, y predicted {y_predicted}")
        # calculate r_squared
        r_sq = r_squared(y, y_predicted)
        
        pylab.figure()
        
        # add points to graph
        pylab.plot(x, y, 'bo', label="Data Points")
        # plot line of best fit
        pylab.plot(x, y_predicted, 'r-', label = "Model")
        pylab.legend()
        # add labels to graph
        pylab.xlabel("Years")
        pylab.ylabel("Degrees Celsius")
        
        # if len(model) == 2, calculate SE/slope
        if len(model) == 2:
            se_slope = se_over_slope(x, y, y_predicted, model)
            pylab.title(f'Degree of fit: {len(model) - 1} \n R2: {r_sq} \n Ratio of SE: {se_slope}.')
        
        else:
           pylab.title(f'Degree of fit: {len(model) - 1} \n R2: {r_sq}.')
        pylab.show()

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    city_avg = 0
    total_national_averages = []
    
    # iterate over each year
    for year in years:
        all_cities_avgs = []
        # iterate over each city
        for city in multi_cities:
            
            # add each city's yearly average temp to a list
            city_avg = pylab.mean(climate.get_yearly_temp(city, year))
            all_cities_avgs.append(city_avg)
            
        # find the average for that year and add that to a list
        total_national_averages.append(sum(all_cities_avgs) / len(all_cities_avgs))
    
    # once you have each years averages in a list, turn into a pylab array
    total_national_averages = pylab.array(total_national_averages)
    return total_national_averages    

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_averages = []
    for i in range(1, len(y) + 1):
        if i < window_length:
            moving_averages.append(pylab.average(y[:i]))
        else:
            moving_averages.append(pylab.average(y[i - window_length : i]))
    return pylab.array(moving_averages)
    
def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    rmse = pylab.sqrt(pylab.sum((y-estimated)**2) / len(y))
    return rmse

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    annual_std_devs = []
    for year in years:
        cities_yearly_temps = []
        for city in multi_cities:
            yearly_temp = climate.get_yearly_temp(city, year)
            cities_yearly_temps.append(yearly_temp)
        cities_yearly_temps = pylab.array(cities_yearly_temps)
        daily_means = cities_yearly_temps.mean(axis=0)
        std_dev = pylab.std(daily_means)
        annual_std_devs.append(std_dev)
    annual_std_devs = pylab.array(annual_std_devs)
    return annual_std_devs                   

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        # create line of best fit using coefficients
        y_predicted = predicted_values(x, model)
        print(f"eval models, y predicted {y_predicted}")
        # calculate r_squared
        rmse_value = rmse(y, y_predicted)
        
        pylab.figure()
        
        # add points to graph
        pylab.plot(x, y, 'bo', label="Data Points")
        # plot line of best fit
        pylab.plot(x, y_predicted, 'r-', label = "Model")
        pylab.legend()
        # add labels to graph
        pylab.xlabel("Years")
        pylab.ylabel("Degrees Celsius")
        pylab.title(f'Degree of fit: {len(model) - 1} \n RMSE: {rmse_value}.')
        pylab.show()


if __name__ == '__main__':


    # Part A.4
    
    #NEW YORK CITY, JANUARY 10
    # new_york_test = Climate("data.csv")
    # x = pylab.array(TRAINING_INTERVAL)
    # y = [new_york_test.get_daily_temp("NEW YORK", 1, 10, year) for year in x]
    # y = pylab.array(y)
    # models = generate_models(x, y, [1])
    # evaluate_models_on_training(x, y, models)
  
    # NEW YORK CITY, ANNUAL
    # annual_test = Climate('data.csv')
    # x_annual = pylab.array(TRAINING_INTERVAL)
    # y_annual = [pylab.mean(annual_test.get_yearly_temp("NEW YORK", year)) for year in x_annual]
    # annual_model = generate_models(x_annual, y_annual, [1])
    # evaluate_models_on_training(x_annual, y_annual, annual_model)
    
    
    # Part B
    # NATIONAL YEARLY AVERAGE
    # test3 = Climate('data.csv')
    # test3_years = pylab.array(TRAINING_INTERVAL)
    # test3_national_avg = gen_cities_avg(test3, CITIES, TRAINING_INTERVAL)
    # test3_model = generate_models(test3_years, test3_national_avg, [1])
    # evaluate_models_on_training(test3_years, test3_national_avg, test3_model)    

    # Part C
    # test4 = Climate('data.csv')
    # test4_years = pylab.array(TRAINING_INTERVAL)
    # national_yearly_averages = gen_cities_avg(test4, CITIES, TRAINING_INTERVAL)
    # test4_moving_avg = moving_average(national_yearly_averages, 5)
    # test4_model = generate_models(test4_years, test4_moving_avg, [1])
    # evaluate_models_on_training(test4_years, test4_moving_avg, test4_model)

    # Part D.2
    # test5 = Climate('data.csv')
    # test5_years = pylab.array(TRAINING_INTERVAL)
    # test5_national_avgs = gen_cities_avg(test5, CITIES, TRAINING_INTERVAL)
    # test5_moving_avgs = moving_average(test5_national_avgs, 5)
    # training_models = generate_models(test5_years, test5_moving_avgs, [1, 2])
    # evaluate_models_on_training(test5_years, test5_moving_avgs, training_models)

    # # PREDICTION
    # test_national_avgs = gen_cities_avg(test5, CITIES, TESTING_INTERVAL)
    # test_data_moving_avgs = moving_average(test_national_avgs, 5)
    
    # evaluate_models_on_testing(pylab.array(TESTING_INTERVAL), test_data_moving_avgs, training_models)
    # Part E
    climate = Climate('data.csv')
    std_dev = gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
    moving_avg = moving_average(std_dev, 5)
    models = generate_models(pylab.array(TRAINING_INTERVAL), moving_avg, [1])
    evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), moving_avg, models)
