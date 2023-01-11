import os
from torchvision import transforms
from PIL import Image
import numpy as np
from imgaug import augmenters as iaa
import random
import torch

class Dataset:
    def __init__(self, image_dir, gt_dir):
        included_extensions = ['tif','tiff']
        self.image_dir = image_dir #directory with training images
        self.samples = sorted([fn for fn in os.listdir(image_dir)
              if any(fn.endswith(ext) for ext in included_extensions)])
        self.gt_dir = gt_dir
        self.numsamples = len(self.samples)
        if gt_dir != None:
            self.gt_samples = sorted([fn for fn in os.listdir(gt_dir)
                if any(fn.endswith(ext) for ext in included_extensions)])
        self.inp_transforms = transforms.Compose(
            [
                transforms.Grayscale()
            ]
        )

    def __len__(self):
        return len(self.samples)

    def __getitem__(self,idx):
        image_path = os.path.join(self.image_dir, self.samples[idx])
        gt_path = os.path.join(self.gt_dir, self.gt_samples[idx])
        image = Image.open(image_path)
        image = np.array(image)
        image = image.astype(int)
        if self.gt_dir != None:
            gt = Image.open(gt_path)
            gt = np.array(gt)
            gt = np.expand_dims(gt, axis=0)
        else:
            gt = None       
        return image, gt

    def transformation(self):
        transformation = iaa.Sequential(
            [
                iaa.CropToFixedSize(512, 512),
                iaa.Fliplr(0.5),
                iaa.Sometimes(0.5, iaa.Affine(rotate=(-90, 90))),
                iaa.Sometimes(0.5,iaa.GaussianBlur(sigma=(0.0, 3.0)))
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