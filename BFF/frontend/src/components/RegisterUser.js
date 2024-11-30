import React, { useState } from "react";
import { createUser } from "../api";

const RegisterUser = () => {
    const [user, setUser] = useState({
        email: "",
        username: "",
        password: "",
        country: "Israel",
        language: "English",
        categories: [],
        notification_channel: "email",
        telegram_user_id: "",
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await createUser(user);
            alert("User registered successfully!");
        } catch (error) {
            alert("Error registering user!");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="email" placeholder="Email" value={user.email} onChange={(e) => setUser({ ...user, email: e.target.value })} required />
            <input type="text" placeholder="Username" value={user.username} onChange={(e) => setUser({ ...user, username: e.target.value })} required />
            <input type="password" placeholder="Password" value={user.password} onChange={(e) => setUser({ ...user, password: e.target.value })} required />
            <select value={user.country} onChange={(e) => setUser({ ...user, country: e.target.value })}>
                <option value="Israel">Israel</option>
                <option value="US">US</option>
                <option value="UK">UK</option>
                <option value="France">France</option>
            </select>
            <select value={user.language} onChange={(e) => setUser({ ...user, language: e.target.value })}>
                <option value="English">English</option>
                <option value="Hebrew">Hebrew</option>
                <option value="French">French</option>
            </select>
            <fieldset>
                <legend>Categories</legend>
                <label>
                    <input type="checkbox" value="politics"
                           onChange={(e) => setUser({...user, categories: [...user.categories, e.target.value]})}/>
                    Politics
                </label>
                <label>
                    <input type="checkbox" value="business"
                           onChange={(e) => setUser({...user, categories: [...user.categories, e.target.value]})}/>
                    Business
                </label>
                <label>
                    <input type="checkbox" value="technology"
                           onChange={(e) => setUser({...user, categories: [...user.categories, e.target.value]})}/>
                    Technology
                </label>
                <label>
                    <input type="checkbox" value="health"
                           onChange={(e) => setUser({...user, categories: [...user.categories, e.target.value]})}/>
                    Health
                </label>
                <label>
                    <input type="checkbox" value="sports"
                           onChange={(e) => setUser({...user, categories: [...user.categories, e.target.value]})}/>
                    Sports
                </label>
                <label>
                    <input type="checkbox" value="environment"
                           onChange={(e) => setUser({...user, categories: [...user.categories, e.target.value]})}/>
                    Environment
                </label>
                <label>
                    <input type="checkbox" value="science"
                           onChange={(e) => setUser({...user, categories: [...user.categories, e.target.value]})}/>
                    Science
                </label>
                <label>
                    <input type="checkbox" value="arts_and_entertainment"
                           onChange={(e) => setUser({...user, categories: [...user.categories, e.target.value]})}/>
                    Arts and Entertainment
                </label>
            </fieldset>
            <button type="submit">Register</button>
        </form>
    );
};

export default RegisterUser;
