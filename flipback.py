#!/usr/bin/env python
# coding: utf-8
import time
import boto3

client = boto3.client('ec2',region_name='us-east-1')
describe_instance =client.describe_instances()

Instance_Id = []
Instance_Type = ""
describe_instance_i = {}
for i in describe_instance['Reservations']:
    for j in i['Instances']:
        for tag in j['Tags']:
            if tag['Value'] == "Testing_Server":
                describe_instance_i = client.describe_instances(InstanceIds=[j['InstanceId']])
                print('{} has tag {}'.format(j['InstanceId'], tag['Value']))
                print('Instance type of {} is {}'.format(j['InstanceId'], j['InstanceType']))
                Instance_Id.append(j['InstanceId'])
                Instance_Type += j['InstanceType']
        print("*"*30)   

current_state = describe_instance_i['Reservations'][0]['Instances'][0]['State']['Name']

#flip back to previous instance state
print("STOPPING THE INSTANCE AND CHANGING THE INSTANCE TYPE TO IT'S ORIGINAL")
for instance in Instance_Id:
    
    response = client.stop_instances(InstanceIds=[instance])
    for state in response['StoppingInstances']:
        current_state = state['CurrentState']['Name']
        print("After stopping current state is:: ",current_state)
        while current_state == "stopping" or current_state == "stopped":
            time.sleep(25)
            modify_instance = client.modify_instance_attribute(InstanceId=instance,InstanceType={'Value':Instance_Type})
            if (modify_instance['ResponseMetadata']['HTTPStatusCode'] == 200):
                describe_current_state_instance = client.describe_instances(InstanceIds=[instance])
                current_state = describe_current_state_instance['Reservations'][0]['Instances'][0]['State']['Name']
                print("Current instance State is::  ",current_state)
                print("Starting the instance")
                start_response = client.start_instances(InstanceIds = [instance])
                time.sleep(25)
                current_state = start_response['StartingInstances'][0]['CurrentState']['Name']
                print("Current state after starting the instance:: ",current_state)
    