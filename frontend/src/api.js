
import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; 

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});


export const getAuthToken = () => localStorage.getItem("token");

apiClient.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token && !config.noAuth) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});


export const deleteTag = async (tagId) => {
  try {
    const response = await apiClient.delete(`/tags/${tagId}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting tag:", error.response ? error.response.data : error);
    return { error: "Failed to delete tag" };
  }
};

export const createTag = async (tagname, tagval, tagdesc) => {
  try {
    const tagData = {
      name:  tagname,
      value:  tagval,
      description: tagdesc,
    };
    const response = await apiClient.post(`/tags`, tagData
    );
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.detail || "Unknown error occurred" };
  }
};

export const fetchUserTags = async () => {
  try {
    const response = await apiClient.get("/tags/me");
    return response.data;
  } catch (error) {
    console.error("Error fetching tags:", error);
    return [];
  }
};

export const registerUser = async (email, username, password) => {
  return apiClient.post(`/auth/register`, { email, username, password }, { noAuth: true });
};

export const loginUser = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  return await apiClient.post(`/auth/jwt/login`, formData, { 
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    noAuth: true
  });
};

export const getUserInfo = async () => {
  return apiClient.get(`/users/me`);
};

export const logoutUser = async () => {
  return apiClient.post(`/auth/jwt/logout`);
};

export const getApiUrl = () => API_URL;
