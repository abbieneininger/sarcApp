import os
from torchvision import transforms
from PIL import Image
import numpy as np
from imgaug import augmenters as iaa
import random
import torch

class TrainDataset:
    def __init__(self, img_dir, gt_dir):
        self.img_dir = img_dir #directory with training images
        self.samples = sorted(os.listdir(img_dir))
        self.gt_dir = gt_dir
        self.numsamples = len(self.samples)
        self.gtsamples = sorted(os.listdir(gt_dir))
        self.inp_transforms = transforms.Compose(
            [
                transforms.Grayscale(),
                transforms.ToTensor()
            ]
        )

    def __len__(self):
        return len(self.samples)

    def __getitem__(self,idx):
        img_path = os.path.join(self.img_dir, self.samples[idx])
        gt_path = os.path.join(self.gt_dir, self.gtsamples[idx])
        image = Image.open(img_path)
        image = self.inp_transforms(image)
        image = np.array(image)
        gt = Image.open(gt_path)
        gt = np.array(gt)
        gt = np.expand_dims(gt, axis=0)
        return image, gt

    def transformation(self):
        transformation = iaa.Sequential(
            [
                iaa.CropToFixedSize(256, 256),
                iaa.Fliplr(0.5),
                iaa.Sometimes(
                    0.7, iaa.ElasticTransformation(alpha=(10,40), sigma=(6,10))
                ),
                iaa.Sometimes(0.5, iaa.Affine(rotate=(-90, 90))),
            ]
        )
        return transformation

    def getBatch(self, batchSize):
        batch_images = []
        batch_gt = []
        for i in range(batchSize):
            temp_image, temp_gt = self[random.randrange(0, self.numsamples)]
            temp_gt = np.expand_dims(temp_gt, axis=3)
            transformation = self.transformation()
            temp_image, temp_gt = transformation(
                images=temp_image, segmentation_maps=temp_gt
            )
            temp_gt = temp_gt[:, :, :, 0]
            
            temp_image, temp_gt = torch.tensor(temp_image), torch.tensor(temp_gt)
            batch_images.append(temp_image)
            batch_gt.append(temp_gt)
        batch_images = torch.stack(batch_images, dim=0)
        batch_gt = torch.stack(batch_gt, dim=0)
        return batch_images, batch_gt