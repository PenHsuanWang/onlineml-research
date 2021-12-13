from river import ensemble
from sklearn.ensemble import RandomForestClassifier
from tools.data_loader import TimeSeriesDataLoader
from tqdm import tqdm

import math
import pickle
from os import path

# preparing data
DATA_HOME_PATH = "data/highway_etc_traffic/eda_data/"

DATA_YEAR_MONTH_LIST = [
    '2019_01', '2019_02', '2019_03', '2019_04', '2019_05', '2019_06', #0~6
    '2019_07', '2019_08', '2019_09', '2019_10', '2019_11', '2019_12', #6~12
    '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', #12~18
    '2020_07', '2020_08', '2020_09', '2020_10', '2020_11', '2020_12', #18~24
    '2021_01', '2021_02', '2021_03', '2021_04', '2021_05', '2021_06', #24~30
    '2021_07', '2021_08', '2021_09', '2021_10', '2021_11', '2021_12'  #30~26
]


#=============================================================#
# Defination of functions for following data processing steps #
#=============================================================#
def combine_data_path(year_month) -> str:
    return DATA_HOME_PATH + "highway_traffic_eda_data_ready_for_ml_" + year_month + '.csv'


def preparation_data_for_test(data_path) -> TimeSeriesDataLoader:
    data_loader = TimeSeriesDataLoader(
        data_path,
        time_series_column_name="DateTime", time_format="%yyyy-%mm-%dd %HH:%MM:%SS"
    )
    data_loader.drop_feature("TrafficJam")
    data_loader.drop_feature("TrafficJam30MinLater")
    data_loader.drop_feature("MeanSpeed")
    data_loader.drop_feature("MeanSpeed10MinAgo")
    data_loader.drop_feature("MeanSpeed30MinAgo")
    data_loader.drop_feature("MeanSpeed60MinAgo")
    data_loader.drop_feature("Upstream1MeanSpeed")
    data_loader.drop_feature("Upstream2MeanSpeed")
    data_loader.drop_feature("Upstream3MeanSpeed")
    data_loader.drop_feature("Downstream1MeanSpeed")
    data_loader.drop_feature("Downstream2MeanSpeed")
    data_loader.drop_feature("Downstream3MeanSpeed")
    
    full_data = data_loader.get_full_df()

    X = full_data
    y = X.pop("TrafficJam60MinLater")
    X.drop(["DateTime"], axis=1, inplace=True)
    
    return X, y

def prepare_dataloader_for_test(data_path) -> TimeSeriesDataLoader:
    data_loader = TimeSeriesDataLoader(
        data_path,
        time_series_column_name="DateTime", time_format="%yyyy-%mm-%dd %HH:%MM:%SS"
    )
    data_loader.drop_feature("TrafficJam")
    data_loader.drop_feature("TrafficJam30MinLater")
    data_loader.drop_feature("MeanSpeed")
    data_loader.drop_feature("MeanSpeed10MinAgo")
    data_loader.drop_feature("MeanSpeed30MinAgo")
    data_loader.drop_feature("MeanSpeed60MinAgo")
    data_loader.drop_feature("Upstream1MeanSpeed")
    data_loader.drop_feature("Upstream2MeanSpeed")
    data_loader.drop_feature("Upstream3MeanSpeed")
    data_loader.drop_feature("Downstream1MeanSpeed")
    data_loader.drop_feature("Downstream2MeanSpeed")
    data_loader.drop_feature("Downstream3MeanSpeed")
    
    return data_loader
    
#=================================#
# End of methods defination parts #
#=================================#

#----------------------------------------------------------#
# Start of Online ML Time Series Training/Testing workflow #
#----------------------------------------------------------#

MODEL_SAVE_FILE = './model_store/sklearn/rfc/sklearn_rfc_etc_data_2020_10_10days.pickle'
# MODEL_SAVE_FILE = './model_store/river/adarf/river_adarf_etc_data_2020_10.pickle'
if path.isfile(MODEL_SAVE_FILE):
    
    print("persist model file {} is found ! loaded model from file, going to do prediction".format(MODEL_SAVE_FILE))
    with open(MODEL_SAVE_FILE, 'rb') as f:
        model = pickle.load(f)
        
else:
    print("persist model file {} not found! create and doing training process!".format(MODEL_SAVE_FILE))

    #======================#
    # Model initialization #
    #======================#
    model = RandomForestClassifier(
        n_estimators=500,
        criterion="gini",
        max_depth=30,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    # model = ensemble.AdaptiveRandomForestClassifier(
    #     n_models=500,
    #     max_depth=30,
    #     split_criterion='gini',
    #     grace_period = 2000
    # )

    datapaths_training = list(map(lambda x : combine_data_path(DATA_YEAR_MONTH_LIST[x]), range(21, 22)))
    
    # X, y = preparation_data_for_test(datapaths_training)
    # model.fit(X, y)
    
    
    data_loader_incremental_training = prepare_dataloader_for_test(datapaths_training)
    
    sub_df_by_date = data_loader_incremental_training.sub_df_by_time_interval('2020-10-01', '2020-10-10')
    
    X = sub_df_by_date
    y = X.pop("TrafficJam60MinLater")
    X.drop(["DateTime"], axis=1, inplace=True)
    
    model.fit(X, y)
    
    #========================#
    # Splitting data by date #
    #========================#
    # for i_date in data_loader_incremental_training.get_distinct_date_set_list():
    #     print('going to running date: {}'.format(i_date))
    #     sub_df_by_date = data_loader_incremental_training.get_sub_df_by_date(i_date)
    #     X = sub_df_by_date
    #     y = X.pop("TrafficJam60MinLater")
    #     X.drop(["DateTime"], axis=1, inplace=True)
        
    #     for index, raw in tqdm(X.iterrows(), total=X.shape[0]):
    #         try:
    #             model.learn_one(raw, y[index])
    #         except:
    #             print("error happen")

    #     with open(MODEL_SAVE_FILE, 'wb') as f:
    #         pickle.dump(model, f)
    
    #=======================#
    # End of Training Model #
    #=======================#
    
    
#====================================#
# End of Model Training/Preparation, #
# Going to do model validation.      #
#====================================#

datapaths_testing = list(map(lambda x : combine_data_path(DATA_YEAR_MONTH_LIST[x]), range(22, 23)))


# X_test, y_test = preparation_data_for_test(datapaths_testing)
# pred_proba_result = model.predict_proba(X_test)

# pred_proba_result_true_class = pred_proba_result[y_test == 1][:, 1]
# pred_proba_result_false_class = pred_proba_result[y_test == 0][:, 1]

# #====================================#
# # Visualization of model performance #
# #====================================#
# from tools.model_perform_visualization import PredictionProbabilityDist

# draw_pred_proba = PredictionProbabilityDist(pred_proba_result, y_test)

# draw_pred_proba.draw_proba_dist_by_true_false_class_seperated()
# draw_pred_proba.show_plt()
# draw_pred_proba.save_fig("output_plot/highway_pred_proba_distribution_test.pdf")


#================================#
# Drawing acc trend plot by date #
#================================#
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

data_loader_for_test = prepare_dataloader_for_test(datapaths_testing)

num_target_list = []
acc_trend_list = []
recall_trend_list = []
recall_uncertainty_list = []
f_1_score_list = []

for i_date in data_loader_for_test.get_distinct_date_set_list():
    sub_df_by_date = data_loader_for_test.get_sub_df_by_date(i_date)
    X_test = sub_df_by_date
    y_test = X_test.pop("TrafficJam60MinLater")
    X_test.drop(["DateTime"], axis=1, inplace=True)
    
    pred_proba_result = model.predict_proba(X_test)
    
    pred_proba_casting_binary = list(map(lambda x : 0 if x < 0.4 else 1, pred_proba_result[:, 1]))
    
    num_target = y_test.tolist().count(1)
    
    acc = accuracy_score(y_test, pred_proba_casting_binary)
    recall = recall_score(y_test, pred_proba_casting_binary)
    recall_uncertainty = math.sqrt((recall)*(1-recall)/num_target)
    f_1_score = f1_score(y_test, pred_proba_casting_binary, average='weighted')

    print("accuracy: {}%".format(acc*100))
    print("recall rate: {}%".format(recall*100))
    print("f1 score: {}".format(f_1_score))
    
    num_target_list.append(num_target)
    acc_trend_list.append(acc*100)
    recall_trend_list.append(recall*100)
    recall_uncertainty_list.append(recall_uncertainty*100)
    f_1_score_list.append(f_1_score*100)


from tools.model_perform_visualization import TrendPlot

x_list = data_loader_for_test.get_distinct_date_set_list()

trend_plot = TrendPlot(figsize_x=14, figsize_y=4, is_time_series=True)
trend_plot.plot_trend(x_list, acc_trend_list,  label="accuracy")
trend_plot.plot_trend_with_error_bar(x_list, recall_trend_list, yerr=recall_uncertainty_list, markersize=4, capsize=2, label="recall rate")
# trend_plot.plot_bar(x_list, num_target_list)
trend_plot.save_fig(title="Acc Trend Plot", save_fig_path='output_plot/trend_test.pdf')
