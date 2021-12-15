Project-IR-WA

Elias Asskali 218912 - Adam Dbouk 217294 - Jordi Tortosa 217105

------------------------------------------------------------------------

PART 1

We first have to import all necessary libraries.

In second place we execute the next cell which will read and parse the json saving in an array called tweets the text of each tweet stored in "full_text" in the json file. It will also print the number of instances in the datasource.

The third cell has an emoji pattern variable used to detect emojis in the text and a url pattern to detect urls.
The functions remove_emojis and remove_urls will remove emojis and urls given a string.
Given a line as parameter, build_terms will:
	Transform to lowercase
	Remove emojis
	Remove urls
	Tokenise the line
	Remove stop words
	Remove punctuation (except # and @)
	Perform stemming
	Remove empty words

In the last line we can test the pre-processing

------------------------------------------------------------------------

PART 2

In the first cell of Part 2 Indexing and Evaluation we create the inverted index given all lines as a parameter.
In the next cell we can see an example of the inverted index for the term 'research'.

The second defined function is the search function which will return the list of docs that contain the words of the query given as a parameter.
In the next cell we can test the function writting a query.

In the third cell we create the inverted index and compute the tf, df and idf. 
After this we define the rank_documents function, which will rank the documents based on tf-idf weights.

In the part of Evaluation there are declared different evaluation techniques.
The first evaluation technique is the function 'precision_at_k' which returns the precision of the documents k docummments as we can see in the next cell where we test the function
The next function is the average precision which has the same parameters as 'precision_at_k' and the mean average precision which is tested in its following cell.
In the next cell we define the Mean Reciprocal Rank using the true relevance labels, the predicted scores and the number of documents to return the reciprocal rank for the query.
This can be tested in the following cells.
Last but not least we compute the dcg and ndcg with the same parameters and their results can be seen in the next cells.

In the next cell we load the 'word2vec language model' which will last more or less 20 minutes to load.
The next function defined is 'vector_representation' which represents a tweet given as a parameter in a vector way. This can be tested in the following cell.
The last function is 'plot_tweets' where given a number of lines the function plots all tweets and adds the tweet id as a label for each tweet.
We test the method with the first 50 tweets, if we put more tweets the labels will cover the plot.

There has been a problem with this Part of the project, we didn't understand the firts exercice of the 'Evaluation' part so we used the 'test_predictions.csv' given in the lab instead of using a document made by us.

------------------------------------------------------------------------

PART 3

The first two cells of the project are about TF-IDF + cosine similarity given terms and couments as a parameter.
The next one is a test to try our ranking given an example of a query.

In the following cell we define our own way to score documents where we will need tweet_index to get infomation about the tweet as well as the documents and the index terms.
The next defined function is the search function which will return the list of docs that contain the words of the query given as a parameter.

And as we did before the next cell is for testing our score and check the result taking into account the given query.

In the next part we have the first cell with the code for computing the document ranking using cosine similarity and tweet2vec where we will need the tweet index to extract information of the tweet.
In the next cell we will represent all documents as a tweet vector for the given query and compute the result.
As always the following cell is in charge of testing how good is the development before given queries.

------------------------------------------------------------------------

PART 4:

To represent the tweets we have created two classes, Tweet and TweetInfo, the first one has the basic info of a tweet, extracted from the json, while TweetInfo will have extra info like the url and the ranking.

When we first start the web app the search engine will call read_json that will return the lines containing each one a tweet. This lines will be passed as a parameter to load_or_create_index_tfidf which will either load a pickle file containing the index, tf, df and idf or create them using create_index_tfidf and saving it in a pickle file, this will save us time creating the index each time the web app is executed as the index creation is an expensive operation. Then, we will pass the lines obtained before to load_documents_corpus which will create a dictionary with the tweet id as the key and a Tweet instance as the object.

The search engine class also has a search algorithm that given a query, builds terms for the query, gets the ids of all the documents containing at least a query term and also calls with this ids the method get_max_popularity_score which will return the max popularity score from the documents passed as parameter (popularity = 0.4*likes + 0.6*retweets), then it will call rank_documents which will apply the tf-idf + cosine similarity with the added popularity score and will return the ids of the documents sorted by ranking.

Finally build tweets will take this ordered list, the list of tweets and the query that lead to this ranking and a list of TweetInfo instances that will be those tweets, but as before we will add the url which will contain the tweet id, the query and the ranking, and we will also store the ranking itself.

In analytics_data we have created 4 classes, the first one is AnalyticsData, where we have created 4 dictionaries: fact_clicks (which will store the document_id as a key and a click counter as a value), fact_results (which will do the same but for each query), fact_queries (which will store the query and the term counter) and the fact_users that will store the user_id and the object User() as the value).
The second class is Click, where we have the doc_id, with its query and the position of the document.
The third one is Query, where we have the query with the number of documents and the number of times that has been asked. 
And finally we have User where we have the ip as the id, the browser, platform, and date.
We will use these classes to struct the information obtained from the web_app.py and show it in the html.
In web_app.py we will define 'search_form()' where we will request the information from a user_agent, if the ip (which will be the id) is not in the fact_user we will add this user and its information to the dictionary.
The next definition will be 'search_from_post()' where we will request the query and render the results.html where we will show all the results of the query.
In 'doc_details()' we will store all the requested information in the dictionaries fact_clicks, fact_results, fact_queries, which will store the count of the document clicks and the queries.
In 'dashboards()'  we will get all the information that we will use to do the plots and finally render the template of the dashboard.html.
In 'sentiment_form()' we will just render the html template.

When it comes to the html apart from adding the UPF and other logos we also tried to show the resulting docs from a query as clean as possible, we added the likes and retweets with its corresponding icons and also an url to see the whole tweet.
We also added the dashboard and sentiment access from any screen of the web.

Finally, We have to say that we had some problems with html and javascript showing the dashbord statistics, it has been implemented but the dashboard only shows the first graphic, we don't know why it is not showing. In the report we explained all the analytics we implemented.