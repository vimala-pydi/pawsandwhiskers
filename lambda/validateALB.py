import json
import boto3
import ptvsd

ptvsd.enable_attach(address=('0.0.0.0', 3000))

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

  completed = False
  progress_percent = 0
  message   = "" # "Not yet completed"
  metadata  = {
    "ALB":               "Not Found",
    "HTTP80 Listener":   "Not Found",
    "HTTP8080 Listener": "Not Found",
  }

  #######
  ## * List load balancers
  ## * Look for an ALB in the JAM VPC
  ## * Look for http80 and http8080 listeners
  #######
  elbv2 = boto3.client('elbv2')
  # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_load_balancers
  alb_response = elbv2.describe_load_balancers();
  found_alb = False
  found_listener_http80   = False
  found_listener_http8080 = False
  for alb in alb_response['LoadBalancers']:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_listeners
    found_alb = True
    message = message + "Found Load Balancer; "
    metadata["ALB"]   = "Found Load Balancer"
    listener_response = elbv2.describe_listeners(
      LoadBalancerArn=alb['LoadBalancerArn'],
    )
    for listener in listener_response['Listeners']:
      if listener['Protocol'] == 'HTTP':
        if listener['Port'] == 80:
          found_listener_http80 = True
          message = message + "Found HTTP80 Listener; "
          metadata["HTTP80 Listener"] = "Found HTTP80 Listener"

        if listener['Port'] == 8080:
          found_listener_http8080 = True
          message = message + "Found HTTP8080 Listener; "
          metadata["HTTP8080 Listener"] = "Found HTTP8080 Listener"



  if found_alb:
    progress_percent = 33
    if found_listener_http8080 and found_listener_http80:
      completed = True
      progress_percent = 100
    elif found_listener_http8080 or found_listener_http80:
      progress_percent = 66
      message = message + "1 Listener to go...."
    else:
      message = message + "2 Listeners to go...."
  else:
    message = message + "1 ALB and 2 Listeners to go..."



  return {
    "completed": completed, # required: whether this task is completed
    "message":   message,   # required: a message to display to the team indicating progress or next steps
    "progressPercent": progress_percent,   # optional: any whole number between 0 and 100
    "metadata":  metadata, # optional: a map of key:value attributes to display to the team
  }



if __name__ == "__main__":
  print(lambda_handler({}, ""))


