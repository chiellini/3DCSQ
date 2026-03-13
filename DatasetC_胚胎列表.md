# Dataset C 胚胎样本完整列表

## 文件结构
```
Dataset C/
├── WT_Sample1/
│   └── SegCell/
│       ├── WT_Sample1_001_segCell.nii.gz
│       ├── WT_Sample1_002_segCell.nii.gz
│       └── ... (共 255 个时间点)
├── WT_Sample2/
│   └── SegCell/
│       └── ... (共 195 个时间点)
└── ...
```

## 胚胎样本详情

### 野生型 (Wild Type) - 8 个
| 胚胎名称 | 时间点数量 | 文件大小 (约) |
|---------|-----------|-------------|
| WT_Sample1 | 255 | 260 MB |
| WT_Sample2 | 195 | 200 MB |
| WT_Sample3 | 185 | 190 MB |
| WT_Sample4 | 220 | 230 MB |
| WT_Sample5 | 195 | 200 MB |
| WT_Sample6 | 205 | 210 MB |
| WT_Sample7 | 205 | 210 MB |
| WT_Sample8 | 195 | 200 MB |

### lag-1 突变体 - 2 个
| 胚胎名称 | 时间点数量 | 文件大小 (约) |
|---------|-----------|-------------|
| MT_lag-1_Sample1 | 195 | 200 MB |
| MT_lag-1_Sample2 | 195 | 200 MB |

### pop-1 突变体 - 2 个
| 胚胎名称 | 时间点数量 | 文件大小 (约) |
|---------|-----------|-------------|
| MT_pop-1_Sample1 | 140 | 150 MB |
| MT_pop-1_Sample2 | 155 | 160 MB |

## 总计
- **12 个胚胎样本**
- **2,390 个时间点**
- **约 2.4 GB 数据**

## 使用示例

### 分析单个野生型胚胎
```python
SELECTED_EMBRYOS = ["WT_Sample1"]
```

### 分析所有野生型胚胎
```python
SELECTED_EMBRYOS = [
    "WT_Sample1", "WT_Sample2", "WT_Sample3", "WT_Sample4",
    "WT_Sample5", "WT_Sample6", "WT_Sample7", "WT_Sample8"
]
```

### 分析突变体
```python
SELECTED_EMBRYOS = ["MT_lag-1_Sample1", "MT_pop-1_Sample1"]
```

### 对比分析（野生型 vs 突变体）
```python
SELECTED_EMBRYOS = [
    "WT_Sample1",  # 野生型对照
    "WT_Sample2",  # 野生型对照
    "MT_lag-1_Sample1",  # lag-1 突变体
    "MT_pop-1_Sample1"   # pop-1 突变体
]
```

## 快速测试
建议先使用少量胚胎进行测试：
```python
# 快速测试配置
SELECTED_EMBRYOS = ["WT_Sample3"]  # 时间点较少，适合测试
```

## 注意事项
1. **第一次运行**: 建议只选择 1-2 个胚胎进行测试
2. **完整分析**: 可以选择所有 12 个胚胎，但处理时间较长
3. **内存使用**: 每个时间点文件约 1MB，注意内存使用
4. **输出目录**: 结果保存在 `./results/Dataset C/` 目录下

## 文件命名格式
```
{胚胎名称}_{时间点编号}_segCell.nii.gz
例如：WT_Sample1_001_segCell.nii.gz
```
