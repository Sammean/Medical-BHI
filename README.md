# The Brain Health Index

## Introduction

This is an implementation of  [*The brain health index: Towards a combined measure of neurovascular and neurodegenerative structural brain injury*](https://journals.sagepub.com/doi/10.1177/1747493018770222).

This project also referenced [*Normative values of the brain health index in UK biobank*](https://doi.org/10.1016/j.ynirp.2023.100176) when coding.

## Method

### 1. Register

- Register T1w MRI to a standard template (MNI152_T1_1mm) using six-point rigid body registration

- Register other MRIs to the standardised T1w MRI(registered to MNI152) using 12-point affine registration

### 2. ICV Mask

- Using BET on standardised T1w MRI to generate the mask of brain, which than be considered as the ICV mask.

   (The validity of this step is debatable~)

### 3. Calculate BHI

- Applying ICV masks on MRIs of one subject to obtain the brains
- Stack all the brains of one subject. So, a voxel now have more than one value, and it can be recognized a feature with multi-attributes
- Using Gaussian Mixture Models (GMM), setting the `n_components=2`, to fit the data, which means the voxels are divided into 2 classes: one is the "Health", another is "Abnormal"
- Getting the probabilities of each voxel belonging to which class from the prediction of GMM by calling`GMM.predict_proba()`
- The mean of the probability of being predicted as a 'Health' voxel is then counted as the BHI

## Requirement

- ANTs or antpyx (python library) : For registration
- BET : For brain extraction (contained in FSL, need Linux, so ~ ^-^ ~)
- Scikit-learn, Numpy, Scipy : For Use of Gaussian Mixture Models & Calculating
- SimpleITK : For reading and writing NIFTI (*.nii) files

---

## About the Data

### 1. Data Preprocessing

In `util` are some scripts for processing data. Here are some main introductions.

- `register.py`: run this to register MRIs.
- `bet_script.py`:  If FSL was installed, run this to obtain the brain masks.

### 2. Data Formation

Provided there are original MRIs of various modalities in correspond directories, `e.g. /T1, /T2, /FLAIR, ...`

1. Register to a template, obtaining registered MRIs: `/T1_reg, /T2_reg, /FLAIR_reg, ...`
2. Bet MRIs of one modality, obtaining the brain masks: `/brain_masks`

Once get the `registered data` and the `brain masks`, than BHI could be calculated.

---

## About Visualization

- **If want to check the 'Health Mask'**

  Restore the annotated codes in `bhi.py`, "Brain Health Mask Visualization" part

  Use parameter `Ratio` to control the generated health masks

  (I found the ratio is usually set to a small value (e.g. 0.05~0.5), and the larger the ratio, the smaller the generated masks are)
