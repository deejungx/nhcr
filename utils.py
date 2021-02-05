import cv2
import numpy as np
import json
from skimage.transform import resize

from class_generator import upload_class_index

CLASS_INDEX = None
CLASS_INDEX_PATH = 'dataset/dhcd_class_index.json'

def img_to_array(uploaded_img):
    """
    Convert uploaded image to a format that the model can interpret.

    Param uploaded_img: img file in jpg/png format
    Return: 32x32 pixel binarized image 
    """
    img = cv2.imread(uploaded_img, 0)
    out = preprocess(img)
    return out


def preprocess(img):
    """
    Pre-process the uploaded image by applying binarization, filtering noise, 
    thickening stroke and resizing the image size.

    Param img: nparray image
    Return: 32x32 pixel binarized image 
    """
    # Otsu's Binarization
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # Morphological transformations -
    # Dilation
    kernel = np.ones((40,40), np.uint8)
    dilation = cv2.dilate(thresh,kernel,iterations = 1)
    # Opening
    k = np.ones((42,42), np.uint8)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, k)
    # Resize cv2 implementation 
    # resized = cv2.resize(thresh, (32,32), interpolation=cv2.INTER_NEAREST)
    # Resize skimage implementation
    resized = resize(opening, (32,32), anti_aliasing=True, order=3, preserve_range=True)
    return resized


def decode_predictions(predictions, top=1):
    """
    Decodes the predictions of DHCD model.

    Param preds: Numpy array encoding a batch of predictions.
    Param top: Integer, how many top-guesses to return.

    Return: A list of top class prediction tuples
            `(class_name, class_description, score)`.
    """
    global CLASS_INDEX

    if CLASS_INDEX is None:
        # If dataset/dhcd_class_index.json file does not exist,
        # uncomment the following line to generate the file:
        # upload_class_index()
        with open(CLASS_INDEX_PATH) as jfile:
            CLASS_INDEX = json.load(jfile)
    
    results = []
    for pred in predictions:
        top_indices = np.argsort(pred)[-top:]
        result = [tuple(CLASS_INDEX[str(i)]) + (float(pred[i]),) for i in top_indices]
        result.sort(key=lambda x: x[2], reverse=True)
        results.append(result)
    return results


# Testing
# def test(file_name):
#     sample_img = f'samples/{file_name}'
#     out = img_to_array(sample_img)
#     cv2.imwrite('images/sample4.png', out)

# test('tin.jpg')