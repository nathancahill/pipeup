
var Stream = (function() {
    var init, socket, status, key, ping;

    init = function() {
        status = "connecting";
        socket = new ReconnectingWebSocket("ws://" + document.location.host + "/ws");
        key = document.location.pathname.substring(1, 7);

        socket.onopen = function(event) {
            status = "connected";
            socket.send(JSON.stringify({action: "sub", key: key}));

            ping = setInterval(keepalive, 15000);  // 15 seconds

            print("Connected.\n");
        };

        socket.onmessage = function(event) {
            message = JSON.parse(event.data);

            if (message.action === "update") {
                if (message.key === key) {
                    print(message.msg);                
                }
            } else if (message.action === "close") {
                status = "closed";
                print(message.msg);
                socket.close();
            }
        };

        socket.onclose = function(event) {
            clearInterval(ping);

            if (status !== "closed") {
                print("Lost connection.\n");
                print("Connecting...\n");
            }
        };
    };

    keepalive = function() {
        socket.send(JSON.stringify({action: "ping", key: key}));
    };

    print = function(text) {
        $(".stream pre").append(document.createTextNode(text));
        $(".stream").get(0).scrollTop = $(".stream").get(0).scrollHeight;
    };

    return {
        init: init
    };
})();
