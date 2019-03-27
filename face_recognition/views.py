from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse, HttpResponse
import base64, os, cv2
from keras.models import model_from_json
from keras.preprocessing import image
from keras import optimizers
from keras import backend as k
import numpy as np

def index(request):
	return render(request, 'face_recognition/index.html', {})

def results(request):

	# Read JS base64 and save to jpg file.
	base64_image = request.POST['img-src']
	content = base64_image.split('base64,')[-1]
	imgdata = base64.b64decode(content)
	filename = 'face_recognition/static/this_guy.jpg'
	with open(filename, 'wb') as f:
		f.write(imgdata)

	# Read just saved jpg file, detect face and save the circled jpg.
	this_guy = cv2.imread('face_recognition/static/this_guy.jpg')
	face_cascade = cv2.CascadeClassifier('face_recognition/static/haarcascade_frontalface_default.xml')
	gray = cv2.cvtColor(this_guy, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	# face maybe not recognised.
	circled = None
	for (x,y,w,h) in faces:
		circled = cv2.rectangle(this_guy, (x, y), (x+w, y+h), (255, 0, 0), 2)
	if circled is None:
		return render(request, 'face_recognition/face_not_recognized.html', {})
	else:
		cv2.imwrite('face_recognition/static/circled.jpg', circled)

	# Save cropped face to jpg
	cv2.imwrite('face_recognition/static/cropped.jpg', this_guy[y+2: y+h-2, x+2: x+w-2])

	cropped_photo_path = 'face_recognition/static/cropped.jpg'
	result = load_model(cropped_photo_path)

	return render(request, 'face_recognition/results.html', result)

def load_model(photo_path):
	# release memory
	k.clear_session()
	
	json_file_path = 'face_recognition/static/face_recognition_model.json'
	weights_path = 'face_recognition/static/face_recognition.h5'
	width, height = 150, 150

	# Model reconstruction from JSON file
	with open(json_file_path, 'r') as f:
	    model = model_from_json(f.read())

	# Load weights into the new model
	model.load_weights(weights_path)
	model.compile(
		loss='binary_crossentropy',
		optimizer=optimizers.Adam(amsgrad=True),
		metrics=['acc'])

	img = image.load_img(photo_path, target_size=(width, height))
	x = image.img_to_array(img)
	x = np.expand_dims(x, axis=0)
	x /= 255.

	classes = model.predict_classes(x)
	people = model.predict(x).reshape(-1)
	# :-(
	names = ['Julie', 'Melanie', 'Xingda']
	pct = []
	for person in people:
		pct.append("{0:.3f}".format(float(person) * 100)+"%")

	if classes[0] == 0:#meiyu
		person =  "julie"
	elif classes[0] == 1:
		person =  "melanie"
	elif classes[0] == 2:
		person = "xingda"

	return {
		"person": person,
		"names": names,
		"pcts": pct,
	}