# -*- coding: utf-8 -*-
"""Customer_Segmentation_Using_K_Means_Clustering_pynb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ocFey3admM9xMlBWaC8YeTXBE0R7UWRD

### Problem statement:Mall Customer Segmentation Using KMeans Clustering
"""

# Commented out IPython magic to ensure Python compatibility.
#Importing the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
from mpl_toolkits.mplot3d import Axes3D
# %matplotlib inline

#Reading the data file
data=pd.read_csv("Mall_Customers.csv")

#Exploring the dataset
data.head()

data.shape

data.info()

data.dtypes

#Cheking the null values in dataset
data.isnull().sum()

#Relationship between variable
data.corr()

#Distribution of Annnual Income
plt.figure(figsize=(10, 6))
sns.distplot(data['Annual Income (k$)'])
plt.title('Distribution of Annual Income (k$)', fontsize = 20)
plt.xlabel('Range of Annual Income (k$)')
plt.ylabel('Count')
plt.savefig('Distribution of Annual Income (k$)',bbox_inches='tight',dpi=400)

"""Most of the annual income falls between 50K to 85K."""

age18_25 = data.Age[(data.Age <= 25) & (data.Age >= 18)]
age26_35 = data.Age[(data.Age <= 35) & (data.Age >= 26)]
age36_45 = data.Age[(data.Age <= 45) & (data.Age >= 36)]
age46_55 = data.Age[(data.Age <= 55) & (data.Age >= 46)]
age55above = data.Age[data.Age >= 56]

x = ["18-25","26-35","36-45","46-55","55+"]
y = [len(age18_25.values),len(age26_35.values),len(age36_45.values),len(age46_55.values),len(age55above.values)]

plt.figure(figsize=(15,6))
sns.barplot(x=x, y=y, palette="rocket")
plt.title("Number of Customer and Ages")
plt.xlabel("Age")
plt.ylabel("Number of Customer")
plt.savefig("Number of Customer and Ages",bbox_inches='tight',dpi=400)
plt.show()

"""There are customers of a wide variety of ages."""

#Distribution of spending score
plt.figure(figsize=(10, 6))
sns.distplot(data['Spending Score (1-100)'])
plt.title('Distribution of Spending Score (1-100)', fontsize = 20)
plt.xlabel('Range of Spending Score (1-100)')
plt.ylabel('Count')
plt.savefig('Distribution of Spending Score (1-100)',bbox_inches='tight',dpi=400)

"""The maximum spending score is in the range of 40 to 60."""

genders = data.Gender.value_counts()
sns.set_style("darkgrid")
plt.figure(figsize=(10,4))
sns.barplot(x=genders.index, y=genders.values)
plt.show()

"""### Clustering based on 3 features"""

#We take just the Annual Income,Age and Spending score 
X=data[['Age',"Annual Income (k$)","Spending Score (1-100)"]]
X.head()

#Scatterplot of Annual Income vs Spending Score
plt.figure(figsize=(10,6))
sns.scatterplot(x = 'Annual Income (k$)',y = 'Spending Score (1-100)',  data = X  ,s = 60 )
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)') 
plt.title('Spending Score (1-100) vs Annual Income (k$)')
plt.show()

#Scatterplot of the input data
plt.figure(figsize=(10,6))
sns.scatterplot(x = 'Age',y = 'Spending Score (1-100)',  data = X )
plt.xlabel('Age')
plt.ylabel('Spending Score (1-100)') 
plt.title('Spending Score (1-100) vs Age')
plt.show()

#Normalizing the value 
from sklearn.preprocessing import StandardScaler
X1 =StandardScaler().fit_transform(X.values)
X1 = np.nan_to_num(X1)

X1[:5]

"""#### Calculation the K Value"""

#Importing KMeans from sklearn
from sklearn.cluster import KMeans

#Lets calculate the K value
sse=[]
for i in range(1,11):
    km=KMeans(n_clusters=i)
    km.fit(X)
    sse.append(km.inertia_)

#The elbow curve
plt.figure(figsize=(12,6))
plt.plot(range(1,11),sse, linewidth=2, color="red", marker ="8")
plt.xlabel("K Value")
plt.xticks(np.arange(1,11,1))
plt.ylabel("SSE")
plt.savefig('Calculation K Value',bbox_inches='tight',dpi=400)
plt.show()

"""Here in the graph, after 5 the drop is minimal, so we take 5 to be the number of clusters."""

#Taking 5 clusters
km1=KMeans(n_clusters=5)
#Fitting the input data
km1.fit(X1)
#predicting the labels of the input data
y=km1.predict(X1)
#adding the labels to a column named label
data["label"] = y
#The new dataframe with the clustering done
data.head()

"""### Result"""

#Ploting Final Cluster in 3D
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data.Age[data.label == 0], data["Annual Income (k$)"][data.label == 0], data["Spending Score (1-100)"][data.label == 0], c='blue', s=60)
ax.scatter(data.Age[data.label == 1], data["Annual Income (k$)"][data.label == 1], data["Spending Score (1-100)"][data.label == 1], c='red', s=60)
ax.scatter(data.Age[data.label == 2], data["Annual Income (k$)"][data.label == 2], data["Spending Score (1-100)"][data.label == 2], c='green', s=60)
ax.scatter(data.Age[data.label == 3], data["Annual Income (k$)"][data.label == 3], data["Spending Score (1-100)"][data.label == 3], c='orange', s=60)
ax.scatter(data.Age[data.label == 4], data["Annual Income (k$)"][data.label == 4], data["Spending Score (1-100)"][data.label == 4], c='purple', s=60)
ax.view_init(30, 185)
plt.xlabel("Age")
plt.ylabel("Annual Income (k$)")
ax.set_zlabel('Spending Score (1-100)')
plt.savefig('Final clustering result',bbox_inches='tight',dpi=400)
plt.show()
