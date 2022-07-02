#!/usr/bin/env python
# coding: utf-8

import time
from texttable import Texttable
import boto3
import os
InstanceType = os.getenv("InstanceType")

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


# In[66]:

current_state = describe_instance_i['Reservations'][0]['Instances'][0]['State']['Name']


t = Texttable()
for instance in Instance_Id:
    
    response = client.stop_instances(InstanceIds=[instance])
    for state in response['StoppingInstances']:
        current_state = state['CurrentState']['Name']
        print("*"*60)
        print("<<<<After Stopping the instance>>>>")
        t.add_rows([['Name','Instance_Id', 'Instance_Type','Instance_State'], [Instance_Name,instance ,Instance_Type,current_state]])
        print(t.draw())
        while current_state == "stopping" or current_state == "stopped":
            time.sleep(25)
            modify_instance = client.modify_instance_attribute(InstanceId=instance,InstanceType={'Value':InstanceType})
            if (modify_instance['ResponseMetadata']['HTTPStatusCode'] == 200):
                describe_current_state_instance = client.describe_instances(InstanceIds=[instance])
                current_state = describe_current_state_instance['Reservations'][0]['Instances'][0]['State']['Name']
                print("*"*60)
                print("<<<<After changing the instance type>>>>")
                t.add_rows([['Name','Instance_Id', 'Instance_Type','Instance_State'], [Instance_Name,instance ,Instance_Type,current_state]])
                print(t.draw())
                print("*"*60)
                print("<<<<Starting the instance>>>>")
                start_response = client.start_instances(InstanceIds = [instance])
                time.sleep(25)
                current_state = start_response['StartingInstances'][0]['CurrentState']['Name']
                t.add_rows([['Name','Instance_Id', 'Instance_Type','Instance_State'], [Instance_Name,instance ,Instance_Type,current_state]])
                print(t.draw())
                print("*"*60)

    

            
            

    
    

