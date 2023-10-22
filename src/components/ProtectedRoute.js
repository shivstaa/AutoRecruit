import React, { useEffect } from "react"; // <-- Import useEffect
import { useAuth } from "./AuthContext";
import { Outlet, useNavigate, useLocation } from "react-router-dom";

function ProtectedRoute() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (!user) {
      // Redirect to login and remember where the user tried to go
      navigate("/login", { state: { from: location } });
    }
  }, [user, navigate, location]);

  return user ? <Outlet /> : null; // <-- Check if user is present, then render the Outlet, else render null
}

export default ProtectedRoute;
