from torch.utils.tensorboard import SummaryWriter
import torch
import torch.utils.tensorboard as tensorboard
from trainDataset2factor import TrainDataset
from trainAndVal2factor import train, validate, DiceCoefficient
from unet2factor import UNet
import torch.nn as nn

def implement2factor(TRAIN_IMG_PATH, TRAIN_GT_PATH, VAL_IMG_PATH, VAL_GT_PATH):
    loader = TrainDataset(TRAIN_IMG_PATH,TRAIN_GT_PATH)
    validation_loader = TrainDataset(VAL_IMG_PATH, VAL_GT_PATH)

    #define unet
    out_channels = 1
    activation = nn.Sigmoid()
    loss_fn = torch.nn.BCEWithLogitsLoss()
    dtype = torch.FloatTensor
    d_factors = [(2,2),(2,2),(2,2),(2,2)]

    net = torch.nn.Sequential(
        UNet(in_channels=1,
        num_fmaps=16,
        fmap_inc_factors=3,
        downsample_factors=d_factors,
        activation='ReLU',
        padding='same',
        num_fmaps_out=16,
        constant_upsample=True
        ),
        torch.nn.Conv2d(in_channels= 16, out_channels=out_channels, kernel_size=1, padding=0, bias=True))

    device = torch.device("cpu")
    net = net.to(device)
    num_epochs = 2
    step = 0
    tb_logger = SummaryWriter('logs/testRun100421')
    optimizer = torch.optim.Adam(net.parameters())
    while step < num_epochs:
        train(net, loader, optimizer, loss_fn, step, tb_logger, activation)
        step += 1
        validate(net, validation_loader, loss_fn, DiceCoefficient(), tb_logger, step, activation)

def main():
    TRAIN_IMG_PATH = "D:/MyomesinTrainingData/train"
    TRAIN_GT_PATH = "D:/MyomesinTrainingData/gt"
    VAL_IMG_PATH = "D:/MyomesinTrainingData/valtrain"
    VAL_GT_PATH = "D:/MyomesinTrainingData/valgt"
    implement2factor(TRAIN_IMG_PATH, TRAIN_GT_PATH, VAL_IMG_PATH, VAL_GT_PATH)

if __name__ == '__main__':
    main()   