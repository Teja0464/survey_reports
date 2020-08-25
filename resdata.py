from pymongo import MongoClient
from flask_restful import Api,Resource
from flask import Flask, request
from flask_cors import CORS
import xlsxwriter

app = Flask(__name__)
api = Api(app)
CORS(app)

try:
    client = MongoClient('mongodb+srv://khushig999:khushigupta@heraizen-0308.rebyp.mongodb.net/test?retryWrites=true&w=majority')
    db = client.surveydb
    res = db["survey"]
    ques = db["questions"]
except Exception as e:
    print(f"Error...... + {e}")



@app.route('/getAllIds',methods = ["GET"])
def getAllIds():
    ret = []
    result = client['surveydb']['questions'].aggregate([
    {
        '$project': {
            'topicId': 1, 
            '_id': 0
        }
    }
    ])
    for re in result:
        ret.append(re['topicId'])
    return {"message":ret}

@app.route('/getAllhds',methods = ["GET"])
def getAllhds():
    ret = []
    result = client['surveydb']['questions'].aggregate([
    {
        '$project': {
            'topicName': 1, 
            '_id': 0
        }
    }
    ])
    for re in result:
        ret.append(re['topicName'])
    return {"message":ret}


@app.route('/getsubs',methods = ["POST"])
def getsubs():
    para = request.json
    ret = []
    result = client['surveydb']['questions'].aggregate([
        {
            '$match': {
                'topicId': para["id"]
            }
        }, {
            '$unwind': {
                'path': '$data'
            }
        }, {
            '$project': {
                'data.desc': 1, 
                '_id': 0
            }
        }
    ])
    for re in result:
        ret.append(re["data"]["desc"])
    return {"message":ret}

@app.route('/getsubsbyhd',methods = ["POST"])
def getsubsbyhd():
    para = request.json
    ret = []
    result = client['surveydb']['questions'].aggregate([
        {
            '$match': {
                'topicName': para["hd"]
            }
        }, {
            '$unwind': {
                'path': '$data'
            }
        }, {
            '$project': {
                'data.desc': 1, 
                '_id': 0
            }
        }
    ])
    for re in result:
        ret.append(re["data"]["desc"])
    return {"message":ret}

@app.route('/getchartsid',methods = ["POST"])
def getchartsid():
    para = request.json
    idname = para["id"]
    sec1 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.topicId': idname,
                'answers.section': 1
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sec2 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.topicId': idname,
                'answers.section': 2
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sec3 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.topicId': idname,
                'answers.section': 3
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sd1 = []
    for x in sec1:
        sd1.append({"option":x["_id"],"count":x["total"]})
    sd2 = []
    for x in sec2:
        sd2.append({"option":x["_id"],"count":x["total"]})
    sd3 = []
    for x in sec3:
        sd3.append({"option":x["_id"],"count":x["total"]})
    
    return {"sd1": sd1,"sd2":sd2,"sd3":sd3}




@app.route('/getchartshd',methods = ["POST"])
def getchartshd():
    para = request.json
    result = client['surveydb']['questions'].aggregate([
        {
            '$match': {
                'topicName': para['hd']
            }
        }
    ])
    idres = ""
    for re in result:
        print(re['topicId'])
        idres = re['topicId']
    sec1 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.topicId': idres,
                'answers.section': 1
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sec2 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.topicId': idres,
                'answers.section': 2
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sec3 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.topicId': idres,
                'answers.section': 3
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sd1 = []
    for x in sec1:
        sd1.append({"option":x["_id"],"count":x["total"]})
    sd2 = []
    for x in sec2:
        sd2.append({"option":x["_id"],"count":x["total"]})
    sd3 = []
    for x in sec3:
        sd3.append({"option":x["_id"],"count":x["total"]})
    
    return {"sd1": sd1,"sd2":sd2,"sd3":sd3}
    



@app.route('/getsubchart',methods = ["POST"])
def subchart():
    para = request.json
    result = client['surveydb']['questions'].aggregate([
        {
            '$unwind': {
                'path': '$data'
            }
        }, {
            '$match': {
                'data.desc': para['sub']
            }
        }, {
            '$project': {
                'data.ref': 1, 
                '_id': 0
            }
        }
    ])
    ref = ""
    for re in result:
        print(re["data"]["ref"])
        ref = re["data"]["ref"]
    sec1 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.ref': ref,
                'answers.section': 1
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sec2 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.ref': ref,
                'answers.section': 2
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sec3 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.ref': ref,
                'answers.section': 3
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sd1 = []
    for x in sec1:
        sd1.append({"option":x["_id"],"count":x["total"]})
    sd2 = []
    for x in sec2:
        sd2.append({"option":x["_id"],"count":x["total"]})
    sd3 = []
    for x in sec3:
        sd3.append({"option":x["_id"],"count":x["total"]})
    
    return {"sd1": sd1,"sd2":sd2,"sd3":sd3}







@app.route('/getresct',methods = ["GET"])
def resct():
    result = client['surveydb']['survey'].aggregate([
        {
            '$project': {
                'email': 1, 
                '_id': 0
            }
        }
    ])
    cnt = 0
    for re in result:
        cnt = cnt+1
    return {"message":cnt}

@app.route('/getorct',methods = ["GET"])
def orct():
    result = client['surveydb']['survey'].aggregate([
        {
            '$group': {
                '_id': {
                    'org': '$org'
                }, 
                'cnt': {
                    '$sum': 1
                }
            }
        }
    ])
    cnt = 0
    for re in result:
        cnt = cnt+1
    return {"message":cnt}

@app.route('/getevy',methods = ["GET"])
def getevy():
    sec1 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.section': 1
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sec2 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.section': 2
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sec3 = client['surveydb']['survey'].aggregate([
        {
            '$unwind': {
                'path': '$answers'
            }
        }, {
            '$match': {
                'answers.section': 3
            }
        }, {
            '$group': {
                '_id': '$answers.choice', 
                'total': {
                    '$sum': 1
                }
            }
        }
    ])
    sd1 = []
    for x in sec1:
        sd1.append({"option":x["_id"],"count":x["total"]})
    sd2 = []
    for x in sec2:
        sd2.append({"option":x["_id"],"count":x["total"]})
    sd3 = []
    for x in sec3:
        sd3.append({"option":x["_id"],"count":x["total"]})
    
    return {"sd1": sd1,"sd2":sd2,"sd3":sd3}


# def sheet():
#     workbook = xlsxwriter.Workbook('C:/Users/teja/Documents/PS_Heraizen/reports.xlsx')
#     worksheet = workbook.add_worksheet()
#     worksheet.write(0,0,'Reports for the survey on School Education')
#     row = 2
#     col = 0
#     ret = []
#     result = client['surveydb']['questions'].aggregate([
#     {
#         '$project': {
#             'topicName': 1, 
#             '_id': 0
#         }
#     }
#     ])
#     for re in result:
#         worksheet.write(row,col,re['topicName'])
#         row +=3
#         col +=1
#         res = client['surveydb']['questions'].aggregate([
#             {
#                 '$match': {
#                     'topicName': re['topicName']
#                 }
#             }, {
#                 '$unwind': {
#                     'path': '$data'
#                 }
#             }, {
#                 '$project': {
#                     'data.desc': 1, 
#                     '_id': 0
#                 }
#             }
#         ])
#         for desc in res:
#             ret.append(desc["data"]["desc"])
#             worksheet.write(row,col,desc["data"]["desc"])
#             row+=1
#         row+=2
#         col = 0

#     workbook.close()


# sheet()
app.run(port=5000,debug=True)
