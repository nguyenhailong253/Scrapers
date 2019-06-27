# HOW IT WORKS
- Use multiprocessing (4 processes) which takes turn to grab 1 one category and run scraper on it
- Request each page of that category
- On each page, get list of divs that contain news
- Loop for each div, scrape general info on thumbnail
- Use the url from thumbnail, access full article
- Scrape details of article
- Process data and save to DB

# Functions
## Base
- set_up_logs(): Create log file and set formatter
- get_categories_dict(): Get dict with category name as key, url as value
- format_article_url(tail): Format URL with 2 components: root and tail
- format_page_url(name, page_num): Format URL with page number
- initialize_data(): Initialize all fields of data obj to null
- process_article_type(article_type): Get second item in list of article type and strip 'type-'
- process_time(time, date): Convert to standard time format %Y-%m-%d %H:%M:%S
- process_text(text): Strip, replace newline or spaces neccessary
- process_data(key, raw_data): Based on key, call other process functions
- process_extras(): Convert extras to json and call process time to cacl posted_at
- save_news(values): Insert data to DB 
- check_news_existed(news_id): Query if news already existed

## Scraper
- scrape_attrs_tags(div, key, value): Process content of html tag a, img, or None
- scrape_extras(key, result): Check if key in EXTRA_KEY and assign result to value based on key
- scrape(div, html_attrs): Scrape article details, given its html div and set of attributes
- scrape_pages(category, page_num): Iterate through all articles in 1 page and call scrape func
- run(category)

# Rules
- Zing organizes their news chronologically: latest on first page, oldest on the last
- Some categories only have up to page 5 (like Politics), but most have up to page 50
- Sometimes Zing puts popular articles on top (usually not more than 10 but sometimes could be more), which are not necessary the latest ones (could be yesterday or within this week), so I have added extra logic to check if more than 25 articles already scraped on the first page, then we have scraped all the latest one.
- Pages have different number of articles, some might have 40, others could have 120

- Video-type article has no author

# Most common article type
- text: only text
- hasvideo: text with >1 video
- picture: slideshow of photos
- video: only 1 video, no text
- infographic: only 1 picture

