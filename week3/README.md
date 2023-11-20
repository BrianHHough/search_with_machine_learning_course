


# Query Rewriting

## Manual Classification

Run:
```bash
python /workspace/search_with_machine_learning_course/utilities/categoryViewer.py --max_depth 2
```
Output:
```bash
Best Buy
Best Buy > Appcessories™
Best Buy > Appliance Install Delivery Repair
Best Buy > Appliances
Best Buy > Audio & MP3
Best Buy > Best Buy For Business
Best Buy > Best Buy Gift Cards
Best Buy > Buy Back Program
Best Buy > Cameras & Camcorders
Best Buy > Car, Marine & GPS
Best Buy > Computers & Tablets
Best Buy > Customer Service
Best Buy > Deal of the Day
Best Buy > Deals Near Me
Best Buy > Featured Offers
Best Buy > Financing and Rewards
Best Buy > Geek Squad
Best Buy > Geek Squad Protection
Best Buy > Gift Center
Best Buy > Health, Fitness & Sports
Best Buy > Home
Best Buy > Magnolia Home Theater
Best Buy > Mobile Phones
Best Buy > Movies & Music
Best Buy > Musical Instruments
Best Buy > Name Brands
Best Buy > Office
Best Buy > Online Trade In
Best Buy > Outlet Center
Best Buy > Recycling
Best Buy > TV & Home Theater
Best Buy > Video Games
```

## Heuristic Classification

Run:
```bash
cd /workspace/search_with_machine_learning_course/week3
head /workspace/datasets/train.csv | cut -d , -f3 | python 
```
Output:
```bash
Best Buy > TV & Home Theater > TVs
Best Buy > TV & Home Theater > TVs
Best Buy > Computers & Tablets > E-Readers
Best Buy > TV & Home Theater > TVs
Best Buy > TV & Home Theater > TVs
Best Buy > Magnolia Home Theater > Televisions
Best Buy > Computers & Tablets > Laptop & Netbook Computers
Best Buy > Mobile Phones > Mobile Phone Accessories
Best Buy > TV & Home Theater > TVs
```

Run:
```bash
grep touchpad /workspace/datasets/train.csv | cut -d',' -f3 | python leavesToPaths.py --max_depth 3 | sort | uniq -c | sort -nr | head
```
Output:
```bash
  17995 Best Buy > Computers & Tablets > Tablets & iPad
    166 Best Buy > Computers & Tablets > Laptop & Netbook Computers
     70 Best Buy > Computers & Tablets > E-Readers
     61 Best Buy > Computers & Tablets > Mice & Keyboards
     34 Best Buy > TV & Home Theater > TVs
     33 Best Buy > Appliances > Small Appliances
     24 Best Buy > Movies & Music > Movies & TV Shows
     14 Best Buy > Computers & Tablets > Desktop & All-in-One Computers
     13 Best Buy > Mobile Phones > All Mobile Phones with Plans
     13 Best Buy > Computers & Tablets > Hard Drives
```


Mining for logs for categories:
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
            "size": 2,
            "field": "category.keyword"
          }
        }
      }
    }
  }
}
```
Output:
```json
{
  "took": 19,
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
      "sum_other_doc_count": 5391204,
      "buckets": [
        {
          "key": "lcd tv",
          "doc_count": 49566,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 879,
            "buckets": [
              {
                "key": "abcat0101001",
                "doc_count": 48414
              },
              {
                "key": "cat02015",
                "doc_count": 273
              }
            ]
          }
        },
        {
          "key": "2622037 2127204 2127213 2121716 2138291",
          "doc_count": 25593,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 9798,
            "buckets": [
              {
                "key": "abcat0101001",
                "doc_count": 14088
              },
              {
                "key": "pcmcat247400050000",
                "doc_count": 1707
              }
            ]
          }
        },
        {
          "key": "Hp touchpad",
          "doc_count": 22170,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 1464,
            "buckets": [
              {
                "key": "pcmcat209000050008",
                "doc_count": 20358
              },
              {
                "key": "pcmcat242000050005",
                "doc_count": 348
              }
            ]
          }
        },
        {
          "key": "iPad",
          "doc_count": 17409,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 3981,
            "buckets": [
              {
                "key": "pcmcat209000050007",
                "doc_count": 11319
              },
              {
                "key": "pcmcat209000050008",
                "doc_count": 2109
              }
            ]
          }
        },
        {
          "key": "hp touchpad",
          "doc_count": 16845,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 1320,
            "buckets": [
              {
                "key": "pcmcat209000050008",
                "doc_count": 15159
              },
              {
                "key": "pcmcat242000050005",
                "doc_count": 366
              }
            ]
          }
        },
        {
          "key": "iPhone 4s",
          "doc_count": 16200,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 1476,
            "buckets": [
              {
                "key": "pcmcat209400050001",
                "doc_count": 14187
              },
              {
                "key": "pcmcat171900050029",
                "doc_count": 537
              }
            ]
          }
        },
        {
          "key": "ipad",
          "doc_count": 15108,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 3405,
            "buckets": [
              {
                "key": "pcmcat209000050007",
                "doc_count": 9384
              },
              {
                "key": "pcmcat209000050008",
                "doc_count": 2319
              }
            ]
          }
        },
        {
          "key": "Beats",
          "doc_count": 14415,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 2661,
            "buckets": [
              {
                "key": "pcmcat144700050004",
                "doc_count": 9612
              },
              {
                "key": "pcmcat143000050007",
                "doc_count": 2142
              }
            ]
          }
        },
        {
          "key": "Touchpad",
          "doc_count": 14004,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 972,
            "buckets": [
              {
                "key": "pcmcat209000050008",
                "doc_count": 12789
              },
              {
                "key": "pcmcat242000050002",
                "doc_count": 243
              }
            ]
          }
        },
        {
          "key": "LaborDay_Computers_20110902",
          "doc_count": 13284,
          "Docs": {
            "doc_count_error_upper_bound": 0,
            "sum_other_doc_count": 5676,
            "buckets": [
              {
                "key": "pcmcat247400050000",
                "doc_count": 6801
              },
              {
                "key": "pcmcat209000050008",
                "doc_count": 807
              }
            ]
          }
        }
      ]
    }
  }
}
```
^ Categories look good! Also, can see top category dominating the logs

## Machine-Learned Classification
This allows learning and generalization from infrequent or unique queries to give a representative collection of historical query-result pairs from clicks or purchases, and train a model to generalize to all clicks.

Directly mining the data only gives confidence for relatively frequent queries.

## Hierarchy
For analyzing hierarchical taxonomy - leaf categories for mapping content, but doesn't always the case for queries

