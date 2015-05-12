
var Stream = (function() {
    var init, socket;

    init = function(key) {
        socket = new WebSocket("ws://" + document.location.host + "/ws");

        socket.onopen = function(event) {
            socket.send(JSON.stringify({action: 'sub', key: key})); 
        };

        socket.onmessage = function(event) {
            message = JSON.parse(event.data);

            if (message.key === key) {
                $(".stream pre").append(document.createTextNode(message.msg));                
            }
        }

        console.log(key);
    };

    return {
        init: init
    }
})();
