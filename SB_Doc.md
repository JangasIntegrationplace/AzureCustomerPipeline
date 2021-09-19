## Inbound Msg (Relevant for Web)

**Message must contain a label with it's source type**

```
msg = {
    source_thread_id: str
    body: str
    info: dict
}
```

## Get Slack
msg = {
    source_thread_id: str
    source_type: str
    body: str
    info: dict
}

## Dispatch
msg = {
    source_thread_id: str
    source_type: str
    body: str
    info: dict
    thread_ts: str
}


## Output
msg = {
    source_thread_id: str
    source_type: str
    body: str
    info: dict
    thread_ts: str
}


## Reverse Dispatch
msg = {
    source_thread_id: str
    source_type: str
    body: str
    thread_ts: str
}
