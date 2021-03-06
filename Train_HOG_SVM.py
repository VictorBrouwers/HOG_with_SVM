# Importing the necessary modules:

import os
import numpy as np
from skimage.feature import hog
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from PIL import Image # This will be used to read/modify images (can be done via OpenCV too)
from numpy import *

# define parameters of HOG feature extraction
orientations = 9
pixels_per_cell = (5, 5)
cells_per_block = (2, 2)


# define size of sliding window and training data. Choose similar dimensions to typical training data dimensions
nx, ny = 20, 20


# define path to images:
# this is the path of your positive input dataset
pos_im_path = r"C:\path\to\file\folder"
# define the same for negatives
neg_im_path = r"C:\path\to\file\folder"

# read the image files:
pos_im_listing = os.listdir(pos_im_path) # it will read all the files in the positive image path (so all the required images)
neg_im_listing = os.listdir(neg_im_path)
num_pos_samples = size(pos_im_listing) # simply states the total no. of images
num_neg_samples = size(neg_im_listing)
print(num_pos_samples) # prints the number value of the no.of samples in positive dataset
print(num_neg_samples)
data= []
labels = []

# compute HOG features and label them:
for file in pos_im_listing: #this loop enables reading the files in the pos_im_listing variable one by one
    img = Image.open(pos_im_path + '\\' + file) # open the file
    img = img.resize((nx,ny)) # resize every image to the same size. Ensures same amount of HOG features extracted.
    gray = img.convert('L') # convert the image into single channel i.e. RGB to grayscale
    # calculate HOG for positive features
    fd = hog(gray, orientations, pixels_per_cell, cells_per_block, block_norm='L2', feature_vector=True)# fd= feature descriptor
    data.append(fd)
    labels.append(1)
    
# Same for the negative images
for file in neg_im_listing:
    img= Image.open(neg_im_path + '\\' + file)
    img = img.resize((nx,ny))
    gray= img.convert('L')
    # now calculate the HOG for negative features
    fd = hog(gray, orientations, pixels_per_cell, cells_per_block, block_norm='L2', feature_vector=True) 
    data.append(fd)
    labels.append(0)
# encode the labels, converting them from strings to integers
le = LabelEncoder()
labels = le.fit_transform(labels)

#%%
# Partitioning the data into training and testing splits, using 80%
# of the data for training and the remaining 20% for testing. These percentages can be changed by test_size.
print(" Constructing training/testing split...")
(trainData, testData, trainLabels, testLabels) = train_test_split(
	np.array(data), labels, test_size=0.20, random_state=42)
#%% Train the linear SVM
print(" Training Linear SVM classifier...")
model = LinearSVC(C=1) # choose C according to your needs
print(trainData.shape)
model.fit(trainData, trainLabels)
#%% Evaluate the classifier
print(" Evaluating classifier on test data ...")


predictions = model.predict(testData)
print(classification_report(testLabels, predictions))


# Save the model:
#%% Save the Model
joblib.dump(model, 'name_model.npy')
