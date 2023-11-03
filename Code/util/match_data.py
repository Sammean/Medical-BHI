# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2023/11/02 10:28
# @Author  : Sammean Shaw
# @FileName: match_data.py
import shutil
import glob
import os


class MatchFinder(object):
    def __init__(self, fl_p=None, t1_p=None, des_p=None):
        self.fp = fl_p
        self.tp = t1_p
        self.pairs = 0
        self.fpd = os.path.join(des_p, 'FLAIR')
        self.tpd = os.path.join(des_p, 'T1')
        os.makedirs(des_p, exist_ok=True)
        os.makedirs(self.fpd, exist_ok=True)
        os.makedirs(self.tpd, exist_ok=True)

    def find(self):
        for item in glob.glob(f'{self.fp}/*.nii.gz'):
            file_name = os.path.basename(item)
            idx = file_name.split('_')[0] + '_' + file_name.split('_')[1]
            for p in glob.glob(f'{self.tp}/*.nii.gz'):
                file_name2 = os.path.basename(p)
                if file_name2.startswith(idx):
                    print(f'>>> Find A Pair : {idx} , Copying......')
                    shutil.copy(item, os.path.join(self.fpd, file_name))
                    shutil.copy(p, os.path.join(self.tpd, file_name2))
                    self.pairs += 1
                    # print(f'Done! Current Number of Pairs is : {self.pairs} <<<')
                    break
        print(f'*** Find Pairs {self.pairs} in Total ***')
        return


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.getcwd()))
    mf = MatchFinder(os.path.join(root, 'Data', 'FLAIR_raw'),
                     os.path.join(root, 'Data', 'T1_raw'),
                     os.path.join(root, 'Data', 'Paired'))
    mf.find()
