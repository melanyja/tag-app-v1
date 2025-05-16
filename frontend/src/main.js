import { createApp } from "vue";
import AppWrapper from "./AppWrapper.vue";
import router from "./router";
import "./style.css"
import 'primeicons/primeicons.css'
import 'vue3-toastify/dist/index.css';


const app = createApp(AppWrapper)

app.use(router).mount("#app");
