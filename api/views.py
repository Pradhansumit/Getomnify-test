from rest_framework.views import APIView, Response


class HelloWorldView(APIView):
    def get(self, request) -> Response:
        return Response({"message": "Hello World"})
