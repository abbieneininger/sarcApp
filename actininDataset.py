import os
from PIL import Image

class ActininDataset():
    def __init__(self, folders):
        self.img_dir = None
        self.binary_dir = None
        self.data_dir = None
        if bool(folders.get('-IMG-')):
            self.img_dir = folders['-IMG-']
            self.img_samples = sorted(os.listdir(self.img_dir))

        if bool(folders.get('-BIN-')):
            self.binary_dir = folders['-BIN-']
            self.binary_samples = sorted(os.listdir(self.binary_dir))

        if bool(folders.get('-DATA-')):
            self.data_dir = folders['-DATA-']
            self.data_samples = sorted(os.listdir(self.data_dir))

    # get the total number of samples
    def __len__(self):
        if self.img_dir is not None:
            return len(self.img_samples)
        if self.binary_dir is not None:
            return len(self.binary_samples)
        if self.data_dir is not None:
            return len(self.data_samples)

    # fetch the training sample given its index
    def __getitem__(self, idx):
        image = None
        binary = None
        data_path = None
        
        if self.img_dir is not None:
            img_path = os.path.join(self.img_dir, self.img_samples[idx])
            image = Image.open(img_path)
            #image.mode = 'I'
        if self.binary_dir is not None:
            binary_path = os.path.join(self.binary_dir, self.binary_samples[idx])
            binary = Image.open(binary_path)
        if self.data_dir is not None: 
            name = self.data_samples[idx]
            if name[0] == ".":
                name = name[2:]
            data_path = os.path.join(self.data_dir, name)
        
        return image, binary, data_path