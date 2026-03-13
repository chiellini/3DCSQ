from pathlib import Path
import os
import sys

# 配置路径
dataset_c_path = Path(r"E:\CityU-Onedrive-Backup\Zelin OneDrive - City University of Hong Kong - Student\MembraneProjectData\CMapSubmission\Dataset Access\Dataset C")

print("=" * 80)
print("Dataset C Embryo Scan")
print("=" * 80)
print(f"\nPath: {dataset_c_path}")
print(f"Exists: {dataset_c_path.exists()}\n")

if dataset_c_path.exists():
    # Get all subdirectories
    embryo_dirs = [d for d in dataset_c_path.iterdir() if d.is_dir()]
    
    print(f"Found {len(embryo_dirs)} embryo samples:\n")
    
    embryo_names = []
    for embryo_dir in sorted(embryo_dirs):
        embryo_name = embryo_dir.name
        
        # Count nii.gz files
        nii_files = list(embryo_dir.glob("*_segCell.nii.gz"))
        
        embryo_names.append(embryo_name)
        print(f"  - {embryo_name}: {len(nii_files)} timepoint files")
    
    print("\n" + "=" * 80)
    print("Python List Format (copy to Notebook):")
    print("=" * 80)
    print(f"\nSELECTED_EMBRYOS = {embryo_names}\n")
    
    print("=" * 80)
    print("Plain Text Format:")
    print("=" * 80)
    for name in embryo_names:
        print(name)
else:
    print("Path does not exist!")
