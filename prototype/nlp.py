import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendation(match_skills, mentors, count=5):
    mentors = pd.DataFrame(mentors)
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(mentors.skills)
    title_vector = vectorizer.transform([match_skills])
    cosine_sim = cosine_similarity(vectors, title_vector)
    idx = np.argsort(np.array(cosine_sim[:,0]))[-count:]
    ans = mentors.iloc[idx]
    return ans.email