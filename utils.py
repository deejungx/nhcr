import cv2
import numpy as np

# Use for testing -
# path = 'samples/da.jpg'


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
    # Binarization
    ret,thresh = cv2.threshold(img,100,255,cv2.THRESH_BINARY_INV)

    # Morphological transformations -
    # Dilation
    kernel = np.ones((40,40), np.uint8)
    dilation = cv2.dilate(thresh,kernel,iterations = 1)
    # Opening
    k = np.ones((45,45), np.uint8)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, k)

    # Resize to (32,32) 
    resized = cv2.resize(thresh, (32,32), interpolation=cv2.INTER_NEAREST)

    return resized


def decode_predictions(predictions):
    """
    Decodes the predictions of DHCD model.

    Param preds: Numpy array encoding a batch of predictions.
    Param top: Integer, how many top-guesses to return.

    Return: A list of top class prediction tuples
            `(class_name, class_description, score)`.
    """
    pass