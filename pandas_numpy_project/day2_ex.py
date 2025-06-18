import pandas as pd
import numpy as np

# import and create json file

js = pd.DataFrame({"Name": ['Heril','Raghav','Kavish','Heetraj'],"subjects": ['Maths','Science','Java','Python'],"Marks":[70,80,34,None]})
columns_js = js.columns.str.strip().str.lower()
print("JSON dataset")
print()
print(columns_js)
print()
print(js.head())
print()
print(js.tail(2))
print()
print("Null values in table: ",js.isnull().sum())
print()
print(js.info())
print()
print(js.describe())
print()
js_json = js.to_json("jsonfile")


df = pd.read_csv("C:\\Users\\Heril\\Downloads\\abc2.csv")
columns_df = df.columns.str.strip().str.lower()
print("csv dataset")
print()
print(columns_df)
print("Table size:", df.shape)
print(df)
print()
print(df.head())
print()
print(df.tail(5))
print()
print("Null values in table: ",df.isnull().sum())
print()
print(df[['language','student']])
print()
print(df.iloc[3])
print()
print(df.loc[df['science'].isnull()])
print()
filtered_data = (df[(df['science'] > 25) & (df['maths'] > 25)])
print(filtered_data)
print()

# Mean,median,mode function

mean = df['history'] = df["history"].mean()
print("mean:",mean)
mode = df['maths'] = df["maths"].mode()
print("mode:",mode)
median = df["science"] = df["science"].median()
print("median:" , median)

# fillna and dropna

print(df.fillna(1,inplace= True))
print()
print(df.fillna({'science': df['science'].mean(), 'maths': 0}, inplace= True))
print()
print(df.fillna(method = 'ffill', inplace=True))
print()
print(df.fillna(method = 'bfill', inplace=  True ))
print()
print(df.fillna(df['history'].mean(), inplace=True))
print()
print(df.fillna(df.interpolate()))
print(df)
df.dropna(inplace= True)
df.dropna(subset=['science'], inplace=True)
df.dropna(axis= 1, inplace= True)
df.dropna(how='all', inplace= True)
df.dropna(thresh = 4, inplace=True)

# data cleaning

print(df.duplicated().sum())
print(df.drop_duplicates(inplace=True))
df['history'] = df["history"].astype(int)
print(df["history"].dtype)



# Numpy operations

arr1 = np.array([[[2,5,7],[9,1,4],[3,6,9]]], ndmin= 3)  #ndmin is use to change the dimensions of array
print(arr1.ndim)   #gives dimension of data
print(arr1.shape)

arr = np.array([[2,4,6,8],[10,12,14,16]])
print(arr)
print(arr.shape)
print()
reshaped_data = arr.reshape(2,2,2)
print(reshaped_data)
print()

# reshaping with automatic calculation (-1)

arr2 = np.random.randint(1,100,6)          # you can also try np.arange(value) to get array
print(arr2)
reshaped_arr2 = arr2.reshape(2,-1)
print(reshaped_arr2)

# filtering array

arr3  = np.array([10, 25, 37, 44, 55, 60])
filtered_arr = arr3[arr3 > 30]  
print(filtered_arr)

arr4 = np.array([10, 25, 37, 44, 55, 60])
filtered_arr1 = arr4[(arr4 > 30) & (arr4 < 50)]  
print(filtered_arr1)

arr5 = np.array([10, 25, 37, 44, 55, 60])
indices = np.where(arr5 % 2 == 0)  # Find indices of even numbers
print(arr5[indices])


# indexing and slicing

arr_6 = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
print(arr_6)
print(arr_6[1,::2])

arr2d = np.array([[[ 1,  2,  3,  4], 
                  [ 5,  6,  7,  8], 
                  [ 9, 10, 11, 12],[13,14,15,16]],[[ 17, 18, 19,  20], 
                  [ 21,  22,  23,  24], 
                  [ 25, 26, 27, 28],[29,30,31,32]]])

print(arr2d.shape)
print(arr2d.ndim) 
print(arr2d)

print(arr2d[0,1,2])

# to print odd no in table
print(arr2d[0,0:,0::2])
print(arr2d[1,0:,0::2])

# to print eve no in table
print(arr2d[0,::,1::2])
print(arr2d[1,::,1::2])








