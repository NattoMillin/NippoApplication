"use client";

import { UserDetailType } from "@/actions/user";
import Image from "next/image";

interface UserDetailProps {
  user: UserDetailType;
}

// 投稿者詳細
const UserDetail = ({ user }: UserDetailProps) => {
  return (
    <div>
      <div className="space-y-5 break-words whitespace-pre-wrap mb-5">
        <div className="font-bold text-xl text-center">{user.name}</div>
      </div>
    </div>
  );
};

export default UserDetail;
