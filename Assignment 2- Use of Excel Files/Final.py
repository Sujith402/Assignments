import pandas as  pd

def total_price(ticket_type,ticket_number):
    if ticket_type=='senior':
        price=senior_ticket_price
    elif ticket_type=='adult':
        price=adult_ticket_price
    elif ticket_type=='child':
        price=child_ticket_price
    total_price=price*int(ticket_number)
    return int(total_price)

def find_location(theater):
    df1=df.loc['theaters']
    return list(df1[df1.theater_name==theater]['theater_location'])[0]

def find_length(movie):
    df1=df.loc['movies']
    return list(df1[df1.movie_title==movie]['movie_length'])[0]

#1.Merge the data required in a single data frame. 
# Reads each sheet as a separate dataframe 
xls=r'V:\Comp Projects\Assignment 2- Use of Excel Files\movie theater sales data.xlsx'
df1 = pd.read_excel(xls,'sales')
df2 = pd.read_excel(xls,'ticket types')
df3 = pd.read_excel(xls,'theaters')
df4 = pd.read_excel(xls,'movies')
df = pd.concat([df1,df2,df3,df4],keys=['sales','ticket types','theaters','movies'],sort=False)

senior_ticket_price=df.loc['ticket types'].loc[2,'ticket_price']
adult_ticket_price=df.loc['ticket types'].loc[1,'ticket_price']
child_ticket_price=df.loc['ticket types'].loc[0,'ticket_price']


#2.	Find the theatre that made the second-highest sales for the movie ‘The Seaborn Identity’
#3. Find the city of the theatre that made the third-highest sales only with ‘senior’
#4.	Find the longest movie that made third-maximum sales.
sales_movies={}
req_df1=df.loc['movies']
for name in list(req_df1['movie_title']):
    sales_movies[name]=0

sales_theaters={'The Empirical House':0,'Sumdance Cinemas':0,'The Frame':0,"Richie's Famous Minimax Theatre":0}
sales_senior={'The Empirical House':0,'Sumdance Cinemas':0,'The Frame':0,"Richie's Famous Minimax Theatre":0}
req_df=df.loc['sales']

for i in req_df.index.tolist():
    row=req_df.iloc[i,:]
    sale=total_price(row[2],row[3])
    if row[1]=='The Seaborn Identity':
        sales_theaters[row[0]]+=sale
    if row[2]=='senior':
        sales_senior[row[0]]+=sale
    sales_movies[row[1]]+=sale

theatre_sales_theaters=sorted(sales_theaters,key=lambda x:sales_theaters[x])
theatre_sales_senior=sorted(sales_senior,key=lambda t:sales_senior[t])
movie_sales_movies=sorted(sales_movies,key=lambda j:sales_movies[j])
print('The theatre that made the second-highest sales for the movie ‘The Seaborn Identity’ is',theatre_sales_theaters[-2])
print('The theatre that made the third-highest sales only with senior is',theatre_sales_senior[-3],'which is located at',find_location(theatre_sales_senior[-3]))
print('The movie that made the third maximum sales is',movie_sales_movies[-3],'. It spans for',find_length(movie_sales_movies[-3]),'minutes')





