from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


import tensorflow as tf

# create a session for training
sess = tf.InteractiveSession()

# construct the model
x = tf.placeholder(tf.float32, shape=[None, 784])
y_1hot = tf.placeholder(tf.float32, shape=[None, 10])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

sess.run(tf.global_variables_initializer())
# Apply a linear model to image array
# Apply softmax regression
y = tf.nn.softmax(tf.matmul(x, W)+b)

# configuring training criteria
mse=tf.reduce_mean(tf.keras.losses.mse(y_1hot, y))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(mse)

# train
for i in range(60000):
    # randomly pick 100 data from mnist.train
    batch = mnist.train.next_batch(100)
    # run the training
    train_step.run(feed_dict={x: batch[0], y_1hot: batch[1]})
    # print the present accuracy for every 500 steps
    if i%500 == 0:
        print ('training step: ' + str(i))
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_1hot, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print(accuracy.eval(feed_dict={x: mnist.test.images, y_1hot: mnist.test.labels}))
# save the trained model
save = tf.train.Saver()
address = '/Users/wuericchenjie/Python3Projects/THE_Project/models/model1/handwritten2.ckpt'
save.save(sess, address)
sess.close()



