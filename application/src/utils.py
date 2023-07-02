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
import streamlit.components.v1 as components

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
    df = pd.read_csv('data.csv')
    # geo = gpd.read_file('./gemeenteWijk.shp')
    # df = df[df.year == 2021]
    # df = geo.merge(df, left_on=['gwb'], right_on=['gwb_code_10'], how='left')
    # df = df.dropna(subset=['geometry'])

    return df


def plot(code):
    html_url = f"https://pinkcapybucket.s3.eu-central-1.amazonaws.com/maps/{code}.html"
    iframe_html = f'<iframe src="{html_url}" width="100%" height="800px" frameborder="0"></iframe>'

    return components.html(iframe_html, height=680)


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
    username = ""
    password = ""

    send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, username, password)
