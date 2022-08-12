from email import message
import json
from tabnanny import check
import pandas as pd 
import numpy as np

class DataCheck:
    def __init__(self, salePath, activityPath, predictDay) -> None:
        self.salePath = salePath 
        self.activityPath = activityPath 
        self.predictDay = predictDay 

    def saleCheck(self):
        checkcode = 0
        message = [] 
        try:
            df_sale = pd.read_excel(self.salePath) 
            cols = list(df_sale.columns) 
            try:
                df_sale[cols[0]] = pd.to_datetime(df_sale[cols[0]]) 
            except:
                message.append("输入正确的日期格式 yyyy-MM-dd")
            cols_menu = cols[1:] 
            cols_menu_dup = list(pd.value_counts(cols_menu).loc[lambda x: x>2].index) 
            if cols_menu_dup:
                message.append(f"存在相同净菜：{'|'.join(cols_menu_dup)}")
            cols_menu_null = [i for i in cols_menu if i in ['', np.nan]]  
            if cols_menu_null:
                message.append("净菜字段缺失")
        except:
            message.append('无法读取文件, 输入正确的xlsx格式文件或者文件需要解密') 
        
        if len(message) == 0:
            checkcode = 1 
        return checkcode, message 

    def activityCheck(self):
        checkcode = 0 
        message = [] 
        try:
            df_act = pd.read_excel(self.activityPath) 
            df_act.columns = ['holiday', 'ds', 'lower_window', 'upper_window'] 
            try:
                df_act['ds'] = pd.to_datetime(df_act['ds']) 
            except:
                message.append("输入正确的日期格式 yyyy-MM-dd") 
            if df_act.isnull().sum().sum() > 0:
                message.append('存在数据缺失') 
        except:
            message.append('无法读取文件, 输入正确的xlsx格式文件或者文件需要解密')  

        if len(message) == 0:
            checkcode = 1 
        return checkcode, message  
    
    def predictdayCheck(self):
        checkcode = 0 
        message = [] 
        try:
            n_day = int(self.predictDay) 
            if n_day <= 0:
                message.append("输入大于0的整数")  
            elif n_day > 35:
                message.append("输入预测天数需小于等于35")
        except:
            message.append('输入正确的数字格式')
        
        if len(message) == 0:
            checkcode = 1 
        return checkcode, message   

    def mainCheck(self): 
        result = []
        code1, msg1 = self.saleCheck() 
        code2, msg2 = self.activityCheck() 
        code3, msg3 = self.predictdayCheck() 

        for inputdata, code, msg in zip(['销售历史数据', '活动数据', '预测天数'], [code1, code2, code3], [msg1, msg2, msg3]):
            if not code:
                result += [{
                    "code": code,
                    "inputdata":inputdata,
                    #  
                    "msg":i, 
                } for i in msg]   
        if result:
            return {"checkresult":0, "input":{"salePath":self.salePath, "activityPath":self.activityPath, "predictDay":self.predictDay}, "error":result} 
        else:
            return {"checkresult":1, "input":{"salePath":self.salePath, "activityPath":self.activityPath, "predictDay":self.predictDay}, "error":None}  

if __name__ == '__main__':
    check1 = DataCheck(
        r'C:\Users\yan.zy\Desktop\WorkStation\2022-06-20 净菜销量预测\input\sale_data.xlsx',
        r'C:\Users\yan.zy\Desktop\WorkStation\2022-06-20 净菜销量预测\input\activity.xlsx',
        -1,
    ) 
    print(json.dumps(check1.mainCheck(), ensure_ascii=False))






