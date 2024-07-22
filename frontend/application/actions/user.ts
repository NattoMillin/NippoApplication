"use server";

interface TemporarrySignupProps {
  number: string;
  password: string;
  rePassword: string;
}

// アカウント仮登録
export const temporarrySignup = async ({
  number,
  password,
  rePassword,
}: TemporarrySignupProps) => {
  try {
    const body = JSON.stringify({
      number,
      password,
      re_password: rePassword,
    });

    // アカウント仮登録を送信
    const apiRes = await fetch(`${process.env.API_URL}/api/auth/users/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body,
    });

    // APIレスポンスが正常でない場合、失敗を返す
    if (!apiRes.ok) {
      return {
        success: false,
      };
    }

    // 成功を返す
    return {
      success: true,
    };
  } catch (error) {
    console.error(error);
    // エラー発生時に、失敗を返す
    return {
      success: false,
    };
  }
};

interface ForgotPasswordProps {
  email: string;
}

// パスワード再設定
export const forgotPassword = async ({ email }: ForgotPasswordProps) => {
  try {
    const body = JSON.stringify({
      email,
    });

    // パスワード再設定を送信
    const apiRes = await fetch(
      `${process.env.API_URL}/api/auth/users/reset_password/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body,
      }
    );

    // APIレスポンスが正常でない場合、失敗を返す
    if (!apiRes.ok) {
      return {
        success: false,
      };
    }

    // 成功を返す
    return {
      success: true,
    };
  } catch (error) {
    console.error(error);
    // エラー発生時に、失敗を返す
    return {
      success: false,
    };
  }
};

interface ResetPasswordProps {
  uid: string;
  token: string;
  newPassword: string;
  reNewPassword: string;
}

// パスワード再設定確認
export const resetPassword = async ({
  uid,
  token,
  newPassword,
  reNewPassword,
}: ResetPasswordProps) => {
  try {
    const body = JSON.stringify({
      uid,
      token,
      new_password: newPassword,
      re_new_password: reNewPassword,
    });

    // パスワード再設定確認を送信
    const apiRes = await fetch(
      `${process.env.API_URL}/api/auth/users/reset_password_confirm/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body,
      }
    );

    // APIレスポンスが正常でない場合、失敗を返す
    if (!apiRes.ok) {
      return {
        success: false,
      };
    }

    // 成功を返す
    return {
      success: true,
    };
  } catch (error) {
    console.error(error);
    // エラー発生時に、失敗を返す
    return {
      success: false,
    };
  }
};

export interface UserDetailType {
  uid: string;
  name: string;
  created_at: string;
}

interface GetUserDetailProps {
  userId: string;
}

// ユーザー詳細取得
export const getUserDetail = async ({ userId }: GetUserDetailProps) => {
  try {
    // APIからユーザー詳細を取得
    const apiRes = await fetch(`${process.env.API_URL}/api/users/${userId}/`, {
      method: "GET",
      cache: "no-store",
      credentials: "include",
    });

    // APIレスポンスが正常でない場合、失敗とnullを返す
    if (!apiRes.ok) {
      return {
        success: false,
        user: null,
      };
    }

    // レスポンスをJSONとして解析し、ユーザー詳細を取得
    const user: UserDetailType = await apiRes.json();

    // 成功と取得したユーザー詳細を返す
    return {
      success: true,
      user,
    };
  } catch (error) {
    console.error(error);
    // エラー発生時に、失敗とnullを返す
    return {
      success: false,
      user: null,
    };
  }
};

interface UpdateUserProps {
  name: string;
}

// プロフィール編集
export const updateUser = async ({ name }: UpdateUserProps) => {
  try {
    const body = JSON.stringify({
      name,
    });

    // プロフィール編集を送信
    const apiRes = await fetch(`${process.env.API_URL}/api/auth/users/me/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body,
    });

    // APIレスポンスが正常でない場合、失敗とnullを返す
    if (!apiRes.ok) {
      return {
        success: false,
        user: null,
      };
    }

    // レスポンスをJSONとして解析し、ユーザー詳細を取得
    const user: UserDetailType = await apiRes.json();

    // 成功と取得したユーザー詳細を返す
    return {
      success: true,
      user,
    };
  } catch (error) {
    console.error(error);
    // エラー発生時に、失敗とnullを返す
    return {
      success: false,
      user: null,
    };
  }
};

interface UpdatePasswordProps {
  currentPassword: string;
  newPassword: string;
  reNewPassword: string;
}

// パスワード変更
export const updatePassword = async ({
  currentPassword,
  newPassword,
  reNewPassword,
}: UpdatePasswordProps) => {
  try {
    const body = JSON.stringify({
      current_password: currentPassword,
      new_password: newPassword,
      re_new_password: reNewPassword,
    });

    // パスワード変更を送信
    const apiRes = await fetch(
      `${process.env.API_URL}/api/auth/users/set_password/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body,
      }
    );

    // APIレスポンスが正常でない場合、失敗を返す
    if (!apiRes.ok) {
      return {
        success: false,
      };
    }

    // 成功を返す
    return {
      success: true,
    };
  } catch (error) {
    console.error(error);
    // エラー発生時に、失敗を返す
    return {
      success: false,
    };
  }
};
