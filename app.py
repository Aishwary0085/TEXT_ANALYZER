import streamlit as st
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string
import time
import re

nltk.download('punkt')
nltk.download('stopwords')

st.title("Mini Text Analyzer By Aishwarya")
st.markdown("This tool analyzes your text input and gives word count, sentence count, and frequent word stats.")

text = st.text_area("📝 Enter your paragraph or text here:", height=200)

if st.button("🔍 Analyze Text"):
    if text.strip() == "":
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Analyzing text..."):
            time.sleep(1.5)

            text = text.lower()
            text = re.sub(r"[’‘`]", "'", text) 
            words = word_tokenize(text)
            sentences = sent_tokenize(text)

            words = [word for word in words if word not in string.punctuation]

            stop_words = set(stopwords.words('english'))
            filtered_words = [word for word in words if word not in stop_words]

            contractions_to_ignore = {"'s", "'m", "'re", "'ve", "'ll", "'d", "n't"}
            filtered_words = [word for word in filtered_words if word not in contractions_to_ignore]

            word_freq = Counter(filtered_words)


            st.success("✅ Analysis Complete!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Words", len(words))
            col2.metric("Sentences", len(sentences))
            col3.metric("Meaningful Words", len(filtered_words))

            st.subheader("📌 Top 10 Frequent Words:")
            freq_df = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency']).sort_values(by='Frequency', ascending=False).head(10)
            st.dataframe(freq_df.style.background_gradient(cmap='Reds'))

            st.markdown("### 📉 Word Frequency Chart")
            st.bar_chart(freq_df.set_index('Word'))