"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { z } from "zod";
import { useForm, SubmitHandler } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Loader2 } from "lucide-react";
import { UserType } from "@/lib/nextauth";
import { updateUser } from "@/actions/user";
import ImageUploading, { ImageListType } from "react-images-uploading";
import Image from "next/image";
import toast from "react-hot-toast";

// 入力データの検証ルールを定義
const schema = z.object({
  name: z.string().min(3, { message: "3文字以上入力する必要があります" }),
  introduction: z.string().optional(),
});

// 入力データの型を定義
type InputType = z.infer<typeof schema>;

interface ProfileProps {
  user: UserType;
}

// プロフィール
const Profile = ({ user }: ProfileProps) => {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  // フォームの状態
  const form = useForm<InputType>({
    // 入力値の検証
    resolver: zodResolver(schema),
    // 初期値
    defaultValues: {
      name: user.name || "",
    },
  });

  // 送信
  const onSubmit: SubmitHandler<InputType> = async (data) => {
    setIsLoading(true);
    let base64Image;

    try {
      // プロフィール編集
      const res = await updateUser({
        name: data.name,
      });

      if (!res.success) {
        toast.error("プロフィールの編集に失敗しました");
        return;
      }

      toast.success("プロフィールを編集しました");
      router.refresh();
    } catch (error) {
      toast.error("プロフィールの編集に失敗しました");
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <div>
      <div className="text-xl font-bold text-center mb-5">プロフィール</div>
      <Form {...form}>

        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-5">
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel>名前</FormLabel>
                <FormControl>
                  <Input placeholder="名前" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />


          <Button disabled={isLoading} type="submit" className="w-full">
            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            変更
          </Button>
        </form>
      </Form>
    </div>
  );
};

export default Profile;
