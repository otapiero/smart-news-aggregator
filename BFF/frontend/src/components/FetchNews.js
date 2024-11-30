import React, { useState } from "react";
import { fetchNews } from "../api";

const FetchNews = () => {
    const [credentials, setCredentials] = useState({ email: "", password: "" });

    const handleFetch = async () => {
        try {
            const response = await fetchNews(credentials);
            alert(JSON.stringify(response.data));
        } catch (error) {
            alert("Error fetching news!");
        }
    };

    return (
        <div>
            <input type="email" placeholder="Email" onChange={(e) => setCredentials({ ...credentials, email: e.target.value })} />
            <input type="password" placeholder="Password" onChange={(e) => setCredentials({ ...credentials, password: e.target.value })} />
            <button onClick={handleFetch}>Send News</button>
        </div>
    );
};

export default FetchNews;
