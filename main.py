# import pyshtools as pysh

import os
import static

import numpy as np

import utils.general_func as general_f


def main():
    print("start cell shape analysis")

    # ------------------------------R fibonacci representation------------------------------------------------
    for cell_index in np.arange(start=4, stop=21, step=1):
        path_tmp = static.data_path + r'Segmentation Results\SegmentedCell/Sample' + f'{cell_index:02}' + 'LabelUnified'
        img_1 = general_f.load_nitf2_img(os.path.join(path_tmp,'Sample{}_068_segCell.nii.gz'.format(f'{cell_index:02}')))
        print('Sample{}_segCell.nii.gz'.format(f'{cell_index:02}'),img_1.get_fdata().shape)
        # print(general_f.load_nitf2_img(os.path.join(static.data_path,r'Segmentation Results\SegmentedCell\Sample04LabelUnified','Sample04_100_segCell.nii.gz')).get_fdata().shape)
    # general_f.show_nitf2_img(os.path.join(static.dir_segemented_tmp1, 'Embryo04_068_segCell.nii.gz'))



    # img_2 = general_f.show_nitf2_img(os.path.join(static.dir_my_data, 'membrane' + 'Embryo04_001_segCell.nii.gz'))
    # R_func.build_R_array_for_embryo(128)
    # ---------------------------------------------------------------------------------------------------------



    # ------------------------------do contraction with sh expand and shc expand------------------------------

    # path_tmp = r'./DATA/Embryo04LabelUnified_C/'
    #
    # SH_func.get_SH_coeffient_from_surface_points(embryo_path=path_tmp, sample_N=100, lmax=49,
    #                                              file_name='Embryo04_009_segCell.nii.gz')
    # p = Process(target=SH_A_func.analysis_calculate_error_contrast,
    #                             args=(path_tmp, 'Embryo04_009_segCell.nii.gz', 'draw_contraction',))
    # p.start()

    # SH_A_func.analysis_compare_SHc(embryo_path=static.dir_segemented_tmp1,
    #                                file_name='Embryo04_009_segCell.nii.gz', behavior='draw_contraction')

    # ---------------------------------------------------------------------------------------------------------

    # # ------------------------------calculate volume and surface of the cells of one embryo ----------------
    # path_tmp = r'./DATA/SegmentCellUnified04-20/Sample20LabelUnified'
    # cell_f.count_volume_surface_normalization_tocsv(path_tmp)
    # # -----------------------------------------------------------------------------------------------------
    # path_tmp = static.dir_segemented_tmp1

    # SH_A_func.analysis_SHcPCA_All_embryo(l_degree=25)

    # path_tmp = r'./DATA/SegmentCellUnified04-20/Sample05LabelUnified'
    # SH_A_func.analysis_SHc_Kmeans_One_embryo(embryo_path=path_tmp, used_degree=9, is_show_cluster=False)



    #
    #
    # SH_A_func.analysis_SHcPCA_One_embryo(embryo_path=path_tmp, l_degree=25, is_show_PCA=True, PCA_num=PCA_NUM)

    # for cell_index in np.arange(start=4, stop=21, step=1):
    #     path_tmp = r'./DATA/SegmentCellUnified04-20/Sample' + f'{cell_index:02}' + 'LabelUnified'
    #     print(path_tmp)
    #     SH_A_func.analysis_SHcPCA_One_embryo(embryo_path=path_tmp, used_degree=9, is_show_PCA=False)
    #     #
    #     # draw_f.draw_comparison_SHcPCA_SH(embryo_path=path_tmp, l_degree=25, cell_name='RANDOM', PCA_num=PCA_NUM)

    # =======we always use l_degree= 25 coefficients are 676 to analyse===============
    # SH_A_func.analysis_SHcPCA_One_embryo(embryo_path=path_tmp, l_degree=25, is_show_PCA=False)

    # ---------------------------draw SHcPCA
    # draw_f.draw_comparison_SHcPCA_SH(embryo_path=path_tmp, l_degree=25, cell_name='RANDOM', used_degree=9,
    #                                  used_PCA_num=18)

    # SH_A_func.analysis_SHcPCA_maximum_clustering(embryo_path=path_tmp, l_degree=25)

    # SH_A_func.analysis_SHcPCA_KMEANS_clustering(embryo_path=path_tmp, l_degree=25)

    # SH_A_func.analysis_SHcPCA_energy_ratio(embryo_path=path_tmp, l_degree=25)


if __name__ == '__main__':
    main()
    # print(__name__)
