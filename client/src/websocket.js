import {
    reactive
} from 'vue'

export default {
    install: (app, options) => {
        const ws = new WebSocket("ws://localhost:8080/ws");
        ws.transcript = reactive([])
        ws.onmessage = function (evt) {
            ws.transcript.push(evt.data)
        };
        app.config.globalProperties.$ws = ws
    }
}