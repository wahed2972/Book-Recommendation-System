from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pivot = pickle.load(open('pivot.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Num_Rating'].values),
                           rating = list(popular_df['Avg_Rating'].values))
    
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    
    # Check if the user_input exists in the pivot table index
    if user_input not in pivot.index:
        # If the book is not found, display an error message
        error_message = f"No recommendations found for '{user_input}'. Please try another book title."
        return render_template('recommend.html', error_message=error_message, data=None)

    # If the book is found, proceed with recommendation
    index = np.where(pivot.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[0:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pivot.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data)

    
if __name__ == '__main__':
    app.run(debug=True)