# Steps to fill your Feature Groups with the same training data as I have

```
$ poetry install
```

```
$ poetry run python tools/ohlc_data_writer.py \
    --hopsworks_project_name <YOUR_HOPSWORKS_PROJECT_NAME> \
    --hopsworks_api_key <YOUR_HOPSWORKS_API_KEY> \
    --feature_group_name <YOUR_FEATURE_GROUP_NAME> \
    --feature_group_version <YOUR_FEATURE_GROUP_VERSION> \
    --csv_file ./ohlc_data.csv
```

For example,
```
$ poetry run python tools/ohlc_data_writer.py \
    --hopsworks_project_name paulescu \
    --hopsworks_api_key iAYSmani2t1wViet.mmOAjVcnsubksPqm546451T0g9q1TmIvTZGx5aOuJXNHbYglYxtuP406TNvs \
    --feature_group_name ohlc_feature_gropu \
    --feature_group_version 2 \
    --csv_file ./ohlc_data.csv
```


