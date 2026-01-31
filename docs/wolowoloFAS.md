# WolowoloFAS Dataset Structure

## Dataset Structure Overview

The `wolowolo_fas` dataset is organized into two main protocol splits: **MCIO** and **WCS**, each containing multiple face anti-spoofing datasets.

### Top-Level Structure

```
wolowolo_fas/
├── MCIO/          # Multi-dataset collection (MCIO protocol)
│   ├── frame/     # Image frames directory
│   └── txt/       # Annotation text files
└── WCS/           # Wild Cross-dataset (WCS protocol)
    ├── frame/     # Image frames directory
    └── txt/       # Annotation text files
```

## MCIO Structure

### Datasets Included

The MCIO protocol contains the following datasets:
- **casia** - CASIA-FASD dataset
- **celeb** - CelebA-Spoof dataset
- **msu** - MSU-MFSD dataset
- **oulu** - OULU-NPU dataset
- **replay** - Replay-Attack dataset

### Directory Layout

```
MCIO/frame/
├── casia/
│   ├── train/
│   │   ├── real/  (PNG files: e.g., 1_1_frame0.png, 1_1_frame1.png)
│   │   └── fake/  (PNG files: e.g., 1_3_frame0.png, 1_4_frame0.png)
│   └── test/
│       ├── real/
│       └── fake/
├── celeb/
│   ├── fake/
│   └── real/
├── msu/
│   ├── train/
│   │   ├── real/
│   │   └── fake/
│   └── test/
│       ├── real/
│       └── fake/
├── oulu/
│   ├── train/
│   │   ├── real/
│   │   └── fake/
│   └── test/
│       ├── real/
│       └── fake/
└── replay/
    ├── train/
    │   ├── real/
    │   └── fake/
    ├── dev/
    │   ├── real/
    │   └── fake/
    └── test/
        ├── real/
        └── fake/
```

### Annotation Files (`txt/`)

The annotation files follow the naming pattern: `{dataset}_{label}_{split}.txt`

**Examples:**
- `casia_real_train.txt` - CASIA real (bona fide) training samples
- `casia_fake_train.txt` - CASIA fake (spoof) training samples
- `casia_real_test.txt` - CASIA real test samples
- `casia_fake_test.txt` - CASIA fake test samples
- `casia_real_shot.txt` - CASIA real few-shot samples
- `casia_fake_shot.txt` - CASIA fake few-shot samples

**File Format:**
Each line contains a relative path to an image file:
```
casia/train/real/17_HR_1_frame0.png
casia/test/real/13_1_frame0.png
casia/train/fake/4_4_frame0.png
```

**Note:** Some train annotation files may contain paths from both train and test directories.

### File Naming Patterns (MCIO)

**Real (Bona Fide) Images:**
- Format: `{subject_id}_{session}_{frame}.png`
- Examples: `1_1_frame0.png`, `1_1_frame1.png`, `1_2_frame0.png`
- HR variants: `{subject_id}_HR_{session}_{frame}.png` (e.g., `1_HR_1_frame0.png`)

**Fake (Spoof) Images:**
- Format: `{subject_id}_{attack_type}_{frame}.png`
- Examples: `1_3_frame0.png`, `1_4_frame0.png`, `1_5_frame0.png`
- HR variants: `{subject_id}_HR_{attack_type}_{frame}.png` (e.g., `1_HR_2_frame0.png`)

## WCS Structure

### Datasets Included

The WCS protocol contains the following datasets:
- **cefa** - CEFA dataset
- **surf** - SiW dataset
- **wmca** - WMCA dataset

### Directory Layout

```
WCS/frame/
├── cefa/
│   ├── train/
│   │   ├── real/  (JPG files)
│   │   └── fake/  (JPG files)
│   └── test/
│       ├── real/
│       └── fake/
├── surf/
│   ├── train/
│   │   ├── real/
│   │   └── fake/
│   └── test/
│       ├── real/
│       └── fake/
└── wmca/
    ├── train/
    │   ├── real/
    │   └── fake/
    └── test/
        ├── real/
        └── fake/
```

### Annotation Files (`txt/`)

Similar naming pattern as MCIO: `{dataset}_{label}_{split}.txt`

**Examples:**
- `cefa_real_train.txt` - CEFA real training samples
- `cefa_fake_train.txt` - CEFA fake training samples
- `cefa_real_test.txt` - CEFA real test samples
- `cefa_fake_test.txt` - CEFA fake test samples
- `cefa_real_shot.txt` - CEFA real few-shot samples
- `cefa_fake_shot.txt` - CEFA fake few-shot samples

**File Format:**
Each line contains a relative path:
```
cefa/test/real/3_272_1_1_1_09.jpg
cefa/test/fake/3_230_3_2_2_07.jpg
cefa/train/real/1_260_1_1_1_05.jpg
```

### File Naming Patterns (WCS)

**WCS datasets use a more complex naming pattern:**
- Format: `{subject_id}_{session}_{label}_{variant}_{frame}.jpg`
- Example: `3_272_1_1_1_09.jpg`
  - `3` - subject ID
  - `272` - session ID
  - `1` - label (1=real, 3=fake)
  - `1` - variant
  - `1` - additional identifier
  - `09` - frame number

## Annotation File Types

Each dataset has three types of annotation files:

1. **`{dataset}_{label}_train.txt`** - Training samples
2. **`{dataset}_{label}_test.txt`** - Test samples
3. **`{dataset}_{label}_shot.txt`** - Few-shot samples (subset for few-shot learning)

## Implementation Notes

### For `load_data_list()` Implementation

When implementing the `load_data_list()` method in your `BaseDataset` subclass:

1. **Read the appropriate annotation file** (e.g., `casia_real_train.txt`)
2. **Parse each line** to extract the relative path
3. **Construct full paths** using `img_prefix` (likely `MCIO/frame/` or `WCS/frame/`)
4. **Assign labels:**
   - `real` → `gt_label: 0` (bona fide/authentic)
   - `fake` → `gt_label: 1` (spoof/attack)
5. **Return list of dictionaries** with `img_path` and `gt_label`

### Example Data Dictionary Structure

```python
{
    'img_path': 'MCIO/frame/casia/train/real/17_HR_1_frame0.png',
    'gt_label': 0  # 0 for real, 1 for fake
}
```

### Dataset Characteristics

- **Multi-dataset support**: Both MCIO and WCS contain multiple face anti-spoofing datasets
- **Separate train/test splits**: Each dataset has its own train/test division
- **Binary classification**: Real (0) vs Fake (1) labels
- **Mixed file formats**: MCIO uses PNG, WCS uses JPG
- **Frame-based**: Images are extracted frames from videos (indicated by `frame0`, `frame1`, etc.)

This structure supports multi-dataset training and evaluation scenarios for face anti-spoofing detection.
