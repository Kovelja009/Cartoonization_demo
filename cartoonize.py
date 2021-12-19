import os
import cv2
import numpy as np
import tensorflow as tf
import network
import guided_filter
from tqdm import tqdm


class Cartoonize:
    def __init__(self, model_path='saved_models', save_folder='cartoonized_images'):
        self.save_folder = save_folder
        self.model_path = model_path
        self.save_folder = save_folder
        self.input_photo = tf.compat.v1.placeholder(tf.float32, [1, None, None, 3])
        self.network_out = network.unet_generator(self.input_photo)
        self.final_out = guided_filter.guided_filter(self.input_photo, self.network_out, r=1, eps=5e-3)
        self.all_vars = tf.compat.v1.trainable_variables()
        self.gene_vars = [var for var in self.all_vars if 'generator' in var.name]
        self.saver = tf.compat.v1.train.Saver(var_list=self.gene_vars)

        self.config = tf.compat.v1.ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.sess = tf.compat.v1.Session(config=self.config)

        self.sess.run(tf.global_variables_initializer())
        self.saver.restore(self.sess, tf.train.latest_checkpoint(model_path))

    def resize_crop(self, image):
        h, w, c = np.shape(image)
        if min(h, w) > 1080:
            if h > w:
                h, w = int(1080 * h / w), 1080
            else:
                h, w = 1080, int(1080 * w / h)
        image = cv2.resize(image, (w, h),
                           interpolation=cv2.INTER_AREA)
        h, w = (h // 8) * 8, (w // 8) * 8
        image = image[:h, :w, :]
        return image

    def cartoonize(self, load_path, name):
        # input_photo = tf.compat.v1.placeholder(tf.float32, [1, None, None, 3])
        # network_out = network.unet_generator(input_photo)
        # final_out = guided_filter.guided_filter(input_photo, network_out, r=1, eps=5e-3)

        # all_vars = tf.compat.v1.trainable_variables()
        # gene_vars = [var for var in all_vars if 'generator' in var.name]
        # saver = tf.compat.v1.train.Saver(var_list=gene_vars)
        #
        # config = tf.compat.v1.ConfigProto()
        # config.gpu_options.allow_growth = True
        # sess = tf.compat.v1.Session(config=config)
        #
        # sess.run(tf.global_variables_initializer())
        # saver.restore(sess, tf.train.latest_checkpoint(model_path))
        # name_list = os.listdir(load_folder)
        # for name in tqdm(name_list):
        try:
            # load_path = os.path.join(load_folder, name)
            save_path = os.path.join(self.save_folder, name)
            image = cv2.imread(load_path)
            image = self.resize_crop(image)
            batch_image = image.astype(np.float32) / 127.5 - 1
            batch_image = np.expand_dims(batch_image, axis=0)
            output = self.sess.run(self.final_out, feed_dict={self.input_photo: batch_image})
            output = (np.squeeze(output) + 1) * 127.5
            output = np.clip(output, 0, 255).astype(np.uint8)
            cv2.imwrite(save_path, output)
        except:
            print('cartoonize {} failed'.format(load_path))

# if __name__ == '__main__':
#     model_path = 'saved_models'
#     load_folder = 'test_images'
#     save_folder = 'cartoonized_images'
#     if not os.path.exists(save_folder):
#         os.mkdir(save_folder)
#     cartoonize(load_folder, save_folder, model_path)
