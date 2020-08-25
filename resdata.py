from pymongo import MongoClient
from flask_restful import Api,Resource
from flask import Flask, request, send_file
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



def subchsheet(desc):
    result = client['surveydb']['questions'].aggregate([
        {
            '$unwind': {
                'path': '$data'
            }
        }, {
            '$match': {
                'data.desc': desc
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

@app.route('/report',methods = ["GET"])
def sheet():
    workbook = xlsxwriter.Workbook('reports.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    main = workbook.add_format()
    main.set_bold()
    main.set_bg_color('blue')
    main.set_font_color('white')
    main.set_underline()
    secf = workbook.add_format()
    secf.set_font_color('blue')
    secf.set_bold()
    secf.set_underline()
    num = workbook.add_format()
    num.set_align('center')
    worksheet.write(0,0,'REPORTS FOR THE SURVEY ON SCHOOL EDUCATION',main)
    row = 4
    col = 0
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
        worksheet.write(row,col,re['topicName'],secf)
        row +=3
        col +=1
        worksheet.write(row-1,col+1,"Present Status in Karnataka",bold)
        worksheet.write(row-1,col+3,"Nature of Implications",bold)
        worksheet.write(row-1,col+5,"Implementation time",bold)
        res = client['surveydb']['questions'].aggregate([
            {
                '$match': {
                    'topicName': re['topicName']
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
        for desc in res:
            ret.append(desc["data"]["desc"])
            rss = row
            css = col+3
            rsss = row
            csss = col+5
            rs = row
            cs = col+1
            worksheet.write(row,col,desc["data"]["desc"])
            rsts =  subchsheet(desc["data"]["desc"])
            sd1 = rsts["sd1"]
            sd2 = rsts["sd2"]
            sd3 = rsts["sd3"]
            for op in sd1:
                rs +=1
                worksheet.write(rs,cs,op['option'])
                worksheet.write(rs,cs+1,op['count'],num)
            for op in sd2:
                rss+=1
                worksheet.write(rss,css,op['option'])
                worksheet.write(rss,css+1,op['count'],num)
            for op in sd3:
                rsss+=1
                worksheet.write(rsss,csss,op['option'])
                worksheet.write(rsss,csss+1,op['count'],num)

            row+=4
        row+=2
        col = 0
    workbook.close()
    return send_file('../reports.xlsx',attachment_filename="report.xlsx")



app.run(port=5000,debug=True)
