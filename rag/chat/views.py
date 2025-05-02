from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ChatView(APIView):
    def get(self, request):
        return Response({
            'message': 'hello'
        })

    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({'error': 'question is requered.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
