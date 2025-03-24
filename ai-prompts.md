# AI Prompts Used:




## Scraping

```
please explain what selenium is and how to use it like i am five and like i am 18. give me steps.
```

```
i have no experience with selenium. I want to use it to scrap job posts from indeed.com. can you explain what to do in each step, and give me example code? I will create a mongoDB to store the info, and create a RESTful API using fastAPI, then a React front end.
```

```
I can find how to modify the CSS selectors in the console of the indeed website, right?
```

```
What are the best practices of web scraping and why?
```

```
what is beautifulsoup?
```

```
what is pagination?
```

```
How to check robot.txt for a website? Show me how to do that for indeed.com
```

```
what is a sitemap and how to use it?
```

```
so it seems i need to process every line of the sitemap to get all urls, is that correct?
```

```
is that true: this sitemap contains all the jobs i need to scrape?
```

```
it seems that i will need to design a database scheme first and make sure when scraping, it will create the right object and at finishing it will be saved?
```

```
great! Now, about doing the scraping, do i need to select the css selector by myself, if i have the schema already designed?
```

```
i am inspecting one webpage i want to scrape(by selenium). I want to check the css selectors, can you help me?i am looking at the elements tab in the console. what to do next?
```

```
what is XPath in "Select Copy → Copy selector (or "Copy → Copy full XPath" if you need XPath instead)."? 

```

```
I plan to scrape @https://weworkremotely.com/  using selenium. can you refer to my schema@schema.py  can create another version of scraper, not using beautifulsoup? You can try json.loads(). please use headless mode and handle errors(timeouts, missing elements, etc). The scraped info will be saved to my google firebase. Ensure there is no duplicate entries. Before scraping the whole thing, i want a test function that only scrapes a given url so i can check its work.
```


## Database

```
you used SQL in the design, but i plan to use non-relational database like mongoDB. what do you think? do you pick SQL for a reason? what are the tradeoffs?
```

```
how to communicate the schema to firebase? Show me the steps to set it up.
```



## Backend

```
in the rest api part of the requirement, it mentions "Implement pagination support in the API responses.". what is pagination support here? i know i need to handle pagination when scrapping.
```

```
can you learn from this scraper.py file about my firebase, also learn from @schema.py about my schema. then create a fastAPI backend that has the following routs? GET /data → Retrieve all scraped data.
o GET /data/{category} → Retrieve data filtered by category.
o GET /data/{company} → Retrieve data by company name (if applicable).
o DELETE /data/{id} → Delete a specific entry (admin functionality).Please Implement pagination support in the API responses. Please put this file in the api folder , it is inside romotejobbank(the root of this project)/backend/api
```

## Frontend

cannot keep track of these. Mainly about telling cursor I want a stylish website that is repsonsive, and then make adjustments.

## Docker

```

can you create this docker instruction on how to run the full project? I want other users to be able to use it conveniently. also give me the steps to test it
```
