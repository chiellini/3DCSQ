# 结果导出模板 - 用于胚胎细胞形状分析

# 汇总所有结果
print("=" * 80)
print("分析结果汇总报告")
print("=" * 80)

if analysis_results:
    total_embryos = len(analysis_results)
    total_timepoints = sum([len(info['timepoints']) for info in analysis_results.values()])
    total_cells = 0
    
    print(f"\n数据集：{SELECTED_DATASET}")
    print(f"分析的胚胎数量：{total_embryos}")
    print(f"分析的时间点数量：{total_timepoints}")
    
    # 按胚胎显示统计信息
    print("\n" + "-" * 80)
    print("胚胎详细统计")
    print("-" * 80)
    
    summary_data = []
    
    for embryo_name, embryo_data in analysis_results.items():
        print(f"\n胚胎：{embryo_name}")
        print(f"  数据集：{embryo_data['dataset']}")
        print(f"  时间点数量：{len(embryo_data['timepoints'])}")
        
        # 汇总该胚胎的所有时间点数据
        all_stats_dfs = embryo_data['stats']
        if all_stats_dfs:
            combined_stats = pd.concat(all_stats_dfs, ignore_index=True)
            
            num_cells = len(combined_stats)
            total_cells += num_cells
            
            print(f"  细胞总数：{num_cells}")
            print(f"  平均体积：{combined_stats['Volume'].mean():.1f} ± {combined_stats['Volume'].std():.1f} 体素")
            print(f"  平均表面积：{combined_stats['Surface'].mean():.1f} ± {combined_stats['Surface'].std():.1f} 体素")
            print(f"  平均广义球度：{combined_stats['General_Sphericity'].mean():.4f} ± {combined_stats['General_Sphericity'].std():.4f}")
            print(f"  平均 Hayakawa 圆度：{combined_stats['Hayakawa_Roundness'].mean():.4f} ± {combined_stats['Hayakawa_Roundness'].std():.4f}")
            print(f"  平均铺展指数：{combined_stats['Spreading_Index'].mean():.4f} ± {combined_stats['Spreading_Index'].std():.4f}")
            print(f"  平均直径：{combined_stats['Diameter'].mean():.2f} ± {combined_stats['Diameter'].std():.2f} μm")
            
            # 保存汇总统计
            embryo_summary_file = OUTPUT_PATH / SELECTED_DATASET / embryo_name / f'{embryo_name}_summary.csv'
            combined_stats.to_csv(embryo_summary_file, index=False)
            
            # 添加到汇总数据
            summary_data.append({
                'Dataset': embryo_data['dataset'],
                'Embryo': embryo_name,
                'Num_Timepoints': len(embryo_data['timepoints']),
                'Num_Cells': num_cells,
                'Mean_Volume': combined_stats['Volume'].mean(),
                'Std_Volume': combined_stats['Volume'].std(),
                'Mean_Surface': combined_stats['Surface'].mean(),
                'Std_Surface': combined_stats['Surface'].std(),
                'Mean_Sphericity': combined_stats['General_Sphericity'].mean(),
                'Std_Sphericity': combined_stats['General_Sphericity'].std(),
                'Mean_Roundness': combined_stats['Hayakawa_Roundness'].mean(),
                'Std_Roundness': combined_stats['Hayakawa_Roundness'].std(),
                'Mean_Spreading': combined_stats['Spreading_Index'].mean(),
                'Std_Spreading': combined_stats['Spreading_Index'].std(),
                'Mean_Diameter': combined_stats['Diameter'].mean(),
                'Std_Diameter': combined_stats['Diameter'].std()
            })
    
    # 创建总体汇总表格
    print("\n" + "=" * 80)
    print("总体统计")
    print("=" * 80)
    print(f"总胚胎数：{total_embryos}")
    print(f"总时间点数：{total_timepoints}")
    print(f"总细胞数：{total_cells}")
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        
        # 保存总体汇总
        overall_summary_file = OUTPUT_PATH / SELECTED_DATASET / f'{SELECTED_DATASET}_overall_summary.csv'
        summary_df.to_csv(overall_summary_file, index=False)
        
        print(f"\n✓ 总体汇总已保存到：{overall_summary_file}")
        
        # 显示汇总表格
        print("\n汇总表格预览:")
        display(summary_df)
    
    # 输出目录结构
    print("\n" + "=" * 80)
    print("输出文件目录结构")
    print("=" * 80)
    print(f"""
{OUTPUT_PATH}/
└── {SELECTED_DATASET}/
    ├── {SELECTED_DATASET}_overall_summary.csv  (总体汇总)
    ├── Sample04LabelUnified/
    │   ├── Sample04LabelUnified_summary.csv  (胚胎汇总)
    │   ├── tp001_volume_surface_stats.csv
    │   ├── tp001_shape_descriptors.csv
    │   └── visualizations/
    │       ├── tp001_shape_descriptors_distribution.png
    │       └── tp001_shape_descriptors_correlation.png
    ├── Sample05LabelUnified/
    │   └── ...
    └── Sample06LabelUnified/
        └── ...
    """)
    
    print("\n" + "=" * 80)
    print(f"✓ 所有结果已保存到：{OUTPUT_PATH / SELECTED_DATASET}")
    print("=" * 80)
    
else:
    print("\n⚠️  没有分析结果可导出")
    print("请先运行前面的分析单元格")
