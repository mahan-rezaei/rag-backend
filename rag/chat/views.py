from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import initialize_chroma_from_pdf, embed_sentences, search_in_chroma

import requests


class InitialPdf(APIView):
    def get(self, reqeust):
        initialize_chroma_from_pdf()
        return Response({'message': 'file added to db successfully.'})


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
        try:
            print("helllllllllllllllllllllllllllllllllllll")
            docs = search_in_chroma(question)
            print(docs)
            context = "\n".join([doc['documents'] for doc in docs])
            prompt = f"اطلاعات زیر رو بخون و به سوال پاسخ بده\n{context}\n\nسوال:{question}\n\nپاسخ:"
            response = requests.post("http://localhost:1234/v1/chat/completions",
                         headers={"Content-Type": "application/json"},
                         json={
                             "model": "gemma-3-4b-it-gguf",
                             "messages": [{'role': 'user', 'content': prompt}],
                             "temperature": 0.4
                         })
            response.raise_for_status()
            result = response.json()
            answre = result["choices"][0]["messages"]["content"]
            

            return Response({'answre': answre},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        
