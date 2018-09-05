import csv
import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')

# column_names = ["review_id","user_id","business_id","stars","date","text","useful","funny","cool"]
rating_index = 3
text_index = 5

def utf8len(s):
    # print len(s.decode('utf-8'))
    return len(s.decode('utf-8'))

with open('yelp.test.shuffled.csv') as csv_file:
    # csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')     
    line_count = 0
    total = 0
    correct = 0
    for csv_row in csv_reader:
        total = total + 1

        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # Amazon Comprehend Document size (UTF-8 characters) 5,000 bytes 
            if utf8len(csv_row[text_index]) < 5000:

                comprehend_response = comprehend.detect_sentiment(Text=csv_row[text_index], LanguageCode='en')

                actual_rating = 'POSITIVE'            
                if csv_row[rating_index] != 'stars':  #Do not process header rows
                    if int(csv_row[rating_index]) == 3:
                        actual_rating = 'NEUTRAL'
                    elif int(csv_row[rating_index]) < 3:
                        actual_rating = 'NEGATIVE'

                    predicted = comprehend_response['Sentiment']
                    # print ("{}\t{}\tActual:{}\tPredicted: {} ").format(csv_row[0],csv_row[rating_index],actual_rating, predicted)

                    if ( predicted.upper() == 'MIXED'):
                        predicted='NEUTRAL'

                    if ( predicted.upper() != actual_rating.upper()):
                        print ("{}\t{}\tActual:{}\tPredicted: {} ").format(csv_row[0],csv_row[rating_index],actual_rating, predicted)
                    else:
                        correct =  correct + 1

            line_count += 1
    print('Processed {} lines.').format(line_count)

    print("Correctly predicted {} out of {}, with percent{}").format(correct, total, (correct*100)/total)




