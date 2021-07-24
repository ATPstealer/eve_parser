from keras import models
from keras import layers
import numpy as np
from eve_parser.models import MarketHistory
import operator


def run():
    #type_ids = [34, 1230, 17471, 17470, 28430, 28432, 28431]
    type_ids = [28846, 28848, 28844, 28850]
    count_depth = 15
    count_history = 250
    shift_days = 5
    num_epochs = 80

    market_history = receive_history(type_ids)
    market_data, market_target = build_data(market_history, type_ids, count_depth, count_history, shift_days)
    market_check_data, market_check_target = build_data(market_history, type_ids, count_depth, shift_days, 0)
    market_predict_data, blank = build_data(market_history, type_ids, count_depth, count_depth, 0)

    model = build_model(market_data)
    model.fit(market_data, market_target, epochs=num_epochs, batch_size=5,
              validation_data=(market_check_data, market_check_target))

    val_mse, val_mae = model.evaluate(market_check_data, market_check_target)
    print(val_mse)
    print(val_mae)

    predict = model.predict(market_predict_data)

    for pre in predict:
        print(pre)


def build_model(market_data):
    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_shape=(market_data.shape[1], market_data.shape[2])))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    model.summary()
    print(model.input_shape)
    return model


def receive_history(type_ids):
    market_history = dict()
    for item_type in type_ids:
        market_history[item_type] = MarketHistory.objects.filter(region_id="10000002", type_id=item_type)
        market_history[item_type] = sorted(market_history[item_type], key=operator.attrgetter('date'))
    return market_history


def build_data(market_history, type_ids, count_depth, count_history, shift_days):
    count_types = len(type_ids)
    market_data = np.arange(count_types * count_history * count_depth, dtype='f').reshape(count_history, count_types * count_depth)
    market_history = receive_history(type_ids)
    start_day = count_depth + count_depth + count_history + shift_days - 1
    end_day = count_depth + count_history + shift_days - 1
    for iteration in range(0, count_history):
        iteration_type = 0
        for item_type in type_ids:
            iteration_date = 0
            if end_day != 0:
                for one_day in market_history[item_type][-start_day:-end_day]:
                    market_data[iteration, iteration_type * count_depth + iteration_date] = one_day.average
                    iteration_date += 1
            else:
                for one_day in market_history[item_type][-start_day:]:
                    market_data[iteration, iteration_type * count_depth + iteration_date] = one_day.average
                    iteration_date += 1
            iteration_type += 1
        start_day -= 1
        end_day -= 1

    print(market_data)

    start_day = count_history + shift_days
    end_day = shift_days
    if count_history == 0:
        return market_data, []
    market_target = np.arange(count_history, dtype='f').reshape(count_history)
    iteration_date = 0
    if end_day != 0:
        for one_day in market_history[type_ids[0]][-start_day:-end_day]:
            market_target[iteration_date] = one_day.average
            iteration_date += 1
    else:
        for one_day in market_history[type_ids[0]][-start_day:]:
            market_target[iteration_date] = one_day.average
            iteration_date += 1

    return market_data, market_target
