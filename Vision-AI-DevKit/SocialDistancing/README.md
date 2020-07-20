## Social distance monitoring using Vision AI Dev Kit

<Architecture image here...>

### Prerequisites

- Follow the [Quick Start](https://azure.github.io/Vision-AI-DevKit-Pages/docs/quick_start/) and setup your Vision AI DevKit.

- [Connect to the video stream](https://azure.github.io/Vision-AI-DevKit-Pages/docs/RTSP_stream/#connect-to-the-video-stream) and verify

### Deployment Guide

- Use the `edgeDeployment.json` and deploy the modules to your Vision AI DevKit edge device using [Azure CLI](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-deploy-modules-cli#deploy-to-your-device), [Azure Portal](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-deploy-modules-portal) or [Visual Studio Code](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-deploy-modules-vscode). 

    - `az iot edge set-modules --device-id [device id] --hub-name [hub name] --content edgeDeployment.json`

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