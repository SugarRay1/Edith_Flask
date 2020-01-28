import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xlrd
import xlwt
import os


# st 财务鉴别 模型
def main():
    data = pd.read_csv('../data/train_data/train_data_1.csv', encoding='GB18030')
    x = data.iloc[:, 3:-1]  # x: x1-x9 特征数据
    y = data.iloc[:, -1]  # y: FAIL 目标数据

    # Create a basic model instance
    model = create_model()

    checkpoint_path = "../data/checkpoints_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # Create checkpoint callback
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1, period=5)

    history = model.fit(x, y, epochs=200, callbacks=[cp_callback])  # 训练


# Returns a short sequential model
def create_model():
    model = tf.keras.Sequential()  # 顺序模型
    model.add(tf.keras.layers.Dense(6, input_shape=(9,), activation='relu'))
    model.add(tf.keras.layers.Dense(6, activation='relu'))
    model.add(tf.keras.layers.Dense(6, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))  # sigmoid在逻辑回归中使用
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])  # bin:二元交叉熵 acc：正确率
    return model


if __name__ == "__main__":
    main()
