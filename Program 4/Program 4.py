import csv
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout

def preprocess():

    with open(r'C:\Users\Emc11\Dropbox\Software\School\4.Spring 2020\Program 4\ramen-ratings.csv', encoding='utf8') as csv_file:
        reviews = [line[:-1] for line in csv.reader(csv_file)]
    
    companies = [review[1] for review in reviews[1:]]
    for company in set(companies):
        if companies.count(company) == 1:
            for num, review in enumerate(reviews):
                if company in review: 
                    reviews[num][1] = 'Other'
                    break
                        
    variety = [word for review in reviews[1:] for word in review[2].split()]
    variety = {word for word in variety if variety.count(word) >= 100}
    for num, review in enumerate(reviews[1:]):
        
        try: reviews[num + 1][2] = ' '.join(set(review[2].split()) & variety)
        except: pass
        reviews[num + 1][0] = int(reviews[num + 1][0])
        reviews[num + 1][1] = reviews[num + 1][1].encode('utf-8')
        reviews[num + 1][2] = reviews[num + 1][2].encode('utf-8')
        reviews[num + 1][3] = reviews[num + 1][3].encode('utf-8')
        reviews[num + 1][4] = reviews[num + 1][4].encode('utf-8')
        reviews[num + 1][5] = None if reviews[num + 1][5] == 'Unrated' else float(reviews[num + 1][5])

    return reviews[0], reviews[1:]

epochs = 5
batch = 64
columns, data = preprocess()
x_train, y_train = [i[:-1] for i in data[:2250]], [i[-1:] for i in data[:2250]]
x_test, y_test = [i[:-1] for i in data[2250:]], [i[-1:] for i in data[2250:]]

model = Sequential([
    Flatten(input_shape=[len(data), 1]),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(5, activation='softmax')
    ])

model.compile(
    optimizer='adam', metrics=['accuracy'],
    loss='sparse_categorical_accuracy'
    )

model.fit(
    x_train, y_train, epochs=epochs, batch_size=batch
    )
test_loss, test_accuracy = model.evaluate(x_test, y_test)

