# author: long nguyen (nguyenhailong253@gmail.com)

# +  -  -  - URLS -  -  - +

ROOT = 'https://news.zing.vn'

URL_TAIL = '.html'

PAGE = 'trang'

# +  -  -  - CONSTANT KEYWORDS -  -  - +

PARENTS = 'parents'

CHILDREN = 'children'

TAG = 'tag'

ATTRS = 'attribute'

ATTRS_TAGS = ['a', 'img']

RAW_KEY = ['article_body', 'tags']

EXTRA_KEY = ['like_count', 'dislike_count',
             'rating_count', 'viral_count', 'comment_count']

# +  -  -  - DIVS & CLASSNAMES SPECIFICATIONS -  -  - +

SUBCATE_SPECS = {
    "parents": {
        "tag": "div",
        "attribute": {"class": "subcate"},
    },
    "children": {
        "tag": "a",
        "attribute": "href"
    }
}

THUMBNAIL_SPECS = {
    "parents": {
        "tag": "article",
        "attribute": {"class": "article-item"},
    },
    "children": {
        "src_id": {
            "tag": None,
            "attribute": "article-id",
        },
        "article_type": {
            "tag": None,
            "attribute": "class",
        },
        "topic_id": {
            "tag": None,
            "attribute": "topic-id",
        },
        "url": {
            "tag": "a",
            "attribute": "href",
        },
        "img_src": {
            "tag": "img",
            "attribute": "src",
        },
        "title": {
            "tag": "p",
            "attribute": {"class": "article-title"},
        },
        "publish_time": {
            "tag": "span",
            "attribute": {"class": "time"},
        },
        "publish_date": {
            "tag": "span",
            "attribute": {"class": "date"},
        },
        "category": {
            "tag": "span",
            "attribute": {"class": "category"},
        },
        "like_count": {
            "tag": "span",
            "attribute": {"class": "like-count"},
        },
        "dislike_count": {
            "tag": "span",
            "attribute": {"class": "dislike-count"},
        },
        "rating_count": {
            "tag": "span",
            "attribute": {"class": "rating-count"},
        },
        "viral_count": {
            "tag": "span",
            "attribute": {"class": "viral-count"},
        },
    }
}

ARTICLE_SPECS = {
    "parents": {
        "tag": "article",
        "attribute": {"class": "the-article"},
    },
    "children": {
        "author": {
            "tag": "p",
            "attribute": {"class": "author"},
        },
        "comment_count": {
            "tag": "li",
            "attribute": {"class": "comment-count"},
        },
        "article_body": {
            "tag": "div",
            "attribute": {"class": "the-article-body"}
        },
        "tags": {
            "tag": "p",
            "attribute": {"class": "the-article-tags"}
        },
        "summary": {
            "tag": "p",
            "attribute": {"class": "the-article-summary"}
        }
    }
}

CATEGORIES = [
    '/chinh-tri/',
    '/giao-thong/',
    '/do-thi/',
    '/phap-dinh/',
    '/vu-an/',
    '/quan-su-the-gioi/',
    '/tu-lieu-the-gioi/',
    '/phan-tich-the-gioi/',
    '/nguoi-viet-4-phuong/',
    '/tin-tuc-xuat-ban/',
    '/sach-hay/',
    '/tac-gia/',
    '/bat-dong-san/',
    '/hang-khong/',
    '/tai-chinh/',
    '/tieu-dung/',
    '/doanh-nhan/',
    '/mobile/',
    '/internet/',
    '/esport/',
    '/tieu-diem/oppo-reno-series/',
    '/bong-da-viet-nam/',
    '/bong-da-anh/',
    '/vo-thuat/',
    '/hau-truong-the-thao/',
    '/mua-xe/',
    '/lai-xe/',
    '/sao-viet/',
    '/sao-chau-a/',
    '/sao-hollywood/',
    '/nhac-viet/',
    '/nhac-han/',
    '/nhac-au-my/',
    '/tieu-diem/zing-chart/',
    '/phim-chieu-rap/',
    '/phim-truyen-hinh/',
    '/game-show/',
    '/thoi-trang-sao/',
    '/mac-dep/',
    '/lam-dep/',
    '/guong-mat-tre/',
    '/cong-dong-mang/',
    '/su-kien/',
    '/tuyen-sinh-dai-hoc-2019/',
    '/tu-van-giao-duc/',
    '/du-hoc/',
    '/tieu-diem/hoc-tieng-anh/',
    '/khoe-dep/',
    '/dinh-duong/',
    '/me-va-be/',
    '/benh-thuong-gap/',
    '/dia-diem-du-lich/',
    '/kinh-nghiem-du-lich/',
    '/phuot/',
    '/dia-diem-an-uong/',
    '/mon-ngon/',
    '/ttdn/',
    #   # '/nhip-song/cuoi/' NOT EXISTED, redirected to song-tre, below 4 extras
    '/song-tre/',
    '/guong-mat-tre/',
    '/cong-dong-mang/',
    '/su-kien/'
]
