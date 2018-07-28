from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import numpy as np
import tensorflow as tf
from Model import Model


class Classifier(object):

    def __init__(self):
        self.graph = None
        self.output_operation = None
        self.input_operation = None
        self.label_file = None
        self.sess = None
        self.config()

    def classify(self, image):
        input_height = 299
        input_width = 299
        input_mean = 0
        input_std = 255
        t = self.read_tensor_from_image_file(
            image,
            input_height=input_height,
            input_width=input_width,
            input_mean=input_mean,
            input_std=input_std)
        
        results = self.sess.run(self.output_operation.outputs[0], {
            self.input_operation.outputs[0]: t
        })
        results = np.squeeze(results)

        top_k = results.argsort()[-5:][::-1]
        labels = self.load_labels(self.label_file)
        resp = []
        for i in top_k: 
            resp.append(Model(str(labels[i]), float(results[i])))
        return resp

    def load_graph(self, model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)

        return graph

    def read_tensor_from_image_file(self, file_name,
                                    input_height=299,
                                    input_width=299,
                                    input_mean=0,
                                    input_std=255):
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)
        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(
                file_reader, channels=3, name="png_reader")
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(
                tf.image.decode_gif(file_reader, name="gif_reader"))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
        else:
            image_reader = tf.image.decode_jpeg(
                file_reader, channels=3, name="jpeg_reader")
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(
            dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)

        return result

    def load_labels(self, label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    def config(self):
        file_name = "tensorflow/examples/label_image/data/grace_hopper.jpg"
        input_layer = "Placeholder"
        output_layer = "final_result"
        model_file = "classifier/logs/output_graph.pb"
        self.label_file = "classifier/logs/output_labels.txt"
        self.graph = self.load_graph(model_file)
        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        self.input_operation = self.graph.get_operation_by_name(input_name)
        self.output_operation = self.graph.get_operation_by_name(output_name)
        self.sess = tf.Session(graph=self.graph)