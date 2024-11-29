import React, { useState } from "react";
import { updateUser } from "../api";

const UpdateUser = () => {
    const [credentials, setCredentials] = useState({ email: "", password: "" });
    const [userUpdates, setUserUpdates] = useState({
        email: "", // New email (optional)
        password: "", // New password (optional)
        username: "",
        country: "Israel",
        language: "English",
        categories: [],
        notification_channel: "email",
        telegram_user_id: "",
    });

    const handleUpdate = async (e) => {
        e.preventDefault();
        const requestData = {
            user: {
                ...userUpdates,
                email: userUpdates.email || credentials.email, // Fallback to current email
            },
            email: credentials.email, // Old email for authentication
            password: credentials.password, // Old password for authentication
        };

        try {
            const response = await updateUser(requestData);
            alert("User updated successfully!");
        } catch (error) {
            alert("Error updating user!");
        }
    };

    return (
        <form onSubmit={handleUpdate}>
            <h2>Update User</h2>
            {/* Old Credentials */}
            <input
                type="email"
                placeholder="Current Email"
                value={credentials.email}
                onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
                required
            />
            <input
                type="password"
                placeholder="Current Password"
                value={credentials.password}
                onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                required
            />

            {/* Optional Updates */}
            <input
                type="email"
                placeholder="New Email (optional)"
                value={userUpdates.email}
                onChange={(e) => setUserUpdates({ ...userUpdates, email: e.target.value })}
            />
            <input
                type="password"
                placeholder="New Password (optional)"
                value={userUpdates.password}
                onChange={(e) => setUserUpdates({ ...userUpdates, password: e.target.value })}
            />
            <input
                type="text"
                placeholder="New Username (optional)"
                value={userUpdates.username}
                onChange={(e) => setUserUpdates({ ...userUpdates, username: e.target.value })}
            />
            <select
                value={userUpdates.country}
                onChange={(e) => setUserUpdates({ ...userUpdates, country: e.target.value })}
            >
                <option value="Israel">Israel</option>
                <option value="US">US</option>
                <option value="UK">UK</option>
                <option value="France">France</option>
            </select>
            <select
                value={userUpdates.language}
                onChange={(e) => setUserUpdates({ ...userUpdates, language: e.target.value })}
            >
                <option value="English">English</option>
                <option value="Hebrew">Hebrew</option>
                <option value="French">French</option>
            </select>
            <fieldset>
                <legend>Categories (optional)</legend>
                {/* Repeat category checkboxes logic */}
                {["Politics", "Business", "Technology", "Health", "Sports", "Environment", "Science", "Arts and Entertainment"].map(
                    (category) => (
                        <label key={category}>
                            <input
                                type="checkbox"
                                value={category}
                                checked={userUpdates.categories.includes(category)}
                                onChange={(e) => {
                                    const selected = userUpdates.categories.includes(e.target.value)
                                        ? userUpdates.categories.filter((cat) => cat !== e.target.value)
                                        : [...userUpdates.categories, e.target.value];
                                    setUserUpdates({ ...userUpdates, categories: selected });
                                }}
                            />
                            {category}
                        </label>
                    )
                )}
            </fieldset>
            <input
                type="text"
                placeholder="Telegram User ID (optional)"
                value={userUpdates.telegram_user_id}
                onChange={(e) => setUserUpdates({ ...userUpdates, telegram_user_id: e.target.value })}
            />
            <button type="submit">Update User</button>
        </form>
    );
};

export default UpdateUser;
