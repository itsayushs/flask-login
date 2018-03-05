# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 15:19:26 2018
dynamodb func
@author: Ayush Sharma
"""
import boto3 
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb", region_name='ap-south-1', endpoint_url="http://localhost:8000")
table = dynamodb.Table('users')
def getpass(username):
    uname=username 
    try:
        response = table.get_item(
            Key={
                'uname': uname
            }
        )
    except ClientError as e:
        error = e.response['Error']['Message']
        return error
    else:
        item = response['Item']
#      print("GetItem succeeded:") print(json.dumps(item, indent=4, cls=DecimalEncoder))
        return item['pass']
def setdets(uname,passs,email):
    response = table.put_item(
       Item={
            'uname': uname,
            'pass': passs,
            'email': email
        }
    )
    return True

def query(uname):
    response = table.query(
    KeyConditionExpression=Key('uname').eq(uname))
    if response['Count']==0:
        return True #    no such user exist
    else:
        return False