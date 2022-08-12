from unicodedata import name
import warnings

warnings.filterwarnings("ignore")

from fbprophet import Prophet
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import ParameterGrid
from prophet.diagnostics import cross_validation, performance_metrics
import pickle

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


class ProphetTrain:
    def __init__(self, predict_freq_num, data: pd.DataFrame=None, holidays=None):
        self.data = data 
        self.trainData = None 
        self.params = {
            "holidays": holidays,
            "yearly_seasonality": False,
            "daily_seasonality": True,
            "holidays_prior_scale": 0.05,
        }
        self.mape = np.inf
        self.model = None
        self.grid_search_params_path = None
        self.predict_freq_num = predict_freq_num
        self.freq = "d"
        self.predict_data = None

    def get_food_sale(self, menu_name, cap: int = 6):
        """
        取出单个菜谱的销量数据
        """
        date_col = list(self.data.columns)[0]
        food_data = self.data[[date_col, menu_name]]
        food_data.columns = ["ds", "y"]
        self.trainData = food_data.dropna().assign(ds=lambda x: pd.to_datetime(x["ds"]), cap=cap)

    @property
    def train_data_control(self):
        return 1 if len(self.data) > 14 else 0  


    def train_predict_calculation(self, menu_name, iter = 3):
        if not self.train_data_control:
            raise Exception("保持训练数据大于14条") 
        self.model = Prophet(**self.params) 
        self.model.add_seasonality(name="monthly", period=30.5, fourier_order=5)
        self.model.add_seasonality(
            name="weekly", period=7, fourier_order=3, prior_scale=0.1
        )  
        self.get_food_sale(menu_name=menu_name) 
        self.model.fit(self.trainData, iter=iter) 
        future = self.model.make_future_dataframe(
            freq=self.freq, periods=self.predict_freq_num
        ) 
        self.predict_data = self.model.predict(future)[["ds", "yhat_lower", "yhat_upper", "yhat"]].set_index("ds")
        self.predict_data[menu_name] = self.predict_data['yhat'].apply(
            lambda x: np.round(x, 0) if x > 0 else 0
        )
        mape_score = np.abs(
            1 - self.predict_data["yhat"].iloc[ : len(self.trainData)] / self.trainData["y"].values
        ) 
        return np.quantile(mape_score, 0.8)  

if __name__ == '__main__':
    df_sale = pd.read_excel(r'C:\Users\yan.zy\Desktop\WorkStation\2022-06-20 净菜销量预测\input\sale_data.xlsx')
    df_activity = pd.read_excel(r'C:\Users\yan.zy\Desktop\WorkStation\2022-06-20 净菜销量预测\input\activity.xlsx')
    ProphTrainS = ProphetTrain(
                predict_freq_num=int('7'),
                data=df_sale,
                holidays=df_activity,
            ) 
    menu_name = '八宝粥（食万净菜）'
    mape = ProphTrainS.train_predict_calculation(menu_name) 
    print(mape) 
    print(ProphTrainS.predict_data[['ds', menu_name]])







    # def _cv_run(self):
    #     if self.data_size < 14:
    #         raise Exception("数据量不足，请保证数据航速大于14条")
    #     self.model = Prophet(**self.params)
    #     self.model.add_seasonality(name="monthly", period=30.5, fourier_order=5)
    #     self.model.add_seasonality(
    #         name="weekly", period=7, fourier_order=3, prior_scale=0.1
    #     )
    #     self.model.fit(self.data)
    #     cv_result = cross_validation(
    #         self.model,
    #         #             initial = 100, period = 100,
    #         horizon="30 days",
    #         #             units = 'days'
    #         #             f'{self.predict_freq_num}{self.freq}',
    #         #             f'{self.predict_freq_num}{self.freq}'
    #     )
    #     return performance_metrics(cv_result, metrics=["mape"])["mape"][0]

    # def run(self, show: int = 0, retrain=False):
    #     """
    #     根据当前参数生成模型
    #     :param retrain: 是否根据当前参数重新生成模型
    #     :param show:
    #     0:  不保存图片及预测结果 也 不展示图片
    #     1: 展示图片
    #     2: 保存图片及预测结果
    #     3: 保存图片及预测结果 也 展示图片
    #     :return:
    #     """
    #     print(self.data_size)
    #     if self.data_size < 14:
    #         raise Exception("数据量不足，请保证数据行数大于14条")
    #     if retrain or self.model is None:
    #         self.model = Prophet(**self.params)
    #         self.model.fit(self.data, iter=2)
    #     future = self.model.make_future_dataframe(
    #         freq=self.freq, periods=self.predict_freq_num
    #     )
    #     forecast = self.model.predict(future)
    #     if show & 0b01:
    #         #             self.model.plot(forecast).show()  # 绘制预测效果图
    #         #             self.model.plot_components(forecast).show()  # 绘制成分趋势图
    #         pass
    #     if show & 0b10:
    #         print(1)
    #         self.predict_data = forecast[["ds", "yhat_lower", "yhat_upper", "yhat"]]
    #         self.predict_data = self.predict_data.assign(
    #             yhat=lambda x: np.round(x["yhat"], 0)
    #         )
    #     #             self.predict_data.to_csv(f'csv/{self.name}.csv', index=False)
    #     #             self.model.plot(forecast).savefig(f"img/{self.name}-scatter.png")  # 绘制预测效果图
    #     #             self.model.plot_components(forecast).savefig(f"img/{self.name}-trend.png")  # 绘制成分趋势图
    #     mape_score = np.abs(
    #         1 - forecast["yhat"].iloc[: self.data.shape[0]] / self.data["y"].values
    #     )
    #     return np.quantile(mape_score, 0.8)

    # @property
    # def get_predict_df(self):
    #     future = self.model.make_future_dataframe(
    #         freq=self.freq, periods=self.predict_freq_num
    #     )  # 建立数据预测框架，数据粒度为天，预测步长为一年
    #     forecast = self.model.predict(future)
    #     return forecast

    # def grid_search(self, use_cv=True, save_result=True):
    #     """
    #     结合cv进行网格寻参，cv方式网格寻参很慢，一般建议先使用非网格方式，待参数调整完毕再使用cv验证。
    #     :param save_result:
    #     :return:
    #     """
    #     changepoint_range = [i / 10 for i in range(3, 10)]
    #     # seasonality_mode = ['additive', 'multiplicative']
    #     # seasonality_prior_scale = [0.05, 0.1, 0.5, 1, 5, 10, 15]
    #     holidays_prior_scale = [0.05, 0.1, 0.5, 1, 5, 10, 15]
    #     # for sm in seasonality_mode:
    #     for cp in changepoint_range:
    #         # for sp in seasonality_prior_scale:
    #         for hp in holidays_prior_scale:
    #             params = {
    #                 #                     "seasonality_mode": sm,
    #                 "changepoint_range": cp,
    #                 #                     "seasonality_prior_scale": sp,
    #                 "holidays_prior_scale": hp,
    #                 "holidays": self.params.get("activity"),
    #             }
    #             score = self._cv_run() if use_cv else self.run()
    #             if self.mape > score:
    #                 self.mape = score
    #                 self.params = params
    #     if save_result:
    #         future = self.model.make_future_dataframe(
    #             freq=self.freq, periods=self.predict_freq_num
    #         )
    #         forecast = self.model.predict(future)
    #         forecast[["ds", "yhat_lower", "yhat_upper", "yhat"]].iloc[
    #             -self.predict_freq_num :
    #         ].to_csv(f"csv/{self.name}.csv", index=False)
    #         #             self.model.plot(forecast).savefig(f"img/{self.name}-scatter.png")  # 绘制预测效果图
    #         #             self.model.plot_components(forecast).savefig(f"img/{self.name}-trend.png")  # 绘制成分趋势图
    #         self.save_model()
    #     print(f"score:{self.mape}\nparams:{self.params}")
    #     return self

    # def save_model(self):
    #     with open(f"model/{self.name}.pkl", "wb") as fp:
    #         pickle.dump(self, fp)

    # @staticmethod
    # def load_model(name):
    #     with open(f"model/{name}.pkl", "rb") as fp:
    #         return pickle.load(fp)
