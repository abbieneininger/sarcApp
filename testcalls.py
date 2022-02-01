from makeBinary import main as makeBinary
import os
from PIL.TiffTags import TAGS
from PIL import Image

def getMetadata(img):
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag_v2}
    xresPPM = meta_dict['XResolution']
    xresPPM = xresPPM[0]
    xresPPM = xresPPM[0] / xresPPM[1]
    return(xresPPM)

def main():
    img_dir = "C:/Users/abbie/Documents/sarcApp/python/toy data/405"
    img_samples =sorted(os.listdir(img_dir))
    img_path = os.path.join(img_dir, img_samples[1])
    image = Image.open(img_path)
    image.show()
    xres = getMetadata(image)
    numData, headerKeys, bin = makeBinary(image, xres)
    print(numData)

if __name__ == '__main__':
    main()