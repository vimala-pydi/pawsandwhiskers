import boto3

def generate_image_list_html(bucket_name):
    try:
    
        # Generate HTML to display the images
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bunnies - Adopt Bunnies</title>
            <link rel="stylesheet" type="text/css" href="/homestyle.css">
            <link rel="stylesheet" type="text/css" href="/styles.css">
        </head>
        <body>
            <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
              <a class="navbar-brand" href="#">Paws , Whiskers & Friends</a>
              <div class="collapse navbar-collapse" id="navbarNav">
                  <ul class="navbar-nav ml-auto">
                        <a class="nav-link" href="index.html">Home</a>
                        <a class="nav-link" href="dogs.html">Paws</a>
                        <a class="nav-link" href="cats.html">Whiskers</a>
                        <a class="nav-link" href="bunnies.html">Bunnies</a>
                </ul>
            </div>
        </div>
    </nav>
    <ul>
       <li><img src="https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny1-min.jpg"/>
       <img src="https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny2-min.jpg"/></li>
       <li><img src="https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny3-min.jpg"/>
       <img src="https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny4-min.jpg"/></li>
    </ul>
        </body>
        </html>
        """
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }

def lambda_handler(event, context):
    # Replace 'your-bucket-name' with your actual S3 bucket name
    bucket_name = 'your-bucket-name'
    
    return generate_image_list_html("bunnies-jam")
