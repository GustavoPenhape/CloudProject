import uuid
import math
from support_functions_ostack import get_token_for_admin, get_token_for_admin_in_project, get_flavors, get_images,build_network, build_subnet, build_port,get_console_url_per_instance,create_topology 
class TopoConstructor:
    def lineConstructor(self,VMs,CIDR,neutron,nova):
        numberNetworks = len(VMs) - 1
        networks = []
        #Create Networks
        for i in range(numberNetworks):
            nameNetwork = str(uuid.uuid4())
            networks.append(nameNetwork)
            nameSubnet = str(uuid.uuid4())
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova) 
        #Create VMs
        for i in range(len(VMs)):
            if i == 0:
                VMConstructor.createVM(VMs[i],[networks[i]],neutron,nova)
            elif i == (len(VMs) - 1):
                VMConstructor.createVM(VMs[i],[networks[i-1]],neutron,nova)
            else:
                VMConstructor.createVM(VMs[i],[networks[i-1],networks[i]],neutron,nova)
        return 1
    
    def ringConstructor(self,VMs,CIDR,neutron,nova):
        numberNetworks = len(VMs)
        networks = []
        #Create Networks
        for i in range(numberNetworks):
            nameNetwork = str(uuid.uuid4())
            networks.append(nameNetwork)
            nameSubnet = str(uuid.uuid4())
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova)
        #Create VMs
        for i in range(len(VMs)):
            VMConstructor.createVM(VMs[i],[networks[i-1],networks[i]],neutron,nova)
        return 1
    

    def busConstructor(self,VMs,CIDR,neutron,nova):
        numberNetworks = 1
        networks = [] 
        #Create Networks
        for i in range(numberNetworks):
            nameNetwork = str(uuid.uuid4())
            networks.append(nameNetwork) # network = ["asxcsda","asdqoi","foiwenfweip"]
            nameSubnet = str(uuid.uuid4())
            network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
            NetworkConstructor.createNetwork(network,neutron,nova)
        #Create VMs
        for i in range(len(VMs)):
            VMConstructor.createVM(VMs[i],[networks[0]],neutron,nova)
        return 1

    def linkConstructor(VMs, network,neutron, nova, CIDR):
        #Crear enlace entre dos vms
        if len(network) == 0 and len(VMs) == 2:
            networkC = networkConstructor(CIDR=CIDR,neutron=neutron,nova=nova)
            for vm in VMs:
                VMConstructor.editVM(VM=vm,network=networkC.nameNetwork,neutron=neutron,nova=nova)
            return 1
        elif len(network) == 1 and len(VMs) == 1:
            VMConstructor.editVM(VM=VMs[0],network=network[0],neutron=neutron,nova=nova)
            return 1
        else:
            return 1
        
    def linkDestructor(VM, network, neutron, nova):
        pass
        
def networkConstructor(CIDR,neutron,nova):
        nameNetwork = str(uuid.uuid4())
        nameSubnet = str(uuid.uuid4())
        network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
        NetworkConstructor.createNetwork(network,neutron,nova)
        return network            

