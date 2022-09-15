import tensorflow as tf
import numpy as np
import pickle

with open('./adasyn/x_ecfpada.p', 'rb') as ada_x:
    ada_x_ecfp6s = pickle.load(ada_x)

with open('./adasyn/y_ecfpada.p', 'rb') as ada_y:
    ada_y_ecfp6s = pickle.load(ada_y)

feature = {
    'X': tf.train.Feature(float_list=tf.train.FloatList(value=ada_x_ecfp6s.flatten())),
    'Y': tf.train.Feature(float_list=tf.train.FloatList(value=ada_y_ecfp6s.flatten()))
}
data = tf.train.Example(features=tf.train.Features(feature=feature))

seralised = data.SerializedToString()

writer = tf.python_io.TFRecordWriter('ADA_ecfp6.tfrecord')
writer.write(seralised)
writer.close()