import { reactive, provide, inject } from "vue";
import { getUserInfo, logoutUser } from "../api";

export const userState = reactive({
  user: null,
  token: localStorage.getItem("token") || null,
});

const fetchUser = async () => {
  if (!userState.token) return;
  try {
    const response = await getUserInfo(userState.token);
    userState.user = response.data;
  } catch (error) {
    console.error("Failed to fetch user:", error);
    logout();
  }
};

const login = async (token) => {
  userState.token = token;
  localStorage.setItem("token", token);
  await fetchUser();
};

const logout = async () => {
  if (userState.token) {
    await logoutUser(userState.token);
  }
  userState.user = null;
  userState.token = null;
  localStorage.removeItem("token");
};

export const provideUserStore = () => {
    console.log("Providing user store")
    provide("userStore", {
      userState,
      fetchUser,
      login,
      logout,
    });
  
    if (userState.token) {
      fetchUser();
    }
  };
  

export const useUserStore = () => {
  console.log("Here in useSerStore")
  return inject("userStore");
};
