import csv
from datetime import datetime


def read_csv_file(filename, objtype): 
    """ Function takes a CSV file and a class definition as input
    and returns a list of that object type. It ignores the 
    header line of the CSV file. The class constructor needs 
    to handle how the list item is handled."""

    obj_list = []

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            objinstance = objtype(row)
            obj_list.append(objinstance)


    return obj_list


def percent_difference(value, orig):
    return (value - orig) / float(orig)


class AppleStockPrice:
    """ Class to hold the stock price"""
    def __init__(self,listing):
        self.date_ = datetime.strptime(listing[0], "%Y-%m-%d")
        self.open_ = float(listing[1])
        self.high_ = float(listing[2])
        self.low_ = float(listing[3])
        self.close_ = float(listing[4])
        self.volume_ = int(listing[5])
        self.adjclose_ = float(listing[6])


class NasdaqPrice:
    """ Class to hold the NASDAQ price"""
    def __init__(self,listing):
        self.date_ = datetime.strptime(listing[0], "%Y-%m-%d")
        self.open_ = float(listing[1])
        self.high_ = float(listing[2])
        self.low_ = float(listing[3])
        self.close_ = float(listing[4])
        self.volume_ = int(listing[5])
        self.adjclose_ = float(listing[6])


class FitnessDataObject:
    """ Data used to evaluate the fitness of the evolved model """

    def __init__(self):
        self.data = {}

    def add_signal(self, name, value = 0.0):
        if type(name) is str and name not in self.data:
            self.data[name] = value
        else:
            print "Signal name isn't a string"

    def delete_signal(self, name):
        if type(name) is str and name in self.data:
            del self.data[name]
        else:
            print "Signal name isn't a string or signal doesn't exist"

    def get_signals(self):
        return self.data.keys()

    def add_signals(self, names):
        if names:
            for name in names:
                self.add_signal(name)

    def put_value(self, signal_name, value):
        self.data[signal_name] = value

    def get(self, signal_name):
        return self.data[signal_name]


class DataHandler:


    def get_dataset(self, file_class):
        apple_stock_prices = read_csv_file(file_class[0][0], file_class[0][1])
        nasdaq_stock_prices = read_csv_file(file_class[1][0], file_class[1][1])
        dataset = []


        for i in xrange(1, len(apple_stock_prices)):

            model = FitnessDataObject()
            open_diff = percent_difference(apple_stock_prices[i].open_, apple_stock_prices[i-1].open_)
            high_diff = percent_difference(apple_stock_prices[i].high_, apple_stock_prices[i-1].high_)
            low_diff = percent_difference(apple_stock_prices[i].low_, apple_stock_prices[i-1].low_)
            close_diff = percent_difference(apple_stock_prices[i].close_, apple_stock_prices[i-1].close_)
            volume_diff = percent_difference(apple_stock_prices[i].volume_, apple_stock_prices[i-1].volume_)
            adjclose_diff = percent_difference(apple_stock_prices[i].adjclose_, apple_stock_prices[i-1].adjclose_)
            #dates_ = apple_stock_prices[i].date_

            model.add_signal("delta_open", open_diff)
            model.add_signal("delta_high", high_diff)
            model.add_signal("delta_low", low_diff)
            model.add_signal("delta_close", close_diff)
            model.add_signal("delta_volume", volume_diff)
            model.add_signal("delta_adjclose", adjclose_diff)
            # model.add_signal("date", dates_)
            dataset.append(model)
            
        for i in xrange(1, len(nasdaq_stock_prices)):
            
            model = FitnessDataObject()
            open_diff = percent_difference(nasdaq_stock_prices[i].open_, nasdaq_stock_prices[i-1].open_)
            high_diff = percent_difference(nasdaq_stock_prices[i].high_, nasdaq_stock_prices[i-1].high_)
            low_diff = percent_difference(nasdaq_stock_prices[i].low_, nasdaq_stock_prices[i-1].low_)
            close_diff = percent_difference(nasdaq_stock_prices[i].close_, nasdaq_stock_prices[i-1].close_)
            volume_diff = percent_difference(nasdaq_stock_prices[i].volume_, nasdaq_stock_prices[i-1].volume_)
            adjclose_diff = percent_difference(nasdaq_stock_prices[i].adjclose_, nasdaq_stock_prices[i-1].adjclose_)

            #print nasdaq_stock_prices[i].volume_
            #print nasdaq_stock_prices[i-1].volume_
            #print  (nasdaq_stock_prices[i].volume_ -  nasdaq_stock_prices[i-1].volume_) / float(nasdaq_stock_prices[i -1].volume_)



            #volume_diff = 100 *(nasdaq_stock_prices[i].volume_ - nasdaq_stock_prices[i-1].volume_) /  nasdaq_stock_prices[i - 1].volume_
            #print volume_diff
            #dates_ = nasdaq_stock_prices[i].date_


            model.add_signal("delta_nasdaq_open", open_diff)
            model.add_signal("delta_nasdaq_high", high_diff)
            model.add_signal("delta_nasdaq_low", low_diff)
            model.add_signal("delta_nasdaq_close", close_diff)
            model.add_signal("delta_nasdaq_volume", volume_diff)
            model.add_signal("delta_nasdaq_adjclose", adjclose_diff)
            dataset.append(model)

        return dataset

    def __init__(self, files):
        file_class = [(files[0] , AppleStockPrice), (files[1] , NasdaqPrice)]
        self.dataset = self.get_dataset(file_class)


    def signal_ranges(self):
        signal_ranges = []
        if self.dataset != None:
            for signal in self.dataset[0].get_signals():
                l = map(lambda x:x.get(signal), self.dataset)
                min_max = (min(l), max(l))
                signal_ranges.append(min_max)
        else:
            print "Dataset is None"
        return signal_ranges


    def get_signal_list(self):
        signal_data = []
        for i in xrange(len(self.dataset)):
            vals = []
            for signal in self.dataset[i].get_signals():
                val = self.dataset[i].get(signal)
                vals.append(val)
            signal_data.append(vals)
        return signal_data
