import base64

# Convert image file to Base64 string
def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base64_string = base64.b64encode(binary_data).decode('utf-8')
    return base64_string


def base64_to_image(base64_string: str, output_path: str) -> None:
    # Decode the Base64 string
    binary_data = base64.b64decode(base64_string)
    # Write the binary data to an image file
    with open(output_path, "wb") as output_file:
        output_file.write(binary_data)

 
base64_str = image_to_base64("wss.png")
print("Base64 Encoded String:", base64_str)   

 
# base64_to_image(base64_str, "decoded_image.png")
# print("Image successfully saved as 'decoded_image.png'")
