The main model i have created is in model.ipynb, and was trained on about 30.000 images (10.00 Ads, 20.000 simple images i.e. data_medium.rar)

i am currently working on the PreTrained_Model.ipnyb, which is a pre-trained NN trained on the same 30.000 images.

The Data_Augmentation files will not be needed probably as we have collected more data which are enough to achive 90%+ accuracy in our Model.

The Model_Optimizers was used to select the optimal optimizer

The Dataset

```
Dataset
└── shuffled_cleaned_images (35.000)     
    ├── train (60%)
    │   ├── Ads
    │   └── Regular
    ├── val (20%)
    │   ├── Ads
    │   └── Regular
    └── test (20%)
        ├── Ads
        └── Regular
```
https://github.com/dessa-oss/DeepFake-Detection
