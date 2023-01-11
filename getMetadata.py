from PIL.TiffTags import TAGS

def getMetadata(img):
    #AC: this only works for tiffs. Add other image capabilities?
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag_v2}
    xresPPM = meta_dict['XResolution']
    xresPPM = xresPPM[0]
    xresPPM = xresPPM[0] / xresPPM[1]
    return(xresPPM)