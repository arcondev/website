Title: Register Pascal VOC dataset for detection and segmentation in Detectron2
Date: 2020-09-30
Category: Blog
Tag: detectron2, pascalvoc, dataset
Author: Saurav Tuladhar
Slug: register-voc-detectron2
Summary: Detectron2's builtin Pascal VOC provides only bounding-box labels. We need to define custom function to load VOCs segmentation label to dataset dict.

Detectron2 recognizes Pascal VOC{2007/2012} as built-in datasets. But the built-in dataset catalog for Pascal VOC provides only the bounding-box labels. This limits the use of Pascal VOC dataset to detection tasks. However, the Pascal VOC 2012 dataset does come with class and object segmentation label as well. In this post we discuss how to register VOC 2012 dataset with the segmentation labels added to the data dict. This will allow us to use the VOC dataset with Mask R-CNN models.

## Load segmentation label to data dict
We define `get_pascal_dict` function to read the segmentation mask and bounding box labels. The segmentation mask is converted to run-length-encoding (RLE) format and add to the dataset dict record. 

```python
def get_pascal_dicts(img_dir, d='train'):
    '''
    Returns VOC dataset_dicts given path to "VOC2012" folder
    '''
   
    dataset_dicts = []
    
    filename_train = img_dir / 'ImageSets/Segmentation/{}.txt'.format(d)
    with open(filename_train) as f:
        imlist = [line.rstrip() for line in f]
    
    for imgidx, imname in enumerate(imlist):
        filename = img_dir / f'JPEGImages/{imname}.jpg'
        xmlfilename = img_dir / f'Annotations/{imname}.xml'
        # Get instance segmentation mask
        segmaskfilename = img_dir / f'SegmentationObject/{imname}.png'
        segmask = np.array(Image.open(segmaskfilename))
        
        record = dict()
        record["file_name"] = filename.as_posix()
        height, width = segmask.shape
        record["height"] = height
        record["width"] = width
        record["image_id"] = imgidx

        # Annotation info
        objs = []  # list to hold annotated objects in the image
        annodata = minidom.parse(xmlfilename.as_posix())
        cat_obj = annodata.getElementsByTagName('object')
        bboxes = annodata.getElementsByTagName('bndbox')
        for idx, o in enumerate(cat_obj):  # loop thru each labeled object 
            obj_name = o.getElementsByTagName('name')[0].firstChild.data
            bbox = o.getElementsByTagName('bndbox')[0]
            xmin = int(bbox.getElementsByTagName('xmin')[0].firstChild.data)
            xmax = int(bbox.getElementsByTagName('xmax')[0].firstChild.data)
            ymin = int(bbox.getElementsByTagName('ymin')[0].firstChild.data)
            ymax = int(bbox.getElementsByTagName('ymax')[0].firstChild.data)
            # Convert segmentation mask map to RLE format
            seg_dict = mask.encode(np.asarray(segmask==(idx+1), order="F"))

            obj = {
                "bbox": [xmin, ymin, xmax, ymax],
                "bbox_mode": BoxMode.XYXY_ABS,
                "segmentation": seg_dict,
                "category_id": name2cat[obj_name],
            }
            objs.append(obj)
        record["annotations"] = objs
        dataset_dicts.append(record)
    return dataset_dicts
```

The `get_pascal_dict()` function can be used to register the VOC dataset as follows
```python
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

for d in ["train", "val"]:
    DatasetCatalog.register("pascal_" + d, lambda d=d: get_pascal_dicts(PATH, d))
    MetadataCatalog.get("pascal_" + d).set(thing_classes=classes)
```

## Sample images
|a|a|a|
|:-|:-|:-|
|![Sample1]({static}/images/0.jpeg)|![Sample1]({static}/images/1.jpeg)|![Sample1]({static}/images/2.jpeg)|