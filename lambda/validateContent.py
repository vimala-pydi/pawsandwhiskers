
import json
import boto3
import urllib3


def check_albs(alb_names):

  global message
  
  found_traefik_ping = False
  found_hamilton_behind_traefik = False

  # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_load_balancers
  #alb_response = elbv2.describe_load_balancers(LoadBalancerArns=svc['loadBalancers'])
  alb_response = elbv2.describe_load_balancers(Names=alb_names)
  for alb in alb_response['LoadBalancers']:
    dnsname = alb['DNSName']

    #req  = requests.get("http://"+dnsname+":8080/ping", verify=False, timeout=3)
    #code = req.status_code
    #body = req.text
    http = urllib3.PoolManager(timeout=5)
    print("Checking ping: http://"+dnsname+":8080/ping")
    resp = http.request('GET', "http://"+dnsname+":8080/ping", retries=False)
    status = resp.status
    body = resp.data.decode('utf-8')
    print("ping status:",status)

    #req  = requests.get(, verify=False, timeout=3)
    #code = req.status_code
    #body = req.text
    if status == 200:
      metadata["Found Traefik ping healthcheck"] = "Connected to Traefik ping Healthcheck"
      found_traefik_ping = True
    else:
      metadata["Found Traefik ping healthcheck"] = "Could not connect to Traefik ping Healthcheck"
      message = message + "Unable to connect to Traefik ping healthcheck. The service may be still starting up; "

    #req  = requests.get("http://"+dnsname+":80/api/1-0/hamilton", verify=False, timeout=3)
    #code = req.status_code
    #body = req.text

    http = urllib3.PoolManager()
    print("Checking Hamilton: "+"http://"+dnsname+":80/api/1-0/hamilton")
    resp = http.request('GET', "http://"+dnsname+":80/api/1-0/hamilton", retries=False)
    status = resp.status
    print("Hamilton Status:",status)
    body = resp.data.decode('utf-8')

    if status == 200:
      metadata["Found services behind Traefik router"] = "Connected to services behind Traefik"
      found_hamilton_behind_traefik = True
    else:
      metadata["Found services behind Traefik router"] = "Could not connect to services behind Traefik"
  return [found_traefik_ping, found_hamilton_behind_traefik]


def check_task_definition_for_traefik(task_definition_family):
  #print("Found Services:",found_services)
  #if not found_traefik_service and len(found_services) > 0:
  print("Could not find Traefik named service in ECS.. But there is a Service found.")
  print("Examining Task Definition: "+task_definition_family)
  ##
  ## Get Service configuration
  ## Get Task Definition configuration
  ## Check Task Definition traefik container
  ##
  # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_services
  #for task_definition_family in found_services:
  #  print("  * "+task_definition_family)
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_task_definition
  taskdefinition_response = ecs.describe_task_definition(taskDefinition=task_definition_family)
  if 'taskDefinition' in taskdefinition_response:
    if 'containerDefinitions' in taskdefinition_response['taskDefinition']:
      print(taskdefinition_response['taskDefinition']['containerDefinitions'])
      for cd in taskdefinition_response['taskDefinition']['containerDefinitions']:
        print("  * Image: ["+cd['image']+"]")
        if 'traefik' in cd['image']:
          print("  FOUND Traefik Container Image")
          found_traefik_service = True
          return True
  return False



def lambda_handler(event, context):

  # Available data provided in the event
  eventTitle        = event.get("eventTitle", None)
  challengeTitle    = event.get("challengeTitle", None)
  taskTitle         = event.get("taskTitle", None)
  teamDisplayName   = event.get("teamDisplayName", None)
  userInput         = event.get("userInput", None) # <-- userInput only available if using the 'Lambda With Input' validation type
  stackOutputParams = event.get("stackOutputParams", {})

  # Example: using CloudFormation stack output param" +
  # bucketName = stackOutputParams.get("S3BucketName", None)

  global completed
  completed = False
  global progress_percent
  progress_percent = 0
  global message
  message   = "" # "Not yet completed"
  global metadata
  metadata  = {
    "Traefik Service":                             "Not Found",
    "Traefik Service Status":                      "Not Found",
    "Traefik Service Desired Count":               "Not Found",
    "Traefik Service Running Count":               "Not Found",
    #"Traefik Service Pending Count":               "Not Found",
    "Traefik Service Launch Type":                 "Not Found",
    "Load Balancers Connected to Traefik Service": "Not Found",
    "Found Traefik ping healthcheck":              "Not Found",
    "Found services behind Traefik router":        "Not Found",
  }

  global found_traefik_service
  found_traefik_service = False
  global found_status_active
  found_status_active   = False
  global found_desired_count
  found_desired_count   = False
  global found_running_count
  found_running_count   = False
  global found_pending_count
  found_pending_count   = False
  global found_launch_type
  found_launch_type     = False
  global found_load_balancers_connected_to_service
  found_load_balancers_connected_to_service = False

  global found_traefik_ping
  found_traefik_ping=False
  global found_hamilton_behind_traefik
  found_hamilton_behind_traefik=False

  global found_services
  found_services = []
  
  alb_names = []

  #######
  ## * List services
  ## * Look for Traefik
  ## * Look for healthy service
  ## * Curl the endpoints for ping and the API's
  #######
  global ecs
  ecs = boto3.client('ecs')
  global elbv2
  elbv2 = boto3.client('elbv2')


  # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_clusters
  cluster_response = ecs.list_clusters()
  for cluster_arn in cluster_response['clusterArns']:

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_services
    list_services_response = ecs.list_services(
      cluster    = cluster_arn,
      launchType = 'FARGATE'
    )
    for svc_arn in list_services_response['serviceArns']:
      # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_services
      services_response = ecs.describe_services(
        cluster  = cluster_arn,
        services = [svc_arn]
      )

      for svc in services_response['services']:
        svcn = svc['serviceName'].lower()
        if svcn not in ["hamilton", "burr", "eliza", "peggy", "angelica"]:
          found_services.append(svc["taskDefinition"])

          if ("traefik" in svcn) or \
             ("traffik" in svcn) or \
             ("traffic" in svcn) or \
             ("traefick" in svcn) or \
             check_task_definition_for_traefik(svc["taskDefinition"]):
            found_traefik_service = True
            progress_percent = progress_percent + 17
            metadata["Traefik Service"] = "Found Traefik Service"

            if 'loadBalancers' in svc:
              if len(svc['loadBalancers']) == 0:
                found_traefik_service = False
                message = message + "Found Traefik Service, but there are no Load Balancers attached; "
              elif len(svc['loadBalancers']) == 1:
                found_traefik_service = False
                message = message + "Found Traefik Service, but there is ONLY one Load Balancer attached. You can not use the AWS Console to create the service and attach the Load Balancer. You must use the AWS CLI. Use a  Clue for how to do it.; "
              elif len(svc['loadBalancers']) > 1:
                found_traefik_service = True
                message = message + "Found Traefik Service, multiple Load Balancers attached; "

            if found_traefik_service:
              if svc['status'] == "ACTIVE":
                metadata["Traefik Service Status"] = svc['status']
                found_status_active = True
                progress_percent = progress_percent + 17

              if svc['desiredCount'] > 0:
                metadata["Traefik Service Desired Count"] = str(svc['desiredCount'])
                found_desired_count = True
                progress_percent = progress_percent + 17

              if svc['runningCount'] > 0:
                metadata["Traefik Service Running Count"] = str(svc['runningCount'])
                found_running_count = True
                progress_percent = progress_percent + 17

          #if svc['pendingCount'] > 0:
          #  metadata["Traefik Service Pending Count"] = str(svc['pendingCount'])
          #  found_pending_count = True
          #  progress_percent = progress_percent + 17
          
          if svc['launchType'] == 'FARGATE':
            metadata["Traefik Service Launch Type"] = svc['launchType']
            found_launch_type = True
            progress_percent = progress_percent + 17
          else:
            metadata["Traefik Service Launch Type"] = svc['launchType'] + ", should be FARGATE"

          alb_names = []
          if len(svc['loadBalancers']) > 0:
            metadata["Load Balancers Connected to Traefik Service"] = str(svc['loadBalancers'])
            found_load_balancers_connected_to_service = True
            progress_percent = progress_percent + 17
            for alb in svc['loadBalancers']:
              print("ALB:",alb,"\n")
              # 'loadBalancers': [{
              #     'targetGroupArn': 'string',
              #     'loadBalancerName': 'string',
              #     'containerName': 'string',
              #     'containerPort': 123
              # },
              if 'loadBalancerName' in alb:
                alb_names.append(alb['loadBalancerName'])
            ##
            ## List ALB
            ## Connect to ALB with Curl
            ##   Connect to port 80 hamilton
            ##   Connect to port 8080 ping
            ##


  ret = check_albs(alb_names)
  print("check_albs results:",str(ret))
  found_traefik_ping = ret[0]
  found_hamilton_behind_traefik = ret[1]

  if not found_status_active:
    message = message + "Service Status is NOT active. Just wait a bit longer, or check if there is an error; "

  if not found_desired_count:
    message = message + "Desired Service Count is not correct. Check if the Service is failing to start; "

  if not found_running_count:
    message = message + "Running Service Count is not correct. Check if the Service is failing to start; "

  #if not found_traefik_ping:
  #  message = message + "Unable to connect to Traefik ping healthcheck. The service may be still starting up; "

  if not found_load_balancers_connected_to_service:
    message = message + "Unable to connect to ALB; "



  print("found_traefik_service....................:",str(found_traefik_service))
  print("found_status_active......................:",str(found_status_active))
  print("found_desired_count......................:",str(found_desired_count))
  print("found_running_count......................:",str(found_running_count))
  print("found_pending_count......................:",str(found_pending_count))
  print("found_launch_type........................:",str(found_launch_type))
  print("found_traefik_ping.......................:",str(found_traefik_ping))
  print("found_hamilton_behind_traefik............:",str(found_hamilton_behind_traefik))
  print("found_load_balancers_connected_to_service:",str(found_load_balancers_connected_to_service))

  # 100 / 8 = 12.5
  # 100 / 7 = 14.285714285714286
  # 100 / 6 = 16.666666666666667
  if (found_traefik_service and \
      found_status_active and \
      found_desired_count and \
      found_running_count and \
      #found_pending_count and \
      found_launch_type and \
      found_traefik_ping and \
      #found_hamilton_behind_traefik and \
      found_load_balancers_connected_to_service):
    completed = True



  return {
    "completed": completed, # required: whether this task is completed
    "message":   message,   # required: a message to display to the team indicating progress or next steps
    "progressPercent": progress_percent,   # optional: any whole number between 0 and 100
    "metadata":  metadata, # optional: a map of key:value attributes to display to the team
  }




if __name__ == "__main__":
  print(handler({}, ""))

