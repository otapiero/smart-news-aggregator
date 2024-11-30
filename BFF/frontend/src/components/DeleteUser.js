import React, { useState } from "react";
import { deleteUser } from "../api";

const DeleteUser = () => {
    const [credentials, setCredentials] = useState({ email: "", password: "" });

    const handleDelete = async (e) => {
        e.preventDefault();

        try {
            await deleteUser(credentials);
            alert("User deleted successfully!");
        } catch (error) {
            alert("Error deleting user!");
        }
    };

    return (
        <form onSubmit={handleDelete}>
            <h2>Delete User</h2>
            <input
                type="email"
                placeholder="Email"
                value={credentials.email}
                onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
                required
            />
            <input
                type="password"
                placeholder="Password"
                value={credentials.password}
                onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                required
            />
            <button type="submit">Delete User</button>
        </form>
    );
};

export default DeleteUser;
