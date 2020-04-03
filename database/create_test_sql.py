import os
import pandas as pd
import numpy as np 
import sqlalchemy as sa
import re
from datetime import datetime

if __name__ == "__main__":
    db_host = os.getenv('CPS_DB_HOST','localhost')
    db_port = os.getenv('CPS_DB_PORT',5432)
    db_name = os.getenv('CPS_DB_NAME','cps')
    db_user = os.getenv('CPS_DB_USER__SERVERADMIN','cps')
    db_pass = os.getenv('CPS_DB_PASS__SERVERADMIN','')
    engine = sa.create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

    datasheet = pd.read_excel('./database/testdata/Физики.xlsx', index_col=None, index_row=0)
    datasheet = datasheet.loc[:,[
        'Фамилия ', 
        'Имя ', 
        'Отчество', 
        'Дата рождения',
        '№ Профс.', 
        '№ Студ. билета', 
        'Срок действия', 
        'E-mail']]
    datasheet = datasheet.rename(columns={
        'Фамилия ': 'lastname',
        'Имя ': 'firstname', 
        'Отчество': 'middlename',
        'Дата рождения': 'birthday', 
        '№ Профс.': 'login_x', 
        '№ Студ. билета': 'login_y', 
        'Срок действия':'expires', 
        'E-mail': 'email'
    })

    for i, row in datasheet.iterrows():
        if type(row['birthday']) == str:
            if re.match(r'\d\d\.\d\d\.\d\d\d\d', row['birthday']): 
                try:
                    datasheet.loc[i,'birthday'] = datetime.strptime(row['birthday'],'%d.%m.%Y')
                except ValueError as e:
                    datasheet.loc[i,'birthday'] = np.nan
            if re.match(r'\d\d\.\d\d\.\d\d', row['birthday']): 
                try:
                    datasheet.loc[i,'birthday'] = datetime.strptime(row['birthday'],'%d.%m.%y')
                except ValueError as e:
                    datasheet.loc[i,'birthday'] = np.nan
            elif re.match(r'\d\d/\d\d/\d\d\d\d', row['birthday']): 
                try:
                    datasheet.loc[i,'birthday'] = datetime.strptime(row['birthday'],'%d/%m/%Y')
                except ValueError as e:
                    datasheet.loc[i,'birthday'] = np.nan
            else:
                datasheet.loc[i,'birthday'] = np.nan
        if type(row['birthday']) == int:
            datasheet.loc[i,'birthday'] = np.nan

    for i, row in datasheet.iterrows():
        if type(row['expires']) == str:
            if re.match(r'\d\d\.\d\d\.\d\d\d\d', row['expires']): 
                try:
                    datasheet.loc[i,'expires'] = datetime.strptime(row['expires'],'%d.%m.%Y')
                except ValueError as e:
                    datasheet.loc[i,'expires'] = np.nan
            if re.match(r'\d\d\.\d\d\.\d\d', row['expires']): 
                try:
                    datasheet.loc[i,'expires'] = datetime.strptime(row['expires'],'%d.%m.%y')
                except ValueError as e:
                    datasheet.loc[i,'expires'] = np.nan
            elif re.match(r'\d\d/\d\d/\d\d\d\d', row['expires']): 
                try:
                    datasheet.loc[i,'expires'] = datetime.strptime(row['expires'],'%d/%m/%Y')
                except ValueError as e:
                    datasheet.loc[i,'expires'] = np.nan
            else:
                datasheet.loc[i,'expires'] = np.nan
        if type(row['expires']) == int:
            datasheet.loc[i,'expires'] = np.nan

    datasheet1 = datasheet.loc[~datasheet['login_x'].isna(),['lastname','firstname','middlename','birthday','login_x','expires','email']].rename(columns={'login_x':'password'})
    datasheet1.loc[:,'type_id'] = 3
    datasheet2 = datasheet.loc[~datasheet['login_y'].isna(),['lastname','firstname','middlename','birthday','login_y','expires','email']].rename(columns={'login_y':'password'})
    datasheet2.loc[:,'type_id'] = 4
    datasheet = pd.concat([datasheet1,datasheet2])
    datasheet.replace('nan', np.nan, inplace=True)

    datasheet=datasheet.astype({
        'lastname': str,
        'firstname': str, 
        'middlename': str, 
        'birthday': np.datetime64,
        'password': str, 
        'expires': np.datetime64, 
        'email': str,
        'type_id': int
    })

    datasheet.to_sql('preregistred_profile', engine, schema='users', if_exists='append', index=False)