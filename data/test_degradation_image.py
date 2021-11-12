import random
import numpy as np
import math
import torch.utils.data as data
import utils.utils_image as util
import torch
from data.degradations import circular_lowpass_kernel, random_mixed_kernels
from utils.img_process_util import USMSharp, filter2D
from data.degradations import random_add_gaussian_noise_pt, random_add_poisson_noise_pt
from torch.nn import functional as F
from utils.diffjpeg import DiffJPEG

def Blur_kernel(img):

    # blur settings for the first degradation
    blur_kernel_size = 21
    kernel_list = ['iso', 'aniso', 'generalized_iso', 'generalized_aniso', 'plateau_iso', 'plateau_aniso']
    kernel_prob = [0, 0, 0, 0, 0, 1]
    blur_sigma = [1, 3]
    betag_range = [0.5, 4]
    betap_range = [1, 2]
    sinc_prob = 0

    # a final sinc filter
    final_sinc_prob = 0.8

    kernel_range = [2 * v + 1 for v in range(3, 11)]  # kernel size ranges from 7 to 21
    pulse_tensor = torch.zeros(21, 21).float()  # convolving with pulse tensor brings no blurry effect
    pulse_tensor[10, 10] = 1

    H, W, _ = img.shape
    # ------------------------ Generate kernels (used in the first degradation) ------------------------ #
    kernel_size = 21
    if np.random.uniform() < 0.0001:
        # this sinc filter setting is for kernels ranging from [7, 21]
        if kernel_size < 13:
            omega_c = np.random.uniform(np.pi / 3, np.pi)
        else:
            omega_c = np.random.uniform(np.pi / 5, np.pi)
        kernel = circular_lowpass_kernel(omega_c, kernel_size, pad_to=False)
    else:
        kernel = random_mixed_kernels(
            kernel_list,
            kernel_prob,
            kernel_size,
            blur_sigma,
            blur_sigma, [-math.pi, math.pi],
            betag_range,
            betap_range,
            noise_range=None)
    # pad kernel
    pad_size = (21 - kernel_size) // 2
    kernel = np.pad(kernel, ((pad_size, pad_size), (pad_size, pad_size)))

    # ------------------------------------- sinc kernel ------------------------------------- #
    if np.random.uniform() < 0.8:
        kernel_size = random.choice(kernel_range)
        omega_c = np.random.uniform(np.pi / 3, np.pi)
        sinc_kernel = circular_lowpass_kernel(omega_c, kernel_size, pad_to=21)
        sinc_kernel = torch.FloatTensor(sinc_kernel)
    else:
        sinc_kernel = pulse_tensor

    # --------------------------------
    # HWC to CHW, numpy(uint) to tensor
    # --------------------------------
    # img = util.uint2tensor3(img)
    # kernel = torch.FloatTensor(kernel)

    return kernel

if __name__ == '__main__':
    img = util.imread_uint('bird.png', 3)
    img = util.uint2single(img)
    ####################### Blur kernel ##########################
    # kernel = Blur_kernel(img)
    # saved_kernel = (kernel - np.min(kernel)) / (np.max(kernel) - np.min(kernel)) * 255
    # kernel = torch.FloatTensor(kernel)
    # img = util.single2tensor4(img)
    # out = filter2D(img, kernel)
    # name='plateau_aniso'
    # util.imsave(saved_kernel, name+'_kernel.png')
    # out = util.tensor2uint(out)
    # util.imsave(out,name+'_bird.png')

    ######################### Noise ###############################
    # img = util.single2tensor4(img)
    # #out = random_add_poisson_noise_pt(img, scale_range=[0.05, 3], gray_prob=0, clip=True, rounds=False)
    # out = random_add_gaussian_noise_pt(img, sigma_range=[1, 30], clip=True, rounds=False, gray_prob=1)
    # name = 'random_add_gaussian_noise_pt2'
    # out = util.tensor2uint(out)
    # util.imsave(out, name + '_bird.png')
    ######################### Resize #########################################
    # random resize
    # img = util.single2tensor4(img)
    # updown_type = random.choices(['up', 'down', 'keep'], [ 0.8, 0.1, 0.1 ])[0]
    # if updown_type == 'up':
    #     scale = np.random.uniform(1, 1.5)
    # elif updown_type == 'down':
    #     scale = np.random.uniform(0.15, 1)
    # else:
    #     scale = 1
    # mode = 'bilinear' # random.choice(['area', 'bilinear', 'bicubic'])
    # out = F.interpolate(img, scale_factor=scale, mode=mode)
    #
    # name = 'bilinear'
    # out = util.tensor2uint(out)
    # util.imsave(out, name + '_bird.png')
    ###############JPEG##################################
    img = util.single2tensor4(img)
    jpeger = DiffJPEG(differentiable=False)

    jpeg_p = img.new_zeros(img.size(0)).uniform_(*[ 30, 95 ])
    out = torch.clamp(img, 0, 1)
    out = jpeger(img, quality=jpeg_p)
    name = 'jpeger'
    out = util.tensor2uint(out)
    util.imsave(out, name + '_bird.png')
