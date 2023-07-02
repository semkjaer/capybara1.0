Important files
root:
  pred_xg.ipynb: contains the XGBoost algoritm and the code to create the dataset which the backend of the app pulls from.
  application/:
    contains all files for the application expects for the data
    /home.py is the homepage, other pages are in the /pages/ map
  
  data/
    Contains the feature datasets on which the model is based
    
  WijkBuurtkaart_2022_v1/
    Contains the geodata used for the geomaps

  ts_total.csv 
    Contains the processed data for loading into the app

  all other folders/files are not in use currently


installation:

anywhere you want the repo folder to be in terminal:
download repo
```
git clone https://github.com/semkjaer/capybara1.0
```
cd to repo
```
cd capybara1.0
```
create virtual environment (first time only):
```
python -m venv ../capy-env
```

activate virtual environment:
on windows:
```
. ../capy-env/Scripts/activate
```
on mac:
```
. ../capy-env/bin/activate
```
install python requirements:
```
pip install -r requirements.txt
```
download WijkBuurtkaart_2022_v1 at https://www.cbs.nl/-/media/cbs/dossiers/nederland-regionaal/wijk-en-buurtstatistieken/wijkbuurtkaart_2022_v1.zip
**unzip** and add the folder WijkBuurtkaart_2022_v1 to the root folder of this repo '~/capybara1.0/WijkBuurtkaart_2022_v1'

To run streamlit app locally, from capybara1.0 folder:
```
streamlit run application/src/home.py
```
then go to http://localhost:8501 or check terminal

