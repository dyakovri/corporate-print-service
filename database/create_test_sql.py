import os
import pandas as pd
import numpy as np 
import sqlalchemy as sa

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
        '№ Профс.', 
        '№ Студ. билета', 
        'Срок действия', 
        'E-mail']]
    datasheet=datasheet.astype({
        'Фамилия ': str,
        'Имя ': str, 
        'Отчество': str, 
        '№ Профс.': str, 
        '№ Студ. билета': str, 
        'Срок действия': np.datetime64, 
        'E-mail': str
    })
    datasheet = datasheet.rename(columns={
        'Фамилия ': 'lastname',
        'Имя ': 'firstname', 
        'Отчество': 'middlename', 
        '№ Профс.': 'login_x', 
        '№ Студ. билета': 'login_y', 
        'Срок действия':'expires', 
        'E-mail': 'email'
    })

    datasheet.loc[:,'expires'] = datasheet['expires'].fillna(np.datetime64('2020-01-01'))
    
    datasheet1 = datasheet.loc[~datasheet['login_x'].isna(),['lastname','firstname','middlename','login_x','expires','email']].rename(columns={'login_x':'login'})
    datasheet1.loc[:,'type_id'] = 3
    datasheet2 = datasheet.loc[~datasheet['login_y'].isna(),['lastname','firstname','middlename','login_y','expires','email']].rename(columns={'login_y':'login'})
    datasheet2.loc[:,'type_id'] = 4
    datasheet = pd.concat([datasheet1,datasheet2])
    datasheet.replace('nan', np.nan, inplace=True)
    
    # print(datasheet['middlename'])
    datasheet.to_sql('preregistred_profile', engine, schema='users', if_exists='replace', index=False)