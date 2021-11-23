from pickle import dump, load
from re import match, search

from scipy.ndimage import generate_binary_structure, grey_dilation

import config
import numpy as np
import os
import pandas as pd

from sklearn.cluster import KMeans

from time import time

import pyshtools as pysh
import matplotlib.pyplot as plt
import dict as dict

from tqdm import tqdm

from scipy import spatial

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from matplotlib import cm
import matplotlib.patches

from datetime import datetime

from matplotlib.font_manager import FontProperties

from transformation.PCA import calculate_PCA_zk_norm
from transformation.SH_represention import get_nib_embryo_membrane_dict, get_SH_coeffient_from_surface_points
from utils.cell_func import get_cell_name_affine_table
from utils.draw_func import draw_3D_points, Arrow3D, set_size
from utils.general_func import read_csv_to_df, load_nitf2_img
from utils.sh_cooperation import collapse_flatten_clim, do_reconstruction_for_SH
from itertools import combinations

"""
Sample06,ABalaapa,078
"""


def show_cell_SPCSMs_info():
    # Sample06,ABalaapa,078
    # Sample06,Dpaap,158
    print('waiting type you input')
    embryo_name, cell_name, tp = str(input()).split(',')
    # cell_name = str(input())
    # tp = str(input())

    print(embryo_name, cell_name, tp)

    embryo_path_csv = os.path.join(r'.\DATA\my_data_csv\SH_time_domain_csv',
                                   embryo_name + 'LabelUnified_l_25_norm.csv')
    embryo_csv = read_csv_to_df(embryo_path_csv)

    # fig_points = plt.figure()
    fig_SPCSMs_info = plt.figure()
    plt.axis('off')

    embryo_path_name = embryo_name + 'LabelUnified'
    embryo_path = os.path.join(r'.\DATA\SegmentCellUnified04-20', embryo_path_name)
    file_name = embryo_name + '_' + tp + '_segCell.nii.gz'
    dict_cell_membrane, dict_center_points = get_nib_embryo_membrane_dict(embryo_path,
                                                                          file_name)
    _, cell_num = get_cell_name_affine_table()
    keys_tmp = cell_num[cell_name]

    local_surface_points = dict_cell_membrane[keys_tmp] - dict_center_points[keys_tmp]
    axes_tmp = fig_SPCSMs_info.add_subplot(2, 3, 1, projection='3d')
    draw_3D_points(local_surface_points, ax=axes_tmp, fig_name='original ' + cell_name + '::' + tp)

    instance_tmp = pysh.SHCoeffs.from_array(collapse_flatten_clim(embryo_csv.loc[tp + '::' + cell_name]))
    axes_tmp = fig_SPCSMs_info.add_subplot(2, 3, 2, projection='3d')

    draw_3D_points(do_reconstruction_for_SH(sample_N=50, sh_coefficient_instance=instance_tmp),
                   ax=axes_tmp, fig_name=cell_name + '::' + tp, cmap='viridis')

    sn = 20
    x_axis = Arrow3D([0, sn + 3], [0, 0],
                     [0, 0], mutation_scale=20,
                     lw=3, arrowstyle="-|>", color="r")
    axes_tmp.add_artist(x_axis)
    y_axis = Arrow3D([0, 0], [0, sn + 3],
                     [0, 0], mutation_scale=20,
                     lw=3, arrowstyle="-|>", color="r")
    axes_tmp.add_artist(y_axis)
    z_axis = Arrow3D([0, 0], [0, 0],
                     [0, sn + 23], mutation_scale=20,
                     lw=3, arrowstyle="-|>", color="r")
    axes_tmp.add_artist(z_axis)

    axis_points_num = 1000
    lineage_ = np.arange(0, sn, sn / axis_points_num)
    zeros_ = np.zeros(axis_points_num)
    # xz=np.zeros(axis_points_num)
    axes_tmp.scatter3D(lineage_, zeros_, zeros_, s=10, color='r')
    axes_tmp.scatter3D(zeros_, lineage_, zeros_, s=10, color='r')
    sn = sn + 15
    lineage_ = np.arange(0, sn, sn / axis_points_num)
    zeros_ = np.zeros(axis_points_num)
    axes_tmp.scatter3D(zeros_, zeros_, lineage_, s=10, color='r')
    axes_tmp.axis('off')

    # lineage_ = np.arange(-sn, 0, sn / axis_points_num)
    # zeros_ = np.zeros(axis_points_num)
    # axes_tmp.scatter3D(zeros_, zeros_, lineage_, s=10, color='r')

    axes_tmp.text(sn / 3 * 2, 0, -.2 * sn, 'x', 'x', ha='center')
    axes_tmp.text(0, sn / 3 * 2, -.2 * sn, 'y', 'y', ha='center')
    axes_tmp.text(-0.1 * sn, 0, sn / 3 * 2, 'z', 'z', ha='center')

    # Sample06,ABalaapa,078
    # Sample06,P1,001
    axes_tmp = fig_SPCSMs_info.add_subplot(2, 3, 3)
    grid_tmp = instance_tmp.expand(lmax=50)
    # axin=inset_axes(axes_tmp, width="50%", height="100%", loc=2)
    grid_tmp.plot(ax=axes_tmp, cmap='RdBu', cmap_reverse=True, title='Heat Map',
                  xlabel='Longitude (from positive half x-axis)',
                  ylabel='Latitude (from horizontal x-y plane)')

    axes_tmp = fig_SPCSMs_info.add_subplot(2, 3, 4)
    instance_tmp.plot_spectrum(ax=axes_tmp, fname=cell_name + '::' + tp + ' spectrum curve')
    axes_tmp.set_title(cell_name + '::' + tp + ' spectrum curve')

    axes_tmp = fig_SPCSMs_info.add_subplot(2, 3, 5)
    instance_tmp.plot_spectrum2d(ax=axes_tmp, fname=cell_name + '::' + tp + ' 2D spectra')
    axes_tmp.set_title(cell_name + '::' + tp + ' 2D spectra')

    print(instance_tmp.spectrum())
    # axes_tmp = fig_SPCSMs_info.add_subplot(2, 3, 4)
    #
    # axes_tmp = fig_SPCSMs_info.add_subplot(2, 3, 5)
    #
    # axes_tmp = fig_SPCSMs_info.add_subplot(2, 3, 6)
    # axes_tmp.set_title('volume: '+str(instance_tmp.volume()) + '  ' + 'centroid: '+str(instance_tmp.centroid()))
    axes_tmp = fig_SPCSMs_info.add_subplot(2, 3, 6, projection='3d')
    grid_tmp.plot3d(cmap='RdBu', cmap_reverse=True,
                    ax=axes_tmp)

    plt.show()


def calculate_spectrum():
    print('waiting input ============>')
    # Sample06,ABalaapa,078,ABalaapa,079
    embryo_name, cell_name1, tp1, cell_name2, tp2 = str(input()).split(',')
    embryo_path = os.path.join(r'D:\cell_shape_quantification\DATA\my_data_csv\SH_time_domain_csv',
                               embryo_name + 'LabelUnified_l_25_norm.csv')
    embryo_csv = read_csv_to_df(embryo_path)

    # # fig_points = plt.figure()
    # fig_SPCSMs_info = plt.figure()
    # plt.axis('off')

    instance_tmp1 = pysh.SHCoeffs.from_array(collapse_flatten_clim(embryo_csv.loc[tp1 + '::' + cell_name1]))
    instance_tmp2 = pysh.SHCoeffs.from_array(collapse_flatten_clim(embryo_csv.loc[tp2 + '::' + cell_name2]))

    # log_spectrum1 = np.log(instance_tmp1.spectrum())
    # log_spectrum2 = np.log(instance_tmp2.spectrum())
    # print('eclidean log',spatial.distance.euclidean(log_spectrum1, log_spectrum2))
    # print('cosine log',spatial.distance.cosine(log_spectrum1, log_spectrum2))

    print('euclidean', spatial.distance.euclidean(instance_tmp1.spectrum(), instance_tmp2.spectrum()))
    # print(instance_tmp1.spectrum(), instance_tmp2.spectrum())

    print('cosine', spatial.distance.cosine(instance_tmp1.spectrum(), instance_tmp2.spectrum()))

    # print('mahalanobis',spatial.distance.mahalanobis(instance_tmp1.spectrum(), instance_tmp2.spectrum()))

    print('correlation', spatial.distance.correlation(instance_tmp1.spectrum(), instance_tmp2.spectrum()))


# transfer 2d spectrum to spectrum (1-d curve adding together)
def transfer_2d_to_spectrum():
    path_original = os.path.join('D:/cell_shape_quantification/DATA/my_data_csv/SH_time_domain_csv', 'SHc.csv')
    path_norm = os.path.join('D:/cell_shape_quantification/DATA/my_data_csv/SH_time_domain_csv', 'SHc_norm.csv')

    saving_original_csv = pd.DataFrame(columns=np.arange(start=0, stop=26, step=1))
    df_csv = read_csv_to_df(path_original)
    for row_idx in df_csv.index:
        saving_original_csv.loc[row_idx] = pysh.SHCoeffs.from_array(
            collapse_flatten_clim(df_csv.loc[row_idx])).spectrum()
        # print(num_idx)
        # print(saving_original_csv)
    print(saving_original_csv)
    saving_original_csv.to_csv(
        os.path.join('D:/cell_shape_quantification/DATA/my_data_csv/SH_time_domain_csv', 'SHc_Spectrum.csv'))

    saving_norm_csv = pd.DataFrame(columns=np.arange(start=0, stop=26, step=1))
    df_csv = read_csv_to_df(path_norm)
    for row_idx in df_csv.index:
        saving_norm_csv.loc[row_idx] = pysh.SHCoeffs.from_array(
            collapse_flatten_clim(df_csv.loc[row_idx])).spectrum()
        # print(num_idx)
        # print(saving_original_csv)
    saving_norm_csv.to_csv(
        os.path.join('D:/cell_shape_quantification/DATA/my_data_csv/SH_time_domain_csv', 'SHc_norm_Spectrum.csv'))
    print(saving_norm_csv)


def cluster_with_spectrum():
    # Neuron, Pharynx, Intestine, Skin, Muscle, Germcell, death, unspecifed
    cluster_num = 6
    estimator = KMeans(n_clusters=cluster_num, max_iter=10000)
    path_original = os.path.join('D:/cell_shape_quantification/DATA/my_data_csv/SH_time_domain_csv',
                                 'SHc_norm_Spectrum.csv')
    concat_df_Spectrum = read_csv_to_df(path_original)
    result_origin = estimator.fit_predict(np.power(concat_df_Spectrum.values, 1 / 2))
    print(estimator.cluster_centers_)
    df_kmeans_clustering = pd.DataFrame(index=concat_df_Spectrum.index, columns=['cluster_num'])
    df_kmeans_clustering['cluster_num'] = result_origin
    df_kmeans_clustering.to_csv(
        os.path.join(config.dir_my_data_SH_clustering_csv,
                     'normsqrt_spectrum_cluster_k{}.csv'.format(cluster_num)))


def build_label_supervised_learning():
    cshaper_data_label_df = pd.DataFrame(columns=['Fate'])

    path_original = os.path.join('D:/cell_shape_quantification/DATA/my_data_csv/SH_time_domain_csv',
                                 'SHc_norm_Spectrum.csv')
    concat_df_Spectrum = read_csv_to_df(path_original)

    dfs = pd.read_excel(config.cell_fate_path, sheet_name=None)['CellFate']
    fate_dict = {}
    for idx in dfs.index:
        # print(row)
        name = dfs.loc[idx]['Name'].split('\'')[0]
        fate = dfs.loc[idx]['Fate'].split('\'')[0]
        fate_dict[name] = fate
    print(fate_dict)
    for idx in tqdm(concat_df_Spectrum.index, desc='Dealing with norm spectrum'):
        cell_name = idx.split('::')[2]
        tmp_cell_name = cell_name
        while tmp_cell_name not in fate_dict.keys():
            tmp_cell_name = tmp_cell_name[:-1]
        cshaper_data_label_df.loc[idx] = fate_dict[tmp_cell_name]
    print(cshaper_data_label_df)
    cshaper_data_label_df.to_csv(os.path.join('D:/cell_shape_quantification/DATA/my_data_csv/SH_time_domain_csv',
                                              '17_embryo_fate_label.csv'))
    # print(dfs.loc[dfs['Name'] == 'ABalaaaalpa\'']['Fate'])


def SPCSMs_SVM():
    print('reading dsf')
    t0 = time()
    cshaper_X = read_csv_to_df(
        os.path.join('.\DATA\my_data_csv\SH_time_domain_csv', 'SHc_norm.csv'))
    cshaper_Y = read_csv_to_df(
        os.path.join('.\DATA\my_data_csv\SH_time_domain_csv',
                     '17_embryo_fate_label.csv'))
    X_train, X_test, y_train, y_test = train_test_split(
        cshaper_X.values, cshaper_Y.values.reshape((cshaper_Y.values.shape[0],)), test_size=0.2,
        random_state=datetime.now().microsecond)
    print("reading done in %0.3fs" % (time() - t0))

    print(X_train.shape)
    print(y_train.shape)

    print("Total dataset size:")
    print("n_samples: %d" % cshaper_X.values.shape[0])
    print("n_spectrum: %d" % cshaper_X.values.shape[1])
    print("n_classes: %d" % len(dict.cell_fate_dict))

    # #############################################################################
    # Compute a PCA (eigen shape) on the face dataset (treated as unlabeled
    # dataset): unsupervised feature extraction / dimensionality reduction
    n_components = 48

    print("Extracting the top %d eigenshape from %d cells"
          % (n_components, X_train.shape[0]))
    t0 = time()
    pca = PCA(n_components=n_components, svd_solver='randomized', whiten=True).fit(X_train)
    print("done in %0.3fs" % (time() - t0))

    print("Projecting the input data on the eigenshape orthonormal basis")
    t0 = time()
    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)
    print("done in %0.3fs" % (time() - t0))
    #
    # print(X_train.shape)
    # print(X_train_pca.shape)
    # print(X_test_pca.shape)
    # print(pca.inverse_transform(X_train_pca))

    # #############################################################################
    # Train a SVM classification model

    print("Fitting the classifier to the training set")
    t0 = time()
    # param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
    #               'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
    #
    # param_grid = {'C': [1e4],
    #               'gamma': [0.001], }
    # clf = GridSearchCV(
    #     SVC(kernel='rbf', class_weight='balanced'), param_grid
    # )
    # clf = clf.fit(X_train_pca, y_train)
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto', probability=True))
    #
    # print(y_train.shape)
    #
    # random_indices=np.random.choice(X_train_pca.shape[0],size=100000,replace=False)
    # print(random_indices)
    # X_train_cut=X_train_pca[random_indices,:]
    #
    # print(X_train_cut.shape)
    # print(X_train_pca.shape)
    #
    # y_train_cut=y_train[random_indices]
    #
    #
    # print(y_train.shape)

    clf.fit(X_train_pca, y_train)
    print('test score', clf.score(X_test_pca, y_test))

    print("done in %0.3fs" % (time() - t0))
    print("Best estimator found by grid search:")
    print(clf)

    # #############################################################################
    # Quantitative evaluation of the model quality on the test set

    print("Predicting cell fate on the test set")
    t0 = time()
    y_pred = clf.predict(X_test_pca)
    print("done in %0.3fs" % (time() - t0))

    print(clf.classes_)
    print(classification_report(y_test, y_pred, target_names=dict.cell_fate_dict))
    print(confusion_matrix(y_test, y_pred, labels=dict.cell_fate_dict))

    print("Predicting probability of cell fate on the test set")
    t0 = time()
    clf.predict_proba(X_test_pca).tofile('test_proba.csv', sep=',', format='%10.5f')
    print("done in %0.3fs" % (time() - t0))


def draw_figure_for_science():
    # Sample06,Dpaap,158
    # Sample06,ABalaapa,078
    print('waiting type you input1')
    embryo_name1, cell_name1, tp1 = str(input()).split(',')

    print('waiting type you input2')
    embryo_name, cell_name, tp = str(input()).split(',')
    # cell_name = str(input())
    # tp = str(input())

    print(embryo_name, cell_name, tp)

    embryo_path_csv = os.path.join(r'D:\cell_shape_quantification\DATA\my_data_csv\SH_time_domain_csv',
                                   embryo_name + 'LabelUnified_l_25_norm.csv')
    embryo_csv = read_csv_to_df(embryo_path_csv)

    # plt.rcParams['text.latex.preamble'] = [r"\usepackage{lmodern}"]
    params = {'text.usetex': True,
              }
    plt.rcParams.update(params)
    fig_SPCSMs_info = plt.figure()

    axes_tmp1 = fig_SPCSMs_info.add_subplot(2, 2, 1, projection='3d')
    instance_tmp1 = pysh.SHCoeffs.from_array(
        collapse_flatten_clim(embryo_csv.loc[tp1 + '::' + cell_name1])).expand(lmax=100)
    instance_tmp1_expanded = instance_tmp1.data

    Y2d = np.arange(-90, 90, 180 / 203)
    X2d = np.arange(0, 360, 360 / 405)
    X2d, Y2d = np.meshgrid(X2d, Y2d)

    axes_tmp1.plot_surface(X2d, Y2d, instance_tmp1_expanded, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False, rstride=60, cstride=10)

    axes_tmp2 = fig_SPCSMs_info.add_subplot(2, 2, 2)
    instance_tmp1.plot(ax=axes_tmp2, cmap='RdBu', cmap_reverse=True, title='Heat Map',
                       xlabel='x of X-Y plane',
                       ylabel='y of X-Y plane', axes_labelsize=12, tick_interval=[60, 60])
    set_size(5, 5, ax=axes_tmp2)

    # embryo_path_name = embryo_name + 'LabelUnified'
    # embryo_path = os.path.join('D:/cell_shape_quantification/DATA/SegmentCellUnified04-20', embryo_path_name)
    # file_name = embryo_name + '_' + tp + '_segCell.nii.gz'
    # dict_cell_membrane, dict_center_points = sh_represent.get_nib_embryo_membrane_dict(embryo_path,
    #                                                                                    file_name)
    instance_tmp = pysh.SHCoeffs.from_array(collapse_flatten_clim(embryo_csv.loc[tp + '::' + cell_name]))
    axes_tmp3 = fig_SPCSMs_info.add_subplot(2, 2, 3, projection='3d')
    draw_3D_points(do_reconstruction_for_SH(sample_N=50, sh_coefficient_instance=instance_tmp),
                   ax=axes_tmp3, cmap=cm.coolwarm)
    sn = 20
    x_axis = Arrow3D([0, sn + 3], [0, 0],
                     [0, 0], mutation_scale=20,
                     lw=3, arrowstyle="-|>", color="r")
    axes_tmp3.add_artist(x_axis)
    y_axis = Arrow3D([0, 0], [0, sn + 3],
                     [0, 0], mutation_scale=20,
                     lw=3, arrowstyle="-|>", color="r")
    axes_tmp3.add_artist(y_axis)
    z_axis = Arrow3D([0, 0], [0, 0],
                     [0, sn + 23], mutation_scale=20,
                     lw=3, arrowstyle="-|>", color="r")
    axes_tmp3.add_artist(z_axis)

    axis_points_num = 1000
    lineage_ = np.arange(0, sn, sn / axis_points_num)
    zeros_ = np.zeros(axis_points_num)
    # xz=np.zeros(axis_points_num)
    axes_tmp3.scatter3D(lineage_, zeros_, zeros_, s=10, color='r')
    axes_tmp3.scatter3D(zeros_, lineage_, zeros_, s=10, color='r')
    sn = sn + 15
    lineage_ = np.arange(0, sn, sn / axis_points_num)
    zeros_ = np.zeros(axis_points_num)
    axes_tmp3.scatter3D(zeros_, zeros_, lineage_, s=10, color='r')
    # axes_tmp.axis('off')

    # longitude circle
    x_lon = np.arange(0, 15, 15 / 1000)
    # print(x_lon)
    y_lon = np.sqrt(225 - np.power(x_lon, 2))
    # print(y_lon)
    axes_tmp3.scatter3D(x_lon, y_lon, np.zeros(1000), s=3, color='blue')
    axes_tmp3.text(23, 23, 0, 'longitude', (-1, 1, 0), ha='center')

    # latitude circle
    y_lat = np.arange(0, 15, 15 / 1000)
    z_lat = np.sqrt(225 - np.power(y_lat, 2))
    axes_tmp3.scatter3D(np.zeros(1000), y_lat, z_lat, s=3, color='black')
    axes_tmp3.text(0, 18, 18, 'latitude', (-1, 1, 0), ha='center')

    axes_tmp3.text(sn / 3 * 2, 0, -.2 * sn, 'x', (-1, 1, 0), ha='center').set_fontstyle('italic')
    axes_tmp3.text(0, sn / 3 * 2, -.2 * sn, 'y', (-1, 1, 0), ha='center').set_fontstyle('italic')
    axes_tmp3.text(-0.1 * sn, 0, sn + 10, 'z', (-1, 1, 0), ha='center').set_fontstyle('italic')

    axes_tmp3.text('XXXXXXXX', xy=(0.93, -0.01), ha='left', va='top', xycoords='axes fraction', weight='bold',
                   style='italic')
    # axes_tmp3.annotate('XXXXXXXX', xy=(0.93, -0.01), ha='left', va='top', xycoords='axes fraction', weight='bold', style='italic')

    axes_tmp4 = fig_SPCSMs_info.add_subplot(2, 2, 4)
    grid_tmp = instance_tmp.expand(lmax=100)
    # axin=inset_axes(axes_tmp, width="50%", height="100%", loc=2)
    grid_tmp.plot(ax=axes_tmp4, cmap='RdBu', cmap_reverse=True, title='Heat Map',
                  xlabel='Longitude (X-Y plane)',
                  ylabel='Latitude (Y-Z plane)', axes_labelsize=12, tick_interval=[60, 60])

    fig_SPCSMs_info.text(0, 0.7, '3D Surface Mapping', fontsize=12)
    fig_SPCSMs_info.text(0, 0.25, '3D Object Mapping', fontsize=12)
    # Sample06,Dpaap,158
    # Sample06,ABalaapa,078

    # axes_tmp1.add_patch(
    #     matplotlib.patches.Rectangle((200., -4.), 50., 6., transform=axes_tmp1.transData, alpha=0.3, color="g"))

    arrow = matplotlib.patches.FancyArrowPatch(
        (0.4, 0.7), (0.6, 0.7), transform=fig_SPCSMs_info.transFigure,  # Place arrow in figure coord system
        fc="g", connectionstyle="arc3,rad=0.2", arrowstyle='simple', alpha=0.3,
        mutation_scale=40.
    )
    # 5. Add patch to list of objects to draw onto the figure
    fig_SPCSMs_info.patches.append(arrow)

    arrow = matplotlib.patches.FancyArrowPatch(
        (0.4, 0.3), (0.6, 0.3), transform=fig_SPCSMs_info.transFigure,  # Place arrow in figure coord system
        fc="g", connectionstyle="arc3,rad=0.2", arrowstyle='simple', alpha=0.3,
        mutation_scale=40.
    )
    # 5. Add patch to list of objects to draw onto the figure
    fig_SPCSMs_info.patches.append(arrow)

    plt.show()


def calculate_cell_contact_surface():
    # Sample06,Dpaap,158
    # Sample06,ABalaapa,078
    # print('waiting type you input1')
    # embryo_name1, cell_name1, tp1 = str(input()).split(',')
    #
    # print('waiting type you input2')
    # embryo_name2, cell_name2, tp2 = str(input()).split(',')

    number_cell, cell_number = get_cell_name_affine_table()

    # ------------------------------calculate contact points for each cell ----------------------------------------------
    path_tmp = r'./DATA/SegmentCellUnified04-20/Sample20LabelUnified'
    for file_name in os.listdir(path_tmp):
        if os.path.isfile(os.path.join(path_tmp, file_name)):
            print(path_tmp, file_name)

            this_img = load_nitf2_img(os.path.join(path_tmp, file_name))

            img_arr = this_img.get_data()

            x_num, y_num, z_num = img_arr.shape

            # arr_unique,arr_indices,arr_count=np.unique(img_arr,return_counts=True,return_index=True)
            arr_unique = np.unique(img_arr)
            # print(arr_unique)
            # print(arr_indices)
            # print(arr_count)

            dict_img_cell_calculate = {}
            for x in range(x_num):
                for y in range(y_num):
                    for z in range(z_num):
                        dict_key = img_arr[x][y][z]
                        if dict_key != 0:
                            if dict_key in dict_img_cell_calculate:
                                dict_img_cell_calculate[dict_key].append([x, y, z])
                            else:
                                dict_img_cell_calculate[dict_key] = [[x, y, z]]
            cell_points_dict = {}

            t0 = time()

            for cell_number in arr_unique[1:]:
                print('dealing with ', cell_number, 'dilation things')
                targe_arr = np.array(dict_img_cell_calculate[cell_number])
                # print(dict_img_cell_calculate[cell_number])
                # print(dict_img_cell_calculate[cell_number][:, 0])
                x_min_boundary = np.min(targe_arr[:, 0]) - 1
                x_max_boundary = np.max(targe_arr[:, 0]) + 1

                y_min_boundary = np.min(targe_arr[:, 1]) - 1
                y_max_boundary = np.max(targe_arr[:, 1]) + 1

                z_min_boundary = np.min(targe_arr[:, 2]) - 1
                z_max_boundary = np.max(targe_arr[:, 2]) + 1

                cut_img_arr = img_arr[x_min_boundary:x_max_boundary, y_min_boundary:y_max_boundary,
                              z_min_boundary:z_max_boundary]

                # set all points as zero expect cell_number dealing with
                cut_img_arr = (cut_img_arr == cell_number).astype(int)

                # print(np.unique(cut_img_arr,return_counts=True))
                # with the original image data
                struct_element = generate_binary_structure(3, -1)
                cut_img_arr_dilation = grey_dilation(cut_img_arr, footprint=struct_element)
                # print(np.unique(cut_img_arr_dilation,return_counts=True))

                cut_img_arr_dilation = cut_img_arr_dilation - cut_img_arr
                print(np.unique(cut_img_arr_dilation, return_counts=True))

                point_position_x, point_position_y, point_position_z = np.where(cut_img_arr_dilation == 1)
                cell_points_dict[cell_number] = []
                for i in range(len(point_position_x)):
                    cell_points_dict[cell_number].append(str(point_position_x[i] + x_min_boundary) + '_' + str(
                        point_position_y[i] + y_min_boundary) + '_' + str(point_position_z[i] + z_min_boundary))
                # print(cell_points_dict[cell_number])

            contact_points_dict = {}
            key_list_tmp = combinations(cell_points_dict.keys(), 2)

            for idx in key_list_tmp:
                print(idx, 'cell contact surface points counting')
                y = [x for x in cell_points_dict[idx[0]] if x in cell_points_dict[idx[1]]]
                if len(y) > 0:
                    print(len(y))
                    str_key = str(idx[0]) + '_' + str(idx[1])
                    contact_points_dict[str_key] = y
            # print(contact_points_dict)

            contact_saving_path = r'./DATA/cshaper_contact_data'
            with open(os.path.join(contact_saving_path, file_name.split('.')[0] + '.json'), 'wb') as fp:
                dump(contact_points_dict, fp)

            # load()
            print("done in %0.3fs" % (time() - t0))

            # print(cell_points_dict)

    # -------------------------------------------------------------------------------------------------------


def display_contact_points():
    # Sample20,ABalaaapa,126
    # Sample20,Dpaap,158
    # Sample20,ABalaapa,078

    print('waiting type you input: samplename and timepoints for embryogenesis')
    embryo_name, cell_name, tp = str(input()).split(',')

    # get center points
    embryo_path_name = embryo_name + 'LabelUnified'
    embryo_path = os.path.join(r'.\DATA\SegmentCellUnified04-20', embryo_path_name)
    file_name = embryo_name + '_' + tp + '_segCell.nii.gz'
    _, dict_center_points = get_nib_embryo_membrane_dict(embryo_path, file_name)
    num_cell_name, cell_num = get_cell_name_affine_table()

    this_cell_keys = cell_num[cell_name]

    with open(os.path.join(r'./DATA/cshaper_contact_data', embryo_name + '_' + tp + '_segCell.json'), 'rb') as fp:
        data = load(fp)
    display_key_list = []
    for idx in data.keys():

        if str(this_cell_keys) in idx:
            display_key_list.append(idx)

    fig_contact_info = plt.figure()
    plt.axis('off')
    item_count = 1
    this_cell_center = dict_center_points[this_cell_keys]
    for idx in display_key_list:
        if item_count > 9:
            break
        draw_points_list = []
        print(idx)
        for item_str in data[idx]:
            x, y, z = item_str.split('_')
            x, y, z = int(x), int(y), int(z)
            # print(item_str)
            # print(x, y, z)
            draw_points_list.append([x, y, z])

        a = idx.split('_')
        a.remove(str(this_cell_keys))
        contact_cell_num = int(a[0])
        ax = fig_contact_info.add_subplot(3, 3, item_count, projection='3d')
        draw_3D_points(np.array(draw_points_list), fig_name=cell_name + '_' + num_cell_name[contact_cell_num], ax=ax)

        dfs = pd.read_excel(config.cell_fate_path, sheet_name=None)['CellFate']
        fate_cell = dfs[dfs['Name'] == cell_name + '\'']['Fate'].values[0].split('\'')[0]
        # for idx in dfs.index:
        #     # print(row)
        #     name = dfs.loc[idx]['Name'].split('\'')[0]
        #     fate = dfs.loc[idx]['Fate'].split('\'')[0]
        #     fate_dict[name] = fate

        ax.text(this_cell_center[0], this_cell_center[1], this_cell_center[2], cell_name + '_' + fate_cell,
                (-1, 1, 0), ha='center')

        contact_cell_fate = dfs[dfs['Name'] == num_cell_name[contact_cell_num] + '\'']['Fate'].values[0].split('\'')[0]
        contact_cell_center = dict_center_points[contact_cell_num]
        ax.text(contact_cell_center[0], contact_cell_center[1], contact_cell_center[2],
                num_cell_name[contact_cell_num] + '_' + contact_cell_fate,
                (-1, 1, 0), ha='center')

        #
        # contact_arrow = Arrow3D([0, 0], [0, 0],
        #                  [0, sn + 23], mutation_scale=20,
        #                  lw=3, arrowstyle="-|>", color="r")
        # ax.add_artist(contact_arrow)

        item_count += 1
    plt.show()

def calculate_SH_PCA_coordinate():
    PCA_matrices_saving_path = os.path.join(r'.\DATA\my_data_csv\SH_PCA_coordinate', 'SHc_norm_PCA.csv')

    path_saving_csv_normalized = os.path.join(config.dir_my_data_SH_time_domain_csv, 'SHc_norm.csv')
    df_SHc_norm = read_csv_to_df(path_saving_csv_normalized)
    print('finish read all embryo cell df_sh_norm_coefficients--------------')

    sh_PCA = PCA(n_components=24)
    pd.DataFrame(data=sh_PCA.fit_transform(df_SHc_norm.values),index=df_SHc_norm.index).to_csv(PCA_matrices_saving_path)





if __name__ == "__main__":

    calculate_SH_PCA_coordinate()
    #
    # print('test2 run')
    # print(str(190) in '190_11')
    # display_contact_points()
    # show_cell_SPCSMs_info()
