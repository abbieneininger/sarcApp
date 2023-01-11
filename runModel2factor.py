from turtle import width
import torch
from unet2factor import UNet
import torch.nn as nn
from PIL import Image
from matplotlib import cm
import numpy as np
import os
from imgaug import augmenters as iaa
from natsort import natsorted

def runModel2factor(folders, fmaps):
    DATA_PATH = folders.get('-IMG-')
    OUTPUT_PATH = folders.get('-OUT-')
    checkpoint = folders.get('-MODEL-')

    # define unet
    out_channels = 1
    activation = nn.Sigmoid()
    loss_fn = torch.nn.BCEWithLogitsLoss()
    dtype = torch.FloatTensor
    d_factors = [(2, 2), (2, 2), (2, 2), (2, 2)]

    model = torch.nn.Sequential(
        UNet(
            in_channels=1,
            num_fmaps=fmaps,
            fmap_inc_factors=3,
            downsample_factors=d_factors,
            activation="ReLU",
            padding="same",
            num_fmaps_out=fmaps,
            constant_upsample=True,
        ),
        torch.nn.Conv2d(
            in_channels=fmaps, out_channels=out_channels, kernel_size=1, padding=0, bias=True
        ),
    )

    model.load_state_dict(torch.load(checkpoint))
    device = torch.device("cpu")
    model.to(device)
    model.eval()
    included_extensions = ['tif','tiff']
    image_dir = DATA_PATH #directory with training images
    samples = natsorted([fn for fn in os.listdir(image_dir)
        if any(fn.endswith(ext) for ext in included_extensions)])

    numsamples = len(samples)

    with torch.no_grad():
        for idx in range(numsamples):
            print(idx)
            image_path = os.path.join(image_dir, samples[idx])
            image = Image.open(image_path)
            image = np.array(image)
            image = image.astype(int)
            image_size = image.shape
            image_width =image_size[1]
            image_height = image_size[0]
            transformation = iaa.CenterCropToMultiplesOf(height_multiple=16,width_multiple=16)
            x = transformation(image=image) 
            x = torch.tensor(x)
            x = torch.unsqueeze(x, 0)
            x = torch.unsqueeze(x, 0)
            x = x.to(device)
            prediction = model(x.float())
            prediction = activation(prediction)
            prediction = torch.squeeze(prediction, 0)
            prediction = torch.squeeze(prediction, 0)
            prediction = np.array(prediction)
            transformation2 = iaa.CenterPadToFixedSize(width=image_width, height=image_height)
            padded_prediction = transformation2(image = prediction)
            im1 = Image.fromarray(np.uint8(cm.gray(padded_prediction)*255))
            name = f"{samples[idx]}"
            path = OUTPUT_PATH
            newpath = os.path.join(path, name)
            im1.save(newpath+".tiff", "TIFF")