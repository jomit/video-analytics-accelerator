import json

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


def calculateDistance(personInfo):
    print("Calculating distance")
    print(personInfo)
    p1 = personInfo[0]
    p2 = personInfo[1]
    d = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
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
        return 1
    elif 0 < d_hor < c_calib_hor and 0 < d_ver < c_calib_ver:
        return 2
    else:
        return 0
    

personInfo = []

inf_obj1 = Test('{"id": 4, "label": "person", "position_y": 441.936, "position_x": 728.832, "width": 693.888, "confidence": 89, "height": 625.968}')
inference = Inference(inf_obj1)
center = [int(inference.position_x + inference.width / 2), int(inference.position_y + inference.height / 2)]
personInfo.append([inference.width, inference.height, center])

inf_obj2 = Test('{"id": 4, "label": "person", "position_y": 675.972, "position_x": 419.904, "width": 236.928, "confidence": 65, "height": 294.948}')
inference = Inference(inf_obj2)
center = [int(inference.position_x + inference.width / 2), int(inference.position_y + inference.height / 2)]
personInfo.append([inference.width, inference.height, center])

result = calculateDistance(personInfo)

print(result)