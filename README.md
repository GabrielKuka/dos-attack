# Slowloris Attack

Perform a Denial of Service attack towards a server. Work best when the server is running Apache.

This is an example of a low-bandwidth DOS attack also known as _slowloris_.

Dependencies:

1. colorama
2. argparse

Installation:
`pip3 install -r requirements.txt`

Example usage:
`python3 main.py 127.0.0.1 -p 80 -s 600`

### Idea:

A **GET** request always ends with 2 new line characters "\n\n". Instead of sending 2 new line characters in the header, send only one. This tells the server that the request is not fully sent yet.
This connection will be terminated by the server if no further data is sent. That is why this script will send random numbers to the server every now and then so that the **GET** is never finished.

Apache servers have a limit for open connections (200). Sending +200 **GET** requests that are never closed will make the server not answer to other requests.

If the server decides to close the connection by itself, the script recreates the connections again, so that we always have at least 200 connections with the server.
