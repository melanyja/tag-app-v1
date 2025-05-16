import { createRouter, createWebHistory } from "vue-router";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import Dashboard from "./views/Dashboard.vue";
import Home from "./views/Home.vue";
import Tags from "./views/Tags.vue";
import { userState } from './stores/UserStore'; 
import Documents from "./views/Documents.vue";
import Settings from "./views/Settings.vue";
import ModifyDocument from "./views/ModifyDocument.vue";
import UserTags from "./views/UserTags.vue";

const routes = [
  { path: "/login", component: Login },
  { path: "/signup", component: Register },
  { path: "/manage-tags", component: UserTags, meta: { requiresAuth: true } },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },
  { path: "/tags", component: Tags, meta: { requiresAuth: true } },
  { path: "/documents", component: Documents, meta: { requiresAuth: true } },
  { path: "/settings", component: Settings, meta: { requiresAuth: true } },
  { path: "/update-document", component: ModifyDocument, meta: { requiresAuth: true } },
  { path: "/", component: Home },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    if (userState.token && userState.user) {
      console.log("User authenticated");
      next();
    } else {
      console.log("User not authenticated");
      next("/login");
    }
  } else {
    console.log("public route");
    next();
  }
});

export default router;
