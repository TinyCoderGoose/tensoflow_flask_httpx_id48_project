import datetime
import os
import random

import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow import keras
import numpy as np
from tensorflow_core.python.training.rmsprop import RMSPropOptimizer
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard

#数据归一化
def pretreatment(train_data,train_labels,test_data,test_labels):
    order = np.argsort(np.random.random(train_labels.shape))
    train_data = train_data[order]
    train_labels = train_labels[order]
    mean = train_data.mean(axis=0)
    std = train_data.std(axis=0)
    train_data = (train_data-mean)/std
    test_data = (test_data-mean)/std
    return (train_data,train_labels),(test_data,test_labels)

#创建模型
def build_model(train_data):
    model = keras.Sequential([
        keras.layers.Dense(64,activation=tf.nn.relu,input_shape=(train_data.shape[1],)),
        keras.layers.Dense(64,activation=tf.nn.relu),
        keras.layers.Dense(1)
    ])
    optimizer = RMSPropOptimizer(0.001)
    model.compile(loss='mse',optimizer=optimizer,metrics=['mae'])

    return model
#回调函数
class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if epoch % 50 == 0:print('')
        print('>>',end='')
#显示
def plot_history(history):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [1000$]')
    plt.plot(history.epoch,np.array(history.history['mae']),label='Train Loss')
    plt.plot(history.epoch,np.array(history.history['val_mae']),label='Val Loss')
    plt.legend()
    plt.ylim([0,5])
    plt.show()

#自定义训练函数
def my_fit(model,train_data,train_labels,EPOCHS):
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20)
    history = model.fit(train_data, train_labels, epochs=EPOCHS, validation_split=0.2, verbose=0,callbacks=[early_stop,PrintDot()])
    print()
    # plot_history(history)
    return model

# 3 构造批数据
def create_batch_dataset(X, y, train=True, buffer_size=100, batch_size=128):
    batch_data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y))) # 数据封装，tensor类型
    if train: # 训练集
        return batch_data.cache().shuffle(buffer_size).batch(batch_size)
    else: # 测试集
        return batch_data.batch(batch_size)

def create_dataset(X, y, seq_len=10):
    features = []
    targets = []
    for i in range(0, len(X) - seq_len, 1):
        data = X[i:i + seq_len]  # 序列数据
        label = y[i + seq_len]  # 标签数据
        # 保存到features和labels
        features.append(data)
        targets.append(label)
    # 返回
    return np.array(features), np.array(targets)
if __name__ == '__main__':
    (train_data,train_labels),(test_data,test_labels) = keras.datasets.boston_housing.load_data()
    (train_data, train_labels), (test_data, test_labels) = pretreatment(train_data, train_labels, test_data,
                                                                            test_labels)

    model = build_model(train_data)
    print(type(model))
    model.load_weights('./forecast.h5')
    test_predictions = model.predict(test_data).flatten()
    # model = my_fit(model, train_data, train_labels, 202)
#
# if __name__ == '__main__':
#     (train_data,train_labels),(test_data,test_labels) = keras.datasets.boston_housing.load_data()
#
#     plt.figure(figsize=(16, 8))
#     plt.plot(train_labels, label='Close Price history')
#     plt.show()
#
#     (train_data, train_labels), (test_data, test_labels) = pretreatment(train_data, train_labels, test_data,
#                                                                         test_labels)
#     model = build_model(train_data)
#     model = my_fit(model, train_data, train_labels, 202)
#     test_predictions = model.predict(test_data).flatten()
#     [loss, mae] = model.evaluate(test_data, test_labels, verbose=0)
#     print('\n')
#     for i in range(len(test_labels)):
#         print('真实：%s' % test_labels[i])
#         print('预测：%s' % test_predictions[i])