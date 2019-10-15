from flask import Flask, request
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from PIL import Image
import numpy as np
import CQLSimulator as cqlsm
from cassandra.cluster import Cluster
import time


# import mnist dataset to relative address "MNIST_data"

mnist= input_data.read_data_sets("MNIST_data", one_hot=True)
# initialize a new flask framework
app=Flask(__name__)

# construct a cluster connecting with localhost and create a keyspace
KEYSPACE = "results"
cluster = Cluster(contact_points=['0.0.0.0'], port=9042)
session = cluster.connect()
cqlsm.createKeySpace(session, KEYSPACE)

@app.route ('/upload', methods= ['POST', 'GET'])
def upload ():
    if request.method == 'POST':
        # get the coming from client in request object, save the image
        img=request.files['image']
        saved_file_path = 'inputGraph.png'
        img.save (saved_file_path)
        # from process_image, convert image tom appropriate form
        normalized_pv = process_image(saved_file_path)
        # perdict the image
        result = perdict (normalized_pv)
        # log the data into cassandra
        file_name = img.filename
        current_time = str(time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(time.time())))
        cqlsm.insert_data(session, file_name, current_time, result)

        return result


# Use existing model to predict the number in an image

# pixel_values: the list of image pixel normalized by process_image method
# return: the numerical value of prediction result

# requires: len (pixel_values) == 784 and
# [pixel_value corresponds to a image containing a number]
def perdict (pixel_values):

    x = tf.placeholder(tf.float32, [None, 784])
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))

    y = tf.nn.softmax(tf.matmul(x, W) + b)

    init = tf.initialize_all_variables()
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(init)
        saver.restore(sess, "/Users/wuericchenjie/Python3Projects/THE_Project/models/model1/handwritten1.ckpt")  # The location of the model previously stored
        print ("Model restored.")

        prediction = tf.argmax(y, 1)
        predint = prediction.eval(feed_dict={x: [pixel_values]}, session=sess)


    return str(predint[0])




# convert 28x28 image into greyscale, then into 784 dimension list,
# each element ranged 0 to 1, higher is darker

# path: a string of path directing to an image
# return: a normalized list of pixel values
def process_image(path):
    img= Image.open(path)
    img=img.resize((28, 28))
    img=img.convert ('L') # transfer to greyscale
    # convert image to pixel values in a pillow matrix,
    # then convert to ordinary list
    pixel_values = list(img.getdata())


    # normalize pixel value to range 0~1. Original range 0~255
    normalized_pv = np.zeros(len(pixel_values))
    for index in range(len(pixel_values)):
        normalized_pv[index] = (255 - pixel_values[index]) * 1.0 / 255.0
    # print (normalized_pv) # test
    # img.show() # test
    return normalized_pv


if __name__=='__main__':
    app.run(port='8000', host= '0.0.0.0')