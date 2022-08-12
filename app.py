#!/bin/env python
from app import create_app, socket_

app = create_app(debug=True)

if __name__ == '__main__':
    socket_.run(app)
