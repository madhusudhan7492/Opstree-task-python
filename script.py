#!/usr/bin/env python
# coding: utf-8

# In[1]:


import boto3

client = boto3.client('ec2',region_name='us-east-1')


# In[4]:


describe_instance =client.describe_instances()


# ##  Get the instance_id which has tag as Testing_Server

# In[6]:


Instance_Id = []
Instance_Type = ""
for i in describe_instance['Reservations']:
    for j in i['Instances']:
        for tag in j['Tags']:
            if tag['Value'] == "Testing_Server":
                print('{} has tag {}'.format(j['InstanceId'], tag['Value']))
                print('Instance type of {} is {}'.format(j['InstanceId'], j['InstanceType']))
                Instance_Id.append(j['InstanceId'])
                Instance_Type += j['InstanceType']
        print("*"*30)        


# In[66]:


import subprocess
import time
for instance in Instance_Id:
    describe_instance_i =client.describe_instances(InstanceIds=[instance])
    current_state = describe_instance_i['Reservations'][0]['Instances'][0]['State']['Name']
    response = client.stop_instances(InstanceIds=[instance])
    for state in response['StoppingInstances']:
        current_state = state['CurrentState']['Name']
        print("After stopping current state is:: ",current_state)
        while current_state == "stopped":
            time.sleep(25)
            modify_instance = client.modify_instance_attribute(InstanceId=instance,InstanceType={'Value':'t2.micro'})
            if (modify_instance['ResponseMetadata']['HTTPStatusCode'] == 200):
                describe_current_state_instance = client.describe_instances(InstanceIds=[instance])
                current_state = describe_current_state_instance['Reservations'][0]['Instances'][0]['State']['Name']
                print("Current instance State is::  ",current_state)
                print("Starting the instance")
                start_response = client.start_instances(InstanceIds = [instance])
                time.sleep(25)
                current_state = start_response['StartingInstances'][0]['CurrentState']['Name']
                file1 = subprocess.run(["ansible-playbook","main.yml"])
                print(file1)

            
            

    
    

