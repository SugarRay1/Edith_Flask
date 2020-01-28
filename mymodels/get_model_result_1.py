import pandas as pd
import os
import mymodels.train_model_1 as model_1


def main():
    data = pd.read_csv('../userdata/test_data_1.csv', encoding='GB18030')
    test_x = data.iloc[:, -9:]  # x: x1-x9 特征数据
    # test_y = data.iloc[:, -1]  # y: FAIL 目标数据
    print(test_x)

    # 检验
    checkpoint_path = "../data/checkpoints_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    model = model_1.create_model()

    print()
    print("读取前：")
    print(model.predict_classes(test_x))

    print()
    print("读取后：")
    model.load_weights(checkpoint_path)
    print(model.predict_classes(test_x))
    print(model.predict_classes(test_x).tolist())
    print(model.predict_classes(test_x)[0])
    print(type(model.predict_classes(test_x).tolist()))


def get_result(test_x):
    # 检验
    checkpoint_path = "data/checkpoints_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    model = model_1.create_model()
    model.load_weights(checkpoint_path)
    datas = model.predict_classes(test_x)

    return datas


if __name__ == "__main__":
    main()
