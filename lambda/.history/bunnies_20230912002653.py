import json

def generate_html_response(images):
    # Start the HTML document
    html =  """
    <!DOCTYPE html><html><head><title>Paws, Whiskers AND Friends</titlE>
     <head>
            <title>Bunnies - Adopt Bunnies</title>
            <link rel="stylesheet" type="text/css" href="css/styles.css">
            <link rel="stylesheet" type="text/css" href="css/homestyle.css">
    </head>
    <body>
     <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
              <a class="navbar-brand" href="#">Paws Whiskers & Friends</a>
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
     """
    # Create two horizontal tile containers (two rows)
    html += "<div style='display: flex; flex-wrap: wrap;'>"
    html += "<div style='display: flex; flex-wrap: wrap; width: 50%;'>"

    # Calculate the number of images per row
    num_images_per_row = len(images) // 2

    # Iterate through the list of image URLs and create image tags for each
    for index, src in enumerate(images):
        # Resize the image to fit into a square tile (adjust the width and height as needed)
        img_tag = f"<img src='{src}' alt='Image' style='max-width: 100%; height: auto; width: {100 / num_images_per_row}%;'>"
        html += f"<div style='margin: 10px; width: {100 / num_images_per_row}%;'>{img_tag}</div>"

        # Start a new row for the second set of images
        if index == num_images_per_row - 1:
            html += "</div><div style='display: flex; flex-wrap: wrap; width: 50%;'>"

    # Close the tile containers and the HTML document
    html += "</div></div></body></html>"

    return html

def lambda_handler(event, context):
    # Provide a list of image URLs in the 'src' variable
    image_urls = [
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny1-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny2-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny3-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny4-min.jpg'
        # Add more image URLs as needed
    ]

    # Generate the HTML response with the images resized and arranged in two rows
    html_response = generate_html_response(image_urls)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html_response
    }
