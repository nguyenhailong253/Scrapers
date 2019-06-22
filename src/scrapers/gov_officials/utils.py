# author: long nguyen (nguyenhailong253@gmail.com)

# +  -  -  - URL OF EACH MINISTRY WEBSITE -  -  - +

URLS = {
    # "gov": "http://chinhphu.vn/portal/page/portal/chinhphu/chinhphu/chinhphuduongnhiem",
    # # "parliament": "https://infographics.vn/dai-bieu-quoc-hoi.vna",
    # "defence": "http://www.mod.gov.vn/wps/portal/!ut/p/b1/vZPbkqIwEIafZR5gisQg4mUg4SQB5Aw3FqvgAREdNAJPP-7W1N6N3uxO-ipVX9fff3f9Qi6kQn4q-H5bXPftqTj-_ufSSsOOLysQA9mAEjCRQaQ4DpCuwweQPQBVx4Y4swGQbX0KTGxE_nyJEMDoVX8ipHEGFdKyLaWpB-okrfvmrJMdJRKeNURXFEztophXomxTlHJuj-LtZpDbdVmuEUhKqPSdXxCNn6UBTt7fsdeXYuwseL922fJoBsjOqqgN2E6sjoW35bZkKjf5GtJspltRxpiZQLonGUjC665FMuIyjouIF-Dtyx_45mHw2l_-FFFnX8CzFf4BnsyQPYDZtxIyEEIhBeIqOAxnc6xH_wDu0Dnge0gvAyTJyCiKnFBbdBsVBrSZQBINLFRYSLKBERc6TuptYj9SMCbOdOW-EkQ_LQj_t6DuGhowrdCaBu5yAhbwhx26__6GlpBvj-2vR8jjOGt70rEteSSw7ujhnnq8JujqH_Al0NUws9J63oDRZx8TdFpVI8_yuOwItQnyLsXxoIkLURMHR1YldakHkbQxSKaUCXY_qnxyv0wnp5VEp5Hos6A_u0l5M-yR2EkHmpZXWj8NrYhx0CG-0JxTMx8VGedJjIv1m-AYbVMK5yZ65NY3xvRvlZ_-rScW/dl4/d5/L2dBISEvZ0FBIS9nQSEh/",
    # "public_security": "http://bocongan.gov.vn/gioi-thieu/lanh-dao-bo-duong-nhiem.html",
    # "foreign_affair": "http://www.mofa.gov.vn/vi/bng_vietnam/nr040824153458/",
    "justice": "https://moj.gov.vn/Pages/lanh-dao-duong-nhiem.aspx",
    # "finance": "https://www.mof.gov.vn/webcenter/portal/btc/r/m/gioithieu/lanhdao?_afrLoop=70951142228500859#!%40%40%3F_afrLoop%3D70951142228500859%26centerWidth%3D0%2525%26leftWidth%3D100%2525%26rightWidth%3D0%2525%26showFooter%3Dfalse%26showHeader%3Dfalse%26_adf.ctrl-state%3Devgh2w4pu_134",
    # "industry_trade": "http://www.moit.gov.vn/web/guest/lanh-dao-bo",
    # "labour": "http://www.molisa.gov.vn/vi/Pages/danhsachlanhdao.aspx",
    # "transport": "http://mt.gov.vn/vn/Pages/danhsachlanhdao.aspx",
    # "construction": "http://www.xaydung.gov.vn/en/web/guest/gioi-thieu",
    # "ict": "http://www.mic.gov.vn/pages/thongtin/97877/co-cau-to-chuc.html",
    # "education": "https://moet.gov.vn/gioi-thieu/co-cau-to-chuc/Pages/default.aspx?CateID=1155&Details=1",
    # "agriculture": "https://www.mard.gov.vn/Pages/danh-ba-dien-thoai.aspx",
    # "planning": "http://www.mpi.gov.vn/Pages/ldbkhtd.aspx",
    # "home_affair": "https://www.moha.gov.vn/gioi-thieu/lanh-dao-bo.html",
    # "health": "https://moh.gov.vn/web/guest/lanh-dao-duong-nhiem",
    # "tech": "https://www.most.gov.vn/vn/Pages/DanhSachLanhDao.aspx",
    # "culture": "https://bvhttdl.gov.vn/gioi-thieu-ve-bo/lanh-dao-bo.htm",
    # "environment": "http://www.monre.gov.vn/Pages/lanh-dao-bo.aspx",
    # "gov_office": "http://vpcp.chinhphu.vn/Home/gioi-thieu-vpcp/lanh-dao-van-phong-chinh-phu.vgp",
    # "inspectorate": "http://www.thanhtra.gov.vn/Pages/co-cau-to-chuc.aspx?CQID=0&LVID=33",
    # "state_bank": "https://www.sbv.gov.vn/webcenter/portal/vi/menu/trangchu/gioithieunhnn/blddn?_afrLoop=15521027813626577#%40%3F_afrLoop%3D15521027813626577%26centerWidth%3D80%2525%26leftWidth%3D20%2525%26rightWidth%3D0%2525%26showFooter%3Dfalse%26showHeader%3Dfalse%26_adf.ctrl-state%3Duk36uxlsk_124",
    # "ethnic": "http://ubdt.gov.vn/Danhbadienthoai.aspx",
}

# +  -  -  - TAGS AND CLASS NAMES OF CHILDREN DIV ON EACH MINISTRY WEBSITE -  -  - +

''' 
  Format of Specs:

  'ministry_name': {
    "title": {
      "tag-containing-data": ...,
      "attribute-of-tag": ...,
      "unused-tag-with-similar-attributes-but-different-children" (if have any):..
    },
    "name": {
      "tag-containing-data": ...,
      "attribute-of-tag": ...,
    }
    "extra-data-1": {
      "tag-containing-data": ...,
      "attribute-of-tag": ...,
    },
    "extra-data-2": {
      "tag-containing-data": ...,
      "attribute-of-tag": ...,
    }
  }

'''

SPECS = {
    "gov": {
        "title": {
            "tag": "strong",
            "attribute": "",
        },
        "name": {
            "tag": "a",
            "attribute": {"class": "tinmoi"},
        }
    },

    "defence": {
        "title": {
            "tag": "td",
            "attribute": {"align": "left"},
            "unused": {
                "tag": "strong",
                "attribute": "",
            }
        },
        "name": {
            "tag": "td",
            "attribute": {"align": "left"},
            "unused": {
                "tag": "strong",
                "attribute": "",
            }
        },
        "rank": {
            "tag": "td",
            "attribute": {"align": "left"},
            "unused": {
                "tag": "strong",
                "attribute": "",
            }
        }
    },

    "public_security": {
        "name": {
            "tag": "strong",
            "attribute": "",
        },
        "DOB": {
            "tag": "div",
            "attribute": {"class": "label"},
        },
        "ethnicity": {
            "tag": "div",
            "attribute": {"class": "label"},
        },
        "birthplace": {
            "tag": "div",
            "attribute": {"class": "label"},
        },
        "title": {
            "tag": "div",
            "attribute": {"class": "label"},
        }
    },

    # "foregin_affair": {
    #     "name": {
    #         "tag": "a",
    #         "attribute": "",
    #     },
    #     "title": {
    #         "tag": "a",
    #         "attribute": "",
    #     }
    # },

    "justice": {
        "name": {
            "tag": "a",
            "attribute": "",
        },
        "title": {
            "tag": "a",
            "attribute": "",
        }
    },
}

# +  -  -  - PARENT DIV'S TAGS & ATTRIBUTES -  -  - +

PARENT_DIV = {
    "gov": {
        "parent": {
            "tag": "td",
            "attribute": {"width": "100%", "valign": "top", "style": "background-image: url(/templates/govportal/chinhphu/images/bgr_page.jpg);"}
        },
        "children": {
            "tag": "td",
            "attribute": {"align": "center", "valign": "top"}
        }
    },

    "defence": {
        "parent": {
            "tag": "table",
            "attribute": {"class": "ta_border"}
        },
        "children": {
            "tag": "tr",
            "attribute": "",
        },
    },

    "public_security": {
        "parent": {
            "tag": "div",
            "attribute": {"class": "contentContainer"}
        },
        "children": {
            "tag": "div",
            "attribute": {"class": "info"},
        },
    },

    # "foreign_affair": {
    #     "parent": {
    #         "tag": "table",
    #         "attribute": {"id": "portal-columns"}
    #     },
    #     "children": {
    #         "tag": "td",
    #         "attribute": {"valign": "top"},
    #     },
    # },

    "justice": {
        "parent": {
            "tag": "div",
            "attribute": {"class": "content-news"}
        },
        "children": {
            "tag": "p",
            "attribute": {"class": "title"},
        },
    }
}

# +  -  -  - OFFICE TERM -  -  - +
OFFICE_TERM = "2016 - 2021"

# +  -  -  - ========================================================= -  -  - +

JUSTICE = {
    "url": "",

}
