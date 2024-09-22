#!/bin/bash

case "$1" in
    start)
        # Prompt for the SSL passphrase
        read -s -p "Enter PEM pass phrase: " ssl_passphrase
        echo

        # Export the SSL_PASSPHRASE environment variable
        export SSL_PASSPHRASE="$ssl_passphrase"

        # Start the server
        nohup python3 server.py &
        echo "Service started"
        ;;
    stop)
        pkill -f server.py
        echo "Service stopped"
        ;;
    restart)
        pkill -f server.py
        # Prompt for the SSL passphrase again
        read -s -p "Enter PEM pass phrase: " ssl_passphrase
        echo
        export SSL_PASSPHRASE="$ssl_passphrase"
        nohup python3 server.py &
        echo "Service restarted"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac
exit 0
