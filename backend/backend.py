from flask import Flask,request
from flask import render_template
from sklearn.externals import joblib
import json
import numpy as np

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('index.html')

    
@app.route('/test',methods=['POST'])
def test():
    url = request.json['url']
    neiwai=request.json['neiwai']
    zifu_num=0
    shuzi_num=0
    zimu_num=0
    T_zifu_num=0
    for str in url:
        if str.isalpha():
            zimu_num+=1
        elif str.isdigit():
            shuzi_num+=1
        else:
            zifu_num+=1
    T_zifu_num =zifu_num - ( url.count('.') + url.count(':') + url.count('/'))
    svm_model=joblib.load('LR_model.m')
    data=np.array([zimu_num,shuzi_num,zifu_num,T_zifu_num] + neiwai)
    print("================"+"webpage data"+"=========================")
    print(data)
    predicted = svm_model.predict(data.reshape(1,-1))
    print("================="+"predicted"+"===========================")
    print(predicted)
    if predicted==0:
        return json.dumps({"res":0})
    else:
        return json.dumps({"res":1})


if __name__ == '__main__':
    app.run(port=2222,debug=True)