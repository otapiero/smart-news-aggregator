import React from "react";
import './App.css';
import { BrowserRouter as Router, Route, Routes, Link } from "react-router";
import RegisterUser from "./components/RegisterUser";
import UpdateUser from "./components/UpdateUser";
import DeleteUser from "./components/DeleteUser";
import FetchNews from "./components/FetchNews";

const App = () => {
    // This is just a demo app to show how to use the BFF API
    // it is not a production ready app and should not be used as such
    return (
        <Router>
            <nav>
                <ul>
                    <li><Link to="/">Register User</Link></li>
                    <li><Link to="/update">Update User</Link></li>
                    <li><Link to="/delete">Delete User</Link></li>
                    <li><Link to="/fetch-news">Fetch News</Link></li>
                </ul>
            </nav>
            <main>
                <Routes>
                    <Route path="/" element={<RegisterUser />} />
                    <Route path="/update" element={<UpdateUser />} />
                    <Route path="/delete" element={<DeleteUser />} />
                    <Route path="/fetch-news" element={<FetchNews />} />
                </Routes>
            </main>
        </Router>
    );
};

export default App;
