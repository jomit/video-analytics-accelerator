# Social distance monitoring using Vision AI Dev Kit

<Architecture image here...>

### Prerequisites

- Follow the [Quick Start](https://azure.github.io/Vision-AI-DevKit-Pages/docs/quick_start/) and setup your Vision AI DevKit.

- [Connect to the video stream](https://azure.github.io/Vision-AI-DevKit-Pages/docs/RTSP_stream/#connect-to-the-video-stream) and verify

### Deployment Guide

- Use the `edgeDeployment.json` and deploy the modules to your Vision AI DevKit edge device using [Azure CLI](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-deploy-modules-cli#deploy-to-your-device), [Azure Portal](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-deploy-modules-portal) or [Visual Studio Code](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-deploy-modules-vscode). 

    - `az iot edge set-modules --device-id [device id] --hub-name [hub name] --content edgeDeployment.json`

### Testing Guide

- Find the IP address of your camera
    - `adb shell ifconfig wlan0`

- Open the camera stream using VLC or other tools
    - `rtsp://<IP address of camera>:8900/live`

- Monitor IoT Hub messages. 
    - `az iot hub monitor-events --hub-name <iot-hub-name> --device-id <device-id>`
    - The messages are sent every 5 seconds (which is configurable)
    - Once 2 persons are detected in a frame, it sends a message of `{"type": "distanceAlert", "riskLevel" : <high, medium or low>}`
    <PRE>
    {
        "event": {
            "origin": "visiondevkit",
            "payload": "{\"height\": 254.988, \"confidence\": 67, \"id\": 2, \"width\": 193.92, \"position_y\": 531.9, \"label\": \"person\", \"position_x\": 689.856}"
        }
    }
    {
        "event": {
            "origin": "visiondevkit",
            "payload": "{\"type\": \"distanceAlert\", \"riskLevel\": \"medium\"}"
        }
    }</PRE>

### Development Guide

- Set up [Linux](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-develop-for-linux) or [Windows](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-develop-for-windows) development environment for IoT Edge

- Open folder in Visual Studio Code and make necessary updates.

- Change the version in `SocialDistancingInferenceModule\module.json` file

- Right click on `SocialDistancing\deployment.template.json` file and select `Build and Push IoT Edge Solution`

- Right click on `SocialDistancing\deployment.template.json` file and select `Generate IoT Edge Deployment Manifest`. This will generate the deployment manifest in `SocialDistancing\config` folder.

- Right click on the generated manifest file and select `Create Deployment for Single Device`

- Select your device from the list and monitor the deployment on the device.

    - `adb shell iotedge list`
    - `adb shell iotedge logs edgeAgent`
    - `adb shell iotedge logs edgeHub`
    - `adb shell iotedge logs SocialDistancingInferenceModule`

## Resources