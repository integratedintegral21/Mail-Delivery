# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping


class Letter:
    def __init__(self, data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki, ilosc_dni_roboczych, on_time):
        self.data_wyslania = data_wyslania     # 0
        self.data_dotarcia = data_dotarcia     # 1
        self.miejsce_wysylki = miejsce_wysylki # 2 
        self.miejsce_celu = miejsce_celu       # 3
        self.typ = typ                         # 4
        self.numer_przesylki = numer_przesylki # 5
        self.ilosc_dni_roboczych = ilosc_dni_roboczych # 6
        self.on_time = on_time # 0 - spozniony, 1 - na czas, 2 - nie wiadomo jeszcze

    def self_print(self):
        print(self.data_wyslania)
        print(self.data_dotarcia)
        print(self.miejsce_wysylki)
        print(self.miejsce_celu)
        print(self.typ)
        print(self.numer_przesylki)
        print(self.on_time)
        print(self.ilosc_dni_roboczych)
        print("-------------------------------")

    def to_dict(self):
        return {
            'data_wyslania': self.data_wyslania,
            'data_dotarcia': self.data_dotarcia,
            'ilosc_dni_roboczych': self.ilosc_dni_roboczych,
            'czy_na_czas': self.on_time,
            'typ': self.typ,
            'numer_przesylki': self.numer_przesylki,
            'miejsce_wysylki': self.miejsce_wysylki,
            'miejsce_celu': self.miejsce_celu
        }
    def to_file(self):
        line = str(self.data_wyslania) + ',' + str(self.data_dotarcia)  + ',' + str(self.miejsce_wysylki) + ',' + str(self.miejsce_celu) + ',' + str(self.typ) + ',' + str(self.numer_przesylki) + ',' + str(self.on_time) + ',' + str(self.ilosc_dni_roboczych)
        return line
    
class Letter_ext(Letter):
    def __init__(self, data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki, ilosc_dni_roboczych, on_time, dystans, czas):
        super().__init__(data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki, ilosc_dni_roboczych, on_time)
        self.dystans = dystans
        self.czas = czas

    def self_print(self):
        print("-------------------------------")
        print(self.data_wyslania)
        print(self.data_dotarcia)
        print(self.miejsce_wysylki)
        print(self.miejsce_celu)
        print(self.typ)
        print(self.numer_przesylki)
        print(self.on_time)
        print(self.ilosc_dni_roboczych)
        print(self.dystans)
        print(self.czas)
        print("-------------------------------")

    def to_dict(self):
        return {
            'data_wyslania': self.data_wyslania,
            'data_dotarcia': self.data_dotarcia,
            'ilosc_dni_roboczych': self.ilosc_dni_roboczych,
            'czy_na_czas': self.on_time,
            'typ': self.typ,
            'numer_przesylki': self.numer_przesylki,
            'miejsce_wysylki': self.miejsce_wysylki,
            'miejsce_celu': self.miejsce_celu,
            'dystans': self.dystans,
            'czas': self.czas
        }

    def to_file(self):
        line = str(self.data_wyslania) + ';' + str(self.data_dotarcia)  + ';' + str(self.miejsce_wysylki) + ';' + str(self.miejsce_celu) + ';' + str(self.typ) + ';' + str(self.numer_przesylki) + ';' + str(self.on_time) + ';' + str(self.ilosc_dni_roboczych) + ';' + str(self.dystans) + ';' + str(self.czas)
        return line


def split_data(text): # dostawanie ze stringa daty
    day_and_hour = text.split(" ")
    day = day_and_hour[0].split("-")
    hour = day_and_hour[1].split(":")
    y = datetime.datetime(int(day[0]), int(day[1]), int(day[2]), int(hour[0]), int(hour[1]))
    return y

def map_type(x):
    if(x=='List polecony priorytetowy'):
        return 0  # priorytet bedzie pod 0
    else:
        return 1 # a ekonomiczny pod 1
    
def get_place_type(place):
    words = place.split(' ')
    w1 = words[0]
    if(w1=='UP'):
        return 0
    elif(w1=='FUP'):
        return 1
    elif(w1=='AP'):
        return 2
    else:
        return 3
    
def get_place_type_OH(place):
    words = place.split(' ')
    w1 = words[0]
    if(w1=='UP'):
        return 'UP'
    elif(w1=='FUP'):
        return 'FUP'
    elif(w1=='AP'):
        return 'AP'
    else:
        return 'Unk'

def get_dist(d):  # dystans w kilometrach, ponizej jednego wszystko do 0
    words = d.split(' ')
    if(len(words)>1):
        if(words[1]=='km'):
            return float(words[0])
        else:
            return 0
    else:
        return 0    

def get_diff_h(data_wyslania, data_dotarcia):
    d1 = data_wyslania.to_pydatetime()
    d2 = data_dotarcia.to_pydatetime()
    diff = d2 - d1
    return diff.total_seconds()/3600;    
 
def get_time(t):
    words = t.split(' ')
    if(len(words)==4):
        return 60*int(words[0])+int(words[2])
    elif(len(words)==2):
        if(words[1]=='min'):
            return int(words[0])
        else:
            return 60*int(words[0])
    else:
        return 0    

def boundary(g):
    if(g<15):
        return 1
    else:
        return 0
    
listofletters = []
set_1 = set()

# ------------------------------------------------------- czytyanie dotychczasowego zbioru
f = open('wyniki4.txt', 'r', encoding='utf-8')
text = f.read()
text = text[:-2] # pominiecie ostatniego znaku - czyli \n, bo powoduje to martwy wiersz w tabeli
f.close()
table = text.split('\n')

for t in table: # dla kazdego rekordu
    tab_of_line = t.split(';') # podzial wiersza wedlug przecinkow
    if(tab_of_line[1]!='nie doszedl'):
        letter_1 = Letter_ext(split_data(tab_of_line[0]), split_data(tab_of_line[1]), tab_of_line[2], tab_of_line[3], tab_of_line[4], tab_of_line[5], tab_of_line[7], tab_of_line[6],tab_of_line[8],tab_of_line[9])
        a = len(set_1)
        set_1.add(letter_1.numer_przesylki)
        b = len(set_1)
        if b>a: # warunek, ze tej przesylki nie ma jeszcze w secie
            if(letter_1.data_wyslania<letter_1.data_dotarcia): # warunek na dobre daty
                if(letter_1.on_time!='2'): # warunek na znany typ przesylki
                    listofletters.append(letter_1)
        
    else:
        letter_1 = Letter_ext(split_data(tab_of_line[0]), tab_of_line[1], tab_of_line[2], tab_of_line[3], tab_of_line[4], tab_of_line[5], tab_of_line[7], tab_of_line[6],tab_of_line[8],tab_of_line[9])
    
# ------------------------------------------------


df = pd.DataFrame.from_records([l.to_dict() for l in listofletters])

# dataframe gotowy, teraz obrobka ficzerow 

df=df.assign(dzien_tygodnia=lambda x: x.data_wyslania.dt.dayofweek)
df['ilosc_dni_roboczych']=df['ilosc_dni_roboczych'].astype(int)
df.loc[df['typ']!='Przesyłka firmowa polecona zamiejscowa'] # pozbywamy sie tego malo licznego typu, zeby nie robic encodingu na typie
df = df.loc[df['typ']!='Przesyłka firmowa polecona zamiejscowa']
df['typ']=df['typ'].map({'List polecony priorytetowy':0, 'List polecony ekonomiczny':1})
#df.drop(columns=['czy_na_czas', 'numer_przesylki', 'miejsce_celu'], inplace=True)
df['typ_placowki']=df['miejsce_wysylki'].apply(get_place_type)
df['typ_placowki']=df['miejsce_wysylki'].apply(get_place_type_OH)
df=df.assign(godzina=lambda x: x.data_wyslania.dt.hour)
df['dyst']=df['czas'].apply(get_dist)
df['y2'] = df[['data_wyslania', 'data_dotarcia']].apply(lambda x : get_diff_h(*x), axis = 1)
df['czas']=df['dystans'].apply(get_time)
#df.drop(columns=['data_wyslania', 'data_dotarcia', 'miejsce_wysylki','dystans'], inplace=True)
df=df[df['ilosc_dni_roboczych']<10] # odrzucamy skrajne wartosci, to patologie pocztowe, a utrudnia klasyfikacje
df['granica_15'] = df['godzina'].apply(boundary)

# teraz przygotowanie modelu

categorical_cols_ORD = ['typ','granica_15']
categorical_cols_OH=['dzien_tygodnia','typ_placowki']
numerical_cols=['czas','dyst','godzina']


numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('std_scaler', StandardScaler())
])

categorical_ORD_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('std_scaler', StandardScaler())
])

categorical_OH_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('cat_ORD', categorical_ORD_transformer, categorical_cols_ORD),
        ('cat_OH', categorical_OH_transformer, categorical_cols_OH),
        ('num', numerical_transformer, numerical_cols)
    ])


post = df.sample(frac=1)
y = post['y2']

X_transformed = preprocessor.fit_transform(post)

X_train = X_transformed[:23733]
y_train = y[:23733]
X_valid = X_transformed[23733:]
y_valid = y[23733:]

X_train = np.asarray(X_train)
X_valid = np.asarray(X_valid)
y_train = np.asarray(y_train)
y_valid = np.asarray(y_valid)

# przygotowanie modelu
model = keras.Sequential([
    layers.Dense(units=50, activation='relu', input_shape=[15]),
    layers.Dropout(0.05),
    layers.Dense(units=50, activation='relu'),
    layers.Dropout(0.05),
    layers.Dense(units=50, activation='relu'),
    layers.Dropout(0.05),
    layers.Dense(units=1),
])


model.compile(
    optimizer="adam",
    loss="mae",
)

early_stopping = EarlyStopping(
    min_delta=0.0001, # minimium amount of change to count as an improvement
    patience=30, # how many epochs to wait before stopping
    restore_best_weights=True,
)
model.summary()

# trening

history = model.fit(
    X_train, y_train,
    validation_data=(X_valid, y_valid),
    batch_size=32,
    epochs=300,
    callbacks=[early_stopping],
    verbose=1
)


history_df = pd.DataFrame(history.history)
history_df.loc[:, ['loss', 'val_loss']].plot();
print("Minimum validation loss: {}".format(history_df['val_loss'].min()))
print("Gap between val: {}".format(history_df['val_loss'].iloc[-1]-history_df['loss'].iloc[-1]))

# przewidywanie
test_preds = model.predict(X_valid)