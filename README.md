Project-IR-WA

Elias Asskali 218912 - Adam Dbouk 217294 - Joel Lamata 

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
