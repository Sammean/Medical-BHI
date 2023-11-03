# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 202311/02 22:29
# @Author  : Sammean Shaw
# @FileName: scratch.py
import SimpleITK as sitk
import numpy as np

if __name__ == '__main__':
    mask = r'E:\Win10_data\BHI\Dataset\Paired\mask\sub-OAS30001_ses-d2430_T1w_mask.nii.gz'
    mri = r'E:\Win10_data\BHI\Dataset\Paired\Reg_with_MNI152\sub-OAS30001_ses-d2430_T1w.nii.gz'
    mri2 = r'E:\Win10_data\BHI\Dataset\Paired\Reg_with_MNI152_T1\sub-OAS30001_ses-d2430_FLAIR.nii.gz'
    arr = sitk.GetArrayFromImage(sitk.ReadImage(mask))
    img = sitk.GetArrayFromImage(sitk.ReadImage(mri))
    img2 = sitk.GetArrayFromImage(sitk.ReadImage(mri2))
    data = np.stack((img[arr != 0], img2[arr != 0]), axis=-1)  # [num of brain voxel, 2]

    # Pretend the data is the prediction of GMM ~~~  'QAQ'  ~~~
    # So, each value of data now is the probability of 'health' !!!
    # And is an array with shape like [num of brain voxel, clusters]
    # What a coincidence! The same with origin ~~~
    # By now, the data can be used to calculate BHI, Yeah !
    # But, I want to see!!! How to visualize?
    # Next, I need to turn data into 'health' label
    # Consider data[:, 0] is the predicted health probabilities of GMM
    # Set a threshold r, if current element of data > r, the voxel is proposed to be a 'health' one.
    # That is : label = 1 if voxel > r else 0
    # Get Label Array, labels[num of brain voxel]
    # Finally, I need to assign the label according to the mask index !!! T-T !!! Trouble! ~Oh~!!
    # Go to implement it ======>>>>>!!!
    r = 0
    labels = np.where(data[:, 0] > r, 3, 0)
    res = np.zeros_like(arr)
    res[arr != 0] = labels
    # It seems worked !
    # Demo Completed !!! Aha...Try it in Real Data

