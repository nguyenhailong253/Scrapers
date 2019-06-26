# author: long nguyen (nguyenhailong253@gmail.com)

# +  -  -  - CONSTANTS -  -  - +

ROOT = 'https://au.indeed.com'
JD_QUERY = '/viewjob?jk='
LATEST_QUERY = '&sort=date&start='
POP_QUERY = '&start='

PARENT = 'parents'
CHILDREN = 'children'
TAG = 'tag'
ATTRS = 'attribute'

TIME_UNIT = ["hour", "day", "week", "month", "year"]
PERIOD_UNIT = ["hourly", "daily",
               "weekly", "monthly", "yearly"]

STATES = [
    "NSW",
    "New South Wales",
    "QLD",
    "Queensland",
    "TAS",
    "Tasmania",
    "WA",
    "Western Australia",
    "NT",
    "Northern Territory",
    "SA",
    "South Australia",
    "VIC",
    "Victoria"
]

# +  -  -  - SUBCATEGORY TAGS -  -  - +

SUBCATE_TAGS = {
    "parents": {
        "tag": "p",
        "attribute": {"class": "job"},
    },
    "children": {
        "tag": "a",
        "attribute": "href",
    }
}

INFO_SPECS = {
    "parents": {
        "tag": "div",
        "attribute": {"class": "row"}
    },
    "children": {
        "src_id": {
            "tag": None,
            "attribute": "data-jk",
        },
        "title": {
            "tag": "a",
            "attribute": {"class": "jobtitle"},
        },
        "company": {
            "tag": "span",
            "attribute": {"class": "company"},
        },
        "loc": {
            "tag": "div",
            "attribute": {"class": "location"},
        },
        "short_desc": {
            "tag": "div",
            "attribute": {"class": "summary"},
        },
        "posted_at": {
            "tag": "span",
            "attribute": {"class": "date"},
        },
        "sponsored": {
            "tag": "span",
            "attribute": {"class": "sponsoredGray"},
        },
        "salary": {
            "tag": "span",
            "attribute": {"class": "salary no-wrap"},
        },
        "numReviews": {
            "tag": "span",
            "attribute": {"class": "slNoUnderline"},
        },
    }
}

JD_SPECS = {
    "tag": "div",
    "attribute": {"id": "jobDescriptionText", "class": "jobsearch-jobDescriptionText"}
}


INFO_SPECS_BACKUP = {
    "src_id": {
        "tag": None,
        "attribute": "data-tk",
    },
    "title": {
        "tag": "a",
        "attribute": {"class": "jobtitle turnstileLink"},
    },
    "salary": {
        "tag": "span",
        "attribute": {"class": "no-wrap"},
    },
    "loc": {
        "tag": "span",
        "attribute": {"class": "location"},
    },
}
