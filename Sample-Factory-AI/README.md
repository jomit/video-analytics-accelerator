# Instructions to Test the Factory AI Vision solution
### Create Simulated IoT Edge Device

Quickstart [here](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux)

- `az group create --name iotedgevision --location westus2`

- `az iot hub create --resource-group iotedgevision --name jomitvisionhub --sku F1 --partition-count 2`

- `az iot hub device-identity create --device-id visiondevice1 --edge-enabled --hub-name jomitvisionhub`

- `az iot hub device-identity show-connection-string --device-id visiondevice1 --hub-name jomitvisionhub`

- `az deployment group create \
--resource-group iotedgevision \
--template-uri "https://aka.ms/iotedge-vm-deploy" \
--parameters dnsLabelPrefix='factoryaivm' \
--parameters adminUsername='jomit' \
--parameters deviceConnectionString=$(az iot hub device-identity show-connection-string --device-id visiondevice1 --hub-name jomitvisionhub -o tsv) \
--parameters authenticationType='password' \
--parameters adminPasswordOrKey="<REPLACE_WITH_PASSWORD>"`


- `ssh jomit@factoryaivm.westus2.cloudapp.azure.com`

- `sudo systemctl status iotedge`

- `journalctl -u iotedge`

- `sudo iotedge list`

### Open Ports for Factory AI

- `az network nsg rule create -g iotedgevision --nsg-name <nsg-name> -n AllowEdgeVisionDashboard --priority 100 --access Allow --direction Inbound --destination-port-ranges 8080 5000`


### Create Custom Vision Resource

- Create new [customvision.ai](https://www.customvision.ai/) resource or using existing one and copy the EndPoint and Key from [here](https://www.customvision.ai/projects#/settings)

### Deploy Factory AI Edge Modules

- Replace these values in `deployment.amd64.json`. See `deployment.sample.json` for updated file.
    - `<Training Endpoint>` = Custom vision EndPoint url
    - `<Training API Key>` = Custom vision Key
    - `<cpu or gpu>` = cpu or gpu
    - `<Docker Runtime>` = runc or nvidia

- `az iot edge set-modules --device-id visiondevice1 --hub-name jomitvisionhub --content deployment.amd64.json`

- Browse the Factory AI Dashboard at [`http://factoryaivm.westus2.cloudapp.azure.com:8080/`](http://factoryaivm.westus2.cloudapp.azure.com:8080/)


### Use your RTSP stream from IP Camera or deploy a Simulated RTSP Server as below

- If you want to build your custom docker image see instructions [here](rtspsim-live555/readme.md). And replace the image name below with your name.

- `az network nsg rule create -g iotedgevision --nsg-name <nsg-name> -n Live555 --priority 101 --access Allow --direction Inbound --destination-port-ranges 554`

- Copy `rtspsim-live555\climbinggears.mkv` to the VM

- `ssh jomit@factoryaivm.westus2.cloudapp.azure.com`

- Map the local folder with the mkv file (example: `/home/jomit/videos`) to the container and start the server

    - `sudo docker run --rm -it -p 554:554 -v /home/jomit/videos:/live/mediaServer/media --name live555 jomit/live555:latest`

- Test RTSP stream at `rtsp://factoryaivm.westus2.cloudapp.azure.com:554/media/climbinggears.mkv`

- Add the Camera in Factory AI Dashboard and test it

## Resources

- [Custom vision + Azure IoT Edge for Factory AI](https://github.com/Azure-Samples/azure-intelligent-edge-patterns/tree/master/factory-ai-vision#custom-vision--azure-iot-edge-for-factory-ai)