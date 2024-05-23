#!/bin/bash


# Setup for the analysis

echo "Make sure you are working in bash"
echo $0

# Ask user if working on LPC or lxplus
read -p "Are you working on LPC or lxplus? (Enter 'LPC' or 'lxplus'): " location

# Check user's response and source the appropriate conda.sh script
if [ "$location" == "LPC" ]; then
    source ~/nobackup/mambaforge/etc/profile.d/conda.sh
elif [ "$location" == "lxplus" ]; then
    read -p "Have you installed mamba? (yes/no): " mamba_installed
    if [ "$mamba_installed" == "yes" ]; then
        source ~/sraj/Work_/CUA_20--/Analysis/mambaforge/etc/profile.d/conda.sh
    else
        echo "Please install mamba first."
        exit 1
    fi
else
    echo "Invalid location. Please enter 'LPC' or 'lxplus'."
    exit 1
fi



# Activate the environment
conda activate higgs-dna

echo "Successfully Done!!"
echo "Enjoy and smile:-)"


cd HiggsDNA

#Set PYTHONPATH Environment Variable:
#export PYTHONPATH=/uscms_data/d3/sraj/HiggsDNA:$PYTHONPATH


# Set PYTHONPATH Environment Variable (applicable only for LPC)
if [ "$location" == "LPC" ]; then
    export PYTHONPATH=/uscms_data/d3/sraj/HiggsDNA:$PYTHONPATH
fi
