"use client";

import React from "react";
import { useAuthContext } from "./AuthContext";
import { Navigate } from "react-router-dom";

interface PrivateRouteProps {
  element: React.ReactElement;
}

export const PrivateRoute: React.FC<PrivateRouteProps> = ({ element }) => {
  const { isAuth } = useAuthContext();

  if (isAuth) {
    return element;
  }

  return <Navigate to="/signin" />;
};
