
var StreamPubNub = (function() {
    var init, socket, status, key;

    init = function() {
        status = "connecting";
        key = document.location.pathname.substring(1, 7);
        socket = new PUBNUB.ws("ws://pubsub.pubnub.com/nopublickey/sub-c-a78d8cc0-fa74-11e4-8519-0619f8945a4f/" + key);

        socket.onopen = function(event) {
            status = "connected";
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
