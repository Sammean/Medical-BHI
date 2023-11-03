# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2023/11/02 15:09
# @Author  : Sammean Shaw
# @FileName: bhi.py

import SimpleITK as sitk
import numpy as np
from sklearn.mixture import GaussianMixture
import glob
import os
from scipy.stats import zscore


class BHI(object):
    def __init__(self, mri_list=None, icv_path=None, ratio=0, idx=None):
        self.icv = icv_path
        self.img_list = mri_list
        self.r = ratio
        self.idx = idx

    def get_bhi(self):
        mri_data = None
        icv = sitk.ReadImage(self.icv)
        icv_mask = sitk.GetArrayFromImage(icv)
        for l in self.img_list:
            img = sitk.GetArrayFromImage(sitk.ReadImage(l))
            img = zscore(img)
            mri_data = np.stack((mri_data, img[icv_mask != 0]), axis=-1) \
                if mri_data is not None else img[icv_mask != 0]
        # mri_data = mri_data.reshape((-1, len(self.img_list)))

        n_clusters = 2
        gmm = GaussianMixture(n_components=n_clusters, random_state=725)
        gmm.fit(mri_data)

        posterior_probabilities = gmm.predict_proba(mri_data)
        bhi_mean = np.mean(posterior_probabilities, axis=0)

        # Generate Health Mask
        # labels = np.where(posterior_probabilities > self.r, 3, 0)
        # health_mask = np.zeros_like(icv_mask)
        # health_mask[icv_mask != 0] = labels
        # out = sitk.GetImageFromArray(health_mask)
        # out.CopyInformation(icv)
        # des = os.path.join(os.path.dirname(os.path.dirname(self.icv)), f'health_mask_ratio_{self.r}')
        # os.makedirs(des, exist_ok=True)
        # sitk.WriteImage(out, os.path.join(des, self.idx + '_bhi{:04f}.nii.gz'.format(bhi_mean)))

        return np.max(bhi_mean)


class BHIs(object):
    def __init__(self, mri_list=None, icv_paths=None, ratio=0):
        self.icv = icv_paths
        self.mri_list = mri_list
        self.r = ratio

    def cal_bhi(self):
        bhi_means = []
        for item in os.listdir(self.icv):
            idx = item.split('_')[0] + '_' + item.split('_')[1]
            icv_path = os.path.join(self.icv, item)
            mri_path = []
            for m in self.mri_list:
                p = glob.glob(f'{m}/{idx}*')
                assert len(p) == 1
                mri_path.append(p[0])
            print(f'>>> Calculating Samples {idx} BHI ...')
            op = BHI(mri_path, icv_path=icv_path, idx=idx, ratio=self.r)
            bhi_means.append(op.get_bhi())
        return bhi_means


if __name__ == '__main__':

    # Single-Test
    # mask = r'E:\Win10_data\BHI\Data\Paired\mask\sub-OAS30001_ses-d2430_T1w_mask.nii.gz'
    # flair = r'E:\Win10_data\BHI\Data\Paired\Reg_with_MNI152_brain\sub-OAS30001_ses-d2430_T1w.nii.gz'
    # t1 = r'E:\Win10_data\BHI\Data\Paired\Reg_with_MNI152_T1_brain\sub-OAS30001_ses-d2430_FLAIR.nii.gz'
    # operator = BHI(flair, t1, icv_path=mask, ratio=0.5)
    # res = operator.get_bhi()
    # print(res)

    # Multi-Test
    mask_p = r'E:\Win10_data\BHI\Data\Paired\mask'
    mri_p = [
        r'E:\Win10_data\BHI\Data\Paired\Reg_with_MNI152',
        r'E:\Win10_data\BHI\Data\Paired\Reg_with_MNI152_T1'
    ]
    operator = BHIs(mri_p, mask_p, ratio=0.5)
    res = operator.cal_bhi()
    print(res)
