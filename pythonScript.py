import requests
import json
import time

subscriptionId = ""
# refresh page and get the new bearer
bearer = ""
defaultUrl = f"https://management.azure.com/subscriptions/{subscriptionId}/"

resourceGroupName = "lab4"
virtualNetworkName= "net4"
subnetName= "snet4"
ipName = "ip4"
vmName = "vm4"
networkInterfaceName = "nic4"
apiVersion = "2021-04-01"

def send_httpRequest(url, json_data, headers):


    response = requests.put(url, data=json_data, headers=headers)

    # checking the response
    if response.status_code in {200, 201}:
        print("Successful request\n")
        response_data = response.json()
        print("Response data:\n", response_data)
    else:
        print(f"Error in the request, Status code: {response.status_code}\n\n")

def create_resourceGroup():
    global json_data, headers
    # url for creating resource groups
    urlcreate_resourceGroup = f"{defaultUrl}resourcegroups/{resourceGroupName}?api-version={apiVersion}"

    # necessary json data to create the resource group
    create_resourceGroupPayloadData = {
        "location": "westeurope"
    }
    # converting python data into json format
    json_data = json.dumps(create_resourceGroupPayloadData)

    # set http headers to specify the content type as json
    headers = {"Authorization": f"Bearer {bearer}", 'Content-Type': 'application/json'}

    # call function to send the request and create resource group
    send_httpRequest(urlcreate_resourceGroup, json_data, headers)

def create_virtualNetwork():
    global json_data
    # url for creating virtual network
    urlcreate_virtualNetwork = f"{defaultUrl}resourcegroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}?api-version={apiVersion}"
    
    # json data needed for creating virtual net
    payloadDatacreate_virtualNetwork = {
        "properties": {
            "addressSpace": {
                "addressPrefixes": [
                    "10.0.0.0/16"
                ]
            },
            "flowTimeoutInMinutes": 10
        },
        "location": "westeurope"
    }

    # converting python data into json format
    json_data = json.dumps(payloadDatacreate_virtualNetwork)

    # call function to send the request and create virtual network
    send_httpRequest(urlcreate_virtualNetwork, json_data, headers)

def create_subnet():
    global json_data
    # url for creating subnet
    urlcreate_subnet = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}?api-version={apiVersion}"
   
    # json data needed for creating subnet
    payloadDatacreate_subnet = {
        "properties": {
            "addressPrefix": "10.0.0.0/16"
        }
    }

    # converting python data into json format
    json_data = json.dumps(payloadDatacreate_subnet)

    # call function to send the request and create subnet
    send_httpRequest(urlcreate_subnet, json_data, headers)

def create_ipAddress():
    global json_data
    # url for creating public ip address
    urlcreate_ipAddress = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/publicIPAddresses/{ipName}?api-version={apiVersion}"
    
    # json data needed for creating ip address
    payloadDatacreate_ipAddress = {
        "location": "westeurope"
    }

    # converting python data into json format
    json_data = json.dumps(payloadDatacreate_ipAddress)

    # call function to send the request and create ip address
    send_httpRequest(urlcreate_ipAddress, json_data, headers)
    time.sleep(5)

def create_networkInterface():
    global json_data

    # url to create network interface
    urlcreate_networkInterface = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}?api-version={apiVersion}"
    
    # json data needed for creating nic
    payloadDatacreate_networkInterface = {
        "properties": {
            "ipConfigurations": [
                {
                    "name": "ipconfig1",
                    "properties": {
                        "publicIPAddress": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/publicIPAddresses/{ipName}"
                        },
                        "subnet": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}"
                        }
                    }
                }
            ]
        },
        "location": "westeurope"
    }
    # converting python data into json format
    json_data = json.dumps(payloadDatacreate_networkInterface)

    # call function to send the request and create network interface
    send_httpRequest(urlcreate_networkInterface, json_data, headers)

def create_virtualMachine():
    global json_data
    # url to create VM
    urlcreate_virtualMachine = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}?api-version={apiVersion}"
    
    # json data needed for creating vm
    payloadDatacreate_virtualMachine = {
        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Compute/virtualMachines/{vmName}",
        "type": "Microsoft.Compute/virtualMachines",
        "properties": {
            "osProfile": {
                "adminUsername": "molly",
                "secrets": [

                ],
                "computerName": f"{vmName}",
                "linuxConfiguration": {
                    "ssh": {
                        "publicKeys": [
                            {
                                "path": "/home/molly/.ssh/authorized_keys",
                                "keyData": "ssh-rsa "  }
                        ]
                    },
                    "disablePasswordAuthentication": True
                }
            },
            "networkProfile": {
                "networkInterfaces": [
                    {
                        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}",
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            },
            "storageProfile": {
                "imageReference": {
                    "sku": "16.04-LTS",
                    "publisher": "Canonical",
                    "version": "latest",
                    "offer": "UbuntuServer"
                },
                "dataDisks": [

                ]
            },
            "hardwareProfile": {
                "vmSize": "Standard_D1_v2"
            },
            "provisioningState": "Creating"
        },
        "name": f"{vmName}",
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDatacreate_virtualMachine)

    # call function to send the request and create vm
    send_httpRequest(urlcreate_virtualMachine, json_data, headers)

create_resourceGroup()
create_virtualNetwork()
create_subnet()
create_ipAddress()
create_networkInterface()
create_virtualMachine()

