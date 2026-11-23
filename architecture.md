**Feed messages**
Feed event messages are used to show when the data files were received and read by an application.
The information can be used in conjunction with OLA information to capture the history of the lineage.

1. File arrived
```
{"file_arrived":
    {"event_id": ...,
     "app_name": ...,
     "message_timestamp": ..., (in ISO-8601 format),
     "arrival_time": ...,
     "file_name": ...,
     "file_correlation_id": ...,
     "file_location": ...,
     "data_target_name": ... (name of the feed dataset as defined in th eexcel sheet at onboarding)
     "business_date": ...
     "expected_rowcount": ...
     }
}
```

2. File rejected
```
{"file_rejected": 
    {
    "event_id": ...,
    "app_name": ...,
    "message_timestamp': ...,
    "rejection_timestamp":...,
    "file_name": ...,
    "file_correlation_id": ...,
    "file_location": ...,
    }
}
```

3. Feed error
```
{"feed_error": 
    {
    "event_id": ...,
    "app_name": ...,
    "message_timestamp': ...,
    "error_timestamp":...,
    "file_name": ...,
    }
}
```

4. Feed success
```
{"feed_error": 
    {
    "event_id": ...,
    "app_name": ...,
    "message_timestamp': ...,
    "success_timestamp":...,
    "file_name": ...,
    }
}
```

**Dataset messages**

1. Data available

```
{"data_available": 
    {
        "event_id": ...,
        "app_name": ...,
        "message_timestamp": ...,
        "available_time": ...,
        "data_name": ...,
        "data_name_classifier": ...
        "data_keys": { "key1": "value1", "key2": "value2" }
    }
}
```

**Process messages**
1. Process Queued
```
{"process_queued": 
    {
        "event_id": ...,
        "app_name": ...,
        "message_timestamp": ...,
        "queued_time": ...,
        "process_name": ...,
        "process_correlation_id": ...,
        "process_trigger": ...,
        "business_date": ...
    }
}
```

2. Process cancelled
```
{"process_cancelled": 
    {
        "event_id": ...,
        "app_name": ...,
        "message_timestamp": ...,
        "process_trigger": ('OTHER_PROCESS | 'CRON' | 'ROLLOVER')
    }
}
```

3. Process Fail
```
{"process_fail":
    {
        "event_id": ...,
        "app_name": ...,
        "end_time": ...,
        "process_name": ...,
        "datasets_read": ...
    }
}
```

4. Process complete
```
{"process_complete": 
    {
        "event_id": ...
    }
} 