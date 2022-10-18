import cv2
import albumentations as A

def get_coords(path):
    f = open(path, 'r')
    x = f.readlines()
    tag_arr = []
    coords_arr = []
    for y in x:
        line = str(y).split()
        tag = int(line[0])
        xmin = float(line[1])
        ymin = float(line[2])
        xmax = float(line[3])
        if xmax > 1:
            xmax = 1
        ymax = float(line[4])
        if ymax > 1:
            ymax = 1
        tag_arr.append([tag])
        coords_arr.append([xmin, ymin, xmax, ymax])
    return tag_arr, coords_arr


transform = A.Compose(
    [
        #A.Resize(width=860,height=720),
        #A.RandomCrop(width=1280,height=720),
        A.Rotate(limit=20,p=0.8, border_mode=cv2.BORDER_CONSTANT),  # applied 90 percent of the cases
        #A.HorizontalFlip(p=0.5),
        #A.VerticalFlip(p=0.1),
        A.GaussNoise(p=0.5),
        A.OneOf([A.Blur(blur_limit=3,p=0.5),A.ColorJitter(p=0.5),],p=1.0),
        #A.OneOf([A.InvertImg(p=0.5),A.RGBShift(r_shift_limit=25,g_shift_limit=25,b_shift_limit=25,p=0.9),],p=1.0),
        A.RGBShift(r_shift_limit=25,g_shift_limit=25,b_shift_limit=25,p=0.9),
        A.Perspective(scale=(0.05, 0.1), keep_size=True, pad_mode=0, pad_val=0, mask_pad_val=0, fit_output=False, interpolation=1, always_apply=False, p=0.5),
        A.Affine(scale=0.7, translate_percent=0, translate_px=None, rotate=[-5,5], shear=2, interpolation=1, cval=0, cval_mask=0, mode=0, fit_output=False, always_apply=False, p=0.5),
    ], bbox_params=A.BboxParams(format="yolo",min_area=1024,min_visibility=0.3,label_fields=[])
)
transform2 = A.Compose(
    [
        #A.Resize(width=860,height=720),
        #A.RandomCrop(width=640,height=416),
        A.Rotate(limit=20,p=0.8, border_mode=cv2.BORDER_CONSTANT),  # applied 90 percent of the cases
        #A.HorizontalFlip(p=0.5),
        #A.VerticalFlip(p=0.1),
        A.GaussNoise(p=0.5),
        #A.OneOf([A.Blur(blur_limit=3,p=0.5),A.ColorJitter(p=0.5),],p=1.0),
        A.Blur(blur_limit=3,p=0.5),
        A.ColorJitter(p=0.5),
        #A.OneOf([A.InvertImg(p=0.5),A.RGBShift(r_shift_limit=25,g_shift_limit=25,b_shift_limit=25,p=0.9),],p=1.0),
        #A.RGBShift(r_shift_limit=25,g_shift_limit=25,b_shift_limit=25,p=0.9),
        A.Perspective(scale=(0.05, 0.1), keep_size=True, pad_mode=0, pad_val=0, mask_pad_val=0, fit_output=False, interpolation=1, always_apply=False, p=0.5),
        A.Affine(scale=0.7, translate_percent=0, translate_px=None, rotate=[-5,5], shear=2, interpolation=1, cval=0, cval_mask=0, mode=0, fit_output=False, always_apply=False, p=0.5),
    ], bbox_params=A.BboxParams(format="yolo",min_area=1024,min_visibility=0.3,label_fields=[])
)

import os
import numpy as np
import shutil

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
images_path = 'D:/New-office/p2'#'D:/Officemodel/Officev3_1.1/data/obj-office' #'D:/Augmented/imgs'     #'C:/Users/maind/Desktop/Newfolder/Augmentation/imgs' # OLD images path
txt_path = 'D:/New-office/p2-txt'#'D:/Officemodel/Officev3_1.1/data/obj-office-txt' #'D:/Augmented/txts'                            #'C:/Users/maind/Desktop/Newfolder/Augmentation/txts' # OLD txt path

dir = 'D:/New-office/Retag'#'D:/Augmented/augimgs/'                                 #"C:/Users/maind/Desktop/Newfolder/Augmentation/aug_imgs/" # NEW images path
dir2 = 'D:/New-office/Retag'#'D:/Augmented/augtxts/'                                #"C:/Users/maind/Desktop/Newfolder/Augmentation/aug_txts/" # NEW txt path

#master_list=[]
list_of_images = os.listdir(images_path)
list_of_txts = os.listdir(txt_path)
print('No of Txts : ',len(list_of_txts))
print('No of Images : ',len(list_of_images))
count=0 # total images processed
count8=0
count14=0
count22=0
passed=0 #no of images passed due to class restriction
obj_bad=0
def check_area_and_res(path_to_img,coords_arr,limit=0.005):
    img = cv2.imread(path_to_img)
    wid = img.shape[1]
    hgt = img.shape[0]
    img_area=wid*hgt
    res_good=False
    #print(wid,hgt)
    if (wid >= 416) and (hgt >= 416):
        res_good= True

    area_good = False
    areas = []
    for i in coords_arr:
        x1=i[0]*wid
        y1=i[1]*hgt
        x2=i[2]*wid
        y2=i[3]*hgt
        area=abs(x2-x1)*abs(y2-y1)
        areas.append(area)
    x=min(areas)/img_area
    #print(x)
    if x >= limit:
        area_good = True
    return res_good,area_good

for img,txt in zip(list_of_images,list_of_txts): # zip the image path with mask paths
    path_to_img = str(images_path)+'/'+str(img)
    name_img=img
    path_to_txt = str(txt_path)+'/'+str(txt)
    try:
            tag_arr,coords_arr= get_coords(path_to_txt)
            img = cv2.imread(path_to_img)
        #print(tag_arr[0][0])
        #8/9/14/22
        # Add class iF count
        #if (tag_arr[0][0]==2) and count<=1000: #or (tag_arr[0]==8) or (tag_arr[0]==14) or (tag_arr[0]==22) and:
        #res_good,area_good=check_area_and_res(path_to_img,coords_arr)
        #if area_good and res_good:

            bboxes = coords_arr
            image_list = [img]
            bboxes_list = [bboxes]
            # mask_list = [mask]
            image = np.array(img)
            # mask=np.array(mask)
            try:
                for i in range(3):
                    augmentations = transform(image=image, bboxes=bboxes)  # ,masks=[mask])
                    augmented_img = augmentations["image"]
                    # augmented_mask = augmentations("masks")
                    if len(augmentations["bboxes"]) == 0:
                        continue

                    path = '{}versAoff{}.jpg'.format(str(count), str(i))
                    # print(os.path.join(dir,path))
                    if not cv2.imwrite(os.path.join(dir, path), augmented_img):
                        raise Exception("Could not write image")

                    path2 = '{}versAoff{}.txt'.format(str(count), str(i))
                    file = open(os.path.join(dir2, path2), "w")

                    for y, z in zip(tag_arr, augmentations["bboxes"]):
                        augment_arr = list(z)
                        augment_arr.insert(0, y[0])
                    file.write(str(augment_arr[0]) + ' ' + str(augment_arr[1]) + ' ' + str(augment_arr[2]) + ' ' + str(
                        augment_arr[3]) + ' ' + str(augment_arr[4]) + '\n')

                    file.close()
                    count = count + 1
                    print("No of images augmented 2 : ", count)
            except:
                print("Normal Image Except")
                pass

            else:
                pass


    except:
        print("Bad file except except")
        obj_bad = obj_bad + 1
        #print("No of images  skipped/reformed due to area/resolution :", obj_bad)
        #shutil.copyfile(path_to_img, 'D:/Augmented/aug2' + '/' + str(name_img))
        # print(txt)
        #shutil.copyfile(path_to_txt, 'D:/Augmented/aug2' + '/' + str(txt))
        pass





list_of_new_images = os.listdir(dir)
list_of_new_txts = os.listdir(dir2)
print('No of new TXTS : ',len(list_of_new_txts))
print('No of new IMGS : ',len(list_of_new_images))
print('No of new Normal Augmentations : ',count)
#print('No of new Specific Class transforms : ',passed)
print('No of new Empty TXT : ',obj_bad)

