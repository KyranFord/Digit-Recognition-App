from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from datetime import datetime
from PIL import Image, ImageOps
import io
import base64
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from tensorflow.keras import backend as K
from django.views.decorators.cache import never_cache

model = load_model('lenet.h5')
predicted_class = NULL
import matplotlib.pyplot as plt

def classify(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        
        # Remove the "data:image/png;base64," prefix
        image_data = image_data.replace("data:image/png;base64,", "")
        
        # Convert the base64 image data to bytes
        image_bytes = base64.b64decode(image_data)
        
        # Open the image using PIL
        img = Image.open(io.BytesIO(image_bytes)).convert("L")  # Convert image to grayscale
        
        img = img.resize((28,28))

        # Invert color (Optional: only if your model was trained with inverted colors)
        img = ImageOps.invert(img)

        img = np.array(img)
        img = img.reshape(1, 28, 28, 1)  # Reshape the image to match model's expected input shape
        img = img.astype('float32')
        img = img / 255.0  # Normalize the image

        # Save the image data to a file for inspection
        plt.imshow(img[0, :, :, 0], cmap='gray')
        plt.savefig(f'debug_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')

        res = model.predict(img)
       
        # Clear the session to make sure model predicts on the next request
        K.clear_session()

        # Make predictions
        predicted_class = np.argmax(res)
        print(f"Predicted class: {predicted_class}")

        # Convert predicted_class to string
        predicted_class_str = str(predicted_class)
        
        # Return the predicted class as a JSON response
        return JsonResponse({'predicted_class': predicted_class_str})

def home(request):
    """Renders the home page."""
    return render(
        request,
        'app/index.html',
    )
