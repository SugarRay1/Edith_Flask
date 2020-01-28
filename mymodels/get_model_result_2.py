import pandas as pd
import os
import mymodels.train_model_2 as model_2


def main():
    data = pd.read_csv('../userdata/test_data_2.csv', encoding='GB18030')
    test_x = data.iloc[:, -9:]  # x: x1-x9 特征数据
    # test_y = data.iloc[:, -1]  # y: FAIL 目标数据
    print(test_x)

    # 检验
    checkpoint_path = "../data/checkpoints_2/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    model = model_2.create_model()

    print()
    print("读取前：")
    print(model.predict(test_x))

    print()
    print("读取后：")
    model.load_weights(checkpoint_path)
    print(model.predict(test_x))
    print(model.predict_classes(test_x))
    # print(model.predict(test_x).tolist())
    # print(model.predict(test_x)[0])
    print(type(model.predict(test_x)))
    print(type(model.predict(test_x).tolist()))

    # print((model.predict(test_x) * 100).tolist()[0])

    data_str = ",".join(map(str, (model.predict(test_x) * 100)[0]))
    print(data_str)
    print(type(data_str))
    # 转成四个float
    print(data_str.split(","))
    print(type(data_str.split(",")[0]))
    print(float(data_str.split(",")[0]))
    print(type(float(data_str.split(",")[0])))


def get_alarm_result(test_x):
    # 检验
    checkpoint_path = "data/checkpoints_2/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    model = model_2.create_model()
    model.load_weights(checkpoint_path)
    datas = (model.predict(test_x) * 100)[0]

    return datas.tolist()


if __name__ == "__main__":
    main()
