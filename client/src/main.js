import {
    createApp
} from 'vue'
import App from './App.vue'
import ws from './websocket.js'


const app = createApp(App)
app.use(ws)
app.mount('#app')