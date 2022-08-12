import wx
import wxCalFrame
import pandas as pd
import Prophet_Predict
import warnings
import datetime
import os
warnings.filterwarnings("ignore")

class CalFrame(wxCalFrame.sale_prediction):
    def __init__(self, parent):
        wxCalFrame.sale_prediction.__init__(self, parent)
        self.df_sale = pd.DataFrame()
        self.df_activity = pd.DataFrame()
        self.predict_days = 51
        self.foods = list()
        self.df_output = pd.DataFrame()
        self.df_output1 = pd.DataFrame()
        self.df_output2 = pd.DataFrame()

    def DataCheck(self, event):
        self.check_data = 0
        # 销量数据
        if not self.file_pick1.GetPath():
            # raise ('请选择历史销量数据！\n '+ '#'*20)
            print('请选择历史销量数据！\n '+ '#'*20)
        elif not (self.file_pick1.GetPath().endswith('csv') or self.file_pick1.GetPath().endswith('xlsx')):
            print('销量数据请选择csv或者xlsx文件！\n ' + '#' * 20)
        else:
            if self.file_pick1.GetPath().endswith('csv'):
                self.df_sale = pd.read_csv(self.file_pick1.GetPath())
            else:
                self.df_sale = pd.read_excel(self.file_pick1.GetPath())

        # 活动数据
        if not self.file_pick2.GetPath():
            print('请选择活动数据！\n '+ '#'*20)
        elif not self.file_pick2.GetPath().endswith('xlsx'):
            print('活动数据请选择xlsx文件！\n ' + '#' * 20)
        else:
            if self.file_pick2.GetPath().endswith('csv'):
                self.df_activity = pd.read_csv(self.file_pick2.GetPath())
            else:
                self.df_activity = pd.read_excel(self.file_pick2.GetPath())

        # 预测时长
        if not self.m_textCtrl8.GetValue():
            print('请输入预测天数\n' + '#' * 20)
        else:
            try:
                self.predict_days = int(self.m_textCtrl8.GetValue())
                if self.df_sale.shape[0] >= 1 and self.df_activity.shape[0] >= 1 and self.predict_days <= 50:
                    self.check_data = 1
                    print('数据输入成功!!!')
                else:
                    print('请确认表格形式并保证预测天数小于等于50' + '#' * 20)
            except:
                print('预测天数请输入数字\n' + '#' * 20)
        print('__'*20)



    def PredictionCal(self, event):
        if self.check_data == 0:
            print('请先Check数据')
        else:
            self.foods = list(self.df_sale.columns[1:])[:3]
            print(f'一共{len(self.foods)}个菜谱！,分别为:')
            for i in range(len(self.foods)):
                print(self.foods[i], end=',')
                if (i+1) % 10 == 0:
                    print('\n')
            print('\n')
            print('__'*10 + '\n')

            result_list = []
            for i, food in enumerate(self.foods):
                data = Prophet_Predict.ProphetTrain.get_food_sale(self.df_sale, food)
                pt = Prophet_Predict.ProphetTrain(
                    predict_freq_num=31,
                    data=data,
                    name=food,
                    holidays=self.df_activity,
                )
                print(f'{i+1}|{len(self.foods)}  {food} Training Started...')
                try:
                    pt.run(show=3)
                    result_list.append(pt \
                                       .predict_data[['ds', 'yhat']] \
                                       .assign(yhat=lambda x: [i if i >= 0 else 0 for i in x['yhat']]) \
                                       .rename(columns={'yhat': f'{food}_yhat'}) \
                                       .set_index('ds'))
                    print(f'{food} Prediction End.')
                except:
                    print(f'{food} 销量信息太少， 暂时无法预测！！！')
                finally:
                    print('#' * 50)
            self.df_output = pd.concat(result_list, axis=1).reset_index().assign(ds=lambda x: x['ds'].astype(str))

    def OutPut(self, event):
        self.df_output1 = self.df_output.assign(Pweek=lambda x: [
            str(k)[:10] + "~" + str(m)[:10]
            for k, m in zip(
                [
                    pd.to_datetime(i)
                    - datetime.timedelta(days=pd.to_datetime(i).weekday())
                    for i in x["ds"]
                ],
                [
                    pd.to_datetime(i)
                    + datetime.timedelta(days=6 - pd.to_datetime(i).weekday())
                    for i in x["ds"]
                ],
            )
        ])
        self.df_output2 = self.df_output1.groupby('Pweek').sum().reset_index()
        ew = pd.ExcelWriter(os.path.join(self.m_dirPicker1.GetPath(), '食万净菜销量预测结果.xlsx'))
        if '星期' in self.m_choice3.GetStringSelection() and '天' in self.m_choice3.GetStringSelection():
            self.df_output.to_excel(ew, index=False, sheet_name='by_day')
            self.df_output2.to_excel(ew, index=False, sheet_name='by_week')
            ew.close()
        elif '星期' in self.m_choice3.GetStringSelection():
            self.df_output2.to_excel(ew, index=False, sheet_name='by_week')
            ew.close()
        else:
            self.df_output.to_excel(ew, index=False, sheet_name='by_day')
            ew.close()
        print('输出完成')





app = wx.App(False)
frame = CalFrame(None)
frame.Show(True)
app.MainLoop()