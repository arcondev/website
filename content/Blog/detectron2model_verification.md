Title: Reproducing metrics of R-CNN models in Detectron2 Model Zoo
Date: 2020-09-29
Category: Blog
Authors: Saurav Tuladhar
Tags: detectron2, r-cnn, dl
Slug: reproduce-rcnn-metrics
Summary: How can we reproduce metrics specified on Model Zoo page.

Detectron2 provides metrics for all models in the Model zoo. For this project, we are using the Mask R-CNN models trained on MS COCO dataset. As a part adapting the pre-trained models for your specific use, we wanted to verify the metrics advertised in the Model zoo page. For the verification task, I tested two pretrained models. The annotation (box) and segmentation (mask) AP metrics for the two models are:

|Model|bbox-AP | mask-AP|
|:---------|:----|------|
|R50-FPN-3x|41.0 | 37.2 |
|R50-FPN-1x|38.6 | 35.2 |


Code to reproduce the metrics is straight forward as shown below. First we configure Detectron2 to load the pre-trained weights to the model under test.
```python
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_1x.yaml"))
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_1x.yaml")
predictor = DefaultPredictor(cfg)
```

Then we can use Detectron2's builtin `COCOEvaluator` to evaluate our model and compute the metrics on COCO 2017 validation set,
```python
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader
evaluator = COCOEvaluator("coco_2017_val", cfg, False, output_dir="./output/")
val_loader = build_detection_test_loader(cfg, "coco_2017_val")
print(inference_on_dataset(predictor.model, val_loader, evaluator))
```
We tested two trained Mask R-CNN models from the model zoo and evaluated their metrics on the COCO 2017 validation set. The testing reproduced the exact values for the box AP and mask AP as in the table above. Below is an abridged verison of the model evaluation output for R50-FPN 1x  and R50-FPN 3x model. The computed metrics are in line 6 and 14.

**Metrics for R50-FPN-3x**
```text
Running per image evaluation...
Evaluate annotation type *bbox*
COCOeval_opt.evaluate() finished in 12.82 seconds.
Accumulating evaluation results...
COCOeval_opt.accumulate() finished in 1.37 seconds.
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.410

Running per image evaluation...
Evaluate annotation type *segm*
COCOeval_opt.evaluate() finished in 16.08 seconds.
Accumulating evaluation results...
COCOeval_opt.accumulate() finished in 1.36 seconds.
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.372
```

**Metrics for R50-FPN-1x**
```text
Running per image evaluation...
Evaluate annotation type *bbox*
COCOeval_opt.evaluate() finished in 9.37 seconds.
Accumulating evaluation results...
COCOeval_opt.accumulate() finished in 1.18 seconds.
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.386

Evaluate annotation type *segm*
COCOeval_opt.evaluate() finished in 11.96 seconds.
Accumulating evaluation results...
COCOeval_opt.accumulate() finished in 1.17 seconds.
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.352
```
