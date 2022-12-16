# cd ~/aide-svrtk
# ensure venv running
# ensure Docker running

# Test MAP code locally
python app -i input -o output

# Test MAP with MONAI Deploy
monai-deploy exec app -i input/ -o output/

# Initial packaging of MAP
monai-deploy package app --tag fetalsvrtk/aide:map-test -l DEBUG

# Push to DockerHub
docker push fetalsvrtk/aide:map-test

# Build 3rd-party software on top of MAP
# CPU mode
git checkout map
docker build -t fetalsvrtk/aide:map app/
# GPU mode
git checkout map-gpu-on
docker build -t fetalsvrtk/aide:map-gpu app/

# Test MAP-Extra with MONAI Deploy
monai-deploy run fetalsvrtk/aide:map input output

# Optional: Test scripts within Docker container
# - On DGX:
docker run -it --rm -v /home/troberts/code/aide-svrtk/input/nii_stacks:/home/recon --entrypoint /bin/bash fetalsvrtk/aide:map