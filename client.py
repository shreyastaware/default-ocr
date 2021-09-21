import requests, time, base64, glob, os

# url = "http://127.0.0.1:5000/tesseract"
url = "http://127.0.0.1:5000/easyocr"

begin = time.time()

input_directory = "/home/shreyastaware/Desktop/python_scraping/captcha_decoder_api/IMAGES/2-gujrat-univ/total_images"

imgs = glob.glob(os.path.join(input_directory, "*"))

max_count = len(imgs)
count = 0

for i, img_path in enumerate(imgs):

    with open(img_path, "rb") as f:
        str_b64 = base64.b64encode(f.read())

    payload = {'img' : str_b64}

    response = requests.post(url, data = payload)

    try:
        res = response.json()
        # print(res)
        print(res['result'])
        # print(os.path.basename(img_path))

        if os.path.basename(img_path).split('.')[0] == res['result']:
            count += 1

    except ValueError:

        print(response)
        print("Response content is not valid JSON")

    # if i == 8:
    #     break

print(count, max_count, float(count*100/max_count))

end = time.time()

total_time = end-begin

print(total_time)

