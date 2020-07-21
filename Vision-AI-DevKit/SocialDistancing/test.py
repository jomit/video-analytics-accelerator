import json
from playsound import playsound

class Test(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)

class Inference:

    def __init__(self, inference_object):
        self.id = inference_object.id
        # remove junk final character from the label
        self.label = inference_object.label.strip(" .\t\n")
        self.confidence = inference_object.confidence
        self.position_x = inference_object.position_x
        self.position_y = inference_object.position_y
        self.width = inference_object.width
        self.height = inference_object.height

    def to_json(self):
        return json.dumps(self.__dict__)


def calculateDistanceRiskLevel(personInfo):
    print("Calculating distance")
    print(personInfo)
    # find distance between first 2 persons only for now
    p1 = personInfo[0]
    p2 = personInfo[1]
    d = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    print("Distance =",d)
    w = (p1[0] + p2[0]) / 2
    h = (p1[1] + p2[1]) / 2
    _ = 0
    try:
        _ = (p2[2][1] - p1[2][1]) / (p2[2][0] - p1[2][0])
    except ZeroDivisionError:
        _ = 1.633123935319537e+16
    ve = abs(_ / ((1 + _ ** 2) ** 0.5))
    ho = abs(1 / ((1 + _ ** 2) ** 0.5))
    d_hor = ho * d
    d_ver = ve * d
    vc_calib_hor = w * 1.3
    vc_calib_ver = h * 0.4 * 0.8 # the last one is the angle
    c_calib_hor = w * 1.7
    c_calib_ver = h * 0.2 * 0.8 # the last one is the angle
    if 0 < d_hor < vc_calib_hor and 0 < d_ver < vc_calib_ver:
        playsound('modules/SocialDistancingInferenceModule/alarm.mp3')
        return "high" #1
    elif 0 < d_hor < c_calib_hor and 0 < d_ver < c_calib_ver:
        return "medium" #2
    else:
        return "low" #0
    

def runCalc(data1, data2):
    personInfo = []
    inf_obj1 = Test(data1)
    inference = Inference(inf_obj1)
    center = [int(inference.position_x + inference.width / 2), int(inference.position_y + inference.height / 2)]
    personInfo.append([inference.width, inference.height, center])

    inf_obj2 = Test(data2)
    inference = Inference(inf_obj2)
    center = [int(inference.position_x + inference.width / 2), int(inference.position_y + inference.height / 2)]
    personInfo.append([inference.width, inference.height, center])

    result = calculateDistanceRiskLevel(personInfo)
    print(result)


#high risk
data1 = '{"height": 722.952, "position_y": 344.952, "position_x": 717.888, "label": "person", "id": 13, "confidence": 86, "width": 769.92}'
data2 = '{"height": 702.0, "position_y": 247.968, "position_x": 429.888, "label": "person", "id": 13, "confidence": 67, "width": 243.84}'

#low risk
data3 = '{"height": 575.964, "position_y": 387.936, "position_x": 462.912, "label": "person", "id": 13, "confidence": 95, "width": 326.976}'
data4 = '{"height": 783.972, "position_y": 283.932, "position_x": 725.952, "label": "person", "id": 13, "confidence": 71, "width": 762.816}'

runCalc(data1, data2)
runCalc(data3, data4)
