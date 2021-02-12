import pixivDataAndPicObtainer
import ComputerVisionDBmerge
import ComputerVisionPost
import ComputerVisionValuesExtract

#===============================================
#Key and URL of Ms ComputerVision
#-----------------------------------------------
myKey = '' #put your CV key
url = '' # put your CV url
#===============================================

#===============================================
# save parameters(and the picture) into database
#-----------------------------------------------
params_alreadyKnown = [0, 0, 0, 0] # set your picture's statistical params which has been alreaady known On Pixiv
picsPath = '' #put the picture path you selected to check
filePath = './picData'
pixivDataAndPicObtainer.saveParameter(filePath, picsPath, params_alreadyKnown)
#===============================================

#===============================================
# save parameters(and the picture) into database
#-----------------------------------------------
db = ComputerVisionDBmerge.DB_merge('./values.db')
db.db_allValues(db.db_tableList('all_p_name'), 'p_name')
db.db_concat('all_p_name', db.db_tableList('all_p_name'), 'p_name')
#===============================================

#=====================================================================================================
# POST images to ComputerVision(Ms Azure Machine learning REST API) and acquire stuff of each picture
#-----------------------------------------------------------------------------------------------------
pics = glob.glob(filePath + '/pics/*')
pics = [v.split('/')[-1] for v in pics]

db = ComputerVisionPost.DB_post('values.db')

resizedImg = io.BytesIO()

for pName in pics:
    if db.is_exist(pName.split('.')[0]):
        print(pName.split('.')[0], "has alread existed")
        continue
    else:
        print(pName.split('.')[0], "is nowhere in this DB")

    #time.sleep(5)
    with open(filePath + '/pics/' + pName, 'br') as f:
        img = f.read()

    if len(img) > 4 * 1000 * 1000:
        while resizedImg.tell() == 0 or resizedImg.tell() > 4 * 1000 * 1000: 
            resizedImg.truncate(0)
            resizedImg.seek(0)
            p_img = Image.open(filePath + '/pics/' + pName)
            p_img = p_img.resize((round(p_img.width/1.5), round(p_img.height/1.5)))
            if pName.split('.')[1] == 'jpg':
                p_img.save(resizedImg, format='jpeg')
            else:
                p_img.save(resizedImg, format=pName.split('.')[1])
        img = resizedImg.getvalue()

    

    data = img

    param = {
            'ocp-apim-subscription-key': myKey,
            'Content-Type': 'application/octet-stream'
            }
    request = urllib.request.Request(url,headers=param, data=data)
    try:
        with urllib.request.urlopen(request) as req:
            body = req.read()
            body = json.loads(body)

            bodys = [body]

            keyName = ''
            print('====')
            print(pName)
            print('====')

            print('========================================================')
            print(bodys)
            print('========================================================')

            for bod in bodys:
                if type(bod) == type({}):
                    for k, b in bod.items():
                        if  k == 'name' or k == 'object':
                            print(b)
                            keyName = b.replace(' ','_').replace('-', '_')
                        elif keyName:
                            print(keyName, b)
                            db.db_input(keyName,(pName.split('.')[0],str(b)))
                            keyName = ''
                        else:
                            if type(b) != type({}) and type(b) != type([]):
                                print(k, b)
                                db.db_inputDefault(k,(pName.split('.')[0],k,str(b)))
                        bodys.append(b)
                        print("-----------------------------------")
                elif type(bod) == type([]):
                    for b in bod:
                        bodys.append(b)
        
    except urllib.error.HTTPError as err:
        print(err)
#=====================================================================================================

#===========================================================================
# use Regression for Parameters (statistical and gained by Computer Vision)
#---------------------------------------------------------------------------
db = ComputerVisionValuesExtract.DB_values('./values.db')
db.db_extract('_TMP1', 'p_name')
_tags = db.get_tags()

_tmp_dataSet = db.get_values()
_dataSet = []

_checkSet = [0] * len(_tmp_dataSet[0])
_checkTagSet = [0] * len(_tmp_dataSet[0])
max_index = 0
min_index = 100000000000


for ds in _tmp_dataSet:
    count_non0values = 0
    checkIndex = 0

    _tmp = [ds[0]]
    for index, d in enumerate(ds[1:]):
        if someValueCheck(d, index) != None:
            _v = someValueCheck(d, index)
            if type(_v) != type(0):
                checkIndex += len(_v)
                for in_v in _v:
                    _tmp.append(in_v)
            else:
                checkIndex += 1
                _tmp.append(_v) 
        else:
            checkIndex += 1
            try:
                if d == None:
                    _tmp.append(0)
                elif float(d) >= 1:
                    #_tmp.append(1 / int(d))
                    _tmp.append(1)
                else:
                    if "score" in _tags[index]:
                        _tmp.append(float(d))
                    else:
                        _tmp.append(1)
                    #_tmp.append(float(d))
                    count_non0values += 1
            except ValueError:
                _tmp.append(0)
                _checkSet[checkIndex] = 1
                _checkTagSet[index + 1] = 1
            except TypeError:
                _tmp.append(0)
                _checkSet[checkIndex] = 1
                _checkTagSet[index + 1] = 1
    _dataSet.append([v for v in _tmp + [count_non0values]])

remove_params = []
for i, c in enumerate(_checkSet):
    if c == 1:
        remove_params.append(i)

remove_tags = []
for i, c in enumerate(_checkTagSet):
    if c == 1:
        remove_tags.append(i)

print("---------------------------")
print("no value params' num : ", len(remove_tags))
for rP in remove_tags:
    print(_tags[rP])
print("---------------------------")

for i in range(len(_dataSet)):
    _dataSet[i] = [v for _i, v in enumerate(_dataSet[i]) if _i not in remove_params]
#------------ pixiv Datas --------------------
data = []
dataId = glob.glob(filePath + '/pP_data*')
for d in dataId:
    with open(filePath + '/' + d.split('/')[-1].split('.')[0] + '.csv') as f:
       t_data = f.readlines()


    for td in t_data:
        data.append(td[:-1])

print("-----------------------------------")
print("data Num :", len(data))
print("-----------------------------------")

splitedData = {}
for d in data:
    d = d.split(',')
    _tmp = [d[0:len(params_alreadyKnown)]]
    label_index = len(_tmp)
    param_index = len(_tmp)

    splitedData[d[len(_tmp)]] = _tmp

#--------------- concat two type datas -------------------
_concated_dataSet = []
for _d in _dataSet:
    _concated_dataSet.append(splitedData[str(_d[0])] + _d[1:]) 
#print(_concated_dataSet)
#--------------- Learning --------------
dataSet = numpy.array(_concated_dataSet)
trains, tests = train_test_split(dataSet, test_size=0.2)


clf = KernelRidge(alpha=1, kernel='rbf')
#clf = linear_model.LinearRegression()
clf.fit(trains[:,param_index:],trains[:, :label_index])

print("=============================")
print("Number of parameters : ", len(dataSet[0][param_index:]))
print("=============================")

res = clf.predict(dataSet[:, param_index:])
res[res <0] = 0
print(clf.predict(dataSet[:, param_index:]))
print(res)
print("Score : ", r2_score(dataSet[:, :label_index], res))
print("=============================")
#===========================================================================