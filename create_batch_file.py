import pandas as pd
import numpy as np
import os

# (0, 'PID')
# (1, 'FirstName')
# (2, 'MiddleName')
# (3, 'LastName')
# (4, 'BirthDate')
# (5, 'Gender')
# (6, 'Race')


print('*** Batch File Generator ***')
print('Make sure the excel file is in the same folder as this script')
print('The columns MUST be in this order:')
print('[pid, firstname, middlename, lastname, birthdate, gender, race]')

file_name = input('Enter file name: ')

def main():
    df = pd.read_excel(r'{}.xlsx'.format(file_name))
    df.iloc[:, 1] = df.iloc[:, 1].str.upper()
    df.iloc[:, 2] = df.iloc[:, 2].str.upper()
    df.iloc[:, 3] = df.iloc[:, 3].str.upper()

    df.iloc[:, 3] = df.iloc[:, 3].replace(' ', '-', regex=True)  # last name: replace spaces with dashes
    df.iloc[:, 3] = df.iloc[:, 3].replace('\'', '', regex=True)  # last name: remove apostrophe

    df.iloc[:, 1] = df.iloc[:, 1].replace('\'', '', regex=True)  # first name: remove apostrophe
    df.iloc[:, 1] = df.iloc[:, 1].replace(' ', '', regex=True)  # first name: remove spaces
    df.iloc[:, 1] = df.iloc[:, 1].replace('-', '', regex=True)  # first name: remove dashes

    batch = pd.DataFrame()

    batch['Name'] = np.where(df.iloc[:, 2].isnull(), df.iloc[:, 3] + ',' + df.iloc[:, 1],
                             df.iloc[:, 3] + ',' + df.iloc[:, 1] + ' ' + (df.iloc[:, 2].str[0]))

    batch['Gender'] = np.where(df.iloc[:, 5] == 'Male', 'M', 'F')
    batch['Race'] = np.where(df.iloc[:, 6] == 'White', 'W',
                             np.where(df.iloc[:, 6] == 'Hispanic', 'W', np.where(df.iloc[:, 6] == 'Black', 'B', 'U')))

    batch['BirthDate'] = pd.to_datetime(df.iloc[:, 4], format='%Y-%m-%d').dt.strftime('%Y%m%d')

    for i in df['BirthDate'].iteritems():
        batch['BirthDate'] = pd.to_datetime(df.iloc[:, 4], format='%Y-%m-%d').dt.strftime('%Y%m%d')

    batch_all = pd.DataFrame()
    batch_all['1'] = batch["Name"].str.pad(30, side='right', fillchar=' ') + batch['Gender'] + batch['Race'] + batch[
        'BirthDate']

    batch_all.to_csv(r'batch_file_pre.txt', index=False, header=None)

    with open('batch_file_pre.txt', 'r') as f, open('batch_file.txt', 'w') as fo:
        for line in f:
            fo.write(line.replace('"', '').replace("'", ""))

    f.close()
    fo.close()
    os.remove("batch_file_pre.txt")

if __name__ == "__main__":
    main()