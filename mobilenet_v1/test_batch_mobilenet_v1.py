from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import numpy as np
import tensorflow as tf
import os


def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=224,
                                input_width=224,
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
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


if __name__ == "__main__":
  model_file = \
    "/mnt/project/MobileNet/MobileNet_V1/output_graph_oct_16.pb"
  label_file = "/mnt/project/MobileNet/MobileNet_V1/output_labels_oct_16.txt"
  input_height = 224
  input_width = 224
  input_mean = 0
  input_std = 255
  input_layer = "Placeholder"
  output_layer = "final_result"
  input_name = "import/" + input_layer
  output_name = "import/" + output_layer

  test_image_path = '/mnt/project/NPDI/test_images'
  test_result_file = '/mnt/project/NPDI/test_images_result/test_results_mobilnet_v1/results.txt'

  tot_imgs = 0
  tot_porn_imgs = 0
  tot_non_porn_imgs = 0
  correct_porn_guess = 0
  correct_non_porn_guess = 0

  test_folders = os.listdir(test_image_path)
  with open(test_result_file,'w') as fd:
    fd.write("-"*10+"Mobilenet V1"+"-"*10)
    fd.write("\n")
    with tf.Session(graph=graph) as sess:
      try:
        for correct_label in test_folders: 

          pen = "-"*10 + " Label: " + correct_label + "-"*10
          print (pen)
          fd.write(pen + "\n")

          pen = "Image \t Predicted Label \t Correct Label"
          print(pen)
          fd.write(pen + "\n")

          folder_path = test_image_path + '/' + correct_label

          for image in os.listdir(folder_path):
            tot_imgs += 1
            try:
              file_name = folder_path + '/' + image
              graph = load_graph(model_file)
              t = read_tensor_from_image_file(file_name)

              input_operation = graph.get_operation_by_name(input_name)
              output_operation = graph.get_operation_by_name(output_name)

              
              results = sess.run(output_operation.outputs[0], {
                  input_operation.outputs[0]: t
              })
              results = np.squeeze(results)

              top_k = results.argsort()[-5:][::-1]
              labels = load_labels(label_file)
              
              predicted_label = ''
              if labels[0].startswith("non"):
                labels[0] = "non_porn"


              if results[0] > 0.7:
                predicted_label = labels[0]

              if predicted_label == correct_label:
                if predicted_label == "non_porn":
                  correct_non_porn_guess += 1
                elif predicted_label == "porn":
                  correct_porn_guess += 1
                else:
                  predicted_label = "Not enough confident"

            pen = file_name + "\t" +  predicted_label + "\t" + correct_label
            print (pen)
            fd.write(pen + "\n")

          except:
            pass
        pen = "-"*10 + " Final Results " + "-"*10
        print(pen)
        fd.write(pen + "\n")

        pen = "Total " + correct_label + " : " + str(len(folder_path))
        fd.write(pen + "\n")
        print (pen)

      except:
        pass

  