# 基于prophet的销量预测
## mainCalculator
基于python-wx的图形界面，包含数据输入，数据格式检测，数据输出
![图形界面](https://github.com/zhuzhuyan93/SalesPrediction/blob/master/input/clipboard.png)   
## mainPredictApi
基于flask的本地接口封装
### 数据检测接口
* http://10.107.40.15:9527/datacheck?salepath={历史销售数据}&activitypath={活动数据}&predictday={预测天数} 
### 数据训练及预测
* http://10.107.40.15:9527/predict?salepath={历史销售数据}&activitypath={活动数据}&predictday={预测天数}
