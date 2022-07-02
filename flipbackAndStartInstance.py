#!/usr/bin/env python
# coding: utf-8
import time
import boto3
from texttable import Texttable


client = boto3.client('ec2',region_name='us-east-1')
describe_instance =client.describe_instances()


Instance_Id = []
Instance_Type = ""
Instance_Name = ""
describe_instance_i = {}
for i in describe_instance['Reservations']:
    for j in i['Instances']:
        for tag in j['Tags']:
            if tag['Value'] == "Testing_Server":
                Instance_Name += tag['Value']
                describe_instance_i = client.describe_instances(InstanceIds=[j['InstanceId']])
                print('{} has tag {}'.format(j['InstanceId'], tag['Value']))
                print('Instance type of {} is {}'.format(j['InstanceId'], j['InstanceType']))
                Instance_Id.append(j['InstanceId'])
                Instance_Type += j['InstanceType']
        print("*"*60)   

current_state = describe_instance_i['Reservations'][0]['Instances'][0]['State']['Name']
t = Texttable()
#flip back to previous instance state
print("STOPPING THE INSTANCE AND CHANGING THE INSTANCE TYPE TO IT'S ORIGINAL")
for instance in Instance_Id:
    
    response = client.stop_instances(InstanceIds=[instance])
    for state in response['StoppingInstances']:
        describe_instance_instance = client.describe_instances(InstanceIds=[instance])
        current_state_0 = state['CurrentState']['Name']
        print("*"*60)
        print("<<<<After Stopping the instance>>>>")
        t.add_rows([['Name','Instance_Id', 'Instance_Type','Instance_State'], [Instance_Name,instance ,describe_instance_instance['Reservations'][0]['Instances'][0]['InstanceType'],current_state_0]])
        print(t.draw())
        while current_state_0 == "stopping" or current_state_0 == "stopped":
            time.sleep(35)
            modify_instance = client.modify_instance_attribute(InstanceId=instance,InstanceType={'Value':Instance_Type})
            if (modify_instance['ResponseMetadata']['HTTPStatusCode'] == 200):
                describe_current_state_instance = client.describe_instances(InstanceIds=[instance])
                current_state_1 = describe_current_state_instance['Reservations'][0]['Instances'][0]['State']['Name']
                print("*"*60)
                print("<<<<After changing the instance type>>>>")
                t.add_rows([['Name','Instance_Id', 'Instance_Type','Instance_State'], [Instance_Name,instance ,describe_instance_instance['Reservations'][0]['Instances'][0]['InstanceType'],current_state_1]])
                print(t.draw())
                print("*"*60)
                print("<<<<Starting the instance>>>>")
                start_response = client.start_instances(InstanceIds = [instance])
                time.sleep(35)
                current_state_2 = start_response['StartingInstances'][0]['CurrentState']['Name']
                t.add_rows([['Name','Instance_Id', 'Instance_Type','Instance_State'], [Instance_Name,instance ,describe_instance_instance['Reservations'][0]['Instances'][0]['InstanceType'],current_state_2]])
                print(t.draw())
                print("*"*60)
    