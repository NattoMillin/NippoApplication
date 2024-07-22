"use client";

import { useState } from "react";
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
import { Loader2 } from "lucide-react";
import { temporarrySignup } from "@/actions/user";
import toast from "react-hot-toast";
import Link from "next/link";
import { redirect } from "next/navigation";

// 入力データの検証ルールを定義
const schema = z.object({
  number: z.string().length(6, { message: "桁数が違います必要があります" }),
  password: z.string().min(8, { message: "8文字以上入力する必要があります" }),
});

// 入力データの型を定義
type InputType = z.infer<typeof schema>;

// アカウント仮登録
const Signup = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [isSignUp, setIsSignUp] = useState(false);

  // フォームの状態
  const form = useForm<InputType>({
    // 入力値の検証
    resolver: zodResolver(schema),
    // 初期値
    defaultValues: {
      number: "",
      password: "",
    },
  });

  // 送信
  const onSubmit: SubmitHandler<InputType> = async (data) => {
    setIsLoading(true);

    try {
      // アカウント仮登録
      const res = await temporarrySignup({
        number: data.number,
        password: data.password,
        rePassword: data.password,
      });

      if (!res.success) {
        toast.error("サインアップに失敗しました");
        return;
      }

      setIsSignUp(true);
    } catch (error) {
      toast.error("サインアップに失敗しました");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-[400px] m-auto">
      {isSignUp ? (
        redirect("/")
      ) : (
        <>
          <div className="text-2xl font-bold text-center mb-10">新規登録</div>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-5">
              <FormField
                control={form.control}
                name="number"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>従業員番号</FormLabel>
                    <FormControl>
                      <Input placeholder="xxxx@gmail.com" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>パスワード</FormLabel>
                    <FormControl>
                      <Input type="password" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="text-sm text-gray-500">
                サインアップすることで、利用規約、プライバシーポリシーに同意したことになります。
              </div>

              <Button disabled={isLoading} type="submit" className="w-full">
                {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                アカウント作成
              </Button>
            </form>
          </Form>

          <div className="text-center mt-5">
            <Link href="/login" className="text-sm text-blue-500">
              すでにアカウントをお持ちの方
            </Link>
          </div>
        </>
      )}
    </div>
  );
};

export default Signup;
