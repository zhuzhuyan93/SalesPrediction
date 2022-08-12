import json
import flask
import DataCheck
import Prophet_Predict
import pandas as pd
import datetime

server = flask.Flask(__name__)

@server.route("/datacheck", methods=["get", "post"])
def datacheck():
    salePath = flask.request.values.get("salepath")
    activityPath = flask.request.values.get("activitypath")
    predictDay = flask.request.values.get("predictday")

    check = DataCheck.DataCheck(salePath, activityPath, predictDay)
    checkResult = check.mainCheck()

    return json.dumps(checkResult, ensure_ascii=False, indent=4)


@server.route("/predict", methods=["get", "post"])
def predict():
    salePath = flask.request.values.get("salepath")
    activityPath = flask.request.values.get("activitypath")
    predictDay = flask.request.values.get("predictday")

    check = DataCheck.DataCheck(salePath, activityPath, predictDay)
    checkResult = check.mainCheck()

    if int(checkResult.get("checkresult")) == 0:
        return json.dumps(
            {"checkresult": 0, "msg":"先检查通过数据格式", "result": None}, ensure_ascii=False, indent=4
        )
    else:
        df_sale = pd.read_excel(salePath)
        df_activity = pd.read_excel(activityPath)
        menu_list = list(df_sale.columns[1:])
        result_list = []
        for i, menu_name in enumerate(menu_list[:3]):
            ProphTrain = Prophet_Predict.ProphetTrain(
                predict_freq_num=int(predictDay),
                data=df_sale,
                holidays=df_activity,
            )
            print(f"{i+1}|{len(menu_list)} {menu_name} training started...")

            try:
                mape = ProphTrain.train_predict_calculation(menu_name=menu_name)
                result_list.append(
                    ProphTrain.predict_data[[menu_name]]
                )
                print(f"{menu_name} prediction end. \n Mape is {mape}")
            except:
                print(f"{menu_name} need more sales-information.")
            finally:
                print("##" * 20)
        df_output1 = (
            pd.concat(result_list, axis=1)
            .reset_index()
            .assign(ds=lambda x: x["ds"].astype(str))
        )
        df_output2 = (
            df_output1.assign(
                Pweek=lambda x: [
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
                ]
            )
            .groupby("Pweek")
            .sum()
            # .reset_index()
        )

        return json.dumps(
            {
                "checkresult": 1,
                "msg":"数据格式检查通过",
                "result": {
                    "by_day": df_output1.set_index('ds').to_dict(),
                    "by_week": df_output2.to_dict(),
                },
            },
            ensure_ascii=False,
            indent=4,
        )


server.run(port=9527, debug=True, host="10.107.40.15")

