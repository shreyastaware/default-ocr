import numpy as np, base64, easyocr, unicodedata, cv2, pytesseract as pt
reader = easyocr.Reader(['en'], gpu = False)
from flask import Flask, jsonify, request

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

app = Flask(__name__)

@app.route('/tesseract', methods = ['POST'])
def tesseract():

    data = request.form

    im_bytes = base64.b64decode(data['img'])
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    d = pt.image_to_data(img_bin, output_type=pt.Output.DICT)

    probability = 0
    index = 0
    captcha_text = ''
    status = 1

    n_boxes = len(d['text'])
    for i in range(n_boxes):
        probability = max(int(d['conf'][i]), probability)

        if int(d['conf'][i]) == probability:
            index = i
    
    captcha_text = d['text'][index]

    print(captcha_text)

    response = jsonify({
		"probability": probability,
		"request_id": 4,
		"result": captcha_text,
		"status": status
	})

    return response

@app.route('/easyocr', methods = ['POST'])
def easyocr():

    data = request.form

    im_bytes = base64.b64decode(data['img'])
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    text = reader.readtext(img_bin)

    if len(text):
        out = remove_control_characters(" ".join(list(word[1] for word in text)))
    else:
        out = ''

    print(out)

    response = jsonify({
		"probability": 0.9,
		"request_id": 4,
		"result": out,
		"status": 1
	})

    return response
