#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: vivek Mistry @[Vivek M.]​
Date: 31-05-2018 10:25

Disclaimer:
All information, documentation, and code is provided to you AS-IS and should
only be used in an internal, non-production laboratory environment.

License:
Copyright 2017 BlueCat Networks, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import requests
import logging
from getpass import getpass
import sys
from time import sleep
from ipaddress import ip_network

logging.basicConfig(
                filename="debug-rest.log",
                level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p'
                    )


def get(bam_url, api_call, call_parameters, header):
    """requests get call that returns the json data"""

    call_url = "http://"+bam_url+"/Services/REST/v1/"+api_call+"?"
    try:
        if call_parameters == "":
            response = requests.get(call_url, headers=header)
        else:
            response = requests.get(
                                    call_url,
                                    params=call_parameters,
                                    headers=header
                                    )

        # print(response.text)
        if response.status_code != 200:
            raise requests.ConnectionError(
                    "Code "+str(response.status_code)+" "+response.json()
                    )

    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    return response.json()


def post(bam_url, api_call, call_parameters, header):
    """requests get call that returns the json data"""

    call_url = "http://"+bam_url+"/Services/REST/v1/"+api_call+"?"
    try:
        if call_parameters == "":
            raise ValueError("Missing parameters cannot execute")
        else:
            response = requests.post(
                                    call_url,
                                    params=call_parameters,
                                    headers=header
                                    )

        # print(response.text)
        if response.status_code != 200:
            raise requests.ConnectionError(
                    "Code "+str(response.status_code)+" "+response.json()
                    )

    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    return response


def put(bam_url, api_call, call_parameters, header):
    """requests get call that returns the json data"""

    call_url = "http://"+bam_url+"/Services/REST/v1/"+api_call+"?"
    try:
        if call_parameters == "":
            raise ValueError("Missing parameters cannot execute")
        else:
            response = requests.put(
                                    call_url,
                                    params=call_parameters,
                                    headers=header
                                    )

        # print(response.text)
        if response.status_code != 200:
            raise requests.ConnectionError(
                    "Code "+str(response.status_code)+" "+response.json()
                    )

    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    return response

def deletecall(bam_url, api_call, call_parameters, delete_entity, header):
    """API request to delete and return values"""
    call_url = "http://"+bam_url+"/Services/REST/v1/"+api_call+"?"
    print("You are requesting to delete:")
    print(delete_entity)
    answer = input("Do you want to proceed (y (yes) or n (no))? ")
    try:
        if answer.lower() == "y":
            response = requests.delete(
                                        call_url,
                                        params=call_parameters,
                                        headers=header
                                        )
            return response.json()
        elif answer.lower() == "n":
            return "You aborted deletion"
        else:
            return "You entered an invalid character"
    except requests.exceptions.RequestException as e:
        print(e)


def update_header(login_response, call_header):
    """Function to process and update the header after login"""

    token = str(login_response).split()[2] + " " + str(login_response).split()[3]
    call_header['Authorization'] = token
    return call_header

# input = raw_input


user = input("Enter Your User ID: ")
password = getpass("Enter Password: ")
bamurl = "bam.lab.corp"
header = {'Content-Type': 'application/json'}

# Login parameters
login_param = {"username": user, "password": password}

# login to BAM
login = get(bamurl, "login", login_param, header)

# update header with login token
header = update_header(login, header)

# add DHCP Option
taginfo = {"keyword":"torip","types":"Tag", "start":0, "count": 10}
searchresults = get(bamurl, "searchByObjectTypes", taginfo, header)
print(searchresults)
tortag = {}
for tagitem in searchresults:
    if tagitem["name"] == "torip":
        tortag = tagitem

print(tortag)

network = ip_network("192.168.0.0/24")
print(network)
networkid={"id":105015}
getnetwork = get(bamurl,"getEntityById", networkid, header)
getEntitiesparam = { "parentId": getnetwork['id'],  "type": "IP4Address",  "start": 0,  "count": network.num_addresses}
ipaddresslist = get(bamurl, "getEntities", getEntitiesparam, header)
print(ipaddresslist)
for ip in ipaddresslist:
    linentityparam = {"entity1Id": tortag['id'], "entity2Id": ip['id'], "properties":"" }
    print(linentityparam)
    item = put(bamurl,"linkEntities",linentityparam, header)
    print(item.content)
# logout
logout = get(bamurl, "logout", "", header)
print(logout)
