# Django3

from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import exceptions as jwt_exp
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer
from django.http import JsonResponse
from rest_framework import permissions
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken

import Myapp.settings as settings
import jwt

User = get_user_model()


class TokenObtainView(jwt_views.TokenObtainPairView):
    # token作成(LoginView)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])

        res = Response(serializer.validated_data, status=status.HTTP_200_OK)
        try:
            res.delete_cookie("access_token")
            res.delete_cookie("refresh_token")
        except Exception as e:
            print(e)  # ここら辺適当すぎる

        # httpOnlyなのでtokenの操作は全てdjangoで行う
        res.set_cookie(
            "access_token",
            serializer.validated_data["access"],
            httponly=True,
            # secure=True,
            # samesite="None",
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        )
        res.set_cookie(
            "refresh_token",
            serializer.validated_data["refresh"],
            httponly=True,
            # secure=True,
            # samesite="None",
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        )
        
        return res


# Django3


class TokenVerifyView(views.APIView):
    def post(self, request, *args, **kwargs):
        # Authorization ヘッダーからトークンを取得
        access_token = request.COOKIES.get("access_token")

        if access_token is None:
            return Response(
                {"detail": "Authorization header is missing!!!."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # トークンを検証
        serializer = TokenVerifySerializer(data={"token": access_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            refresh_token = request.COOKIES.get("refresh_token")

            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = refresh.access_token
                res = Response(
                    {"message": "AccessToken Reflesh"}, status=status.HTTP_200_OK
                )

                res.delete_cookie("access_token")

                res.set_cookie(
                    "access_token",
                    str(new_access_token),
                    httponly=True,
                    # secure=True,
                    # samesite="None",
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                )
            except TokenError as re:
                raise InvalidToken(e.args[0])

        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)


class UserAPIView(views.APIView):
    def get_object(self, JWT):

        try:
            payload = jwt.decode(jwt=JWT, key=settings.SECRET_KEY, algorithms=["HS256"])
            # DBにアクセスせずuser_idだけの方がjwtの強みが生きるかも
            # その場合 return payload["user_id"]
            return User.objects.get(id=payload["user_id"])

        except jwt.ExpiredSignatureError:
            # access tokenの期限切れ
            return "Activations link expired"
        except jwt.exceptions.DecodeError:
            return "Invalid Token"
        except User.DoesNotExist:
            return "user does not exists"

    def get(self, request, format=None):
        JWT = request.COOKIES.get("access_token")
        if not JWT:
            return Response({"error": "No token"}, status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object(JWT)

        # エラーならstringで帰ってくるので、型で判定
        # ここイケてないな
        if type(user) == str:
            return Response({"error": user}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(
            {"error": "user is not active"}, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        # アクセストークンのクッキーを削除
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
            response.delete_cookie("access_token")

            # リフレッシュトークンのクッキーを削除
            response.delete_cookie("refresh_token")

            return response
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# # CookieからRefresh_Token取得
# # クライアント側からこいつを叩いてから下のクラスへとリクエストを投げる
# def refresh_get(request):
#     try:
#         refresh_token = request.COOKIES["refresh_token"]
#         return JsonResponse({"refresh": refresh_token}, safe=False)
#     except Exception as e:
#         print(e)
#         return None


def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})


# # HTTPRequestのBodyプロパティから送られてきたtokenを受け取る
# class TokenRefresh(jwt_views.TokenRefreshView):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         try:
#             serializer.is_valid(raise_exception=True)
#         except jwt_exp.TokenError as e:
#             raise jwt_exp.InvalidToken(e.args[0])
#         # token更新
#         res = Response(serializer.validated_data, status=status.HTTP_200_OK)
#         # 既存のAccess_Tokenを削除
#         res.delete_cookie("access_token")
#         # 更新したTokenをセット
#         res.set_cookie(
#             "access_token",
#             serializer.validated_data["access"],
#             max_age=60 * 24 * 24 * 30,
#             httponly=True,
#             secure=True,
#             samesite="None",
#         )
#         return res


# class LoginUserView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSerializer

#     # お手本ではAPIViewを使ってget_object()をオーバーロードしてTokenの検証をしていた
#     # しかし、generics以下のViewでは無理なので、代わりにget()をオーバーライドしてこちらの処理過程にTokenの検証を挿入
#     def get(self, request, *args, **kwargs):
#         # Set-CookieにしているのでCookieからトークンを入手
#         jwt_token = request.COOKIES.get("access_token")
#         if not jwt_token:
#             return Response({"error": "No Token"}, status=status.HTTP_400_BAD_REQUEST)
#         # Token検証
#         try:
#             payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
#             # もしくはreturn payload["user_id"]でもありだそうな。
#             loginuser = User.objects.get(id=payload["user_id"])
#             # オブジェクトで返ってくるのでStringならエラーハンドリング
#             if type(loginuser) == str:
#                 return Response(
#                     {
#                         "error": " Expecting an Object type, but it returned a String type."
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             # アクティブチェック
#             if loginuser.is_active:
#                 # 通常、generics.CreateAPIView系統はこの処理をしなくてもいい
#                 # しかしtry-exceptの処理かつ、オーバーライドしているせいかResponse()で返せとエラーが出るので以下で処理
#                 response = UserSerializer(self.request.user)
#                 return Response(response.data, status=status.HTTP_200_OK)
#             return Response(
#                 {"error": "user is not active"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         # Token期限切れ
#         except jwt.ExpiredSignatureError:
#             return "Activations link expired"
#         # 不正なToken
#         except jwt.exceptions.DecodeError:
#             return "Invalid Token"
#         # ユーザーが存在しない
#         except User.DoesNotExist:
#             payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
#             return payload["user_id"]

#     # PUTメソッドを無効
#     def update(self, request, *args, **kwargs):
#         response = {"message": "PUT method is not allowed"}
#         return Response(response, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(jwt_views.TokenObtainPairView):
#     permission_classes = (permissions.AllowAny,)

#     # LogoutでCookieからToken削除
#     # blacklist()を使って、RefreshTokenを無効にする処理を入れてもよい？
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         try:
#             serializer.is_valid(raise_exception=True)
#         except jwt_exp.TokenError as e:
#             raise jwt_exp.InvalidToken(e.args[0])

#         res = Response(serializer.validated_data, status=status.HTTP_200_OK)

#         try:
#             res.delete_cookie("access_token")
#             res.delete_cookie("refresh_token")
#         except Exception as e:
#             print(e)
#             return None

#         return Response({"Message": "Logout"}, status=status.HTTP_200_OK)
