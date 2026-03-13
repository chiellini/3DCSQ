# 3DCSQ: 三维细胞形状量化分析系统

[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**早期胚胎发育过程中三维细胞形状量化、可视化与分析的有效方法**

李泽林*, 曹剑锋, 关国业*, 唐超, 赵中英, 洪岩

*通讯作者

---

## 目录

- [简介](#简介)
- [摘要](#摘要)
- [功能特色](#功能特色)
- [安装说明](#安装说明)
- [快速入门](#快速入门)
- [项目结构](#项目结构)
- [核心函数](#核心函数)
- [科学概念](#科学概念)
- [使用示例](#使用示例)
- [引用](#引用)

---

## 简介

本仓库包含我们关于三维细胞形状量化研究论文的官方实现。我们开发了三种新颖的形状特征来量化细胞形态，并在活的 *秀丽隐杆线虫 (C. elegans)* 胚胎上进行了全面的实验和评估。

3DCSQ 方法独特地结合了：
- **球面网格 (Spherical Grids)** - 用于表面采样
- **球面谐波 (Spherical Harmonics, SPHARM)** - 用于形状转换
- **主成分分析 (PCA)** - 用于降维

这种综合方法实现了稳健的细胞形状量化、分析和可视化。

---

## 摘要

胚胎发育本质上是三维的，当通过三维荧光成像进行量化时面临重大挑战。传统描述符如体积、表面积和平均曲率往往不足，只能提供全局视图，缺乏局部细节和重建能力。

针对这一问题，我们引入了 **3DCSQ（三维细胞形状量化）**，一种有效的整合方法，用于将数字化的三维细胞形状转换为分析特征向量。主要能力包括：

- **形状识别**：识别细胞形态表型
- **细胞聚类**：基于形状相似性对细胞进行分组
- **模式检测**：识别生物学上可重现的细胞模式

应用于 *秀丽隐杆线虫* 胚胎从 4 细胞到 350 细胞阶段，3DCSQ 可靠地识别和量化生物学上可重现的细胞模式，包括独特的皮肤细胞变形。

**关键词**：球面谐波 (SPHARM)、细胞形状量化、形态可重现性、谱系分析、*秀丽隐杆线虫*

---

## 功能特色

- ✅ 从分割数据中提取三维细胞表面
- ✅ 用于形状表示的球面谐波转换
- ✅ 基于 PCA 的形状特征提取
- ✅ 用于细胞形状分类的 K-means 聚类
- ✅ 细胞谱系树可视化
- ✅ 体积和表面积计算
- ✅ 细胞间接触检测

---

## 安装说明

### 系统要求

- Python 3.9+
- Conda（推荐）

### 环境设置

```bash
# 更新 conda
conda update -n base -c defaults conda

# 从 requirements 创建环境
conda env create -f requirements.txt

# 激活环境
conda activate CellShapeAnalysis
```

### 主要依赖包

| 包 | 版本 |
|---------|---------|
| numpy | ~1.22.4 |
| scipy | ~1.8.1 |
| pandas | ~1.4.2 |
| matplotlib | ~3.5.2 |
| scikit-learn | ~1.1.1 |
| pyshtools | 最新版 |
| open3d | ~0.15.2 |
| nibabel | 最新版 |
| treelib | 最新版 |

---

## 快速入门

```python
import utils.cell_func as cell_f
import transformation.SH_represention as sh_represent

# 加载分割数据
img = cell_f.nii_get_cell_surface('path/to/segmentation.nii.gz')

# 计算球面谐波系数
sh_coefficient = sh_represent.sample_and_SHc_with_surface(
    surface_points, 
    sample_N=30, 
    lmax=14
)

# 执行 PCA 分析
from analysis.SH_analyses import analysis_SHcPCA_One_embryo
analysis_SHcPCA_One_embryo(embryo_path, used_degree=16, l_degree=25)
```

---

## 项目结构

```
cell_shape_quantification/
├── analysis/                    # 分析模块（第3层）
│   ├── SH_analyses.py          # 球面谐波分析函数
│   └── curvature.py            # 曲率计算
│
├── transformation/              # 特征转换（第2层）
│   ├── SH_represention.py      # 球面谐波转换
│   ├── R_matrix_represention.py # 表面采样方法
│   └── PCA.py                  # PCA 分析工具
│
├── lineage_stat/               # 谱系分析（第2层）
│   ├── data_structure.py       # 细胞谱系树构建
│   ├── lineage_tree.py         # 谱系树可视化
│   └── generate_life_span.py   # 寿命数据生成
│
├── utils/                      # 工具函数（第1层）
│   ├── cell_func.py           # 细胞操作（体积、表面、接触）
│   ├── general_func.py        # 坐标转换
│   ├── spherical_func.py      # 球面采样函数
│   ├── sh_cooperation.py      # SPHARM 数组工具
│   ├── shape_preprocess.py    # 表面提取
│   └── draw_func.py           # 可视化工具
│
├── experiment/                 # 实验脚本（第4层）
│   ├── cluster.py             # 聚类实验
│   └── geometry.py            # 几何分析
│
├── static/                     # 配置
│   ├── config.py              # 路径配置
│   └── dict.py                # 细胞命运字典
│
├── DATA/                       # 数据目录（不在仓库中）
│   └── my_data_csv/           # 输出 CSV 文件
│
├── main.py                     # 主程序入口
├── test1.py                    # 核心分析函数
└── requirements.txt            # 依赖项
```

---

## 核心函数

### 球面谐波转换

```python
# 计算一个胚胎的 SPHARM 系数（3D+T 数据）
test1.py/calculate_SPHARM_embryo_for_cells()
test1.py/SPHARM_eigenharmonic()  # 特征谐波权重向量
```

### 球面网格表示

```python
# 计算球面网格系数（特征网格）
test1.py/Map2D_grid_csv()
test1.py/Map_2D_eigengrid()  # 特征网格权重向量
```

### 表面采样

```python
# 以间隔采样细胞表面
transformation/test1.py/do_sampling_with_interval()
```

### 谱系树

```python
# 绘制细胞命运谱系树
lineage_stat/draw_test.py -> draw_cell_fate_lineage_tree_01paper()
```

---

## 科学概念

### 细胞曲率

#### 高斯曲率（使用 libigl）

参考文献：[libigl Python 教程](https://libigl.github.io/libigl-python-bindings/tut-chapter1/)

**主曲率**：表面点处的最大和最小曲率半径。

- [主曲率（维基百科）](https://zh.wikipedia.org/wiki/主曲率)
- [高斯曲率（维基百科）](https://zh.wikipedia.org/wiki/高斯曲率)

### 坐标系统

代码使用标准球面坐标转换：

- **笛卡尔坐标转球面坐标**：将 (x, y, z) 转换为 (r, θ, φ)
- **球面坐标转笛卡尔坐标**：将 (r, θ, φ) 转换为 (x, y, z)

参考文献：[球坐标系（维基百科）](https://zh.wikipedia.org/wiki/球坐标系)

---

## 使用示例

### 1. 生成谱系树

```bash
cd lineage_stat
python generate_life_span.py
```

此命令会：
1. 基于 CD 文件构建树结构
2. 将细胞帧信息添加到树中
3. 生成谱系树文件

### 2. 绘制平均谱系树

过程包括：
1. 构建所有胚胎的平均谱系树
2. 根据时间分辨率提取帧细胞值
3. 计算每个时间点的平均值
4. 对缺失细胞进行插值

### 3. 形状分析流程

```python
# 步骤 1：提取细胞表面
from utils.cell_func import nii_get_cell_surface

# 步骤 2：计算 SPHARM 系数
from transformation.SH_represention import get_SH_coefficient_of_embryo

# 步骤 3：执行 PCA
from analysis.SH_analyses import analysis_SHcPCA_One_embryo

# 步骤 4：聚类
from analysis.SH_analyses import analysis_SHc_Kmeans_One_embryo
```

---

## 数据格式

### 输入数据
- **分割文件**：NIfTI 格式（.nii.gz）
- **名称字典**：CSV 文件，映射细胞标签到名称

### 输出数据
- **SPHARM 系数**：带有形状描述符的 CSV 文件
- **PCA 结果**：主成分和解释方差
- **聚类结果**：细胞聚类分配

---

## 引用

如果您在研究中使用此代码，请引用：

```bibtex
@article{3dcsq2024,
  title={3DCSQ: An effective method for quantification, visualization and analysis of 3D cell shape during early embryogenesis},
  author={Li, Zelin and Cao, Jianfeng and Guan, Guoye and Tang, Chao and Zhao, Zhongying and Yan, Hong},
  journal={...},
  year={2024}
}
```

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 致谢

- 香港城市大学
- 为 *秀丽隐杆线虫* 成像和分析做出贡献的研究团队