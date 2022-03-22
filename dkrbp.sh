#!/bin/sh

# main
git checkout main

docker build -t fetalsvrtk/aide:3dfetal_dcm2nii_op operators/dcm2nii_operator/
docker build -t fetalsvrtk/aide:3dfetal_brain_recon_op operators/fetal_brain_recon_operator/
docker build -t fetalsvrtk/aide:3dfetal_nii2dcm_op operators/nii2dcm_operator/

docker push fetalsvrtk/aide:3dfetal_dcm2nii_op
docker push fetalsvrtk/aide:3dfetal_brain_recon_op
docker push fetalsvrtk/aide:3dfetal_nii2dcm_op

# CPU mode
git checkout cpu-mode

docker build -t fetalsvrtk/aide:3dfetal_brain_recon_op_cpu operators/fetal_brain_recon_operator/

docker push fetalsvrtk/aide:3dfetal_brain_recon_op_cpu
