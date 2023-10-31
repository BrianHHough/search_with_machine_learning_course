# Week 1 Exercises

Check to make sure the indexes are there: `GET /_cat/indices?v`
This should return something like this:
```json
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