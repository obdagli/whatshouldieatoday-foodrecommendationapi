import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def rec_cbcalculator(ds, item_id, num):

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['food_ingredients'])
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    res = {}
    for x, row in ds.iterrows():
        similar_indices = cosine_similarities[x].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[x][i], ds['id'][i]) for i in similar_indices]
        res[row['id']] = similar_items[1:]
    
    def item(id):
        return ds.loc[ds['id'] == id]['food_ingredients'].tolist()[0].split(' - ')[0]

    foods = []
    recs = res[item_id][:num]
    for rec in recs:
        foods.append(str(rec[1]))
    return foods
