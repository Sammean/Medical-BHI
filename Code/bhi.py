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
    """Calculate a Subject BHI
    :parameter
        :param mri_list: the MRIs paths of the subject, e.g. [T1.nii.gz, FL.nii.gz, ... ]
        :param icv_path: the ICV mask path of the subject, e.g. [mask.nii.gz]
        :param ratio: Used to control the map, when generating the visualization of 'health mask'
        :param idx: a inner parameter for the name of generated health mask
    :return
        bhi_mean: BHI
    """
    def __init__(self, mri_list=None, icv_path=None, ratio=0, idx=None):
        self.icv = icv_path
        self.img_list = mri_list
        self.r = ratio
        self.idx = idx

    def get_bhi(self):
        mri_data = None
        icv = sitk.ReadImage(self.icv)
        icv_mask = sitk.GetArrayFromImage(icv)      # icv_mask[D,H,W]
        for l in self.img_list:
            img = sitk.GetArrayFromImage(sitk.ReadImage(l))     # img[D,H,W]
            img = zscore(img)   # Normalization --> img[D,H,W]
            mri_data = np.stack((mri_data, img[icv_mask != 0]), axis=-1) \
                if mri_data is not None else img[icv_mask != 0]
            # mri_data[voxel nums of brain, nums of MRI modalities]

        n_clusters = 2
        gmm = GaussianMixture(n_components=n_clusters, random_state=725)
        gmm.fit(mri_data)

        posterior_probabilities = gmm.predict_proba(mri_data)
        bhi_mean = np.mean(posterior_probabilities, axis=0)     # each class mean probability, bhi_mean[a,b=1-a]
        max_idx = np.argmax(bhi_mean)

        # Generate Health Mask According to Ratio
        # Find more implementation details in /Code/scratch/scratch.py
        labels = np.where(posterior_probabilities[:, max_idx] > self.r, 3, 0)
        health_mask = np.zeros_like(icv_mask)
        health_mask[icv_mask != 0] = labels
        out = sitk.GetImageFromArray(health_mask)
        out.CopyInformation(icv)
        des = os.path.join(os.path.dirname(os.path.dirname(self.icv)), f'health_mask_ratio_{self.r}')
        os.makedirs(des, exist_ok=True)
        sitk.WriteImage(out, os.path.join(des, self.idx + '_bhi{:04f}.nii.gz'.format(bhi_mean[max_idx])))

        # In general, health voxels should more than those present abnormal (I guess~)
        # So, return bigger value
        return bhi_mean[max_idx]


class BHIs(object):
    """Calculate BHIs
    :parameter
        :param mri_list: Multimodal MRI Directory of subjects, e.g. [*/T1, */FL, ... ]
        :param icv_paths: the ICV mask paths of subjects, e.g. [*/Mask]
        :param ratio: Used to control the map, when generating the visualization of 'health mask'
    :return
        bhi_means: BHIs
    """
    def __init__(self, mri_list=None, icv_paths=None, ratio=0):
        self.icv = icv_paths
        self.mri_list = mri_list
        self.r = ratio

    def cal_bhi(self):
        bhi_means = []
        for item in os.listdir(self.icv):       # Collect one subject infos : icv_mask, [MRIs]
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
    # mask = r'E:\Win10_data\BHI\Dataset\Paired\mask\sub-OAS30001_ses-d2430_T1w_mask.nii.gz'
    # flair = r'E:\Win10_data\BHI\Dataset\Paired\Reg_with_MNI152_brain\sub-OAS30001_ses-d2430_T1w.nii.gz'
    # t1 = r'E:\Win10_data\BHI\Dataset\Paired\Reg_with_MNI152_T1_brain\sub-OAS30001_ses-d2430_FLAIR.nii.gz'
    # operator = BHI(flair, t1, icv_path=mask, ratio=0.5)
    # res = operator.get_bhi()
    # print(res)

    # Multi-Test
    mask_p = r'E:\Win10_data\BHI\Dataset\Paired\mask'
    mri_p = [
        r'E:\Win10_data\BHI\Dataset\Paired\Reg_with_MNI152',
        r'E:\Win10_data\BHI\Dataset\Paired\Reg_with_MNI152_T1'
    ]
    operator = BHIs(mri_p, mask_p, ratio=0.05)
    res = operator.cal_bhi()
    print(res)
