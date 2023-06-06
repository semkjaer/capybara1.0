#installation:

anywhere you want the repo folder to be in terminal:
download repo
```
git clone https://github.com/semkjaer/capybara1.0
```
cd to repo
```
git clone https://github.com/semkjaer/capybara1.0
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


To run streamlit app locally, from capybara1.0 folder:
```
streamlit run app.py
```
then go to http://localhost:8501 or check terminal