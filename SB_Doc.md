# Service Bus Message / Function Documentation

This sheet is a raw documentation about required message bodies and
meta data.

If you connect from your backend to the service bus, please note
that you won't get any Feedback about validation since the whole
System is decoupled.

The service bus will take every message (depends on it's size). The
failure will be raised in a function. The response wont be shared
back to client.

It's very important to enable monitoring and watch error logs!


## Inbound Msg (Relevant for Web)

It's the most important information since your webapp will be
connected to that topic. Make sure that it's well formatted.

**Message must contain a label with it's source type**

```
msg = {
    source_thread_id: str
    body: str
    info: dict
}
```

**Warning** Your message must contain the source type information at
it's label, not body. This is implemented for using native filters
of azure service bus, even if it's not used yet. It's a nice to have.


## Get Slack

```
msg = {
    source_thread_id: str
    source_type: str
    body: str
    info: dict
}
```


## Dispatch

```
msg = {
    source_thread_id: str
    source_type: str
    body: str
    info: dict
    thread_ts: str
}
```


## Output

```
msg = {
    source_thread_id: str
    source_type: str
    body: str
    info: dict
    thread_ts: str
}
```


## Reverse Dispatch

```
msg = {
    source_thread_id: str
    source_type: str
    body: str
    thread_ts: str
}
```
