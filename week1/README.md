# Week 1 Exercises

Check to make sure the indexes are there: `GET /_cat/indices?v`
This should return something like this:
```bash
health status index                                     uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .kibana_-152937574_admintenant_1          kUnDXzogTjShsBI7mcUV0g   1   0          1            0      5.1kb          5.1kb
green  open   .kibana_92668751_admin_1                  ZLgmJA-2TWCALeNAxfomcg   1   0         59            0     34.1kb         34.1kb
yellow open   security-auditlog-2023.10.30              J1X6D2nUTBKdR3jK6rOVeA   1   1         64            0    277.3kb        277.3kb
green  open   opensearch_dashboards_sample_data_flights 3mSunE6pTnyVgx04c1fRrQ   1   0      13059            0      5.9mb          5.9mb
yellow open   bbuy_queries                              i_krXHbJTcG__L9_4zHBNw   1   1    3730538            0    762.4mb        762.4mb
yellow open   bbuy_products                             toZa4IC1QIO1JR70QNK97g   1   1    1275077       360806      1.3gb          1.3gb
yellow open   search_fun_test                           EzBEA4GxQECOcbgZH-N-qA   1   1          4            0      6.9kb          6.9kb
green  open   .opendistro_security                      iln1t4KNQHC2PeYBnbzgtw   1   0         10            0     71.7kb         71.7kb
green  open   .kibana_1                                 GvnZo_00TL2H8Typ3ucrJQ   1   0          1            0      4.2kb          4.2kb
```

## Relevance

### Get the Top 10 most issued queries in the logs
The following query is a two-level aggregation on the BestBuy ecommerce dataset  and related product SKUs (Stock Keeping Units):
```bash
GET /bbuy_queries/_search
{
  "size": 0,
  "aggs": {
    "Query": {
      "terms": {
        "size": 10, 
        "field": "query.keyword"
      },
      "aggs":{
        "Docs":{
          "terms":{
            "size": 5,
            "field": "sku.keyword"
          }
        }
      }
    }
  }
}
```
The output looks like this:
```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "Query": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 3594136,
      "buckets": [
        {
          "key": "lcd tv",
          "doc_count": 33044,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 2642,
            "buckets": [
              {
                "key": "2620821",
                "doc_count": 14338
              },
              {
                "key": "2138389",
                "doc_count": 7150
              },
              {
                "key": "2893174",
                "doc_count": 5220
              },
              {
                "key": "1831054",
                "doc_count": 2520
              },
              {
                "key": "2047641",
                "doc_count": 1174
              }
            ]
          }
        },
        {
          "key": "2622037 2127204 2127213 2121716 2138291",
          "doc_count": 17062,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 12730,
            "buckets": [
              {
                "key": "2138291",
                "doc_count": 1308
              },
              {
                "key": "2622037",
                "doc_count": 950
              },
              {
                "key": "2127213",
                "doc_count": 864
              },
              {
                "key": "2127204",
                "doc_count": 708
              },
              {
                "key": "2121716",
                "doc_count": 502
              }
            ]
          }
        },
        {
          "key": "Hp touchpad",
          "doc_count": 14780,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 1048,
            "buckets": [
              {
                "key": "2842056",
                "doc_count": 8392
              },
              {
                "key": "2842092",
                "doc_count": 4806
              },
              {
                "key": "2947041",
                "doc_count": 226
              },
              {
                "key": "2884119",
                "doc_count": 170
              },
              {
                "key": "2884085",
                "doc_count": 138
              }
            ]
          }
        },
        {
          "key": "iPad",
          "doc_count": 11606,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 4484,
            "buckets": [
              {
                "key": "1945531",
                "doc_count": 4282
              },
              {
                "key": "2339322",
                "doc_count": 978
              },
              {
                "key": "1945595",
                "doc_count": 914
              },
              {
                "key": "2842056",
                "doc_count": 568
              },
              {
                "key": "2339386",
                "doc_count": 380
              }
            ]
          }
        },
        {
          "key": "hp touchpad",
          "doc_count": 11230,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 864,
            "buckets": [
              {
                "key": "2842056",
                "doc_count": 6226
              },
              {
                "key": "2842092",
                "doc_count": 3584
              },
              {
                "key": "2947041",
                "doc_count": 244
              },
              {
                "key": "2884119",
                "doc_count": 176
              },
              {
                "key": "2884085",
                "doc_count": 136
              }
            ]
          }
        },
        {
          "key": "iPhone 4s",
          "doc_count": 10800,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 4820,
            "buckets": [
              {
                "key": "3487648",
                "doc_count": 2044
              },
              {
                "key": "3487784",
                "doc_count": 1954
              },
              {
                "key": "3487675",
                "doc_count": 678
              },
              {
                "key": "3487693",
                "doc_count": 672
              },
              {
                "key": "3566966",
                "doc_count": 632
              }
            ]
          }
        },
        {
          "key": "ipad",
          "doc_count": 10072,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 3960,
            "buckets": [
              {
                "key": "1945531",
                "doc_count": 3798
              },
              {
                "key": "1945595",
                "doc_count": 808
              },
              {
                "key": "2339322",
                "doc_count": 794
              },
              {
                "key": "2842056",
                "doc_count": 428
              },
              {
                "key": "2408224",
                "doc_count": 284
              }
            ]
          }
        },
        {
          "key": "Beats",
          "doc_count": 9610,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 4804,
            "buckets": [
              {
                "key": "9836718",
                "doc_count": 1622
              },
              {
                "key": "9492426",
                "doc_count": 1326
              },
              {
                "key": "1232474",
                "doc_count": 818
              },
              {
                "key": "8913606",
                "doc_count": 548
              },
              {
                "key": "9492408",
                "doc_count": 492
              }
            ]
          }
        },
        {
          "key": "Touchpad",
          "doc_count": 9336,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 538,
            "buckets": [
              {
                "key": "2842056",
                "doc_count": 5436
              },
              {
                "key": "2842092",
                "doc_count": 2966
              },
              {
                "key": "2884119",
                "doc_count": 162
              },
              {
                "key": "2947041",
                "doc_count": 158
              },
              {
                "key": "2884085",
                "doc_count": 76
              }
            ]
          }
        },
        {
          "key": "LaborDay_Computers_20110902",
          "doc_count": 8856,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 5080,
            "buckets": [
              {
                "key": "1623912",
                "doc_count": 2838
              },
              {
                "key": "3031648",
                "doc_count": 266
              },
              {
                "key": "1415148",
                "doc_count": 236
              },
              {
                "key": "2845071",
                "doc_count": 230
              },
              {
                "key": "9873408",
                "doc_count": 206
              }
            ]
          }
        }
      ]
    }
  }
}
```
The results look like this:
![](./assets/bbuy_queries-top-10-most-issued-queries-1.png)
![](./assets/bbuy_queries-top-10-most-issued-queries-2.png)

Important to note:
- No normalization on the queries yet. Because of this: `Hp touchpad` and `hp touchpad` are distinct queries. Also, `iPad` and `ipad` are distinct queries too. 
    - An analyzer is usually needed to normalize queries, but sometimes it's helpful to see the raw queries directly to see how/what users are typing.
- Some weird queries, like this `LaborDay_Computers_20110902`, but it's more likely that the search engine made the query automatically, such as the user clicking a promo banner or ad.
- This is an example of nested aggregation, useful pattern for getting high-level view of searcher behavior.
    - The outer aggregation is on the query field (to search by query)
    - The inner aggregation groups each of these buckets by SKU
    - The result is the top-clicked SKUs for each query.

- Another weird query: `2622037 2127204 2127213 2121716 2138291`

Searching the queries for it looks like this: `GET /bbuy_queries/_search?q=query.keyword:"2622037 2127204 2127213 2121716 2138291"`

The results look like this:
```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": 5.3874235,
    "hits": [
      {
        "_index": "bbuy_queries",
        "_id": "EQ_afosBN-9G3tf62XC6",
        "_score": 5.3874235,
        "_source": {
          "user": "1e6af9cdc736be612f1ff5b66efdc6790907075a",
          "sku": 2343102,
          "category": "abcat0101001",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-04T13:40:51.508000",
          "query_time": "2011-10-04T13:36:41.786000"
        }
      },
      {
        "_index": "bbuy_queries",
        "_id": "6Q_afosBN-9G3tf63XD_",
        "_score": 5.3874235,
        "_source": {
          "user": "1ad676897f2bf9a860beb38a04bca5bf6f8edf8b",
          "sku": 2127213,
          "category": "abcat0101001",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-06T20:37:13.942000",
          "query_time": "2011-10-06T20:36:17.519000"
        }
      },
      {
        "_index": "bbuy_queries",
        "_id": "TA_afosBN-9G3tf64XIr",
        "_score": 5.3874235,
        "_source": {
          "user": "1e76bb8cd468f29b782c23c18b928117325f7ec3",
          "sku": 2121716,
          "category": "abcat0101001",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-06T21:07:43.760000",
          "query_time": "2011-10-06T21:07:24.174000"
        }
      },
      {
        "_index": "bbuy_queries",
        "_id": "oA_afosBN-9G3tf64nNL",
        "_score": 5.3874235,
        "_source": {
          "user": "1ae53d76566b5c10c76f16cd25d668809462762c",
          "sku": 1934087,
          "category": "abcat0302013",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-04T20:33:22.969000",
          "query_time": "2011-10-04T20:32:08.278000"
        }
      },
      {
        "_index": "bbuy_queries",
        "_id": "Hg_afosBN-9G3tf65nT_",
        "_score": 5.3874235,
        "_source": {
          "user": "1ae9c8d9dc8792e5d33c9428713f8656778071a7",
          "sku": 2127204,
          "category": "abcat0101001",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-07T13:23:03.843000",
          "query_time": "2011-10-07T13:22:11.749000"
        }
      },
      {
        "_index": "bbuy_queries",
        "_id": "Hw_afosBN-9G3tf65nT_",
        "_score": 5.3874235,
        "_source": {
          "user": "1ae9c8d9dc8792e5d33c9428713f8656778071a7",
          "sku": 2127213,
          "category": "abcat0101001",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-07T13:25:09.964000",
          "query_time": "2011-10-07T13:22:11.749000"
        }
      },
      {
        "_index": "bbuy_queries",
        "_id": "Pg_afosBN-9G3tf65nT_",
        "_score": 5.3874235,
        "_source": {
          "user": "1aeada7b63e991ad937479563480ad76bd5d1823",
          "sku": 3184708,
          "category": "pcmcat247400050000",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-03T16:26:02.110000",
          "query_time": "2011-10-03T16:24:59.948000"
        }
      },
      {
        "_index": "bbuy_queries",
        "_id": "Dw_afosBN-9G3tf65nX_",
        "_score": 5.3874235,
        "_source": {
          "user": "1af14d261011bc6078271c42e3b16b61f5480e32",
          "sku": 2864446,
          "category": "cat02015",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-08T17:20:59.552000",
          "query_time": "2011-10-08T17:20:09.895000"
        }
      },
      {
        "_index": "bbuy_queries",
        "_id": "EA_afosBN-9G3tf65nX_",
        "_score": 5.3874235,
        "_source": {
          "user": "1af14d261011bc6078271c42e3b16b61f5480e32",
          "sku": 2864437,
          "category": "cat02015",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-08T17:21:27.793000",
          "query_time": "2011-10-08T17:20:09.895000"
        }
      },
      {
        "_index": "bbuy_queries",
        "_id": "jw_afosBN-9G3tf67Hdz",
        "_score": 5.3874235,
        "_source": {
          "user": "1aff80a2e01232123797e6fb37b3472ecc4326cf",
          "sku": 3590335,
          "category": "pcmcat247400050000",
          "query": "2622037 2127204 2127213 2121716 2138291",
          "click_time": "2011-10-06T21:39:02.913000",
          "query_time": "2011-10-06T21:36:46.614000"
        }
      }
    ]
  }
}
```
![](./assets/bbuy_queries-top-10-most-issued-queries-3.png)


I search for an individual SKU with this: `GET /bbuy_products/_search?q=sku:2622037`

This returns this value -- a product: "Dynex™ - 19" Class - LED - 720p - 60Hz - HDTV" with productId `1218341074520`
```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 13.902227,
    "hits": [
      {
        "_index": "bbuy_products",
        "_id": "2622037",
        "_score": 13.902227,
        "_source": {
          "productId": [
            "1218341074520"
          ],
          "sku": [
            "2622037"
          ],
          "name": [
            """Dynex™ - 19" Class - LED - 720p - 60Hz - HDTV"""
          ],
          "type": [
            "HardGood"
          ],
          "startDate": [
            "2011-07-24"
          ],
          "active": [
            "false"
          ],
          "regularPrice": [
            "159.99"
          ],
          "salePrice": [
            "159.99"
          ],
          "artistName": [],
          "onSale": [
            "false"
          ],
          "digital": [
            "false"
          ],
          "frequentlyPurchasedWith": [
            "9873241",
            "9881768",
            "9344934",
            "9881886",
            "9004356",
            "1065552",
            "1041455",
            "8939839",
            "3219034",
            "1080293"
          ],
          "accessories": [],
          "relatedProducts": [],
          "crossSell": [],
          "salesRankShortTerm": [
            "85551"
          ],
          "salesRankMediumTerm": [
            "23226"
          ],
          "salesRankLongTerm": [
            "18213"
          ],
          "bestSellingRank": [
            "85581"
          ],
          "url": [],
          "categoryPath": [
            "Best Buy",
            "TV & Home Theater",
            "TVs",
            "All Flat-Panel TVs"
          ],
          "categoryPathIds": [
            "cat00000",
            "abcat0100000",
            "abcat0101000",
            "abcat0101001"
          ],
          "categoryLeaf": [
            "abcat0101001"
          ],
          "categoryPathCount": 4,
          "customerReviewCount": [
            "119"
          ],
          "customerReviewAverage": [
            "4.2"
          ],
          "inStoreAvailability": [
            "false"
          ],
          "onlineAvailability": [
            "false"
          ],
          "releaseDate": [],
          "shippingCost": [
            "0.00"
          ],
          "shortDescription": [
            """ENERGY STAR Qualified
Best Buy Exclusive"""
          ],
          "shortDescriptionHtml": [
            "<font color=#0099ff><b>ENERGY STAR Qualified</b></font><br/><b>Best Buy Exclusive</b>"
          ],
          "class": [
            "SMALL FPTV 0-31\""
          ],
          "classId": [
            "478"
          ],
          "subclass": [
            "SMALL LCD"
          ],
          "subclassId": [
            "5151"
          ],
          "department": [
            "VIDEO"
          ],
          "departmentId": [
            "2"
          ],
          "bestBuyItemId": [
            "1590410"
          ],
          "description": [],
          "manufacturer": [
            "Dynex"
          ],
          "modelNumber": [
            "DX-19E220A12"
          ],
          "image": [
            "http://images.bestbuy.com/BestBuy_US/images/products/2622/2622037_rc.jpg"
          ],
          "condition": [
            "New"
          ],
          "inStorePickup": [
            "false"
          ],
          "homeDelivery": [
            "false"
          ],
          "quantityLimit": [
            "1"
          ],
          "color": [],
          "depth": [],
          "height": [],
          "weight": [
            "6.4 lbs. with stand (5.9 lbs. without)"
          ],
          "shippingWeight": [
            "7.9366"
          ],
          "width": [
            "17.9\""
          ],
          "longDescription": [
            "This Dynex LED HDTV combines rich 5000:1 dynamic contrast, high 250 cd/m² brightness and wide 170° horizontal and 160° vertical viewing angles to enhance the sharpness and detail of your viewing experience."
          ],
          "longDescriptionHtml": [
            "This Dynex LED HDTV combines rich 5000:1 dynamic contrast, high 250 cd/m² brightness and wide 170° horizontal and 160° vertical viewing angles to enhance the sharpness and detail of your viewing experience."
          ],
          "features": [
            """18-1/2" screen measured diagonally from corner to corner
For optimal viewing in kitchens and small rooms.""",
            """Ultraslim design less than 1-3/4" deep
Comes with a table stand or can be mounted on a wall (with optional mounting kit, not included). VESA 100mm x 100mm compliant.""",
            """Incredible dynamic contrast ratio (5000:1)
For enhanced image color and vibrancy.""",
            """High brightness (250 cd/m²)
Offers an arresting viewing experience.""",
            """1366 x 768 pixel resolution
Supports 720p signals for stunning image clarity.""",
            """Two 3W speakers
Deliver simulated surround sound.""",
            """Sound leveler
Prevents fluctuations in sound that tend to happen when TV shows go to commercials or movie soundtracks play.""",
            """Inputs
Include 1 HDMI, 1 composite, 1 component video, 1 PC/VGA, and one 3.5mm PC audio.""",
            """Outputs
Include 1 analog audio.""",
            """1 HDMI input
HDMI cable not included. High-speed HDMI cable is the only connection that can deliver a full HDTV experience complete with an optimum picture and digital surround sound.""",
            """DVI interface
Provides a direct digital-to-digital video hookup with compatible devices.""",
            """Useful additional features
Include channel labeling and a sleep timer."""
          ]
        }
      }
    ]
  }
}
```
![](./assets/bbuy_queries-top-10-most-issued-queries-4.png)


## Relevance Judgements

### Create the Search Template
Use the search template below, add this to the OpenSearch DevTools console, and then execute it to create the hand-tuned ranking search:
```bash
# Create the Search Template - Had to remove the Gaussian decay functions 
POST _scripts/hello_world_template
{
  "script": {
    "lang": "mustache",
    "source": {
      "size": 10,
      "_source": ["sku", "name", "shortDescription"],
      "query": {
        "function_score": {
          "query": {
            "bool": {
              "should": [
                {
                  "match": {
                    "name": {
                      "query": "{{user_query}}",
                      "fuzziness": "1",
                      "prefix_length": 2,
                      "boost": 0.01
                    }
                  }
                },
                {
                  "match_phrase": {
                    "name.hyphens": {
                      "query": "{{user_query}}",
                      "slop": 1,
                      "boost": 50
                    }
                  }
                },
                {
                  "multi_match": {
                    "query": "{{user_query}}",
                    "type": "phrase",
                    "slop": "6",
                    "minimum_should_match": "2<75%",
                    "fields": [
                      "name^10",
                      "name.hyphens^10",
                      "shortDescription^5",
                      "longDescription^5",
                      "department^0.5",
                      "sku",
                      "manufacturer",
                      "features",
                      "categoryPath"
                    ]
                  }
                },
                {
                  "terms": {
                    "sku": ["\"{{#user_query_split}}\",\"{{/user_query_split}}\""],
                    "boost": 50.0
                  }
                },
                {
                  "match": {
                    "name.hyphens": {
                      "query": "{{user_query}}",
                      "operator": "OR",
                      "minimum_should_match": "2<75%"
                    }
                  }
                }
              ],
              "minimum_should_match": 1
            }
          },
          "boost_mode": "multiply",
          "score_mode": "sum",
          "functions": [
            {
              "script_score": {
                "script": "0.0001"
              }
            }
          ]
        }
      }
    },
    "params": {
      "user_query": "",
      "user_query_split": []
    }
  }
}
```

Once run, this should return: 
```json
{
  "acknowledged": true
}
```

### Use the Search Template

```bash
GET bbuy_products/_search/template
{
  "id": "hello_world_template",
  "params": {
    "user_query": "lcd tv",
    "user_query_split": ["lcd", "tv"]
  }
}
```
![](./assets/relevance_judgements-lcd-tv.png)



```bash
GET bbuy_products/_search/template
{
  "id": "hello_world_template",
  "params": {
    "user_query": "ipad",
    "user_query_split": ["ipad"]
  }
}
```
![](./assets/relevance_judgements-ipad.png)


```bash
GET bbuy_products/_search/template
{
  "id": "hello_world_template",
  "params": {
    "user_query": "Touchpad",
    "user_query_split": ["Touchpad"]
  }
}
```
![](./assets/relevance_judgements-touchpad.png)

```bash
GET bbuy_products/_search/template
{
  "id": "hello_world_template",
  "params": {
    "user_query": "Beats",
    "user_query_split": ["Beats"]
  }
}
```
![](./assets/relevance_judgements-beats.png)

To collect relevance judgments, create a table with one row per query-result pair (for the top results for each query), where each row contains the following columns:
- Query.
- Summary of searcher intent. For example, if the query is “Beats”, that summary might be “Beats by Dr. Dre headphones” or “Over the ear headphones by Dr. Dre”.
- Product Id
- Product Name
- “Relevant” or “Not Relevant”

This process works best when there are multiple judges, and overlapping judgements so that each query-result pair is judged independently by at least 2 people. Then you can ask the following questions:
- Where did judges agree and disagree on your relevance judgments? Why?
- What fraction of results where relevant overall? Which queries performed best / worst?
- What were the ranks of the first relevant results?
- What kinds of mistakes did the search engine make? Can you identify potential causes?




# Measuring Relevance
- 2 paths to measure relevance:
  - Try to pout ourselves or others in the minds of searchers and make their judgments
  - Infer users' info needs from behavior (i.e. engagements in the platform)
- We want to make decisions based on aggregate data (collected at whatever scale we can afford)
  - Don't want decisions made based on one person's oponion (judge, user, or dev), or the highest paid person's opinion, or most expensive customer

- 2 ways to collect judgments:
  - Explicit human judgments: manually assign labels to rep sample of content you want to classify
    - But, it's expensive (time + money) and requires human judges to put themselves in position of users
  - Implicit behavioral judgments: mine user behavior (e.g. click data) to collect
    - Low cost, and judges are users
    - But, presentation bias since users only engage with content presented to them and conflates relevancy with desirability and other factors (i.e. user skiips relevant results and may decide to click on irrelevant results out of curiosity)
  
- What to collect in logs for search queries:
  - **Query**: what the user typed into the search box, ​​what the application sent to the search engine.
  - **Parameters**: any categories, facets, or other filters, as well as user-specified sort.
  - **Session**: timestamp, session id, referrer URL, etc.
  - **User**: id if user is logged in, IP address, device, browser, etc.
  - **Results**: ids and titles of all displayed results (with positions), pagination or scrolling information, summary information like number of results and facet counts. In other words, log everything that might influence a user to pick a search result.
  - **Engagement**: which results were clicked or had further engagement like a purchase.
  - **System**: index version, names and versions of ML models, A/B treatments, etc.
- Additional:
  - Track original query and spelling suggestions (+ where those suggestions automatically applied or just suggested to the user as "did you mean?")
  - Typeahead / autocomplete functionality, track both the characters the user typed and the selection completed

- Key Metrics:
  - **Precision (P)**: the proportion of search results that are relevant, with a common practice being to evaluate the precision of the top 10 results, or P@10, and to place higher importance on the ranking of these results using measures like average precision.
  - **Recall (R)**: the percentage of all relevant documents that are successfully retrieved, though it's challenging to quantify as the total number of relevant documents is often unknown, and it's recognized that there is a trade-off between recall and precision, particularly vital in research and legal discovery.
  - **Mean Reciprocal Rank (MRR)**: calculated by averaging the reciprocal (the reciprocal of x is 1/x) ranks of the first relevant result across multiple queries, serving well for both explicit and implicit feedback, and is particularly relevant when a single correct result is expected, with the preference being to count non-clicked queries as zero to avoid inflated performance measures. 
  - **Discounted Cumulative Gain (DCG)**: evaluates the quality of search results by giving more weight to the relevance of higher-ranked results and is nuanced enough to accommodate graded relevance, making it a favorite for businesses where minor changes in search result quality can have significant revenue implications.
  - Simple metrics:
    - Track when return zero results. It's better to show nothing than to confidently show garbage... but in general, no results means something went wrong
    - Find out if there's a way to satisfy user's needs or offer them something that's better than nothing.

- Simple things to do now (shoestring budget)
  - Collect behavioral data for implicit judgments: in-app analytics, log all results shown to the user (to show negative examples), or log representative random sample of sessions or users as large as resources practically allow.
  - Establish ongoing query triage process: on regular basis (i.e. monthly), as well as when major changes or notice any sudden changes in biz metrics... have team each judge results for first 50 most frequent queries and for a random sample of less frequent queries. Calculate key metrics like percision and MRR, and keep those in a spreadsheet or dashboard.
  - Pay close attention to agreement among judges: if folks disagree too often, need to align team.
  - Test in dev before going to prod how a change affects metrics


# Vectors and Token Weights
- Lucene: search engine core of Solr, Elastic, and OpenSearch ([link](https://lucene.apache.org/))
- Token-weighting approaches:
  - tf-idf ([link](https://en.wikipedia.org/wiki/Tf%E2%80%93idf))
  - BM25 ([link](https://en.wikipedia.org/wiki/Okapi_BM25))

- Purpose here is to measure similarity between queries and documents to return docs closest to the query
  - Similarity and closeness are what we are after
  - Vectors: line segment from origin to a point in space (aka our documents and queries)
    - We're using an abbreviation of the Pythangorean Theorem (a² + b² = c²), not to get the length of a vector, but to get its direction from the origin.
    - In a 3D plane, vectors correspond to points on a unit sphere.
    - Use the cosine of the angle (b/c degrees and radians aren't easy to work with directly), which is equal to:
      - 1 at 0 degrees (same direction)
        - A cosine of 1 means 2 vectors point in the same direction, meaning the two vectors are identical
        - Sorting results by cosine is a way of sorting by similarity to the query.
      - -1 at 180 degrees (opposite direction)
      - 0 at 90 degress (right angle)
    - Smaller angle = closer the cosine is to 1, and the more similar the two vectors are
    - Larger angle = farther the cosine is from 1, and the more different the two vectors are
  - Query_Doc_Similarity = cosine(θ)
    - θ = degrees of angle made between Query line and Document line
  - Vector Space: language as a space with thousands of dimensions, one for each word
    - Documents and queries mean the space has hundereds or thousands of dimensions
    - Vector is just like a point, and its coordinates are 1 for each words it contains and 0 for all other words, since most coords are 0s, these are sparse vectors

Example: Represent pre-read materials as vectors like this:

| Doc | brown | dog | dogs | fox | jumped | lazy | lead | out | over | paint |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Doc A | 1 |   | 1 | 1 | 1 | 1 | 1 |   | 1 |   |
| Doc B |   | 1 |   | 1 | 1 |   | 1 |   |   |   |
| Doc C | 1 |   |   |   |   |   | 1 |   |   |   |

Example: Represent queries as vectors:

| Doc | brown | dog | dogs | fox | jumped | lazy | lead | out | over | paint |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| brown dog  | 1 | 1 |   |   |   |   |   |   |   |   |
| lazy fox   |   |   |   | 1 |   | 1 |   |   |   |   |

- Operations with vectors:
  - **Dot product**: scalar value resulting from multiplying the corresponding entries of the two sequences of numbers and then summing those products.
    ```bash
    a * b = (a1 * b1) + (a2 * b2) + ... + (an * bn)
    ```
  - **Cosine**: cosine of the angle θ between two vectors is a measure of how much they point in the same direction.
    ```bash
    cos(θ) = (a * b) / (||a|| * ||b||)
    ```
    - When both vectors are unit vectors (have a magnitude of 1), the dot product gives you the cosine of the angle between them.
    - Math: `a * b = cos(θ)`

  - Dot product of two vectors: form of multiplication where line up 2 arrays, multiply each pair of values from same dimension, and take sum of those products:

  ```bash
  a = (1,4,-2)
  b = (-2,1,7)
  a * b = 1 * (-2) + 4 * 1 + (-2) * 7
  = -2 + 4 - 14 = -12
  ```

- To measure similarity between two vectors (a query and a document)...
  - If two vectors are unit vectors (are of length 1), then you compute their dot product
    - To measure length of vector, compute square root of dot product with itself (aka Pythagorean Theorem)
  - If a vector isn't a unit vector (not of length 1), then normalize it by dividing the vector (dividing each element of the vector) by the length of the vector
    - This looks like:
      ```bash
      ||a|| = √(a * a)
      cos(θ) = (a * b) / ||a||||b||
      ```
    - Example: compute the cosine between the vectors `(1, -2, -2)` and `(2, -1, 2)`
      - Normalize `(1,-2,2)` into unit vector, compute it's length as square root of sum of squares of the components.
        - The magnitude of vector `a` is:
        ```bash
        ||a|| = √(1² + (-2)² + 2²) = √(9) = 3
        ```
        - Resulting `a` unit vector is: `(1/3, -2/3, 2/3)`
      - Normalize `(2, -1, 2)` into unit vector
        - The magnitude of vector `b` is:
        ```bash
        ||b|| = √(2² + (-1)² + 2²) = √(9) = 3
        ```
        - Resulting `b` unit vector is: `(2/3, -1/3, 2/3)`
      - Take dot product to obtain cosine: 
        ```bash
        dp = a * b = (1/3 * 2/3) + (-2/3 * -1/3) + (2/3 * 2/3)
        dp = a * b = (2/9) + (2/9) + (4/9)
        dp = a * b = (8/9)
        dp = 8/9 != 0
        ```
      - The dot product (aka cosine) is 8/9, and does not qual 0, implying that the vectors are not orthogonal (not at right angles to each other), and have positive cosine similarity, meaning there is an acute angle between them.

- Use `tf-idf` to assign token weights for coordinates instead of giving them a weight of 1
  - Give weight (significance) to tokens we believe to be important.
  - A token repeated in a doc is more important to a doc. Measure this as a term frequency (`tf`), optionally normalizing to the doc length.
  - A token occuring in fewer docs in index is more important to the docs in which it occurs. Measure this as the inverse doc frequency (`idf`), and use the negative of the logarithm of the inverse document frequency.
  - The `tf-idf` is the product of these two quantities: `tf * idf`

- Example:


| Documents | Analysis | Equation |
|----------|----------|----------|
| dog, dogs, lazy, out, ... | Occurs in 1 document | -log(1/3) = 0.477 |
| brown, fox, jumped, lead | Occurs in 2 documents | -log(2/3) = 0.176 |
| red | Occurs in 3 documents | -log(3/3) = 0 |

To analyze the `tf-idf` scores, let's review the data again:

| Doc | brown | dog | dogs | fox | jumped | lazy | lead | out | over | paint |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Doc A | 1 |   | 1 | 1 | 1 | 1 | 1 |   | 1 |   |
| Doc B |   | 1 |   | 1 | 1 |   | 1 |   |   |   |
| Doc C | 1 |   |   |   |   |   | 1 |   |   |   |

### Calculate the `tf-idf` score of "dog"
- "dog" appears in only 1 doc (Doc B) of the 3
- Calculate this with the equation:
  ```bash
  IDF(t) = -log(N/nt)
    N = number of docs in collection
    nt = number of docs where term t appears
  IDF = -log(1/3)
  IDF = -(-0.477)
  IDF = 0.477

  TF assumed to be 1
  TF-IDF = 1 * 0.477
  TF-IDF = 0.477
  ```

### Calculate the `tf-idf` score of "fox"
- "fox" appears in 2 docs (Doc A and B) of the 3
- Calculate this with the equation:
  ```bash
  IDF(t) = -log(N/nt)
    N = number of docs in collection
    nt = number of docs where term t appears
  IDF = -log(2/3)
  IDF = -(-0.176)
  IDF = 0.176

  TF assumed to be 1
  TF-IDF = 1 * 0.176
  TF-IDF = 0.176
  ```

### Calculate the `tf-idf` score of "lead"
- "lead" occurs in all 3 docs (3/3)
- Calculate this with the equation:
  ```bash
  IDF(t) = -log(N/nt)
    N = number of docs in collection
    nt = number of docs where term t appears
  IDF = -log(3/3)
  IDF = -(0)
  IDF = 0

  TF assumed to be 1
  TF-IDF = 1 * 0
  TF-IDF = 0
  ```

- In general, `tf-idf` favors words repeated in docs (making tf higher), but infrequent in the index (making idf higher)
- Indexing is an opportunity to compute tf values for reach doc token, and compute idf values for each token when all docs are indexed.
  - To use values for ranking, important they be efficiently available at run time, meaning we store weights as payloads in the inverted index.
  - Search engine should do this automatically but this is an FYI
- Document size matters - the tf size can be normalized by doc length... if this doesn't happen, then `tf * idf` score can favor long docs over short ones, leading to inaccurate relevant results.
  - Normalizing tf by doc length is contentious, but important to consider

# How Search Engines Work
- Most engines have multi-phase ranking approach:
  - Start with relatively cheap scoring function (`tf-idf` or `BM25`)
  - Reduce results to the top scoring docs from that function
  - Proceed with a series of more sophisticated and expensive scoring functions on successively smaller subsets of results
- OpenSearch calls this above rescoring, or cascading ranking - results cascade fromone ranker to the next until final results returned.
- Multiphase ranking approach is computationally efficient, addresses concerns like search result diversity and business rules
- After many changes and tweaks, Machine learning comes in so that humans make relevance judgments and machine optimizes a scoring function based on those judgments.

# Query-Dependent vs. Query-Independent Signals
- **Query-dependent signals**: relate the query to the document and are good for determining relevance.
  - Include the tf-idf and BM25 scores, and can be simpler (e.g. # of query tokens that overlap with tokens in the doc's title field) or more complex (e.g. cosine usng a machine-learned vector space)
  - Tend to be at the heart of relevance, focusing on the relationship between doc and query.
- **Query-independent signals**: ignore the query and are good for determining desirability.
  - Include a doc's popularity, or in context like ecommerce - the price, sales, rank
  - Less about relevance and more about desirability
  - Indicate which relevant results users actually want
  - Drive clicks and purchases just as much as relevance, so these signals make a big difference
  - Can compute these offline, so it's cheap and easy to use them for sorting results at run-time.
- Strategy: use query-dependent signals to determine set of relevant results, and then use query-independent signals to sort the relevant results by their desirability.

# Common Techniques
- **Analyzers**: Refine the quality of tokens extracted from text for improved indexing and ranking by utilizing stemming, punctuation handling, and NLP tools, mindful of language nuances and reindexing needs.
- **Field and document boosting**: Adjust search importance of specific fields or documents to enhance relevance signals, using a straightforward approach with significant impact.
- **Content understanding**: Leverage external resources, rules, or machine learning to enrich content representation in the index for better retrieval and ranking.
- **Synonyms**: Enhance recall by mapping different terms to the same concepts, but manage synonym lists carefully to avoid contextually inappropriate matches.
- **Autophrasing**: Increase precision by identifying and treating multi-token phrases as single semantic units in queries, such as “dress shirt.”
- **Query understanding**: Improve how queries are interpreted and matched using external resources, rules, or machine learning to reflect user intent better.
- **Learning to rank (LTR)**: Employ machine learning for scalable and systematic ranking optimization, based on available data.
- **Pseudo relevance feedback**: Utilize initial search results to refine and discover more pertinent information, despite higher computational costs.
- **Experimentation**: Test different indexing and ranking strategies through offline analysis and online A/B testing to find the most effective approach.
- **Manual overrides**: Apply direct, specific adjustments to search responses for immediate problem-solving, avoiding over-reliance that can lead to complex management issues.
- **User experience**: Address search challenges not only with retrieval and ranking but also through user interface features like autocomplete, faceted search, and spelling correction.

# Relevance Tuning Pitfalls
- **Overfitting**: Avoid crafting models that only excel on specific training data without generalizing well to new, real-world data.
- **Failure to iterate**: Embrace an agile, iterative process for relevance tuning, understanding that initial attempts are unlikely to be perfect.
- **Premature Optimization**: Resist tuning relevance too finely before having substantial data and user feedback to guide decisions.
- **Relying on anecdotal data (anecdata)**: Base relevance adjustments on comprehensive data rather than isolated, possibly non-representative, anecdotes.
- **Lack of tracking or infrastructure**: Ensure the necessary infrastructure for tracking and analyzing search data is in place before attempting relevance tuning.
- **Ignorance of tradeoffs**: Recognize the inherent tradeoffs in relevance tuning, especially between precision and recall, and make informed decisions accordingly.
- **Pursuing diminishing returns**: Be aware of the point at which further investment in relevance tuning yields progressively smaller benefits.
- **Tunnel vision**: Consider the larger context of search sessions and user interactions beyond the search box when addressing relevance.
- **Configuration issues**: Verify that poor search performance isn't due to basic configuration errors before delving into more complex relevance issues.

# Multi-Phase Ranking and LTR

Goal: apply multi-phase ranking to implement learning to rank (LTR) by combining a rules-based approach with a machine learning approach.

- using a multi-phase ranking appraoch manages the tradeoff between model quality and efficiency/speed.
  - Example: 1st ranker uses BM25, then next ranker could feed its 1000 top-scoring results to a classifier, which could feed top 100 results to a more expensive model to obtain final ranking.
  - Stakes increase when focus on the top few results (huge engagement drop between first and second positions)
  - OpenSearch has a **rescoring framework** so that we don't need to fetch a large number of results, score them, send them onto the next ranker, etc. all manually.

## Rescoring
- Using values in a doc, along with a user-defined function, as part of scoring
- OpenSearch/Elastic calls this Function Score query - which can be expensive, making it a good candidate for rescoring
- Basic tool for multi-phase ranking: after scoring using one approach, pick off its top-scoring results and rescore them with another approach.

### Run baseline simple match all query on the `searchml_test` index

If this index doesn't exist yet, create this in the OpenSearch console:
```bash
PUT /searchml_test/_doc/doc_a
{
  "id": "doc_a",
  "title": "Fox and Hounds",
  "body": "The quick red fox jumped over the lazy brown dogs.",
  "price": "5.99",
  "in_stock": "true",
  "category": "childrens"}

PUT /searchml_test/_doc/doc_b
{
    "id": "doc_b",
    "title": "Fox wins championship",
    "body": "Wearing all red, the Fox jumped out to a lead in the race over the Dog.",
    "price": "15.13",
    "in_stock": "true",
    "category": "sports"}

PUT /searchml_test/_doc/doc_c
{
    "id": "doc_c",
    "title": "Lead Paint Removal",
    "body": "All lead must be removed from the brown and red paint.",
    "price": "150.21",
    "in_stock": "false",
    "category": "instructional"}

PUT /searchml_test/_doc/doc_d
{
        "id": "doc_d",
        "title": "The Three Little Pigs Revisted",
        "price": "3.51",
        "in_stock": "true",
        "body": "The big, bad wolf huffed and puffed and blew the house down. The end.",
        "category": "childrens"}
```

By running this baseline query:
```bash
GET searchml_test/_search
{
  "query": {
      "bool": {
          "must": [
              {"match_all": {}}
          ],
          "filter": [
              {"term": {"category": "childrens"}}
          ]
      }
  }
}
```
This is the output:
```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "searchml_test",
        "_id": "doc_a",
        "_score": 1,
        "_source": {
          "id": "doc_a",
          "title": "Fox and Hounds",
          "body": "The quick red fox jumped over the lazy brown dogs.",
          "price": "5.99",
          "in_stock": "true",
          "category": "childrens"
        }
      },
      {
        "_index": "searchml_test",
        "_id": "doc_d",
        "_score": 1,
        "_source": {
          "id": "doc_d",
          "title": "The Three Little Pigs Revisted",
          "price": "3.51",
          "in_stock": "true",
          "body": "The big, bad wolf huffed and puffed and blew the house down. The end.",
          "category": "childrens"
        }
      }
    ]
  }
}
```

Now, run a rescoring query:

```bash
POST searchml_test/_search
{
  "query": {
      "bool": {
          "must": [
              {"match_all": {}}
          ],
          "filter": [
              {"term": {"category": "childrens"}}
          ]
      }
  },
  "rescore": {
    "query": {
      "rescore_query":{
        "function_score":{
          "field_value_factor": {
            "field": "price",
            "missing": 1
          }
        }
        
      },
      "query_weight": 1.0,
      "rescore_query_weight": 2.0
    },
    "window_size": 1 
  }
}
```

Output of this is:
```json
{
  "took": 105,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 12.98,
    "hits": [
      {
        "_index": "searchml_test",
        "_id": "doc_a",
        "_score": 12.98,
        "_source": {
          "id": "doc_a",
          "title": "Fox and Hounds",
          "body": "The quick red fox jumped over the lazy brown dogs.",
          "price": "5.99",
          "in_stock": "true",
          "category": "childrens"
        }
      },
      {
        "_index": "searchml_test",
        "_id": "doc_d",
        "_score": 1,
        "_source": {
          "id": "doc_d",
          "title": "The Three Little Pigs Revisted",
          "price": "3.51",
          "in_stock": "true",
          "body": "The big, bad wolf huffed and puffed and blew the house down. The end.",
          "category": "childrens"
        }
      }
    ]
  }
}
```

### 🐞 Debugging: Error running rescoring query: `illegal_argument_exception` - Text fields are not optimised for operations that require per-document field data like aggregations and sorting

I got this error after doing the PUTs and then running the above rescoring query:
```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [price] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "searchml_test",
        "node": "aTFYW_tGScGCPHJazjKLsQ",
        "reason": {
          "type": "illegal_argument_exception",
          "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [price] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
        }
      }
    ],
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [price] in order to load field data by uninverting the inverted index. Note that this can use significant memory.",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [price] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
      }
    }
  },
  "status": 400
}
```

This is because `price` is treated as a text field, not for numeric operations to perform sorting or aggregations. It seems the mapping for index not been set explicitly so the `price` field can't be inferred by OpenSearch b/c of the quotes.

To fix this:
- Delete Index:
  ```bash
  DELETE /searchml_test
  ```

- Define correct mappings for index before index any docs - tell OS the `price` field is numeric and not text
  ```bash
  PUT /searchml_test
  {
    "mappings": {
      "properties": {
        "id": { "type": "keyword" },
        "title": { "type": "text" },
        "body": { "type": "text" },
        "price": { "type": "float" },
        "in_stock": { "type": "boolean" },
        "category": { "type": "keyword" }
      }
    }
  }
  ```

  This should give an output:
  ```json
  {
    "acknowledged": true,
    "shards_acknowledged": true,
    "index": "searchml_test"
  }
  ```

- Re-index docs with correct mappings
  ```bash
  PUT /searchml_test/_doc/doc_a
  {
    "id": "doc_a",
    "title": "Fox and Hounds",
    "body": "The quick red fox jumped over the lazy brown dogs.",
    "price": 5.99,
    "in_stock": true,
    "category": "childrens"
  }

  ... [Repeat for other documents]
  ```

- Run `rescore` query again after mappings and docs correctly set up
  - Change "window_size": 1 to a larger number to rescore more than just the top document, as window_size defines the number of top documents to be rescored.

  