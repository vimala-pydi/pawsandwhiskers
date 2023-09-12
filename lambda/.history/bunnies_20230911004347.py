import boto3

def generate_image_list_html(bucket_name):
    s3 = boto3.client('s3')
    try:
       
        # Invoke s3 bucket.
        objects = s3.list_objects_v2(Bucket=bucket_name)
        image_urls = [f"https://{bucket_name}.s3.amazonaws.com/{obj['Key']}" for obj in objects.get('Contents', [])]

        # Generate HTML to display the images
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bunnies - Adopt Bunnies</title>
           <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
           <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
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
        """
        
        for url in image_urls:
            html += f"<li><img src='{url}'></li>"
        
        html += """
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
