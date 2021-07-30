from neural_network.include.neural import Neural
import matplotlib.pyplot as plt


def run():
    type_ids = [38]
    count_depth = 30
    count_prediction = 30
    count_history = 250
    shift_days = 0
    num_epochs = 500
    main_weight = 2000
    layers = [[128, "relu"], [d, "relu"], [32, "relu"]]
    currency = list()
    epoch = list()

    neural = Neural(type_ids, main_weight, count_depth, count_prediction, count_history, shift_days, num_epochs, layers)
    neural.run()

    #for i in range(5, 60):
    #    num_epochs = i*10
    #    print(num_epochs)
    #    neural = Neural(type_ids, main_weight, count_depth, count_prediction, count_history, shift_days, num_epochs, layers)
    #    cur = neural.run()
    #
    #    currency.append((cur[0] + cur[1] + cur[2]) / 3)
    #    epoch.append(num_epochs)

    #plt.plot(epoch, currency, 'bo', label='currency avg')
    #plt.legend()
    #plt.show()


