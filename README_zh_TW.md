# 3DCSQ: 三維細胞形狀量化分析系統

[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**早期胚胎發育過程中三維細胞形狀量化、視覺化與分析的有效方法**

李澤林*, 曹劍鋒, 關國業*, 唐超, 趙中英, 洪岩

*通訊作者

---

## 目錄

- [簡介](#簡介)
- [摘要](#摘要)
- [功能特色](#功能特色)
- [安裝說明](#安裝說明)
- [快速入門](#快速入門)
- [專案結構](#專案結構)
- [核心函數](#核心函數)
- [科學概念](#科學概念)
- [使用範例](#使用範例)
- [引用](#引用)

---

## 簡介

本儲存庫包含我們關於三維細胞形狀量化研究論文的官方實作。我們開發了三種新穎的形狀特徵來量化細胞形態，並在活的 *秀麗隱桿線蟲 (C. elegans)* 胚胎上進行了全面的實驗和評估。

3DCSQ 方法獨特地結合了：
- **球面網格 (Spherical Grids)** - 用於表面採樣
- **球面諧波 (Spherical Harmonics, SPHARM)** - 用於形狀轉換
- **主成分分析 (PCA)** - 用於降維

這種綜合方法實現了穩健的細胞形狀量化、分析和視覺化。

---

## 摘要

胚胎發育本質上是三維的，當通過三維螢光成像進行量化時面臨重大挑戰。傳統描述符如體積、表面積和平均曲率往往不足，只能提供全局視圖，缺乏局部細節和重建能力。

針對這一問題，我們引入了 **3DCSQ（三維細胞形狀量化）**，一種有效的整合方法，用於將數位化的三維細胞形狀轉換為分析特徵向量。主要能力包括：

- **形狀識別**：識別細胞形態表型
- **細胞聚類**：基於形狀相似性對細胞進行分組
- **模式檢測**：識別生物學上可重現的細胞模式

應用於 *秀麗隱桿線蟲* 胚胎從 4 細胞到 350 細胞階段，3DCSQ 可靠地識別和量化生物學上可重現的細胞模式，包括獨特的皮膚細胞變形。

**關鍵詞**：球面諧波 (SPHARM)、細胞形狀量化、形態可重現性、譜系分析、*秀麗隱桿線蟲*

---

## 功能特色

- ✅ 從分割數據中提取三維細胞表面
- ✅ 用於形狀表示的球面諧波轉換
- ✅ 基於 PCA 的形狀特徵提取
- ✅ 用於細胞形狀分類的 K-means 聚類
- ✅ 細胞譜系樹視覺化
- ✅ 體積和表面積計算
- ✅ 細胞間接觸檢測

---

## 安裝說明

### 系統需求

- Python 3.9+
- Conda（推薦）

### 環境設置

```bash
# 更新 conda
conda update -n base -c defaults conda

# 從 requirements 創建環境
conda env create -f requirements.txt

# 啟動環境
conda activate CellShapeAnalysis
```

### 主要依賴套件

| 套件 | 版本 |
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

## 快速入門

```python
import utils.cell_func as cell_f
import transformation.SH_represention as sh_represent

# 載入分割數據
img = cell_f.nii_get_cell_surface('path/to/segmentation.nii.gz')

# 計算球面諧波係數
sh_coefficient = sh_represent.sample_and_SHc_with_surface(
    surface_points, 
    sample_N=30, 
    lmax=14
)

# 執行 PCA 分析
from analysis.SH_analyses import analysis_SHcPCA_One_embryo
analysis_SHcPCA_One_embryo(embryo_path, used_degree=16, l_degree=25)
```

---

## 專案結構

```
cell_shape_quantification/
├── analysis/                    # 分析模組（第3層）
│   ├── SH_analyses.py          # 球面諧波分析函數
│   └── curvature.py            # 曲率計算
│
├── transformation/              # 特徵轉換（第2層）
│   ├── SH_represention.py      # 球面諧波轉換
│   ├── R_matrix_represention.py # 表面採樣方法
│   └── PCA.py                  # PCA 分析工具
│
├── lineage_stat/               # 譜系分析（第2層）
│   ├── data_structure.py       # 細胞譜系樹構建
│   ├── lineage_tree.py         # 譜系樹視覺化
│   └── generate_life_span.py   # 壽命數據生成
│
├── utils/                      # 工具函數（第1層）
│   ├── cell_func.py           # 細胞操作（體積、表面、接觸）
│   ├── general_func.py        # 座標轉換
│   ├── spherical_func.py      # 球面採樣函數
│   ├── sh_cooperation.py      # SPHARM 陣列工具
│   ├── shape_preprocess.py    # 表面提取
│   └── draw_func.py           # 視覺化工具
│
├── experiment/                 # 實驗腳本（第4層）
│   ├── cluster.py             # 聚類實驗
│   └── geometry.py            # 幾何分析
│
├── static/                     # 配置
│   ├── config.py              # 路徑配置
│   └── dict.py                # 細胞命運字典
│
├── DATA/                       # 數據目錄（不在儲存庫中）
│   └── my_data_csv/           # 輸出 CSV 檔案
│
├── main.py                     # 主程式入口
├── test1.py                    # 核心分析函數
└── requirements.txt            # 依賴項
```

---

## 核心函數

### 球面諧波轉換

```python
# 計算一個胚胎的 SPHARM 係數（3D+T 數據）
test1.py/calculate_SPHARM_embryo_for_cells()
test1.py/SPHARM_eigenharmonic()  # 特徵諧波權重向量
```

### 球面網格表示

```python
# 計算球面網格係數（特徵網格）
test1.py/Map2D_grid_csv()
test1.py/Map_2D_eigengrid()  # 特徵網格權重向量
```

### 表面採樣

```python
# 以間隔採樣細胞表面
transformation/test1.py/do_sampling_with_interval()
```

### 譜系樹

```python
# 繪製細胞命運譜系樹
lineage_stat/draw_test.py -> draw_cell_fate_lineage_tree_01paper()
```

---

## 科學概念

### 細胞曲率

#### 高斯曲率（使用 libigl）

參考文獻：[libigl Python 教程](https://libigl.github.io/libigl-python-bindings/tut-chapter1/)

**主曲率**：表面點處的最大和最小曲率半徑。

- [主曲率（維基百科）](https://zh.wikipedia.org/wiki/主曲率)
- [高斯曲率（維基百科）](https://zh.wikipedia.org/wiki/高斯曲率)

### 座標系統

程式碼使用標準球面座標轉換：

- **笛卡爾座標轉球面座標**：將 (x, y, z) 轉換為 (r, θ, φ)
- **球面座標轉笛卡爾座標**：將 (r, θ, φ) 轉換為 (x, y, z)

參考文獻：[球座標系（維基百科）](https://zh.wikipedia.org/wiki/球座標系)

---

## 使用範例

### 1. 生成譜系樹

```bash
cd lineage_stat
python generate_life_span.py
```

此命令會：
1. 基於 CD 檔案構建樹結構
2. 將細胞幀信息添加到樹中
3. 生成譜系樹檔案

### 2. 繪製平均譜系樹

過程包括：
1. 構建所有胚胎的平均譜系樹
2. 根據時間解析度提取幀細胞值
3. 計算每個時間點的平均值
4. 對缺失細胞進行插值

### 3. 形狀分析流程

```python
# 步驟 1：提取細胞表面
from utils.cell_func import nii_get_cell_surface

# 步驟 2：計算 SPHARM 係數
from transformation.SH_represention import get_SH_coefficient_of_embryo

# 步驟 3：執行 PCA
from analysis.SH_analyses import analysis_SHcPCA_One_embryo

# 步驟 4：聚類
from analysis.SH_analyses import analysis_SHc_Kmeans_One_embryo
```

---

## 數據格式

### 輸入數據
- **分割檔案**：NIfTI 格式（.nii.gz）
- **名稱字典**：CSV 檔案，映射細胞標籤到名稱

### 輸出數據
- **SPHARM 係數**：帶有形狀描述符的 CSV 檔案
- **PCA 結果**：主成分和解釋變異數
- **聚類結果**：細胞聚類分配

---

## 引用

如果您在研究中使用此程式碼，請引用：

```bibtex
@article{3dcsq2024,
  title={3DCSQ: An effective method for quantification, visualization and analysis of 3D cell shape during early embryogenesis},
  author={Li, Zelin and Cao, Jianfeng and Guan, Guoye and Tang, Chao and Zhao, Zhongying and Yan, Hong},
  journal={...},
  year={2024}
}
```

---

## 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

---

## 致謝

- 香港城市大學
- 對 *秀麗隱桿線蟲* 成像和分析做出貢獻的研究團隊

---

## 聯繫方式

如有問題和支援，請聯繫通訊作者。