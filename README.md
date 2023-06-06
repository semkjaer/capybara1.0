#installation:

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
**unzip** and add de folder WijkBuurtkaart_2022_v1 to the root folder of this repo '~/capybara1.0/WijkBuurtkaart_2022_v1'

To run streamlit app locally, from capybara1.0 folder:
```
streamlit run app.py
```
then go to http://localhost:8501 or check terminal