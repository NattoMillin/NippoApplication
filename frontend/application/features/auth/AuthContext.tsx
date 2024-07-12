"use client";

import React, { createContext, useState, useContext, useEffect } from "react";
import { fetchAsyncTokenRefresh, fetchAsyncTokenVerify } from "./api";

// AuthContextの型を定義
interface AuthContextProps {
  isAuth: boolean;
  signin: () => void;
  signout: () => void;
}

const defaultAuthProvider: AuthContextProps = {
  isAuth: false,
  signin: () => {},
  signout: () => {},
};
const AuthContext = createContext<AuthContextProps>(defaultAuthProvider);

export const useAuthContext = () => {
  return useContext(AuthContext);
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [isAuth, setIsAuth] = useState(false);

  // ユーザーがログインした時に呼び出される関数
  const signin = () => {
    setIsAuth(true);
  };

  // ユーザーがログアウトした時に呼び出される関数
  const signout = () => {
    setIsAuth(false);
  };

  useEffect(() => {
    const verifyUser = async () => {
      // アクセストークンを使用してユーザー情報を取得するAPIリクエスト
      try {
        const response = await fetchAsyncTokenVerify();
        setIsAuth(true);
        return response;
      } catch (error: any) {
        if (error.response && error.response.status === 401) {
          try {
            // リフレッシュトークンを使用して新しいアクセストークンを取得
            await fetchAsyncTokenRefresh();
            // 新しいアクセストークンでユーザー情報取得のリクエストを再試行
            const retryResponse = await fetchAsyncTokenVerify();
            setIsAuth(true);
            return retryResponse;
          } catch (error: any) {
            setIsAuth(false);
          }
        }
      }
    };

    verifyUser();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuth, signin, signout }}>
      {children}
    </AuthContext.Provider>
  );
};
