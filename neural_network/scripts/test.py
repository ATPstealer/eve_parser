from keras.models import Sequential
from keras.layers import Dense
import numpy as np

# загружаем данные с фичами
dataset = np.loadtxt("data.txt", delimiter=",")
# Первые 8 столбцов в примере отвечают за фичи, последний же за класс, разбиваем
X = dataset[:, 0:8]
Y = dataset[:, 8]

# Создаём модель!
model = Sequential()
# Добавляем первый слой Dense, первое число 12 - это количество нейронов,
# input_dim - количество фич на вход
# activation -  функция активации, полулинейная функция max(x, 0)
# именно полулинейные функции позволяют получать нелинейные результаты с минимальными затратами
model.add(Dense(12, input_dim=8, activation='relu'))
# добавляем второй слой с 8ю нейронами
model.add(Dense(8, activation='relu'))
# на выходе при бинарной классификации, функцию активации чаще всего используют sigmoid , реже softmax
# Компилирование модели. binary_crossentropy - опять же не случайно, а т.к. у нас два класса.
# Метрика accuracy используется практически для всех задач классификации
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Наконец дошли до обучения модели, X и Y - понятно,
# epoch - максимальное количество эпох до остановки
# batch_size - сколько объектов будет загружаться за итерацию
model.fit(X, Y, epochs=15, batch_size=10, verbose=2)
# Предсказание
predictions = model.predict(X)