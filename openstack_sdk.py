import json, requests
def password_authentication_with_unscoped_authorization(auth_endpoint, domain_id, username, password):
    url = auth_endpoint + '/auth/tokens'    

    data = \
        {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": username,
                            "domain": {
                                "id": domain_id
                            },
                            "password": password
                        }
                    }
                }
            }
        }
    try:
        r = requests.post(url=url, data=json.dumps(data))
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud: ",e)
        r=None
    return r

def password_authentication_with_scoped_authorization(auth_endpoint, user_id, password, domain_id, project_id):
    url = auth_endpoint + '/auth/tokens'

    data = \
        {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "id": user_id,
                            "domain": {
                                "id": domain_id
                            },
                            "password": password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {
                            "id": domain_id
                        },
                        "id": project_id
                    }
                }
            }
        }
        
    r = requests.post(url=url, data=json.dumps(data))
    # status_code success = 201
    return r

def token_authentication_with_scoped_authorization(auth_endpoint, token, domain_id, project_id):
    url = auth_endpoint + '/auth/tokens'

    data = \
        {
            "auth": {
                "identity": {
                    "methods": [
                        "token"
                    ],
                    "token": {
                        "id": token
                    }
                },
                "scope": {
                    "project": {
                        "domain": {
                            "id": domain_id
                        },
                        "id": project_id
                    }
                }
            }
        }

    r = requests.post(url=url, data=json.dumps(data))
    # status_code success = 201
    return r

def assign_role_to_user_on_project(auth_endpoint, token, project_id, user_id, role_id):
    url = auth_endpoint + '/projects/' + project_id + '/users/' + user_id + '/roles/' + role_id
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

    r = requests.put(url=url, headers=headers)
    # status_code success = 204
    return r

def create_project(auth_endpoint, token, domain_id, project_name, project_description):
        
    url = auth_endpoint + '/projects'
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

    data = \
        {
            "project": {
                "name": project_name,
                "description": project_description,
                "domain_id": domain_id
            }
        }

    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    # status_code success = 201
    return r

def list_projects(auth_endpoint, token, user_id):
    
    url = auth_endpoint + '/users/' + user_id + '/projects'
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

    r = requests.get(url=url, headers=headers)
    return r

# NEUTRON API
def create_network(auth_endpoint, token, name):
    url = auth_endpoint + '/networks'
    data = \
        {
            "network": {
                "name": name,
                "port_security_enabled": "false",
            }
        }
        
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    # status_code success = 201
    return r

def create_subnet(auth_endpoint, token, network_id, name, ip_version, cidr):
    url = auth_endpoint + '/subnets'
    data = \
        {
            "subnet": {
                "network_id": network_id,
                "name": name,
                "enable_dhcp": False,
                "gateway_ip": None,
                "ip_version": ip_version,
                "cidr": cidr
            }
        }

    data = data=json.dumps(data)

    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    r = requests.post(url=url, headers=headers, data=data)
    # status_code success = 201
    return r

def create_port(auth_endpoint, token, name, network_id, project_id):
    url = auth_endpoint + '/ports'
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

    data = \
        {
            'port': {
                'name': name,
                'tenant_id': project_id,
                'network_id': network_id,
                'port_security_enabled': 'false'
            }
        }

    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    # status_code success = 201
    return r


def get_server_console(nova_endpoint, token, server_id, compute_api_version):
    url = nova_endpoint + '/servers/' + server_id + '/remote-consoles'
    headers = {
        'Content-type': 'application/json',
        'X-Auth-Token': token,
        "OpenStack-API-Version": "compute " + compute_api_version
    }
    
    data = \
        {
            "remote_console": {
                "protocol": "vnc",
                "type": "novnc"
                }
        }
    
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    # status_code success = 200
    return r

def create_server(nova_endpoint, token, name, flavor_id, image_id, networks=None):
    url = nova_endpoint + '/servers'
    headers = {
        'Content-type': 'application/json',
        'X-Auth-Token': token,
    }
    
    data = \
        {
            'server': {
                'name': name,
                'flavorRef': flavor_id,
                'imageRef': image_id,
                'networks': networks,
            }
        }
    
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    # status_code success = 202
    return r

def list_flavors(nova_endpoint, token):
    url = nova_endpoint + '/flavors/detail'
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    r = requests.get(url=url, headers=headers)
    # status_code success = 200
    return r

def list_images(auth_endpoint, token, limit=None):
    url = auth_endpoint + '/images'
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

    if limit is not None:
        params = {'limit': limit}
        r = requests.get(url=url, headers=headers, params=params)
    else:
        r = requests.get(url=url, headers=headers)
    return r

