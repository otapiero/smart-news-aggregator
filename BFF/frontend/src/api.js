import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:5003", // Flask BFF URL
});

export const createUser = (user) => api.post("/users", user);
export const updateUser = (requestData) => api.put("/users", requestData);
export const deleteUser = (user) => api.delete("/users", { data: user });
export const fetchNews = (credentials) => api.post("/news", credentials);
