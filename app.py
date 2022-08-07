from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route('/get_text', methods=['POST'])

def get_text():
    output = request.form.to_dict()
    sent1 = output["text1"]
    sent2 = output["text2"]
    sent1_na = non_ascii(sent1)
    sent2_na = non_ascii(sent2)
    sent1_rsc = remove_special_chars(sent1_na)
    sent2_rsc = remove_special_chars(sent2_na)
    low1 = lower(sent1_rsc)
    low2 = lower(sent2_rsc)
    stop1 = removeStopWords(low1)
    stop2 = removeStopWords(low2)
    token_stemming(stop1)
    token_stemming(stop2)
    documents = [sent1,sent2]
    count_vectorizer =CountVectorizer(stop_words='english')
    sparse_matrix = count_vectorizer.fit_transform(documents)
    doc_term_matrix = sparse_matrix.todense()
    dd = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names(), index=['x','y'])
    sim = (cosine_similarity(dd, dd)[0,1])
    return render_template('index.html',prediction=sim)
    
    
if __name__ == '__main__':
    app.run(debug = True,use_reloader=False)