
var StreamPubNub = (function() {
    var init, socket, status, key, ping;

    init = function() {
        status = "connecting";
        key = document.location.pathname.substring(1, 7);

        pubnub = PUBNUB.init({
            origin: '',
            subscribe_key: 'sub-c-a78d8cc0-fa74-11e4-8519-0619f8945a4f'
        });

        pubnub.subscribe({
            channel: key,
            restore: true,
            message: function(message, env, channdl) {
                message = JSON.parse(message);

                if (message.action === "update") {
                    if (message.key === key) {
                        print(message.msg);
                    }
                } else if (message.action === "close") {
                    status = "closed";
                    print(message.msg);

                    pubnub.unsubscribe({
                        channel: key
                    });
                }
            },
            connect: function() {
                status = "connected";
                print("Connected.\n");
            },
            reconnect: function() {
                print("Connected.\n");
            },
            disconnect: function() {
                print("Lost connection.\n");
                print("Connecting...\n");
            }
        });
    };

    print = function(text) {
        $(".stream pre").append(document.createTextNode(text));
        $(".stream").get(0).scrollTop = $(".stream").get(0).scrollHeight;
    };

    return {
        init: init
    };
})();
