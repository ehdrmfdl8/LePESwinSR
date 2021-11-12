import random
import numpy as np
import torch.utils.data as data
import utils.utils_image as util
import albumentations as A


class DatasetPlain(data.Dataset):
    '''
    # -----------------------------------------
    # Get L/H for image-to-image mapping.
    # Both "paths_L" and "paths_H" are needed.
    # -----------------------------------------
    # e.g., train denoiser with L and H
    # -----------------------------------------
    '''

    def __init__(self, opt):
        super(DatasetPlain, self).__init__()
        print('Get L/H for image-to-image mapping. Both "paths_L" and "paths_H" are needed.')
        self.opt = opt
        self.n_channels = opt['n_channels'] if opt['n_channels'] else 3
        self.patch_size = self.opt['H_size'] if self.opt['H_size'] else 64

        # ------------------------------------
        # get the path of L/H
        # ------------------------------------
        self.paths_H = util.get_image_paths(opt['dataroot_H'])
        self.paths_L = util.get_image_paths(opt['dataroot_L'])
        self.L_transform = A.Compose(
            [
                A.Blur(p=opt['Blur'], blur_limit=(3, 30)),
                A.ISONoise(p=opt['ISO_Noise'], intensity=(0.01, 0.1), color_shift=(0.01, 0.05))
            ]
        )
        self.common_transform = A.ReplayCompose(
            [
                A.RandomScale(p=opt['RandomScale'], scale_limit= (-0.7, 0), interpolation=0),
                A.RandomGridShuffle(p=1, grid=(3, 3)),
                A.Cutout(p=opt['Cutout'], num_holes=10, max_h_size=256, max_w_size=256)
            ])
        assert self.paths_H, 'Error: H path is empty.'
        assert self.paths_L, 'Error: L path is empty. Plain dataset assumes both L and H are given!'
        if self.paths_L and self.paths_H:
            assert len(self.paths_L) == len(self.paths_H), 'L/H mismatch - {}, {}.'.format(len(self.paths_L), len(self.paths_H))

    def __getitem__(self, index):

        # ------------------------------------
        # get H image
        # ------------------------------------
        H_path = self.paths_H[index]
        img_H = util.imread_uint(H_path, self.n_channels)

        # ------------------------------------
        # get L image
        # ------------------------------------
        L_path = self.paths_L[index]
        img_L = util.imread_uint(L_path, self.n_channels)

        # ------------------------------------
        # if train, get L/H patch pair
        # ------------------------------------
        if self.opt['phase'] == 'train':

            # H, W, _ = img_H.shape
            img_L = self.L_transform(image=img_L)['image']
            transformed_L = self.common_transform(image=img_L)
            H, W, _ = transformed_L['image'].shape
            transformed_H = A.ReplayCompose.replay(transformed_L['replay'], image=img_H)
            # --------------------------------
            # randomly crop the patch
            # --------------------------------
            rnd_h = random.randint(0, max(0, H - self.patch_size))
            rnd_w = random.randint(0, max(0, W - self.patch_size))
            patch_L = transformed_L['image'][rnd_h:rnd_h + self.patch_size, rnd_w:rnd_w + self.patch_size, :]
            patch_H = transformed_H['image'][rnd_h:rnd_h + self.patch_size, rnd_w:rnd_w + self.patch_size, :]

            # --------------------------------
            # augmentation - flip and/or rotate
            # --------------------------------
            mode = random.randint(0, 7)
            patch_L, patch_H = util.augment_img(patch_L, mode=mode), util.augment_img(patch_H, mode=mode)
            patch_L, patch_H = util.img_pad(patch_L, self.patch_size), util.img_pad(patch_H, self.patch_size)
            # --------------------------------
            # HWC to CHW, numpy(uint) to tensor
            # --------------------------------
            img_L, img_H = util.uint2tensor3(patch_L), util.uint2tensor3(patch_H)

        else:

            # --------------------------------
            # HWC to CHW, numpy(uint) to tensor
            # --------------------------------
            img_L, img_H = util.uint2tensor3(img_L), util.uint2tensor3(img_H)

        return {'L': img_L, 'H': img_H, 'L_path': L_path, 'H_path': H_path}

    def __len__(self):
        return len(self.paths_H)
