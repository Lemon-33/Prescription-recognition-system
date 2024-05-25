from test_sql import Database
import json
import hashlib#导入密码加密模块
import datetime
import uuid
import base64
import time
import ast
from io import BytesIO
from PIL import Image
import pickle
import pylab as plt
import module
import cutP
import OCR

conf={'host':'localhost','user':'root','pw':'711540','db':'test','port':3306}

#计算用户是否登录失效
#登陆失效返回0
#登录没有失效返回1
def cal_time(stamp1,stamp2):#stamp1是token stamp2是目前时间戳
    t1=time.localtime(stamp1)
    t2 = time.localtime(stamp2)
    t1=time.strftime("%Y-%m-%d %H:%M:%S",t1)
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", t2)
    time1=datetime.datetime.strptime(t1,"%Y-%m-%d %H:%M:%S")
    time2 = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
    diff_sec=(time2-time1).seconds
    if (diff_sec)<=3600:
        return 1
    else:
        return 0


#注册
def insert_register(json1):  # user,password1,password2
    db = Database(conf)
    data = json.loads(json1)
    judge = 1  # 保存到数据库变成0，没有保存到数据库保持1

    uname = data['uname']
    password = data['password']
    information = 'Not Found'
    # 看是否重名
    unameFound = '\'' + uname + '\''
    information = db.select_one('user', 'uname=' + unameFound)  # 数据库里该用户的所有信息

    if information == 'Not Found':  # 没有这个用户 没有重名 可以注册
        # 密码加密
        # 待加密信息为password1/password2 字符串形式
        # 创建md5对象
        hl = hashlib.md5()
        # 此处必须声明encode
        # # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
        hl.update(password.encode(encoding='utf-8'))
        result_pd = hl.hexdigest()  # 字符串

        timeStampNow = datetime.datetime.now().timestamp()  # 时间戳
        uname = '\'' + uname + '\''
        result_pd = '\'' + result_pd + '\''
        timeStampNow = '\'' + str(timeStampNow) + '\''
        password = '\'' + password + '\''
        # userid = '\'' + str(uuid.uuid1()) + '\''
        # judge = db.insert('user', {'uname': uname, 'password': result_pd, 'token': timeStampNow})
        judge = db.insert('user', {'uname': uname, 'password': password, 'token': timeStampNow})

        r_data = '1'
        if judge == 1:
            r_data = 'ACCOUNT_REGISTER_FAILED'
        if judge == 0:  # judge 等于0表示成功注册
            # r_data=str(uuid.uuid1())
            r_data = 'successful'

        return r_data

    else:  # 有这个名字 重名了
        r_data = 'Failed_name'
        return r_data

# 登录
def select_login(json2):  # userid,password
    db = Database(conf)
    data = json.loads(json2)
    # judge = 1  # 连接到数据库且查询成功变成0，否则保持1
    uname = data['uname']
    password = data['password']
    password = '\'' + password + '\''

    # 密码加密
    # 待加密信息为pswd
    # 创建md5对象
    hl = hashlib.md5()
    # 此处必须声明encode
    # # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(password.encode(encoding='utf-8'))
    input_pd = hl.hexdigest()  # 字符串

    # 数据库操作类
    db = Database(conf)
    uname = '\'' + uname + '\''
    information = 'Not Found'
    information = db.select_one('user', 'uname=' + uname)  # 数据库里该用户的所有信息

    if information == 'Not Found':
        r_data = 'No_user'

        # self.write('没有此用户，请注册')
        # self.redirect('/register')
    else:
        # 有此用户
        pw = information['password']  # 数据库里的密码
        pw = '\'' + pw + '\''
        print(pw)
        print(password)
        # if input_pd == pw:  # 密码正确
        if password == pw:
            timeStampNow = datetime.datetime.now().timestamp()  # 时间戳
            timeStampNow_save = '\'' + str(timeStampNow) + '\''
            judge = db.update('user', {'token': timeStampNow_save}, 'uname=' + uname)  # 需要测试
            if judge == 1:
                r_data = 'successful' + str(timeStampNow) # 最终阶段 返回token值(放在HTTP的header里面，后续的每一个操作都有token值)
                # r_data = 'successful'
            else:
                r_data = 'mysql mistake'
        else:
            r_data = 'Password mistake'
    return r_data

# 上传
def upload(dic):
    db = Database(conf)
    #data = json.loads(dic)
    uname = dic['uname']
    form_type = dic['form_type']  #0代表药单，1代表海关报单
    files = dic['files']
    img_format = dic['img_format']

    timeStampNow = datetime.datetime.now().timestamp()
    #图片ID 用户名+时间戳
    foldername=uname+str(int(timeStampNow))
    PictureID = uname + str(int(timeStampNow))

    img=files.get('file_send')
    img=img[0]
    #print(type(img))
    data=img.get('body')
    #filename=img.get('filename')
    route="C:/Users/98686/Desktop/img/"  #服务器上的保存路径
    img_route = route + PictureID + img_format
    writer=open(img_route,'wb')
    writer.write(data)
    writer.close()
    
    
    img = '\'' + img_route + '\''
    img_format = '\'' + img_format + '\''
    dateTime = '\'' + str(timeStampNow) +'\''
    outputModuleID = '\'' + str(form_type) + '\''


    res = module.recognize(img_route)
    print(res)
    columns = res['columns']
    rows = res['rows']
    points_row = res['points_row']
    points_col = res['points_col']
    points_col_last = res['points_col_last']
    diff_points_row = res['diff_points_row']
    diff_points_col = res['diff_points_col']
    diff_points_col_last = res['diff_points_col_last']

    information = db.select_all('moduleinformation_test')
    length = len(information)

    # 后面要用的变量
    # inputModuleID=0
    # modulejson=0
    # col=0
    # row=0

    ans = 0
    for i in range(length):
        info = information[i]
        template_row = ast.literal_eval(info['featureCoordinateY'])
        template_col = ast.literal_eval(info['featureCoordinateXUp'])
        template_col_last = ast.literal_eval(info['featureCoordinateXDown'])
        ans = module.match(template_row, template_col, template_col_last, diff_points_row, diff_points_col, diff_points_col_last) #判断是否是同一模板
        if ans == 1:
            points = module.delete_points(template_row, template_col, template_col_last, diff_points_row, diff_points_col, diff_points_col_last,points_row,points_col,points_col_last)
            points_row = points['points_row']
            points_col = points['points_col']
            points_col_last = points['points_col_last']
            #修改
            dic=cutP.cutALL(img_route,points_row,points_col,points_col_last,foldername)
            inputModuleID = info['inputmoduleid']
            modulejson=info['modulejson']
            col=int(info['numXUp'])-1
            row=int(info['numY'])-1
            break
    if ans == 0:
        r_data = 'Module_failed' + PictureID
        timeStampNow = datetime.datetime.now().timestamp()
        inputModuleID = uname + str(int(timeStampNow))
    else:
        r_data = 'Cut_ok'
        cut_route=dic['cut_route']
        foldername=dic['foldername']
        r_data=OCR.convertPictureToText(cut_route,foldername,col,row,modulejson)

    uname = '\'' + uname + '\''
    inputModuleID = '\'' + inputModuleID + '\''
    PictureID = '\'' + PictureID + '\''
    judge = db.insert('imageInformation',{'uname': uname, 'pictureID': PictureID, 'pictureRoute': img, 'pictureFormat': img_format,'dateTime': dateTime, 'inputModuleID': inputModuleID, 'outputModuleID': outputModuleID})

    return r_data



# 保存
class CoordinateCoupleInformation:
    order = int  # 顺序
    key = str  # 关键字
    coordinate1 = str  # 坐标1
    coordinate2 = str  # 坐标2

    def __init__(self, order, key, coordinate1, coordinate2):
        self.order = order
        self.key = key
        self.coordinate1 = coordinate1
        self.coordinate2 = coordinate2


class ModuleInformation:  # 整个模板信息
    CoordinateCoupleInfoList = list

    def __init__(self):
        self.CoordinateCoupleInfoList = []

class CoordinateCoupleInformation_:
    order = int
    key = str
    coordinate1 = str
    coordinate2 = str

    def __init__(self, order, key, coordinate1, coordinate2):
        self.order = order
        self.key = key
        self.coordinate1 = coordinate1
        self.coordinate2 = coordinate2


class JsonHelper:  # 处理json 之后保存到数据库
    def addIntoListIfNotExisted(listToDeal, number):
        if len(listToDeal) == 0:
            listToDeal.append(number)
            return listToDeal
        ifExisted = 0
        defRange = 0.02
        i = 0
        for i in range(len(listToDeal)):
            if number >= listToDeal[i] - defRange and number <= listToDeal[i] + defRange:
                ifExisted = 1
        if ifExisted == 0:
            listToDeal.append(number)
        return listToDeal

    def stringEditor_RemoveAllPartBetweenThese(self, stringText, startText, endText):
        startIndex = stringText.find(startText, 0, len(stringText))
        if startIndex == -1:
            return stringText
        endIndex = stringText.find(endText, 0, len(stringText))
        if endIndex == -1:
            return stringText
        while (startIndex != -1) & (endIndex != -1):
            endIndex = endIndex + len(endText)
            removeText = stringText[startIndex:endIndex]
            stringText = stringText.replace(removeText, '')
            startIndex = stringText.find(startText, 0, len(stringText))
            endIndex = stringText.find(endText, 0, len(stringText))
        return stringText

    def stringEditor_RemoveFirstPartBetweenThese(self, stringText, startText, endText):
        startIndex = stringText.find(startText, 0, len(stringText))
        if startIndex == -1:
            return stringText
        endIndex = stringText.find(endText, 0, len(stringText))
        if endIndex == -1:
            return stringText
        endIndex = endIndex + len(endText)
        removeText = stringText[startIndex:endIndex]
        stringText = stringText.replace(removeText, '')
        return stringText

    def stringEditor_TakeFirstRequiredTextFromString(self, stringText, startText, endText):
        startIndex = stringText.find(startText, 0, len(stringText))
        if startIndex == -1:
            return ''
        stringText = stringText[startIndex:]
        endIndex = stringText.find(endText, 0, len(stringText))
        if endIndex == -1:
            return ''
        return stringText[len(startText):endIndex]

    def stringCoordinateEditor(self, stringCoordinate, chooser):
        stringCoordinate = stringCoordinate.replace(' ', '')
        if chooser == 'x':
            index = stringCoordinate.find(',')
            if index == -1:
                return 0
            if index == 1:
                return stringCoordinate[0]
            else:
                return stringCoordinate[0:int(index - 1)]
        if chooser == 'y':
            index = stringCoordinate.find(',')
            if index == -1:
                return 0
            length = len(stringCoordinate)
            if (index + 1) == (length - 1):
                return stringCoordinate[index + 1]
            else:
                return stringCoordinate[int(index + 1):int(length - 1)]

    def json_serialize(obj):
        obj_dic = JsonHelper.class2dic(obj)
        return json.dumps(obj_dic, ensure_ascii=False)

    def class2dic(obj):
        obj_dic = obj.__dict__
        for key in obj_dic.keys():
            value = obj_dic[key]
            obj_dic[key] = JsonHelper.value2py_data(value)
        return obj_dic

    def value2py_data(value):
        if str(type(value)).__contains__('.'):
            # value 为自定义类
            value = JsonHelper.class2dic(value)
        elif str(type(value)) == "<class 'list'>":
            # value 为列表
            for index in range(0, value.__len__()):
                value[index] = JsonHelper.value2py_data(value[index])
        return value

    def dealWithRecievedJson(self, recievedJson):
        #  关于模板数据&切割图片Json的格式
        #  1.坐标对总数 coordinateAmount:xxx
        #  2.每一个坐标对:order:xxx key:xxx Coordinate1:aaa Coordinate2:bbb PictureContent:abcdefg PictureFormat:jpg
        #  这里直接将Json当成字符串去处理了
        recievedJson = recievedJson.replace(' ', '')
        recievedJson = recievedJson.replace('“', '"')
        recievedJson = recievedJson.replace('”', '"')
        recievedJson = recievedJson.replace('\n', '"')
        recievedJson = recievedJson.replace('\'', '"')
        print('------------------------------------------')
        print(recievedJson)
        userid = JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson, '"uname":', ',')
        # 原始点坐标
        print(JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson, '"c1":"', '",'))
        c1 = ast.literal_eval(JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson, '"c1":"', '",'))
        print(c1)
        # 长总像素
        length = float(JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson, '"length":', ','))
        #print(length)
        # 宽总像素
        width = float(JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson, '"width":', ','))
        #print(width)
        # 图片ID str
        PictureID = JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson, '"PictureID":"', '",')
        #print(PictureID)
        # 图片格式 str
        img_format = JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson, '"img_format":"', '",')
        #print(img_format)

        coordinateAmount = int(JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson, '"coordinateAmount":', ','))
        #  获取总坐标对数目
        count = 1
        #  循环获取每个坐标对的信息
        coordinateInfoList = []
        featureCoordinateXUp = []
        featureCoordinateXDown = []
        featureCoordinateY = []
        while count <= coordinateAmount:
            coordinateInformation_order = int(
                JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson, '"order":', ',"'))
            coordinateInformation_key = JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self, recievedJson,
                                                                                                '"key":"', '",')
            coordinateInformation_coordinate1 = JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self,
                                                                                                        recievedJson,
                                                                                                        '"Coordinate1":"',
                                                                                                        '",')
            if count == coordinateAmount:
                coordinateInformation_coordinate2 = JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self,
                                                                                                        recievedJson,
                                                                                                        '"Coordinate2":"',
                                                                                                        '"}')
                recievedJson = JsonHelper.stringEditor_RemoveFirstPartBetweenThese(self, recievedJson, '"order"',
                                                                                   '"' + coordinateInformation_coordinate2 + '"}')
            else:
                coordinateInformation_coordinate2 = JsonHelper.stringEditor_TakeFirstRequiredTextFromString(self,
                                                                                                        recievedJson,
                                                                                                        '"Coordinate2":"',
                                                                                                        '",')
                recievedJson = JsonHelper.stringEditor_RemoveFirstPartBetweenThese(self, recievedJson, '"order":',
                                                                                   '"' + coordinateInformation_coordinate2 + '",')
            coordinateInformation = CoordinateCoupleInformation(coordinateInformation_order, coordinateInformation_key,
                                                                coordinateInformation_coordinate1,
                                                                coordinateInformation_coordinate2)
            coordinateInfoList.append(coordinateInformation)
            #  print('-----Order' + str(count) + '-----')
            #  print(coordinateInfoList[count-1].order)
            #  print(coordinateInfoList[count-1].key)
            #  print(coordinateInfoList[count-1].coordinate1)
            #  print(coordinateInfoList[count-1].coordinate2)
            count = count + 1
        #  所有坐标对的信息已经装在coordinateInfoList里面了 以上注释代码可以循环print查看
        #  接下来 将打包出新的模板数据Json并且存入数据库
        #  模板数据使用自定义类moduleInformation 实例是moduleInfo
        moduleInfo = ModuleInformation()
        count = 1
        while count <= coordinateAmount:
            coordinateInfo_order = coordinateInfoList[count - 1].order
            coordinateInfo_key = coordinateInfoList[count - 1].key
            coordinateInfo_coordinate1 = coordinateInfoList[count - 1].coordinate1
            coordinateInfo_coordinate2 = coordinateInfoList[count - 1].coordinate2
            coordinateInfo_ = CoordinateCoupleInformation_(coordinateInfo_order, coordinateInfo_key,
                                                           coordinateInfo_coordinate1, coordinateInfo_coordinate2)
            moduleInfo.CoordinateCoupleInfoList.append(coordinateInfo_)
            #  获取特征坐标
            if coordinateInfo_key != 'content':
                #  如果是关键字或者末行
                if coordinateInfo_key != 'lastContent':
                    #  如果是关键字
                    coord1X = coordinateInfoList[count - 1].coordinate1
                    coord1X = float(JsonHelper.stringCoordinateEditor(self, coord1X, 'x'))
                    featureCoordinateXUp = JsonHelper.addIntoListIfNotExisted(featureCoordinateXUp, coord1X)
                    coord2X = coordinateInfoList[count - 1].coordinate2
                    coord2X = float(JsonHelper.stringCoordinateEditor(self, coord2X, 'x'))
                    featureCoordinateXUp = JsonHelper.addIntoListIfNotExisted(featureCoordinateXUp, coord2X)
                elif coordinateInfo_key == 'lastContent':
                    #  如果是末行
                    coord1X = coordinateInfoList[count - 1].coordinate1
                    coord1X = float(JsonHelper.stringCoordinateEditor(self, coord1X, 'x'))
                    featureCoordinateXDown = JsonHelper.addIntoListIfNotExisted(featureCoordinateXDown, coord1X)
                    coord2X = coordinateInfoList[count - 1].coordinate2
                    coord2X = float(JsonHelper.stringCoordinateEditor(self, coord2X, 'x'))
                    featureCoordinateXDown = JsonHelper.addIntoListIfNotExisted(featureCoordinateXDown, coord2X)
            coord1Y = coordinateInfoList[count - 1].coordinate1
            coord1Y = float(JsonHelper.stringCoordinateEditor(self, coord1Y, 'y'))
            featureCoordinateY = JsonHelper.addIntoListIfNotExisted(featureCoordinateY, coord1Y)
            coord2Y = coordinateInfoList[count - 1].coordinate2
            coord2Y = float(JsonHelper.stringCoordinateEditor(self, coord2Y, 'y'))
            featureCoordinateY = JsonHelper.addIntoListIfNotExisted(featureCoordinateY, coord2Y)
            #  print('-----Order' + str(count) + '-----')
            #  print(moduleInfo.CoordinateCoupleInfoList[count-1].order)
            #  print(moduleInfo.CoordinateCoupleInfoList[count-1].key)
            #  print(moduleInfo.CoordinateCoupleInfoList[count-1].coordinate1)
            #  print(moduleInfo.CoordinateCoupleInfoList[count-1].coordinate2)
            count = count + 1
        #  编译成json
        moduleJson = JsonHelper.json_serialize(moduleInfo)
        returnData = {'json': moduleJson, 'PictureID': PictureID, 'img_format': img_format, 'c1': c1, 'length': length,
                      'width': width, 'userid': userid, 'featureCoordinateXUp': featureCoordinateXUp,
                      'featureCoordinateXDown': featureCoordinateXDown, 'featureCoordinateY': featureCoordinateY}
        #  将图片保存至本地 暂时空缺
        #####
        print("X UpList:")
        print(featureCoordinateXUp)
        print("X DownList:")
        print(featureCoordinateXDown)
        print("Y List:")
        print(featureCoordinateY)
        #####
        return returnData

    def save(self,moduleJson,userid,featureCoordinateXUp,featureCoordinateXDown,featureCoordinateY,c1,length,width,PictureID,img_format):
        #  接下来是存入数据库的部分 暂时空缺
        db = Database(conf)
        #  创一个新的数据表 第一列json 是否需要用户id
        moduleJson = moduleJson.replace("'", "\'")
        moduleJson = '\'' + moduleJson + '\''
        #  create module id
        timeStampNow = datetime.datetime.now().timestamp()  # 时间戳

        #  inputTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
        #  inputDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        inputModuleID = userid + str(int(timeStampNow))
        numXUp = len(featureCoordinateXUp)
        numY = len(featureCoordinateY)

        # 切割
        Xup = []
        Xdown = []
        Y = []


        for i in range(len(featureCoordinateXUp)):
            if featureCoordinateXUp[i]<0.002:
                featureCoordinateXUp[i]=0
            if featureCoordinateXUp[i]>1:
                featureCoordinateXUp[i]=1
            Xup.append(int(featureCoordinateXUp[i] * length + c1[0]))

        for i in range(len(featureCoordinateXDown)):
            if featureCoordinateXDown[i]<0.002:
                featureCoordinateXDown[i]=0
            if featureCoordinateXDown[i]>1:
                featureCoordinateXDown[i]=1
            Xdown.append(int(featureCoordinateXDown[i] * length + c1[0]))

        for i in range(len(featureCoordinateY)):
            if featureCoordinateY[i]<0.002:
                featureCoordinateY[i]=0
            if featureCoordinateY[i]>1:
                featureCoordinateY[i]=1
            Y.append(int(featureCoordinateY[i] * width + c1[1]))

        print('-----------------------------------')
        print(Xup)
        print(Xdown)
        print(Y)

        # 裁剪
        # route = "/home/whu-ee/Documents/"
        # bigp="test/"
        route = ""
        img_route = route + bigp+PictureID + img_format
        dic = cutP.cutALL(img_route, Y, Xup, Xdown, PictureID)
        cut_route = dic['cut_route']
        foldername = dic['foldername']
        #

        #foldername="rrr1610364652"
        print('----------convertPictureToText-----------')
        output = OCR.convertPictureToText(route, foldername, numXUp - 1, numY - 1, moduleJson)

        inputModuleID = '\'' + inputModuleID + '\''
        timeStampNow = '\'' + str(timeStampNow) + '\''
        numXUp = '\'' + str(numXUp) + '\''
        numY = '\'' + str(numY) + '\''
        featureCoordinateXUp = '\'' + str(featureCoordinateXUp) + '\''
        featureCoordinateXDown = '\'' + str(featureCoordinateXDown) + '\''
        featureCoordinateY = '\'' + str(featureCoordinateY) + '\''

        judge = db.insert('moduleinformation_test',
                          {'inputmoduleid': inputModuleID, 'timestampnow': timeStampNow, 'modulejson': moduleJson,
                           'featureCoordinateXUp': featureCoordinateXUp,
                           'featureCoordinateXDown': featureCoordinateXDown, 'featureCoordinateY': featureCoordinateY,
                           'numXUp': numXUp, 'numY': numY})
        # information=db.select_one('moduleinformation_test','numY='+'8')#数据库里该用户的所有信息
        # judge = db.insert('moduleinformation1',{'inputmoduleid':inputModlueID,'inputtime':inputTime,'inputdate':inputDate,'modulejson': moduleJson,'featureCoordinateXUp':fcx,'featureCoordinateXDown':fcy,'featureCoordinateY':tf})

        # judge = db.insert('json7',{'json1':inputModlueID,'json2':inputTime,'json3':inputDate,'json4': moduleJson,'json5':fcx,'json6':fcy,'json7':tf})
        # judge = db.insert('modu',{'inputmoduleid':inputModlueID,'inputtime':inputTime,'inputdate':inputDate,'modulejson':moduleJson,'featurecolistX':fcx,'featurecolistY':fcy,'titlefeature':tf})

        # judge = db.insert('jsontest',{'json':tf})

        return str(output)

#确认
def finish(data):  # user,password1,password2
    db = Database(conf)
    
    judge = 1  # 保存到数据库变成0，没有保存到数据库保持1
    uname = data['uname']
    PictureID=data['PictureID']
    ocr_result=data['ocr_result']
    uname = '\'' + str(uname) + '\''
    PictureID = '\'' + str(PictureID) + '\''
    ocr_result = '\'' + str(ocr_result) + '\''

    judge = db.insert('ocrresult', {'uname': uname, 'PictureID': PictureID, 'ocr': ocr_result})
    if judge == 1:
        r_data = 'mysql mistake'
    else:  # judge 等于0表示存到数据库了
        r_data = 'Save_success'
    return r_data



# create table moduleinformation_test(
#     inputmoduleid varchar(200) not null,
#     timestampnow varchar(20) not null,
#     modulejson varchar(10000) not null,
#     featureCoordinateXUp varchar(1000) not null,
#     featureCoordinateXDown varchar(1000) not null,
#     featureCoordinateY varchar(1000) not null,



        

