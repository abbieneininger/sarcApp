import torch.utils.tensorboard as tensorboard
from torch.utils.tensorboard import SummaryWriter
import torch
from youNet_Dataset import Dataset
from trainAndVal2factor import train, validate, DiceCoefficient
from unet2factor import UNet
import torch.nn as nn

def implement2factor(folders,fmaps,epochs):
    TRAIN_IMG_PATH = folders['-TIMG-']
    TRAIN_GT_PATH = folders['-TGT-']
    VAL_IMG_PATH = folders['-VIMG-']
    VAL_GT_PATH = folders['-VGT-']
    OUTPUT_PATH = folders['-OUT-']
    loader = Dataset(TRAIN_IMG_PATH,TRAIN_GT_PATH)
    validation_loader = Dataset(VAL_IMG_PATH, VAL_GT_PATH)

    #define unet
    out_channels = 1
    activation = nn.Sigmoid()
    loss_fn = torch.nn.BCEWithLogitsLoss()
    dtype = torch.FloatTensor
    d_factors = [(2,2),(2,2),(2,2),(2,2)]

    net = torch.nn.Sequential(
        UNet(in_channels=1,
        num_fmaps=fmaps,
        fmap_inc_factors=3,
        downsample_factors=d_factors,
        activation='ReLU',
        padding='same',
        num_fmaps_out=fmaps,
        constant_upsample=True
        ),
        torch.nn.Conv2d(in_channels= fmaps, out_channels=out_channels, kernel_size=1, padding=0, bias=True))

    device = torch.device("cpu")
    net = net.to(device)
    num_epochs = int(epochs)
    step = 0
    #AC: add current date
    tb_logger = SummaryWriter('logs/testRun100421')
    optimizer = torch.optim.Adam(net.parameters())
    while step < num_epochs:
        train(net, loader, optimizer, loss_fn, step, tb_logger, activation)
        step += 1
        validate(net, validation_loader, loss_fn, DiceCoefficient(), tb_logger, step, activation, num_epochs, OUTPUT_PATH)