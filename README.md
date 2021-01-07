# django-news

My very first project with the Django Framework, which I've learned about on the Jetbrains Academy Python course (highly recommended!).

It was quite a bit to learn at first (if you're interested in the learning process, check my gists), but I think I've managed it okay.

It's a simple news page, styled by implementing a static .css file.

News are saved in a .json file, from which they're also loaded (d'oh!).

The main page simply lists all news found, grouped together (via itertools.groupby) by date, so that even if there's multiple news on the same day, they'll still be listed under one date.

Via DTL, links to each news are created automatically, linking to, e.g., news/1, which will be fetched in urlpatterns by Djangos "news/<int:news_id>/" feature.

Clicking on any news will show them on their own page, yadda yadda.~

It's also possible to create news by a post request, which, when successful, will add the news to the json. 

I've not implemented any kind of check if a user is authorized to do so, because I hadn't learned about that yet.

Last but not least, it's also possible to search for news (it looks thorugh news titles for the search parameter).

This is done by a get request that checks if a search query was found and displays the result if there was one; otherwise it'll just display the news.


**Libraries/Modules used**: itertools, datetime, json



