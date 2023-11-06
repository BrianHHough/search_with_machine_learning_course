# Project: Learn to Rank
A Learning to Rank (LTR) system that integrates with OpenSearch (an open-source search engine).

Run:
```bash
./ltr-end-to-end.sh
```

🐞 Output:
```bash
++ python week1/utilities/build_ltr.py --create_ltr_store
Deleted old store response status: 200
Create the new store at https://localhost:9200/_ltr/week1 response status: 200
++ '[' 0 -ne 0 ']'
++ python week1/utilities/build_ltr.py -f week1/conf/ltr_featureset.json --upload_featureset
Installing week1/conf/ltr_featureset.json featureset at https://localhost:9200/_ltr/week1/_featureset/bbuy_main_featureset
POSTing the featureset to https://localhost:9200/_ltr/week1/_featureset/bbuy_main_featureset
Featureset Creation: <Response [201]>
++ '[' 0 -ne 0 ']'
++ echo 'Creating training and test data sets from impressions by splitting on dates'
Creating training and test data sets from impressions by splitting on dates
++ python week1/utilities/build_ltr.py --output_dir /workspace/ltr_output --split_input /workspace/datasets/train.csv --split_train_rows 1000000 --split_test_rows 1000000
Splitting: /workspace/datasets/train.csv and writing train to: train.csv and test to: test.csv in /workspace/ltr_output
Clicks pre filtering: 1865269
Verify info: flag: validity.csv, path: /workspace/ltr_output/validity.csv, exists: True
Clicks post filtering: 1703297
++ '[' 0 -ne 0 ']'
++ echo 'Creating impressions data set'
Creating impressions data set
++ python week1/utilities/build_ltr.py --synthesize_impressions --output_dir /workspace/ltr_output --train_file /workspace/ltr_output/train.csv
Writing impressions to file: /workspace/ltr_output/impressions.csv
++ '[' 0 -ne 0 ']'
++ python week1/utilities/build_ltr.py --ltr_terms_field sku --output_dir /workspace/ltr_output --create_xgb_training -f week1/conf/ltr_featureset.json --click_model heuristic
...
tureset.json --click_model heuristic
Loading impressions from /workspace/ltr_output/impressions.csv
Logging features
Progress[0]: 1080p
Progress[500]: First class
Progress[1000]: Nikita
Progress[1500]: Transformers: dark of the moon
Progress[2000]: droid x
Progress[2500]: marilyn manson
Progress[3000]: the shield
The following queries produced no results: {}
Heuristic click model
NAN counts: 10
Writing XGB Training file to /workspace/ltr_output/training.xgb
Writing feature map to /workspace/ltr_output/xgb-feat-map.txt
++ '[' 0 -ne 0 ']'
++ python week1/utilities/build_ltr.py --output_dir /workspace/ltr_output -x /workspace/ltr_output/training.xgb --xgb_conf week1/conf/xgb-conf.json
Training XG Boost on /workspace/ltr_output/training.xgb for 5 rounds with params: {'objective': 'reg:logistic'}
Dumping out model using feature map: xgb-feat-map.txt
Saving XGB LTR-ready model to /workspace/ltr_output/xgb_model.model.ltr
Saving XGB Binary model to /workspace/ltr_output/xgb_model.model
/home/gitpod/.pyenv/versions/search_with_ml/lib/python3.9/site-packages/xgboost/core.py:160: UserWarning: [06:46:11] WARNING: /workspace/src/c_api/c_api.cc:1240: Saving into deprecated binary model format, please consider using `json` or `ubj`. Model format will default to JSON in XGBoost 2.2 if not specified.
  warnings.warn(smsg, UserWarning)
++ '[' 0 -ne 0 ']'
++ python week1/utilities/build_ltr.py --upload_ltr_model --xgb_model /workspace/ltr_output/xgb_model.model
Deleting model from https://localhost:9200/_ltr/week1/_model/ltr_model
        Delete Model Response: 404: {"_index":".ltrstore_week1","_id":"model-ltr_model","_version":1,"result":"not_found","_shards":{"total":1,"successful":1,"failed":0},"_seq_no":1,"_primary_term":1}
Uploading model to https://localhost:9200/_ltr/week1/_featureset/bbuy_main_featureset/_createmodel
        Upload Model Response: 201: {"_index":".ltrstore_week1","_id":"model-ltr_model","_version":2,"result":"created","forced_refresh":true,"_shards":{"total":1,"successful":1,"failed":0},"_seq_no":2,"_primary_term":1}
++ '[' 0 -ne 0 ']'
++ python week1/utilities/build_ltr.py --xgb_plot --output_dir /workspace/ltr_output
Plotting model quality data
Plotting trees: 4
...
```


## Analyze how weights affect outcomes:

Run the command:
```bash
python week1/utilities/build_ltr.py --xgb_test /workspace/ltr_output/test.csv --train_file /workspace/ltr_output/train.csv --output_dir /workspace/ltr_output --xgb_test_num_queries 200 --xgb_main_query_weight 1 --xgb_rescore_query_weight 1  && python week1/utilities/build_ltr.py --analyze --output_dir /workspace/ltr_output 
```

🐞 Output:
```bash
...
t': [], 'should': [{'match': {'name': {'query': 'Security camera', 'fuzziness': '1', 'prefix_length': 2, 'boost': 0.01}}}, {'match_phrase': {'name.hyphens': {'query': 'Security camera', 'slop': 1, 'boost': 50}}}, {'multi_match': {'query': 'Security camera', 'type': 'phrase', 'slop': '6', 'minimum_should_match': '2<75%', 'fields': ['name^10', 'name.hyphens^10', 'shortDescription^5', 'longDescription^5', 'department^0.5', 'sku', 'manufacturer', 'features', 'categoryPath']}}, {'terms': {'sku': ['Security', 'camera'], 'boost': 50.0}}, {'match': {'name.hyphens': {'query': 'Security camera', 'operator': 'OR', 'minimum_should_match': '2<75%'}}}, {'query_string': {'query': '1403152^0.009  9511986^0.009  9258821^0.057  2753202^0.066  9512137^0.094  9469746^0.019  2753211^0.028  9506652^0.038  9051072^0.009  9176394^0.057  9027233^0.009  3035098^0.019  8840953^0.028  1230889^0.028  9944139^0.019  1252459^0.019  1230825^0.009  1492858^0.047  1403189^0.047  1230961^0.057  1252371^0.019  1049245^0.009  9512306^0.038  3035113^0.009  1403161^0.028  1415148^0.047  9084439^0.009  9176358^0.009  9772225^0.009  9910433^0.009  1216989^0.009  9512048^0.019  9258992^0.009  1230752^0.019  9955162^0.009  2612464^0.038  9931154^0.009  3199084^0.009  9910373^0.009  2122324^0.009  ', 'fields': ['_id']}}], 'minimum_should_match': 1, 'filter': None}}, 'boost_mode': 'multiply', 'score_mode': 'sum', 'functions': [{'filter': {'exists': {'field': 'salesRankShortTerm'}}, 'gauss': {'salesRankShortTerm': {'origin': '1.0', 'scale': '100'}}}, {'filter': {'exists': {'field': 'salesRankMediumTerm'}}, 'gauss': {'salesRankMediumTerm': {'origin': '1.0', 'scale': '1000'}}}, {'filter': {'exists': {'field': 'salesRankLongTerm'}}, 'gauss': {'salesRankLongTerm': {'origin': '1.0', 'scale': '1000'}}}, {'script_score': {'script': '0.0001'}}]}}, '_source': ['sku', 'name']}
RequestError(400, 'search_phase_execution_exception', 'field [salesRankShortTerm] is of type [org.opensearch.index.mapper.TextFieldMapper$TextFieldType@2c9e606b], but only numeric types are supported.') {'size': 500, 'sort': [{'_score': {'order': 'desc'}}], 'query': {'function_score': {'query': {'bool': {'must': [], 'should': [{'match': {'name': {'query': 'Security camera', 'fuzziness': '1', 'prefix_length': 2, 'boost': 0.01}}}, {'match_phrase': {'name.hyphens': {'query': 'Security camera', 'slop': 1, 'boost': 50}}}, {'multi_match': {'query': 'Security camera', 'type': 'phrase', 'slop': '6', 'minimum_should_match': '2<75%', 'fields': ['name^10', 'name.hyphens^10', 'shortDescription^5', 'longDescription^5', 'department^0.5', 'sku', 'manufacturer', 'features', 'categoryPath']}}, {'terms': {'sku': ['Security', 'camera'], 'boost': 50.0}}, {'match': {'name.hyphens': {'query': 'Security camera', 'operator': 'OR', 'minimum_should_match': '2<75%'}}}, {'query_string': {'query': '1403152^0.009  9511986^0.009  9258821^0.057  2753202^0.066  9512137^0.094  9469746^0.019  2753211^0.028  9506652^0.038  9051072^0.009  9176394^0.057  9027233^0.009  3035098^0.019  8840953^0.028  1230889^0.028  9944139^0.019  1252459^0.019  1230825^0.009  1492858^0.047  1403189^0.047  1230961^0.057  1252371^0.019  1049245^0.009  9512306^0.038  3035113^0.009  1403161^0.028  1415148^0.047  9084439^0.009  9176358^0.009  9772225^0.009  9910433^0.009  1216989^0.009  9512048^0.019  9258992^0.009  1230752^0.019  9955162^0.009  2612464^0.038  9931154^0.009  3199084^0.009  9910373^0.009  2122324^0.009  ', 'fields': ['_id']}}], 'minimum_should_match': 1, 'filter': None}}, 'boost_mode': 'multiply', 'score_mode': 'sum', 'functions': [{'filter': {'exists': {'field': 'salesRankShortTerm'}}, 'gauss': {'salesRankShortTerm': {'origin': '1.0', 'scale': '100'}}}, {'filter': {'exists': {'field': 'salesRankMediumTerm'}}, 'gauss': {'salesRankMediumTerm': {'origin': '1.0', 'scale': '1000'}}}, {'filter': {'exists': {'field': 'salesRankLongTerm'}}, 'gauss': {'salesRankLongTerm': {'origin': '1.0', 'scale': '1000'}}}, {'script_score': {'script': '0.0001'}}]}}, '_source': ['sku', 'name'], 'rescore': {'window_size': 500, 'query': {'rescore_query': {'sltr': {'params': {'keywords': 'Security camera', 'click_prior_query': '1403152^0.009  9511986^0.009  9258821^0.057  2753202^0.066  9512137^0.094  9469746^0.019  2753211^0.028  9506652^0.038  9051072^0.009  9176394^0.057  9027233^0.009  3035098^0.019  8840953^0.028  1230889^0.028  9944139^0.019  1252459^0.019  1230825^0.009  1492858^0.047  1403189^0.047  1230961^0.057  1252371^0.019  1049245^0.009  9512306^0.038  3035113^0.009  1403161^0.028  1415148^0.047  9084439^0.009  9176358^0.009  9772225^0.009  9910433^0.009  1216989^0.009  9512048^0.019  9258992^0.009  1230752^0.019  9955162^0.009  2612464^0.038  9931154^0.009  3199084^0.009  9910373^0.009  2122324^0.009  ', 'skus': ['Security', 'camera']}, 'model': 'ltr_model', 'store': 'week1'}}, 'score_mode': 'total', 'query_weight': 1.0, 'rescore_query_weight': '2'}}}
We've executed 200 queries. Finishing.
Writing results of test to /workspace/ltr_output/xgb_test_output.csv
Traceback (most recent call last):
  File "/workspace/search_with_machine_learning_course/week1/utilities/build_ltr.py", line 375, in <module>
    no_results_df = pd.DataFrame(no_results)
  File "/home/gitpod/.pyenv/versions/search_with_ml/lib/python3.9/site-packages/pandas/core/frame.py", line 733, in __init__
    mgr = dict_to_mgr(data, index, columns, dtype=dtype, copy=copy, typ=manager)
  File "/home/gitpod/.pyenv/versions/search_with_ml/lib/python3.9/site-packages/pandas/core/internals/construction.py", line 503, in dict_to_mgr
    return arrays_to_mgr(arrays, columns, index, dtype=dtype, typ=typ, consolidate=copy)
  File "/home/gitpod/.pyenv/versions/search_with_ml/lib/python3.9/site-packages/pandas/core/internals/construction.py", line 114, in arrays_to_mgr
    index = _extract_index(arrays)
  File "/home/gitpod/.pyenv/versions/search_with_ml/lib/python3.9/site-packages/pandas/core/internals/construction.py", line 677, in _extract_index
    raise ValueError("All arrays must be of the same length")
ValueError: All arrays must be of the same length
```