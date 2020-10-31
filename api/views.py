from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .models import Device,Node


# Create your views here.


def BFS_SP(source_device, destination_device): 
    explored = [] 
      
    # Queue for traversing the  
    # graph in the BFS 
    queue = [[source_device]] 
      
    # If the desired node is  
    # reached 
    if source_device == destination_device: 
        print("Same Node") 
        return
      
    # Loop to traverse the graph  
    # with the help of the queue 
    while queue: 
        path = queue.pop(0) 
        node = path[-1] 
          
        # Codition to check if the 
        # current node is not visited 
        if node not in explored: 
            neighbours = graph[node] 
              
            # Loop to iterate over the  
            # neighbours of the node 
            for neighbour in neighbours: 
                new_path = list(path) 
                new_path.append(neighbour) 
                queue.append(new_path) 
                  
                # Condition to check if the  
                # neighbour node is the goal 
                if neighbour == destination_device: 
                    print("Shortest path = ", *new_path) 
                    return
            explored.append(node) 
  
    # Condition when the nodes  
    # are not connected 
    print("So sorry, but a connecting path doesn't exist :(") 
    return

@csrf_exempt
def devices(request,name=None):
    if request.method == "GET":
        devices = Device.objects.all()
        resp={}
        resp["devices"]=[{"type":device.type,"name":device.name} for device in devices]
        return JsonResponse(resp)

    if request.method == "POST":
        res={"msg":None}
        request_data=json.loads(request.body)
        device_name=request_data["name"]
        typee=request_data["type"]
        if typee not in ["COMPUTER","REPEATER"]:
            res["msg"]="type '{}' is not supported".format(type)
            return JsonResponse(res)

        device, created = Device.objects.get_or_create(
            name=device_name,
            defaults={"type":typee,"name":device_name}
        )
        if created:
            res["msg"]="Successfully added {}".format(device)
        else:
            res["msg"]="Device {} already exists".format(device)
        
        return JsonResponse(res)

    if request.method == "PATCH":
        res={"msg":None}
        request_data=json.loads(request.body)
        value=str(request_data["value"])
        device=None
        try:
            device= Device.objects.get(name=name)
        except Exception as e:
            res["msg"]="Device Not Found"
            return JsonResponse(res)

        if not value.isdigit:
            res["msg"]="value should be an integer"
            return JsonResponse(res)

        device.strength=int(value)
        device.save()
        res["msg"]="Successfully defined strength"
        return JsonResponse(res)

def info_routes(request,frm=None,to=None):
    res={"msg":None}
    res["msg"]="Not Implemented"
    return JsonResponse(res)


@csrf_exempt
def connections(request):
    if request.method == "POST":
        res={"msg":None}
        request_data=json.loads(request.body)
        source=request_data["source"]
        targets=request_data["targets"]

        try:
            source_device= Device.objects.get(name=source)
            if source_device in targets:
                res["msg"]: "Cannot connect device to itself"
                return JsonResponse(res)

            for t in targets:
                #print(t)
                try:
                    target_device= Device.objects.get(name=t)
                    print(target_device)
                    if target_device in source_device.connection.all():
                        res["msg"]="Devices are already connected"
                        return JsonResponse(res)
                    else:
                        source_device.connection.add(target_device)
                except Exception as e:
                    res["msg"]="Device {} not found".format(target_device)
                    return JsonResponse(res)
        except Exception as e:
            res['msg']= "Node {} not found".format(source_device)
            return JsonResponse(res)

        res["msg"]="Successfully connected"
        return JsonResponse(res)


def parse_body(body):
    data = {'cmd_type': None,
            'cmd': None,
            'headers': None,
            'cmd_body': None
            }
    body = [b.decode('utf-8').strip() for b in body]
    headers=None
    cmd_body=None

    # fetching cmd and cmd type
    if body and body[0]:
        cmd_type, cmd = body[0].split(" ")
    if len(body) > 1 and body[1]:
        headers = body[1]
    if len(body) > 3 and body[3]:
        cmd_body = body[3]
        try:
            cmd_body = json.loads(cmd_body)
        except Exception as e:
            cmd_body = {}
    data['cmd_type'] = cmd_type
    data['cmd'] = cmd
    if headers:
        headers={i[0].strip():i[1].strip() for i in headers.split(":")}
    data['headers'] = headers
    data['cmd_body'] = cmd_body
    return data


@csrf_exempt
def process(request):
    res={"msg":None}
    if request.method == "POST":
        print("POST")
        # reading the body text from post method
        body = request.readlines()
        data = parse_body(body)
        cmd_type = data["cmd_type"]
        cmd = data["cmd"]
        headers = data["headers"]
        cmd_body = data["cmd_body"]

        if cmd_type and cmd:
            print(cmd_type, cmd)
            url="http://localhost:8080/api"+str(cmd)
            if headers:
                print(headers)
            if cmd_body:
                print(cmd_body)
            if cmd_type == "CREATE":
                if not cmd_body:
                    res["msg"]="Invalid Command."
                    return JsonResponse(res)  
                res=requests.post(url,json=cmd_body)
                return JsonResponse(res.json())
            elif cmd_type == "MODIFY":
                res=requests.patch(url,json=cmd_body)
                return JsonResponse(res.json())
            elif cmd_type == "FETCH":
                res=requests.get(url,json=cmd_body)
                return JsonResponse(res.json())

        # print(str(body))
    return HttpResponse()
