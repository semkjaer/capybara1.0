# data imports
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# app imports
import uuid
import streamlit as st
import streamlit_authenticator as stauth
from utils.auth import auth

if 'key' not in st.session_state:
        st.session_state['key'] = str(uuid.uuid4())

authenticator = auth()
name, authentication_status, username = authenticator.login('Login', 'main')

@st.cache_data
def get_data():
    file = pd.ExcelFile('Wijkdata_Jeugdhulp_in_de_wijk.ods')

    sheet_names = file.sheet_names

    wijk = pd.read_excel(file, sheet_name=sheet_names[-3])  # wijk
    gebr = pd.read_excel(file, sheet_name=sheet_names[-2])  # gebruik
    det = pd.read_excel(file, sheet_name=sheet_names[-1])  # determinanten

    file.close()

    df = det.copy()
    # als je wijk en gemeentecode hebt heb je wijkcode en gemeentenaam niet nodig
    df = df.merge(wijk[['wijk', 'gemeentecode']], on='wijk', how='left')
    # per_jhzv : aandeel jeugdigen met jeugdhulp zonder verblijf, waargenomen -> target variable
    df = df.merge(gebr[['wijk', 'perc_jhzv']], on='wijk', how='left')

    for col in df.columns:
        df[col] = df[col].apply(lambda x: x if x != '.' else np.nan)

    # TODO is nu missig values vullen met gemiddelde hoe willen we dat doen?
    df.fillna(df.mean(), inplace=True)

    # hun schatting root mean squared error (residu = schatting - waargenomen)
    for col in gebr.columns:
        gebr[col] = gebr[col].apply(lambda x: x if x != '.' else np.nan)

    # drop missende schattingen en bereken RMSE
    original_rmse = str((gebr.dropna(subset='residu')['residu']**2).mean()**0.5)

    # buurt_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/buurt_2022_v1.shp')
    wijk_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/wijk_2022_v1.shp')
    # gemeente_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/gemeente_2022_v1.shp')

    wijk_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/wijk_2022_v1.shp')
    wijk_geo['WK_CODE'] = wijk_geo['WK_CODE'].apply(lambda x: x[2:]).astype('float')
    wijk_geo['GM_CODE'] = wijk_geo['GM_CODE'].apply(lambda x: x[2:]).astype('float')
    wijk_final = df.merge(wijk_geo, left_on=['wijk', 'gemeentecode'], right_on=['WK_CODE', 'GM_CODE'], how='left')
    for col in wijk_final.columns:
        wijk_final[col] = wijk_final[col].apply(lambda x: x if x != int(-99999999) else np.nan)

    df = wijk_final.fillna(wijk_final.mean(numeric_only=True))
    df = df.drop(['JRSTATCODE', 'JAAR', 'Shape_Leng', 'Shape_Area', 'geometry', 'wijk', 'WK_CODE', 'WK_NAAM', 'GM_CODE', 'GM_NAAM', 'gemeentecode', 'H2O'], axis=1)

    X = df.drop(['perc_jhzv'], axis=1)

    y = df['perc_jhzv']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    params= {'objective': 'reg:squarederror', 'base_score': None, 'booster': None, 'callbacks': None, 'colsample_bylevel': None, 'colsample_bynode': None, 'colsample_bytree': None, 'early_stopping_rounds': None, 'enable_categorical': False, 'eval_metric': None, 'feature_types': None, 'gamma': None, 'gpu_id': None, 'grow_policy': None, 'importance_type': None, 'interaction_constraints': None, 'learning_rate': 0.1, 'max_bin': None, 'max_cat_threshold': None, 'max_cat_to_onehot': None, 'max_delta_step': None, 'max_depth': 4, 'max_leaves': None, 'min_child_weight': None, 'missing': np.nan, 'monotone_constraints': None, 'n_estimators': 300, 'n_jobs': None, 'num_parallel_tree': None, 'predictor': None, 'random_state': None, 'reg_alpha': None, 'reg_lambda': None, 'sampling_method': None, 'scale_pos_weight': None, 'subsample': None, 'tree_method': None, 'validate_parameters': None, 'verbosity': None}
    # Step 2: Create the base model
    base_model = XGBRegressor(**params)

    # Step 3: Create the bagging ensemble model with the base model
    bagging_model = BaggingRegressor(base_model, n_estimators=10, random_state=42)

    # Step 4: Train the bagging ensemble model
    bagging_model.fit(X_train, y_train)

    # Step 5: Generate ensemble predictions on the test set
    ensemble_predictions = bagging_model.predict(X_test)

    # Step 6: Evaluate the ensemble performance
    mse = mean_squared_error(y_test, ensemble_predictions)
    print("Ensemble Model RMSE:", mse**0.5)
    # Get the feature importances from the base estimators
    importance_scores = np.mean([estimator.feature_importances_ for estimator in bagging_model.estimators_], axis=0)

    # Get the feature names
    feature_names = X_train.columns

    # Sort feature importance scores and feature names in descending order
    sorted_indices = np.argsort(importance_scores)[::-1]
    sorted_importance_scores = importance_scores[sorted_indices]
    sorted_feature_names = feature_names[sorted_indices]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the feature importance
    ax.bar(range(len(sorted_importance_scores)), sorted_importance_scores)
    ax.set_xticks(range(len(sorted_importance_scores)))
    ax.set_xticklabels(sorted_feature_names, rotation=90)
    ax.set_xlabel("Feature")
    ax.set_ylabel("Importance Score")
    ax.set_title("Feature Importance")

    # Ensure tight layout
    plt.tight_layout()

    return fig

if st.session_state["authentication_status"]:
    st.title("Model Page")
    st.write("This is the model page.")
    st.pyplot(get_data())
elif authentication_status == False:
     st.error('Username/password is incorrect')


if authentication_status:
    authenticator.logout('Logout', 'sidebar')


