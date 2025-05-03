from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import initialize_chroma_from_pdf, embed_sentences, search_in_chroma, show_chroma_data

import requests


system_prompt = """
    شما یک مدل هوش مصنوعی مفید هستید که به سوالات کاربران به زبان فارسی پاسخ میدهید.
    دستورات: 
    - به تمام سوالات مرتبط پاسخ دهید
    - از عبارات غیراخلاقی اجتناب کنید
    - پاسخها را ساده و واضح ارائه دهید
    """

class InitialPdf(APIView):
    def get(self, reqeust):
        initialize_chroma_from_pdf()
        return Response({'message': 'file added to db successfully.'})


class ChatView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({'error': 'question is requered.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            print("*"*90)
            print("data in chroma")
            show_chroma_data()
            docs = search_in_chroma(question)
            print("*"*90)
            print("docs")
            print(docs)
            documents_list = docs.get('documents', [])
            context = "\n".join([doc for sublist in documents_list for doc in sublist])
            prompt = f"اطلاعات زیر رو بخون و به سوال پاسخ بده\n{context}\n\nسوال:{question}\n\nپاسخ:"
            
            print("*"*90)
            print("prompt")
            print(prompt)
            response = requests.post("http://127.0.0.1:1234/v1/chat/completions",
                         headers={"Content-Type": "application/json"},
                         json={
                             "model": "gemma-3-4b-it",
                             "messages": [{"role": "system", "content": system_prompt},
                                          {'role': 'user', 'content': prompt}],
                             "temperature": 0.4
                         })
            response.raise_for_status()
            result = response.json()
            answre = result["choices"][0]["message"]["content"]
            

            return Response({'answre': answre},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        
