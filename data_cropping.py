import numpy as np
import os
from  natsort import natsorted
import imageio
import xml.etree.ElementTree as ET

def crop_image(image_np, value):
    im_height, im_width, _ = img.shape
    (ymin, xmin, ymax, xmax) = value[5:]
    crop_img = image_np[xmin:xmax, ymin:ymax]
    return crop_img

POSE = 'RP'
IMAGES_PATH = 'Data\\dataset_1\\Subset_{}\\{}\\train\\jpeg'.format(POSE,POSE)
XML_PATH = 'Data\\dataset_1\\Subset_{}\\{}\\train\\xml'.format(POSE,POSE)
OUT_PATH = 'Data\\dataset_1\\Cropped'

names = [ d for d in os.listdir(IMAGES_PATH) if d.endswith( '.jpg') ]
names = natsorted(names)
for image in names:
    img = imageio.imread(os.path.join(IMAGES_PATH, image))
    xml_file = os.path.join(XML_PATH, image.split('.')[0]+'.xml')
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member in root.findall('object'):
        value = (root.find('filename').text.split('.')[0],
                int(root.find('size')[0].text),
                int(root.find('size')[1].text),
                member[0].text,member[1].text,
                int(member[5][0].text),
                int(member[5][1].text),
                int(member[5][2].text),
                int(member[5][3].text))
        crop_img = crop_image(img, value)
#     plt.figure()
#     plt.imshow(crop_img)
    imageio.imwrite(os.path.join(OUT_PATH,'{}_{}.jpg'.format(value[0],value[4])), crop_img)