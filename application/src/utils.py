import uuid
import yaml
import streamlit as st
from yaml.loader import SafeLoader
from streamlit_extras.app_logo import add_logo
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
# from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@st.cache_resource
def logo():
    return add_logo("application/src/logo_localgovernment.jpg")


def auth():
    with open('./application/config.yaml', 'r') as file:
            config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    return authenticator, config


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

    # hun schatting root mean squared error (residu = schatting - waargenomen)
    for col in gebr.columns:
        gebr[col] = gebr[col].apply(lambda x: x if x != '.' else np.nan)

    # buurt_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/buurt_2022_v1.shp')
    wijk_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/wijk_2022_v1.shp')
    # gemeente_geo = gpd.read_file('./WijkBuurtkaart_2022_v1/gemeente_2022_v1.shp')

    wijk_geo['WK_CODE'] = wijk_geo['WK_CODE'].apply(lambda x: x[2:]).astype('float')
    wijk_geo['GM_CODE'] = wijk_geo['GM_CODE'].apply(lambda x: x[2:]).astype('float')
    df = df.merge(wijk_geo, left_on=['wijk', 'gemeentecode'], right_on=['WK_CODE', 'GM_CODE'], how='left')
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x if x != int(-99999999) else np.nan)
    # wijk_final.to_csv('data_combined.csv', index=False)

    return df


def model(df):
    df = df.fillna(df.mean(numeric_only=True))
    df = df.drop(['JRSTATCODE', 'JAAR', 'Shape_Leng', 'Shape_Area', 'geometry', 'wijk', 'WK_CODE', 'WK_NAAM', 'GM_CODE', 'GM_NAAM', 'gemeentecode', 'H2O'], axis=1)

    X = df.drop(['perc_jhzv'], axis=1)

    y = df['perc_jhzv']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # params= {'objective': 'reg:squarederror', 'base_score': None, 'booster': None, 'callbacks': None, 'colsample_bylevel': None, 'colsample_bynode': None, 'colsample_bytree': None, 'early_stopping_rounds': None, 'enable_categorical': False, 'eval_metric': None, 'feature_types': None, 'gamma': None, 'gpu_id': None, 'grow_policy': None, 'importance_type': None, 'interaction_constraints': None, 'learning_rate': 0.1, 'max_bin': None, 'max_cat_threshold': None, 'max_cat_to_onehot': None, 'max_delta_step': None, 'max_depth': 4, 'max_leaves': None, 'min_child_weight': None, 'missing': np.nan, 'monotone_constraints': None, 'n_estimators': 300, 'n_jobs': None, 'num_parallel_tree': None, 'predictor': None, 'random_state': None, 'reg_alpha': None, 'reg_lambda': None, 'sampling_method': None, 'scale_pos_weight': None, 'subsample': None, 'tree_method': None, 'validate_parameters': None, 'verbosity': None}
    # # Step 2: Create the base model
    # base_model = XGBRegressor(**params)

    # # Step 3: Create the bagging ensemble model with the base model
    # bagging_model = BaggingRegressor(base_model, n_estimators=10, random_state=42)

    # # Step 4: Train the bagging ensemble model
    # bagging_model.fit(X_train, y_train)

    # # Step 5: Generate ensemble predictions on the test set
    # ensemble_predictions = bagging_model.predict(X_test)

    # # Step 6: Evaluate the ensemble performance
    # mse = mean_squared_error(y_test, ensemble_predictions)
    # print("Ensemble Model RMSE:", mse**0.5)
    # # Get the feature importances from the base estimators

    # Load your dataset and split it into training and testing sets

    # Create the XGBoost regressor
    model = XGBRegressor()

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print("Root Mean Squared Error: %.2f" % mse**0.5)

    importances = model.feature_importances_
    feature_names = X_train.columns

    indices = importances.argsort()[::-1][:5]
    top_importances = importances[indices]
    top_feature_names = feature_names[indices]

    # Create a bar plot of top 5 feature importances
    fig, ax = plt.subplots()
    ax.bar(top_feature_names, top_importances)

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=90)

    # Set plot title and labels
    plt.title('Feature Importances')

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    return fig



def send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, username, password):
    # Create a multipart message and set headers
    email_message = MIMEMultipart()
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message["Subject"] = subject

    # Add body to the email
    email_message.attach(MIMEText(message, "plain"))

    # Convert the email message to a string
    email_text = email_message.as_string()

    try:
        # Create a secure SSL/TLS connection to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Log in to the SMTP server
            server.starttls()
            server.login(username, password)
            # Send the email
            server.sendmail(sender_email, receiver_email, email_text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error message: {str(e)}")


def registration_email(receiver_email, registered):
    sender_email = "semkjaer@hotmail.nl"
    if registered == True:
        subject = "A new account has been registered!"
        message = "You can now log in to the app using the credentials you filled in during account creation!"
    else:
        subject = "Account creation authorized"
        message = "Welcome <user>,\n\nYou may now create an account on in our app: http://localhost:8501 "
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    username = "semkjaer@hotmail.nl"
    password = "Sjemma@023"

    send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, username, password)