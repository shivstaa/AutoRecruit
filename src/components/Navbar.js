import { Link } from "react-router-dom";
import { useAuth } from "./AuthContext";
import { useState } from "react";

function Navbar() {
  const { user, setUser } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false); // <-- Local state to manage dropdown visibility

  return (
    <nav className=" text-white p-5 font-bold">
      <ul className="flex justify-between">
        <div className="flex space-x-4">
          <li>
            <Link to="/" className="hover:underline">
              Home
            </Link>
          </li>
          <li>
            <Link to="/profile" className="hover:underline">
              Interview
            </Link>
          </li>
        </div>
        {user ? (
          <div className="relative">
            <span
              className="hover:underline cursor-pointer"
              onClick={() => setShowDropdown(!showDropdown)} // Toggle the dropdown visibility
            >
              Hi {user.username}
            </span>
            {showDropdown && ( // Conditionally render the dropdown
              <ul className="absolute right-0 mt-2 bg-purple-500 text-white rounded shadow-md p-2">
                <li
                  onClick={() => setUser(null)}
                  className="cursor-pointer hover:bg-purple-700 p-2 rounded"
                >
                  Logout
                </li>
              </ul>
            )}
          </div>
        ) : (
          <Link to="/login" className="hover:underline">
            Login
          </Link>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
