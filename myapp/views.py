
import requests,json,re
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets,generics,status
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Books
from .serializers import BooksSerializers
# Create your views here.

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers


@api_view(['GET', 'POST'])
def books_load(request):
    response = requests.get("https://www.anapioficeandfire.com/api/books")
    data = response.json()
    print(response.status_code)
    urls = list(map(lambda x: (x['url']), data))
    ids = []
    for i in urls:
        i = re.sub(r'.*/', '', i)
        ids.append(i)
    names = list(map(lambda x: (x['name']), data))
    isbns = list(map(lambda x: (x['isbn']), data))
    authors = list(map(lambda x: (x['authors']), data))
    nopages = list(map(lambda x: (x['numberOfPages']), data))
    publishers = list(map(lambda x: (x['publisher']), data))
    country = list(map(lambda x: (x['country']), data))
    release_dates = list(map(lambda x: (x['released']), data))

    li = zip(ids, names, isbns, authors, nopages, publishers, country, release_dates)
    for i in li:
        Books.objects.get_or_create(url=i[0], name=i[1], isbn=i[2], authors=i[3], nopages=i[4], publisher=i[5],
                                    country=i[6], released=i[7])
    return Response("Data loaded successfully into Database..!!")

@api_view(['GET', 'POST'])
def books_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        # books = Books.objects.all()
        # serializer = BooksSerializers(books, many=True)
        # print(serializer)
        # return Response(serializer.data)
        response = requests.get("https://www.anapioficeandfire.com/api/books")
        data = response.json()
        print(response.status_code)
        urls = list(map(lambda x: (x['url']), data))
        ids = []
        for i in urls:
            i = re.sub(r'.*/', '', i)
            ids.append(i)
        names = list(map(lambda x: (x['name']), data))
        isbns = list(map(lambda x: (x['isbn']), data))
        authors = list(map(lambda x: (x['authors']), data))
        nopages = list(map(lambda x: (x['numberOfPages']), data))
        publishers = list(map(lambda x: (x['publisher']), data))
        country = list(map(lambda x: (x['country']), data))
        release_dates = list(map(lambda x: (x['released']), data))

        li = zip(ids, names, isbns, authors, nopages, publishers, country, release_dates)

        # for i in li:
        #     Books.objects.get_or_create(url=i[0],name=i[1],isbn=i[2],authors=i[3],nopages=i[4],publisher=i[5],
        #                          country=i[6],released=i[7])
        d = {"status_code": response.status_code, "status": "success"}
        records = []
        for i in li:
            record = {
                "id": i[0],
                "name": i[1],
                "isbn": i[2],
                "authors": i[3],
                "nopages": i[4],
                "publisher": i[5],
                "country": i[6],
                "release_date": i[7]
            }

            records.append(record)
        d["data"] = records
        pickup_records = json.dumps(d, indent=4)
        return HttpResponse(pickup_records, content_type="application/json")


    elif request.method == 'POST':
        serializer = BooksSerializers(data=request.data)
        records = []
        if serializer.is_valid():
            serializer.save()
            d = {"status_code": 201, "status": "success"}

            d1 = {}
            d1["books"] = serializer.data
            records.append(d1)
            d["data"] = records
            return Response(d, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def books_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Books.objects.get(url=pk)
    except Books.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BooksSerializers(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BooksSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'DELETE'])
def books_patch_delete(request, pk):
    """
         update or delete a code snippet.
    """
    try:
        snippet = Books.objects.get(url=pk)
    except Books.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = BooksSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class BooksView(APIView):
#     def get(self,request, format=None):
#         response = requests.get("https://www.anapioficeandfire.com/api/books")
#         data = response.json()
#         print(response.status_code)
#         urls = list(map(lambda x: (x['url']), data))
#         names = list(map(lambda x: (x['name']), data))
#         isbns = list(map(lambda x: (x['isbn']), data))
#         authors = list(map(lambda x: (x['authors']), data))
#         nopages = list(map(lambda x: (x['numberOfPages']), data))
#         publishers = list(map(lambda x: (x['publisher']), data))
#         country = list(map(lambda x: (x['country']), data))
#         release_dates = list(map(lambda x: (x['released']), data))
#
#         li = zip(urls,names,isbns,authors,nopages,publishers,country,release_dates)
#
#         # for i in li:
#         #     Books.objects.create(url=i[0],name=i[1],isbn=i[2],authors=i[3],nopages=i[4],publisher=i[5],
#         #                          country=i[6],released=i[7])
#         d = {"status_code": response.status_code, "status": "success"}
#         records = []
#         for i in li:
#             record = {
#                            "id": i[0],
#                            "name": i[1],
#                            "isbn": i[2],
#                            "authors": i[3],
#                            "nopages": i[4],
#                            "publisher": i[5],
#                            "country": i[6],
#                            "release_date": i[7]
#                     }
#             # print(record)
#             records.append(record)
#         d["data"] = records
#         pickup_records = json.dumps(d, indent=4)
#         return HttpResponse(pickup_records, content_type="application/json")
#
#     def post(self, request, format=None):
#         # d = {"status_code": response.status_code, "status": "success"}
#         d = {}
#         records = []
#         records.append(request.data)
#         d["data"] = records
#         data = request.data
#         params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}
#         response = requests.post("http://www.anapioficeandfire.com/api/books",params= params,json=data)
#         data = response.json()
#         print(response.status_code)
#         print(request.data)
#         return Response(data)
#
#
# class BooksList(generics.ListAPIView):
#     serializer_class = BooksSerializers
#
#     def get_queryset(self):
#         queryset = Books.objects.all()
#         name = self.kwargs['name']
#         name = re.sub(r'.*=', '', name)
#
#         # if name is not None:
#         queryset = Books.objects.all().filter(name__contains=name)
#         print(queryset)
#         return queryset
