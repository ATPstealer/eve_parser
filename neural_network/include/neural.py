from keras import models
from keras import layers
import numpy as np
from eve_parser.models import MarketHistory
import operator


class Neural:

    def __init__(self, type_ids, main_weight, count_depth, count_prediction, count_history, shift_days, num_epochs, layers):
        """
        :param type_ids: IDs items for calculation. 0 - item for predition, 1..* - additional items
        :param main_weight: How many times is the main item more important than the additional
        :param count_depth: days for one data array
        :param count_prediction: days for prediction
        :param count_history: data arrays
        :param shift_days: shift from now
        :param num_epochs: Count of epochs neural network
        :param layers: Layers settings
        """
        self.type_ids = type_ids
        self.count_depth = count_depth
        self.count_prediction = count_prediction
        self.count_history = count_history + 3 - count_history % 3
        self.shift_days = shift_days
        self.num_epochs = num_epochs
        self.main_weight = main_weight
        self.layers = layers
        self.market_history = dict()
        self.count_types = len(self.type_ids)
        self.model = models.Sequential()

    def run(self):
        self.receive_history()
        market_data, market_target = [0, 0, 0], [0, 0, 0]
        for suite in range(0, 3):
            market_data[suite], market_target[suite] = self.build_data(self.count_prediction,
                                                                       int(self.count_history / 3), 2 - suite)
        market_predict_data, blank = self.build_data(0, self.count_prediction, 0)

        val_mse, val_mae = [0, 0, 0], [0, 0, 0]
        #for suite in range(0, 3):
        #    self.build_model(market_data[suite % 3])
        #    self.model.fit(market_data[suite % 3], market_target[suite % 3], epochs=self.num_epochs, batch_size=3)
        #    self.model.fit(market_data[(suite + 1) % 3], market_target[(suite + 1) % 3], epochs=self.num_epochs, batch_size=3)
        #    val_mse[suite], val_mae[suite] = self.model.evaluate(market_data[1], market_target[1])

        self.build_model(market_data[0])
        self.model.fit(market_data[0], market_target[0], epochs=self.num_epochs, batch_size=3)
        self.model.fit(market_data[1], market_target[1], epochs=self.num_epochs, batch_size=3)
        self.model.fit(market_data[2], market_target[2], epochs=self.num_epochs, batch_size=3)

        # print(val_mse, val_mae)
        predict = self.model.predict(market_predict_data)
        for pre in predict:
            print(pre)

    def receive_history(self):
        """ Get market history from database """
        for item_type in self.type_ids:
            self.market_history[item_type] = MarketHistory.objects.filter(region_id="10000002", type_id=item_type)
            self.market_history[item_type] = sorted(self.market_history[item_type], key=operator.attrgetter('date'))

    def build_data(self, count_prediction, count_history, shift_days):
        """
        Function for preparing data for the neural network.
        :param count_prediction: days for prediction
        :param count_history: data arrays
        :param shift_days: shift from now
        :return: numpy arrays withs data and results
        """
        market_data = np.arange(self.count_types * count_history * self.count_depth, dtype='f').\
            reshape(count_history, self.count_types * self.count_depth)
        start_day = self.count_depth + count_prediction + count_history + shift_days - 1
        end_day = count_prediction + count_history + shift_days - 1
        for iteration in range(0, count_history):
            iteration_type = 0
            for item_type in self.type_ids:
                iteration_date = 0
                if end_day != 0:
                    for one_day in self.market_history[item_type][-start_day:-end_day]:
                        market_data[iteration, iteration_type * self.count_depth + iteration_date] = one_day.average
                        if iteration_type != 0:
                            market_data[iteration, iteration_type * self.count_depth + iteration_date] /= self.main_weight
                        iteration_date += 1
                else:
                    for one_day in self.market_history[item_type][-start_day:]:
                        market_data[iteration, iteration_type * self.count_depth + iteration_date] = one_day.average
                        if iteration_type != 0:
                            market_data[iteration, iteration_type * self.count_depth + iteration_date] /= self.main_weight
                        iteration_date += 1

                iteration_type += 1
            start_day -= 1
            end_day -= 1

        start_day = count_history + shift_days
        end_day = shift_days
        if count_history == 0:
            return market_data, []
        market_target = np.arange(count_history, dtype='f').reshape(count_history)
        iteration_date = 0
        if end_day != 0:
            for one_day in self.market_history[self.type_ids[0]][-start_day:-end_day]:
                market_target[iteration_date] = one_day.average
                iteration_date += 1
        else:
            for one_day in self.market_history[self.type_ids[0]][-start_day:]:
                market_target[iteration_date] = one_day.average
                iteration_date += 1

        return market_data, market_target

    def build_model(self, market_data):
        """ Make neural network """
        flag = 1
        for layer in self.layers:
            if flag == 1:
                self.model.add(layers.Dense(layer[0], activation=layer[1], input_shape=(market_data.shape[1], )))
                flag = 0
            else:
                self.model.add(layers.Dense(layer[0], activation=layer[1]))
        self.model.add(layers.Dense(1))
        self.model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
        self.model.summary()
