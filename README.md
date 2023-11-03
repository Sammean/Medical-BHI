# The Brain Health Index

## Introduction

This is an implementation of  [*The brain health index: Towards a combined measure of neurovascular and neurodegenerative structural brain injury.*](https://journals.sagepub.com/doi/10.1177/1747493018770222)

This also referenced [*Normative values of the brain health index in UK biobank*](https://doi.org/10.1016/j.ynirp.2023.100176) when coding.

## Method

### 1. Register

- Register T1w MRI to a standard template : MNI152_T1_1mm using six-point rigid body registration

- Register other MRIs to the standardised T1w MRI(registered to MNI152) using 12-point affine registration

### 2. ICV Mask

- Using BET on standardised T1w MRI to generate the mask of extracted brain, which than be considered the ICV mask.

   (The validity of this step is debatable~)

### 3. Calculate BHI

- Applying ICV mask on each MRI to obtain the brains of one subject
- Stack all the brains of one subject. So, a voxel now have more than one value, and it can be recognized a feature with multi-attributes
- Using Gaussian Mixture Models (GMM), setting the `n_components=2`, to fit the data, which means the voxels are divided into 2 classes: one is the "Health", another is "Abnormal"
- Getting the probabilities of each voxel belonging to which class from the prediction of GMM by calling`GMM.predict_proba()`
- The mean of the probability of being predicted as a 'Health' voxel is then counted as the BHI

## Requirement

- ANTs or Antpyx (python library) : For registration
- BET : For brain extraction (contained in FSL, need Linux, so ~ ^-^ ~)
- Scikit-learn, Numpy, Scipy : For Use of Gaussian Mixture Models & Calculating
- SimpleITK : For reading and writing NIFTI (*.nii) files

---

## About the Data

### 1. Data Preprocessing
### 2. Format of Data

---

## About Visualization

- **If want to check the 'Health Mask'**

(to be continued......)