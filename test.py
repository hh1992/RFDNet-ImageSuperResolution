import os
import cv2
import sys
import glob
import time
import math
import argparse
import numpy as np
import tensorflow as tf 

from model import RFDNNet
from utils import *
from tensorflow.keras import Model, Input


def run(config, model):
    for name in os.listdir(config.test_path):
        fullname = os.path.join(config.test_path, name)
        lr = cv2.imread(fullname)
        out, out_bilinear = upscale_image(model, lr)
        cv2.imwrite(os.path.join(fullname.replace('.png', '_sr.png')), np.array(out))
        cv2.imwrite(os.path.join(fullname.replace('.png', '_bilinear.png')), np.array(out_bilinear))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

	# Input Parameters
    parser.add_argument('--test_path', type=str, default="test/")
    parser.add_argument('--gpu', type=str, default='1')
    parser.add_argument('--weight_test_path', type=str, default= "weights/best.h5")
    parser.add_argument('--RSAfilter', type=int, default=64)
    parser.add_argument('--filter', type=int, default=64)
    parser.add_argument('--feat', type=int, default=64)
    parser.add_argument('--scale', type=int, default=3)

    config = parser.parse_args()
    os.environ['CUDA_VISIBLE_DEVICES'] = config.gpu

    rfanet_x = RFDNNet()
    x = Input(shape=(None, None, 3))
    out = rfanet_x.main_model(x, 3)
    rfa = Model(inputs=x, outputs=out)
    rfa.summary()
    rfa.load_weights(config.weight_test_path)

    run(config, rfa)
