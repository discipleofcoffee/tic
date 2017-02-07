#!/bin/bash

#
# Convert iRAS to wLPS for template for test points.  We will compare these points to those transformed
# from native space. This comparison is valid because these points were independently selected. 
#

iwCtf_extract_affine.py native-SyN-ixi_t1w.nii.gz affine.native-SyN-ixi_t1w.nii.txt
iwCtf_iras_to_wlps.py fiducials_iras_ixi.csv fiducials_wlps_ixi.csv -t affine.native-SyN-ixi_t1w.nii.txt -v

#
# Create matrices
#

iwCtf_extract_affine.py nu.nii.gz affine_iras_to_wras.txt

# These commands were used to transform Constance's points for testing. There is a slight mismatch between
# Constance's fiducials and Jen's fiducials. By using Constance's fiducials there is better 
# alignment with the fiducials on the image. 

iwCtf_iras_to_icsa.py ../input/fiducials_iras_native.csv fiducials_icsa_native.csv -v

# Transfrom points from iCSA to wLPS space
iwCtf_icsa_to_wlps.py fiducials_icsa_native.csv fiducials_wlps_native.csv --transform affine_iras_to_wras.txt  -v

# Calculate CTF matrix from wLPS fiducials
iwCtf_ctf_matrix.py   fiducials_wlps_native.csv affine_wlps_to_wctf.txt

#=========================================================================================================
# Transform from wLPS to wCTF
#

iwCtf_antsApplyTransformPoints.py fiducials_wlps_native.csv fiducials_wlps_ctf.csv -t affine_wlps_to_wctf.txt -v


##=========================================================================================================
# Transform from wLPS to wTemplate
#

echo "=========== IXI Reference"
echo
cat fiducials_wlps_ixi.csv
echo
echo

echo "=========== IXI B"
iwCtf_antsApplyTransformPoints.py fiducials_wlps_native.csv fiducials_wlps_ixi_B.csv \
    -t TemplateToSubject1GenericAffine.mat   TemplateToSubject0Warp.nii.gz -v


##=========================================================================================================
# Perform inverse transformation from Template to wLPS.  This is done as a sanity check
#

echo "=========== IXI Reference"
echo
cat fiducials_wlps_native.csv

echo "=========== IXI B Inverse"

iwCtf_antsApplyTransformPoints.py fiducials_wlps_ixi_B.csv fiducials_wlps_native_C.csv \
    -t SubjectToTemplate1Warp.nii.gz SubjectToTemplate0GenericAffine.mat -v


##=========================================================================================================
# Transform from Template to wCTF. 
#

echo "=========== IXI Reference"
echo
cat fiducials_wlps_ctf.csv

echo "=========== IXI B Inverse"

iwCtf_antsApplyTransformPoints.py fiducials_wlps_ixi_B.csv fiducials_wlps_ctf_B.csv \
    -t affine_wlps_to_wctf.txt SubjectToTemplate1Warp.nii.gz SubjectToTemplate0GenericAffine.mat -v


