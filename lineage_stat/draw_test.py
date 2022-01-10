# import dependency package
import glob
import pickle as pkl
import pandas as pd

from treelib import Node, Tree

import os
import numpy as np
import re
import sys

# import user package
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import lineage_stat.data_structure as data_struct
from lineage_stat.lineage_tree import draw_life_span_tree
from utils.general_func import read_csv_to_df

# ---------------------------------------------------------------------------------
# ##for all, how to combine 20 embryos to one lineage tree pic? a big problem!#####
# ---------------------------------------------------------------------------------

data_path = r'D:/cell_shape_quantification/DATA/'


def draw_PCA(embryo_name, embryo_time_tree, print_num=4):
    # ==================drawing for PCA; multiple lineage tree pictures for one embryo========================
    pca_num = 12

    # ----------------read SHcPCA result first--------------------------------
    path_SHcPCA_csv = os.path.join(data_path + r'my_data_csv/norm_SH_PCA_csv',
                                   embryo_name + '_SHcPCA{}_norm.csv'.format(pca_num))
    df_SHcPCA_target = read_csv_to_df(path_SHcPCA_csv)
    # print('finished read the SHcPCA----->>', path_SHcPCA_csv)
    # ----------------------------------------------------------------------------

    from matplotlib.colors import ListedColormap, LinearSegmentedColormap
    # https: // www.webucator.com / article / python - color - constants - module /
    # colors = ['red4', 'red3', 'red2', 'red1', 'orangered1', 'orange', 'yellow2','yellow1','yellow2', 'lightblue1',lightblue', 'dodgerblue1',
    #           'dodgerblue2', 'dodgerblue3', 'dodgerblue4']

    # colors = np.array(
    #     [(139, 0, 0), (205, 0, 0), (238, 0, 0), (255, 0, 0), (255, 69, 0), (255, 128, 0),
    #      (238, 238, 0), (255, 255, 0), (238, 238, 0),
    #      (89, 210, 255), (63, 180, 255), (30, 144, 255), (28, 134, 238), (24, 116, 205), (16, 78, 139)]) / 255
    # colors2 = ['red4', 'red3', 'red2', 'red1', 'orangered1', 'orange', 'darkolivegreen3','darkolivegreen2','darkolivegreen3', 'lightblue1',lightblue', 'dodgerblue1',
    #           'dodgerblue2', 'dodgerblue3', 'dodgerblue4']
    colors2 = np.array(
        [(139, 0, 0), (205, 0, 0), (238, 0, 0), (255, 0, 0), (255, 69, 0), (255, 128, 0),
         (162,205,90), (188,238,104), (162,205,90),
         (89, 210, 255), (63, 180, 255), (30, 144, 255), (28, 134, 238), (24, 116, 205), (16, 78, 139)]) / 255
    cmap_list = ListedColormap(colors2)
    cmap1 = LinearSegmentedColormap.from_list("mycmap", colors2)

    for i_PCA in range(print_num):
        # print(pd.Series(index=df_SHcPCA_target.index, data=df_SHcPCA_target[str(i_PCA)]).to_dict().keys())
        draw_life_span_tree(embryo_time_tree, values_dict=pd.Series(index=df_SHcPCA_target.index,
                                                                    data=df_SHcPCA_target[str(i_PCA)]).to_dict(),
                            embryo_name=embryo_name,
                            plot_title='PCA_' + str(i_PCA), color_map=cmap1)
    # =================================================================================================


def draw_PCA_combined(print_num=2):
    # ==================drawing for PCA; multiple lineage tree pictures for one embryo========================
    pca_num = 12

    embryo_names = [str(i).zfill(2) for i in range(4, 21)]
    norm_shcpca_csv_path = data_path + r'my_data_csv/norm_SH_PCA_csv'
    df_pd_values_dict = {}
    # ----------------read SHcPCA result first--------------------------------
    for embryo_name in embryo_names:
        path_SHcPCA_csv = os.path.join(norm_shcpca_csv_path,
                                       'Sample' + embryo_name + 'LabelUnified_SHcPCA' + str(pca_num) + '_norm.csv')
        df_pd_values_dict[embryo_name] = read_csv_to_df(path_SHcPCA_csv)
    # ----------------------------------------------------------------------------

    cell_combine_tree, begin_frame = data_struct.get_combined_lineage_tree()

    # frame = time / 1.39 +begin_frame
    column = str(0)
    values_dict = {}
    for node_id in cell_combine_tree.expand_tree(sorting=False):
        for time_int in cell_combine_tree.get_node(node_id).data.get_time():
            # if time_int > 0:
            tp_value_list = []
            for embryo_name in df_pd_values_dict.keys():
                frame_int = int(time_int / 1.39 + begin_frame[embryo_name])
                frame_and_cell_index = f'{frame_int:03}' + '::' + node_id
                if frame_and_cell_index in df_pd_values_dict[embryo_name].index:
                    # print(frame_and_cell_index,df_pd_values_dict[embryo_name].loc[frame_and_cell_index][column])
                    tp_value_list.append(df_pd_values_dict[embryo_name].at[frame_and_cell_index, column])
            # we have already got all values at this time from all(17) embryos, we just need to draw its average
            tp_and_cell_index = f'{time_int:03}' + '::' + node_id

            if len(tp_value_list) == 0: # need to do interpolation
                print(tp_and_cell_index, tp_value_list)
            values_dict[tp_and_cell_index] = np.average(tp_value_list)

    from matplotlib.colors import ListedColormap, LinearSegmentedColormap
    # https: // www.webucator.com / article / python - color - constants - module /
    # colors2 = ['red4', 'red3', 'red2', 'red1', 'orangered1', 'orange', 'darkolivegreen2','darkolivegreen1','darkolivegreen2', 'lightblue1',lightblue', 'dodgerblue1',
    #           'dodgerblue2', 'dodgerblue3', 'dodgerblue4']
    colors2 = np.array(
        [(139, 0, 0), (205, 0, 0), (238, 0, 0), (255, 0, 0), (255, 69, 0), (255, 128, 0),
         (188,238,104)	, (202,255,112), (188,238,104)	,
         (89, 210, 255), (63, 180, 255), (30, 144, 255), (28, 134, 238), (24, 116, 205), (16, 78, 139)]) / 255

    # cmap_list = ListedColormap(colors)
    cmap1 = LinearSegmentedColormap.from_list("mycmap", colors2)
    draw_life_span_tree(cell_combine_tree, values_dict=values_dict,
                        embryo_name='combine_tree',
                        plot_title='PCA_' + column, color_map=cmap1)


def draw_tree_test():
    for embryo_index in np.arange(start=4, stop=21, step=1):
        # if embryo_index == 7:
        # path_tmp = r'./DATA/SegmentCellUnified04-20/Sample' + f'{cell_index:02}' + 'LabelUnified'
        # print(path_tmp)
        # ===========================draw lineage for one embryo=======================================================

        embryo_num = f'{embryo_index:02}'
        embryo_name = 'Sample{}LabelUnified'.format(embryo_num)
        print(embryo_name)

        # --------------read the tree with node and time list in data -----------------
        tmp_path = r'lineage_tree/LifeSpan/Sample{}_cell_life_tree'.format(embryo_num)
        with open(tmp_path, 'rb') as f:
            # print(f)
            cell_life_tree = Tree(pkl.load(f))

        # cell_life_tree.show(key=False)
        max_time = 150

        # ----------------------------------------------------------------------------

        draw_PCA(embryo_name, cell_life_tree, print_num=2)
        # draw_SHCPCA_KMEANS(embryo_name, embryo_time_tree, id_root_tmp)
        #
        # draw_euclidean_tree(embryo_name, embryo_time_tree, id_root_tmp)
        # draw_norm_spectrum_Kmeans(embryo_name, embryo_time_tree, id_root_tmp)


if __name__ == "__main__":
    draw_PCA_combined()
    # draw_tree_test()
    # data_struct.get_combined_lineage_tree()