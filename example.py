import pandas as pd
email = 'example@123'
password = 'passwd'
df = pd.read_csv('data.csv')

print(df[df['mail']==email]['passwd'])
print(email in list(df['mail']))
if email in list(df['mail']):
    if password in list(df[df['mail']==email]['passwd']):
        print("login sucessful")        