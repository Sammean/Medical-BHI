# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2023/11/02 11:02
# @Author  : Sammean Shaw
# @FileName: register.py
import glob
import os
import ants


class Register(object):
    def __init__(self, fix_p=None, mov_p=None, des_p='Registered'):
        self.fp = fix_p
        self.mp = mov_p
        self.rp = os.path.join(os.path.dirname(fix_p), des_p)
        os.makedirs(self.rp, exist_ok=True)

    def reg_awb(self):
        for item in glob.glob(f'{self.fp}/*.nii.gz'):
            file_name = os.path.basename(item)
            idx = file_name.split('_')[0] + '_' + file_name.split('_')[1]
            p = glob.glob(f'{self.mp}/{idx}*.nii.gz')
            assert len(p) == 1
            fi, mi = ants.image_read(item), ants.image_read(p[0])
            print(f'>>> Registering Sample {p[0]} ......')
            reg = ants.registration(fi, mi, type_of_transform="Affine")['warpedmovout']
            ants.image_write(reg, os.path.join(self.rp, os.path.basename(p[0])))
        return

    def reg_standard(self):
        fi = ants.image_read(self.fp)
        for item in glob.glob(f'{self.mp}/*.nii.gz'):
            mi = ants.image_read(item)
            print(f'>>> Registering Sample {item} to MNI152 Template......')
            reg = ants.registration(fi, mi, type_of_transform="Rigid")['warpedmovout']
            ants.image_write(reg, os.path.join(self.rp, os.path.basename(item)))
        return


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.getcwd()))

    # register t1 to flair
    # r = Register(os.path.join(root, 'Data', 'Paired', 'FLAIR'), os.path.join(root, 'Data', 'Paired', 'T1'))
    # r.reg_awb()

    # register t1 with MNI152
    # r = Register(os.path.join(root, 'Data', 'Template', 'MNI152_T1_1mm.nii.gz'),
    #              os.path.join(root, 'Data', 'Paired', 'T1'),
    #              'Reg_with_MNI152')
    # r.reg_standard()

    # register flair to MNI152_t1
    r = Register(os.path.join(root, 'Data', 'Paired', 'Reg_with_MNI152'),
                 os.path.join(root, 'Data', 'Paired', 'FLAIR'),
                 'Reg_with_MNI152_T1')
    r.reg_awb()





