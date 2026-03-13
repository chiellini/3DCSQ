# 胚胎细胞形状分析 - Dataset C 使用说明

## Dataset C 胚胎列表

Dataset C 包含 **12 个胚胎样本**，分为三类：

### 1. lag-1 突变体 (2 个)
- `MT_lag-1_Sample1`
- `MT_lag-1_Sample2`

### 2. pop-1 突变体 (2 个)
- `MT_pop-1_Sample1`
- `MT_pop-1_Sample2`

### 3. 野生型 (8 个)
- `WT_Sample1`
- `WT_Sample2`
- `WT_Sample3`
- `WT_Sample4`
- `WT_Sample5`
- `WT_Sample6`
- `WT_Sample7`
- `WT_Sample8`

## 使用方法

### 1. 打开 Notebook
打开 `胚胎细胞形状分析_CMap 数据版.ipynb`

### 2. 选择要分析的胚胎
在"选择要分析的胚胎样本"单元格中，修改 `SELECTED_EMBRYOS` 列表：

```python
# 示例 1: 分析所有野生型胚胎
SELECTED_EMBRYOS = ["WT_Sample1", "WT_Sample2", "WT_Sample3", 
                    "WT_Sample4", "WT_Sample5", "WT_Sample6", 
                    "WT_Sample7", "WT_Sample8"]

# 示例 2: 分析单个胚胎
SELECTED_EMBRYOS = ["WT_Sample1"]

# 示例 3: 分析突变体
SELECTED_EMBRYOS = ["MT_lag-1_Sample1", "MT_pop-1_Sample1"]

# 示例 4: 混合分析
SELECTED_EMBRYOS = ["WT_Sample1", "MT_lag-1_Sample1", "MT_pop-1_Sample1"]
```

### 3. 运行分析
按顺序执行所有单元格

### 4. 查看结果
结果保存在 `./results/Dataset C/` 目录下

## 注意事项

⚠️ **重要**: 扫描发现所有胚胎目录中都没有 `*_segCell.nii.gz` 文件！

可能的原因：
1. 文件命名格式不同
2. 文件在其他子目录中
3. 需要使用不同的文件扩展名

建议检查：
```python
# 在 Notebook 中添加一个单元格来查看实际文件
import glob
for embryo_name in SELECTED_EMBRYOS:
    embryo_path = DATASET_C_PATH / embryo_name
    all_files = list(embryo_path.glob("*"))
    print(f"{embryo_name}: {len(all_files)} 个文件")
    if all_files:
        print(f"  示例文件：{all_files[0].name}")
```

## 输出文件结构

```
results/
└── Dataset C/
    ├── Dataset_C_overall_summary.csv  (总体汇总)
    ├── WT_Sample1/
    │   ├── WT_Sample1_summary.csv  (胚胎汇总)
    │   ├── tp001_volume_surface_stats.csv
    │   ├── tp001_shape_descriptors.csv
    │   └── visualizations/
    │       ├── tp001_shape_descriptors_distribution.png
    │       └── tp001_shape_descriptors_correlation.png
    └── WT_Sample2/
        └── ...
```

## 分析的形状描述符

基于 EmbSAM (Nature Communications Biology, 2026)：

1. **General Sphericity** - 广义球度
2. **Hayakawa Roundness** - Hayakawa 圆度
3. **Spreading Index** - 铺展指数
4. **Diameter** - 直径

以及传统的：
- Volume (体积)
- Surface (表面积)
