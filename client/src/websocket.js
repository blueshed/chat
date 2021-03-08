import {
    reactive
} from 'vue'

export default {
    install: (app, options) => {
        console.log(options);
        let protocol = document.location.protocol == "https:" ? "wss://" : "ws://";
        let domain = `${document.domain}:${document.location.port}`;
        let ws_url = `${protocol}${domain}${options.url}`;
        if (
            import.meta.env.MODE == "development") {
            ws_url = `${protocol}localhost:8080${options.url}`;
            console.debug("ws:", ws_url);
        }
        const ws = new WebSocket(ws_url);
        ws.state = reactive({
            status: "connecting",
            email: "",
            transcript: []
        })
        ws.onopen = function () {
            ws.state.status = "connected"
        }
        ws.onmessage = function (evt) {
            if (ws.state.email == "") {
                ws.state.email = evt.data
            } else {
                ws.state.transcript.push(JSON.parse(evt.data))
            }
        };
        ws.onclose = function () {
            ws.state.status = "disconnected"
        }
        app.config.globalProperties.$ws = ws
    }
}