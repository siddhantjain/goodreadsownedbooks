# goodreadsownedbooks
Find list of friends who already own that book you want to read
--------------------------------------------------------------------------------------------------------------------------------

## General Instructions
To run this script you you will have to generate your own developer key and secret (I am working on making a web-app out of this, but till then, I can't share my developer keys publicly). Generating the key and secret is fairly straightforward. Just go to the following link:
https://www.goodreads.com/api/keys

Once you have the key and the secret ready, just replace them with the dummy values in the code. There are three occurences where you have to replace the key and two occurences where you will have to replace the secret.

##About the program
I am generating a dictionary of all the owned books by all your friends everytime you run the program. Depending on the number of friends you have on goodreads and number of books they own, this might take a large amount of time (working on bringing this down as well). Please be patient with the program. Thereafter, you can enter the goodreads book id you are searching for. As an output, if any of your goodreads friends own the book, their names will be listed.

Version 1:
This version is very basic and is more of a POC of what can be done and serves as an example to use the goodreads API in Python. 
