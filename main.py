import requests
import json
import time
import requests
from datetime import datetime

with open('token.txt', 'r') as f:
    TOKEN = f.read().strip()

headers = {
    "API-Key": TOKEN
}

def generateSDXLImage(prompt="", samples=1) : 
    
    data = {
        "model_id":  "d961a274-658c-4889-8c1a-bf85416cb1c1",
        "prompt": prompt,
        "negative_prompt": "error, cropped, worst quality, low quality, duplicate, bad proportions, incomplete subject",
        "num_inference_steps": 30,
        "refiner": True,
        "samples": samples,
        "guidance_scale": 7.5,
        "width": 768,
        "height": 768,
        "safety_checker": True,
        "seed": 12345,
    }

    response = requests.post("https://api.imagepipeline.io/sdxl/text2image/v1", headers=headers, data=json.dumps(data))
    statusUrl = "https://api.imagepipeline.io/sdxl/text2image/v1/status/" + response.json()['id']
    fns = saveImagePipleline(statusUrl)

    return fns

def saveImagePipleline(statusUrl):
    fileNames = []
    while True:
        # Send a GET request to ID URL
        response = requests.get(statusUrl, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            if response.json()['status'] == "SUCCESS" :
            # Open a file in binary write mode
                files = response.json()['download_urls']
                for i, image in enumerate(files):
                    f = saveImage(image)
                    if f: fileNames.append(image)
                break
            elif response.json()['status'] == "FAILURE" :
                break
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
            break

        time.sleep(1)

    return fileNames

def saveImage(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f"generated/{timestamp}.png", "wb") as file:
            file.write(res.content)
        return True
    return False

urls = generateSDXLImage(
    prompt="Envision a futuristic cityscape at dawn, as seen from a high vantage point. The architecture is a blend of hyper-modern skyscrapers with sleek, reflective surfaces and eco-friendly green roofs teeming with lush vegetation. Hover cars and drones zip through the air, following invisible traffic lanes, while pedestrians move along floating walkways that connect the buildings at various levels. The sky is painted with hues of soft pink and orange, signaling the break of day, and the city is coming to life with the gentle hum of advanced technology. In the foreground, a large, transparent dome houses a vibrant public park, where people and robots coexist peacefully. The entire scene is a harmonious fusion of nature and technology, symbolizing a sustainable and advanced society.",
    samples=4)

print(urls)

# Example Prompts

# Create a digital painting of a serene and mystical forest at twilight. The forest is illuminated by the soft glow of fireflies, with ancient trees towering into the sky. Their trunks are twisted and covered in luminous moss and delicate ivy. A gentle stream meanders through the forest, reflecting the last rays of the setting sun. In the background, a quaint wooden cabin with a thatched roof emits a warm light from its windows, suggesting a cozy refuge in the heart of the woods. The sky above is a gradient of deep indigo and violet, with the first stars of the night beginning to twinkle. A majestic owl is perched on a gnarled branch, surveying the enchanting scene.
# Envision a futuristic cityscape at dawn, as seen from a high vantage point. The architecture is a blend of hyper-modern skyscrapers with sleek, reflective surfaces and eco-friendly green roofs teeming with lush vegetation. Hover cars and drones zip through the air, following invisible traffic lanes, while pedestrians move along floating walkways that connect the buildings at various levels. The sky is painted with hues of soft pink and orange, signaling the break of day, and the city is coming to life with the gentle hum of advanced technology. In the foreground, a large, transparent dome houses a vibrant public park, where people and robots coexist peacefully. The entire scene is a harmonious fusion of nature and technology, symbolizing a sustainable and advanced society.