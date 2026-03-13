from pathlib import Path
import glob

# Config path
dataset_c_path = Path(r"E:\CityU-Onedrive-Backup\Zelin OneDrive - City University of Hong Kong - Student\MembraneProjectData\CMapSubmission\Dataset Access\Dataset C")

print("=" * 80)
print("Dataset C - SegCell Directory Scan")
print("=" * 80)

# Check a few embryos
embryos_to_check = ['WT_Sample1', 'MT_lag-1_Sample1', 'MT_pop-1_Sample1']

for embryo_name in embryos_to_check:
    embryo_dir = dataset_c_path / embryo_name
    segcell_dir = embryo_dir / "SegCell"
    
    print(f"\n{embryo_name}:")
    print(f"  Embryo Dir: {embryo_dir}")
    print(f"  SegCell Dir Exists: {segcell_dir.exists()}")
    
    if segcell_dir.exists():
        # Find nii.gz files
        nii_files = sorted(glob.glob(str(segcell_dir / "*_segCell.nii.gz")))
        print(f"  Number of nii.gz files: {len(nii_files)}")
        
        if nii_files:
            print(f"  First 3 files:")
            for f in nii_files[:3]:
                file_path = Path(f)
                print(f"    - {file_path.name}")
        
        # Show all items in SegCell directory
        all_items = list(segcell_dir.iterdir())
        print(f"  SegCell Directory Contents ({len(all_items)} items):")
        for item in all_items[:10]:
            if item.is_dir():
                print(f"    [DIR] {item.name}/")
            else:
                size_mb = item.stat().st_size / 1024 / 1024
                print(f"    [FILE] {item.name} ({size_mb:.1f} MB)")
        if len(all_items) > 10:
            print(f"    ... and {len(all_items) - 10} more items")

print("\n" + "=" * 80)
print("Complete Embryo List (with SegCell directory):")
print("=" * 80)

all_embryos = []
for embryo_dir in sorted(dataset_c_path.iterdir()):
    if embryo_dir.is_dir():
        segcell_dir = embryo_dir / "SegCell"
        if segcell_dir.exists():
            nii_files = sorted(glob.glob(str(segcell_dir / "*_segCell.nii.gz")))
            if nii_files:
                all_embryos.append(embryo_dir.name)
                print(f"[OK] {embryo_dir.name}: {len(nii_files)} timepoints")

print("\n" + "=" * 80)
print("Python List Format:")
print("=" * 80)
print(f"\nSELECTED_EMBRYOS = {all_embryos}\n")
