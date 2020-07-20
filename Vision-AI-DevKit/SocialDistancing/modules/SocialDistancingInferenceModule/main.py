# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import sys
if __package__ == '' or __package__ is None:  # noqa
    import os
    parent_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    pkg_name = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
    __import__(pkg_name)
    __package__ = str(pkg_name)
    del os
from . constants import SETTING_OFF
from . error_utils import CameraClientError, log_unknown_exception
from . properties import Properties
from . model_utility import ModelUtility
from . inference import Inference
from . iot_hub_manager import IotHubManager
from iotccsdk import CameraClient
from iothub_client import IoTHubTransportProvider, IoTHubError
import time
import json

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
IOT_HUB_PROTOCOL = IoTHubTransportProvider.MQTT

ipc_provider = None
camera_client = None
iot_hub_manager = None
properties = None
model_util = None


def create_camera(ip_address=None, username="admin", password="admin"):
    if ip_address is None:
        ip_address = model_util.getWlanIp()

    print("ip address = %s" % ip_address)
    if ipc_provider is None:
        print("Create camera with no ipc_provider")
        return CameraClient.connect(
            ip_address=ip_address,
            username=username,
            password=password)

    print("Create camera with ipc_provider %s" % ipc_provider)
    return CameraClient.connect(
        ipc_provider=ipc_provider,
        ip_address=ip_address,
        username=username,
        password=password)


def print_inference(result=None, hub_manager=None, last_sent_time=time.time()):
    global properties
    if (time.time() - last_sent_time <= properties.model_properties.message_delay_sec
            or result is None
            or result.objects is None
            or len(result.objects) == 0):
        return last_sent_time

    print("Here are all the objects:")
    personInfo = []
    for inf_obj in result.objects:
        inference = Inference(inf_obj)
        if (properties.model_properties.is_object_of_interest(inference.label)):
            json_message = inference.to_json()
            iot_hub_manager.send_message_to_upstream(json_message)
            print(json_message)
            last_sent_time = time.time()

        if inference.label == "person":
            center = [int(inference.position_x + inference.width / 2), int(inference.position_y + inference.height / 2)]
            personInfo.append([inference.width, inference.height, center])

    if len(personInfo) > 1:
        result = calculateDistanceRiskLevel(personInfo)
        print(result)
        distanceMessage = {"type": "distanceAlert", "riskLevel" : result}
        iot_hub_manager.send_message_to_upstream(json.dumps(distanceMessage))

    return last_sent_time

def calculateDistanceRiskLevel(personInfo):
    print("Calculating distance")
    print(personInfo)
    # find distance between first 2 persons only for now
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
        return "high" #1
    elif 0 < d_hor < c_calib_hor and 0 < d_ver < c_calib_ver:
        return "medium" #2
    else:
        return "low" #0
    

def main(protocol):
    global ipc_provider
    global camera_client
    global iot_hub_manager
    global properties
    global model_util

    print("Create model_util")
    model_util = ModelUtility()

    print("Create properties")
    properties = Properties()
    camera_props = properties.camera_properties

    # push model
    model_util.transfer_dlc(False)

    print("\nPython %s\n" % sys.version)
    last_time = time.time()

    while True:
        with create_camera() as camera_client:
            try:
                ipc_provider = camera_client.ipc_provider
                camera_props.configure_camera_client(camera_client)
                iot_hub_manager = IotHubManager(
                    protocol, camera_client, properties)
                iot_hub_manager.subscribe_to_events()

                while True:
                    try:
                        while camera_client.vam_running:
                            with camera_client.get_inferences() as results:
                                for result in results:
                                    last_time = print_inference(
                                        result, iot_hub_manager, last_time)

                    except EOFError:
                        print("EOFError. Current VAM running state is %s." %
                              camera_client.vam_running)
                    except Exception:
                        log_unknown_exception(
                            "Exception from get inferences", iot_hub_manager)
                        continue
            except CameraClientError as cce:
                print("Received camera error, but will try to continue: %s" % cce)
                if camera_client is not None:
                    status = camera_client.logout()
                    print("Logout with status: %s" % status)
                camera_client = None
                continue
            except IoTHubError as iothub_error:
                print("Unexpected error %s from IoTHub" % iothub_error)
                return
            except KeyboardInterrupt:
                print("IoTHubModuleClient sample stopped")
                return
            finally:
                print("Try to clean up before the end")
                if camera_client is not None:
                    camera_client.set_overlay_state(SETTING_OFF)
                    camera_client.set_analytics_state(SETTING_OFF)
                    camera_client.set_preview_state(SETTING_OFF)
                    status = camera_client.logout()
                    print("Logout with status: %s" % status)


if __name__ == '__main__':
    main(IOT_HUB_PROTOCOL)
