# LePESwinSR
Swin Transformer for Real World Super Resolution Using Locally-enhanced Position Encoding

## Proposed algorithm
- generator
![proposed_model](img/proposed_model.png)
- LePE(Locally-enhanced Position Encoding)
![LePE_Attention_Block](img/LePE_Attention_Block.png)
- Neck

- discriminator
![patch_GAN](img/patchGAN.png)

## Ablation study
![ablation](img/ablation.png)

![building](img/ablation_study_building.png)

![dog](img/ablation_study_dog.png)

![dped_crop](img/ablation_study_dped_crop.png)

## Comparison with other models


![baby](img/comparison_baby.png)

![butterfly](img/comparison_butterfly.png)

![chip](img/comparison_chip.png)

![frog](img/comparison_frog.png)

[Training code]
- train -PSNR
```
python main_train.py
```

- train -GAN 
```
python main_train_gan.py
```