#### Create Simulated IoT Edge Device

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

#### Open Ports for Factory AI

- `az network nsg rule create -g iotedgevision --nsg-name <nsg-name> -n AllowEdgeVisionDashboard --priority 100 --access Allow --direction Inbound --destination-port-ranges 8080 5000`


#### Create Custom Vision Resource

- Create new [customvision.ai](https://www.customvision.ai/) resource or using existing one and copy the EndPoint and Key from [here](https://www.customvision.ai/projects#/settings)

#### Deploy Factory AI Edge Modules

- Replace these values in `deployment.amd64.json`. See `deployment.sample.json` for updated file.
    - `<Training Endpoint>` = Custom vision EndPoint url
    - `<Training API Key>` = Custom vision Key
    - `<cpu or gpu>` = cpu or gpu
    - `<Docker Runtime>` = runc or nvidia

- `az iot edge set-modules --device-id visiondevice1 --hub-name jomitvisionhub --content deployment.amd64.json`


#### Deploy Simulated RTSP Server

- `az network nsg rule create -g iotedgevision --nsg-name <nsg-name> -n Live555 --priority 101 --access Allow --direction Inbound --destination-port-ranges 554`

- `ssh jomit@factoryaivm.westus2.cloudapp.azure.com`

- `docker run --rm -it -p 554:554 --name live555 jomit/live555:latest`

- Use VLC to browse the RTSP stream at `rtsp://<IoT-Edge-VM-IP>:554/media/tentvideo.mkv`
