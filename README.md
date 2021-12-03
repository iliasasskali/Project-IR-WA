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
cd Application
python3 -m pip install virtualenv
python3 -m venv venv
. venv/bin/activate
python3 -m pip install flask

#Tell the terminal what application to run
export FLASK_APP=main.py
#Tell the terminal what application to run for windows
set FLASK_APP=main.py
#Run the application
flask run