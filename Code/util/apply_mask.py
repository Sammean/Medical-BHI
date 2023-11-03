# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2023/11/02 21:25
# @Author  : Sammean Shaw
# @FileName: apply_mask.py
import SimpleITK as sitk
import os
import glob


class ICVMasker(object):
    def __init__(self, mask_path=None, *args):
        self.mp = mask_path
        self.mri_list = args

    def get_brain(self):
        for item in os.listdir(self.mp):
            idx = item.split('_')[0] + '_' + item.split('_')[1]
            mask = sitk.GetArrayFromImage(sitk.ReadImage(os.path.join(self.mp, item)))
            for m in self.mri_list:
                p = glob.glob(f'{m}/{idx}*')
                assert len(p) == 1
                mri = sitk.ReadImage(p[0])
                out = sitk.GetImageFromArray(mask * sitk.GetArrayFromImage(mri))
                out.CopyInformation(mri)
                des = os.path.join(os.path.dirname(m), os.path.basename(m)+'_brain')
                os.makedirs(des, exist_ok=True)
                print(f'Generate ICV of {p[0]} in Dir {des} ...')
                sitk.WriteImage(out, os.path.join(des, os.path.basename(p[0])))
        return


if __name__ == '__main__':
    root = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'Dataset', 'Paired')
    icv = ICVMasker(os.path.join(root, 'mask'),
                    os.path.join(root, 'Reg_with_MNI152'), os.path.join(root, 'Reg_with_MNI152_T1'))
    icv.get_brain()
