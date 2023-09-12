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
   # Calculate the number of rows based on the number of images and three images per row
    num_rows = (len(images) + 2) // 3  # Add 2 to round up to the nearest integer

    # Define a list of background colors for tiles
    tile_colors = ['#f4d942', '#83d4fa', '#a9e34b', '#ffa8a8', '#b19cd9', '#c4d6b0']

    # Iterate through the rows
    for row in range(num_rows):
        # Start a new row
        html += "<div style='display: flex;'>"

        # Iterate through the images in the current row
        for i in range(3):
            index = row * 3 + i
            if index < len(images):
                # Resize the image to fit into a square tile (adjust the width and height as needed)
                img_tag = f"<img src='{images[index]}' alt='Image' style='max-width: 100%; height: auto; width: 33.33%;'>"

                # Get the background color for the current tile
                tile_color = tile_colors[(row * 3 + i) % len(tile_colors)]

                # Create a div with the image and background color
                tile = f"<div style='margin: 10px; width: 33.33%; background-color: {tile_color};'>{img_tag}</div>"
                html += tile

        # Close the current row
        html += "</div>"

    # Close the HTML document
    html += "</body></html>"

    return html

def lambda_handler(event, context):
    # Provide a list of image URLs in the 'src' variable
    image_urls = [
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny1-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny2-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny3-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunny4-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunnies5-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunnies6-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunnies7-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunnies8-min.jpg',
        'https://aws-jam-challenge-resources.s3.amazonaws.com/pawsandwhiskers/bunnies9-min.jpg'
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
