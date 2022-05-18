import torch
from unet2factor import UNet
import torch.nn as nn
from PIL import Image
from matplotlib import cm
import numpy as np
import os
from imgaug import augmenters as iaa


#DATA_PATH = "E:/Blebbistatin MYH6-7 Project/24H_BB_DAPI_myomesin_actin_titin/MaxIPs/myomesin/BB100/images"
DATA_PATH = "F:/042722_siMYH6_myom_titin_IIA/MaxIPs/titin/all images"
checkpoint = "C:/Users/abbie/Documents/sarcApp GitHub Files/sarcApp/checkPoint_240"
OUTPUT_PATH = "F:/042722_siMYH6_myom_titin_IIA/MaxIPs/titin/all binaries"
#OUTPUT_PATH = "E:/Blebbistatin MYH6-7 Project/24H_BB_DAPI_myomesin_actin_titin/MaxIPs/myomesin/BB100/binaries"

# define unet
out_channels = 1
activation = nn.Sigmoid()
loss_fn = torch.nn.BCEWithLogitsLoss()
dtype = torch.FloatTensor
d_factors = [(2, 2), (2, 2), (2, 2), (2, 2)]

model = torch.nn.Sequential(
    UNet(
        in_channels=1,
        num_fmaps=32,
        fmap_inc_factors=3,
        downsample_factors=d_factors,
        activation="ReLU",
        padding="same",
        num_fmaps_out=32,
        constant_upsample=True,
    ),
    torch.nn.Conv2d(
        in_channels=32, out_channels=out_channels, kernel_size=1, padding=0, bias=True
    ),
)

def save_pred(pred, name, path):
    pred = torch.squeeze(pred, 0)
    pred = torch.squeeze(pred, 0)
    im = Image.fromarray(np.uint8(cm.gray(pred.cpu().numpy())*255))
    newpath = os.path.join(path, name)
    im.save(newpath+".tiff", "TIFF")

model.load_state_dict(torch.load(checkpoint))
device = torch.device("cpu")
model.to(device)
model.eval()
included_extensions = ['tif','tiff']
image_dir = DATA_PATH #directory with training images
samples = sorted([fn for fn in os.listdir(image_dir)
    if any(fn.endswith(ext) for ext in included_extensions)])
numsamples = len(samples)

with torch.no_grad():
    for idx in range(numsamples):
        image_path = os.path.join(image_dir, samples[idx])
        image = Image.open(image_path)
        image = np.array(image)
        image = image.astype(int)
        transformation = iaa.CropToFixedSize(848,1152)
        #transformation = iaa.CropToFixedSize(704,480)
        #transformation = iaa.CropToFixedSize(1408,976)
        x = transformation(image=image)
        x = torch.tensor(x)
        x = torch.unsqueeze(x, 0)
        x = torch.unsqueeze(x, 0)
        x = x.to(device)
        prediction = model(x.float())
        prediction = activation(prediction)
        save_pred(prediction, f"{samples[idx]}", OUTPUT_PATH)