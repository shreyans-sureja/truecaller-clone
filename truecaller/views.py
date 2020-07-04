import textdistance as td
import jwt, datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, request
from .serializer import RegisterUsersSerializer, PeopleSerializer, NumberCheckerSerializer, NumberListSerializer, PeopleDetailsSerializer, NameListSerializer, DetailSerializer, DetailWithoutEmailSerializer
from .models import RegisterUsers, People, PeopleDetails

def check_token(data):
    token = None
    if 'X-ACCESS-TOKEN' in data:
        token = data['X-ACCESS-TOKEN']
    if not token:
        return None
    try:
        info = jwt.decode(token, 'instahyre')
        user = RegisterUsers.objects.get(phone_number=str(info['phone_number']))
        return user
    except:
        return None

@api_view(['POST'])
def register(request):
    serializer = RegisterUsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        user = RegisterUsers.objects.get(phone_number = request.data['phone_number'])
        if user.password == request.data['password']:
            token = jwt.encode({'phone_number':str(user.phone_number), 'exp':datetime.datetime.utcnow() + datetime.timedelta(days=30)},'instahyre')
            return Response({'token' : token},status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def report_spam(request):

    if check_token(request.headers) is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        entry = People.objects.get(phone_number = request.data['phone_number'])
        update = PeopleSerializer.update(PeopleSerializer, entry, request.data)
        return Response(update.data,status=status.HTTP_202_ACCEPTED)
    except:
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_number(request,number):

    if check_token(request.headers) is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = None
    try:
        obj = RegisterUsers.objects.get(phone_number=str(number))
        serializer = NumberCheckerSerializer(obj)
    except:
        list = PeopleDetails.objects.filter(phone_number=number)
        serializer = NumberListSerializer(list,many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_name(request,name):

    if check_token(request.headers) is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    people = PeopleDetails.objects.filter(name__icontains=name)
    text_distance = []

    if not len(people):
        return Response([],status=status.HTTP_200_OK)

    for text in people.iterator():
        text_distance.append(td.sorensen.normalized_similarity(text.name, name))

    serializer = NameListSerializer(people,many=True)

    return Response(list(zip(*(sorted(zip(text_distance, serializer.data),reverse=True))))[1],status=status.HTTP_200_OK)

@api_view(['GET'])
def person_details(request,number):
    user = check_token(request.headers)

    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        searched_person = RegisterUsers.objects.get(phone_number=number)
        obj = PeopleDetails.objects.filter(phone_number=user.phone_number,friend=searched_person)
        print(len(obj))
        serializer = None

        if len(obj):
            serializer = DetailSerializer(searched_person)
        else:
            serializer = DetailWithoutEmailSerializer(searched_person)

        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def post_data(request):

    if check_token(request.headers) is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        PeopleDetailsSerializer.add_details(request.data)
        return Response("succesfull",status=status.HTTP_202_ACCEPTED)
    except:
        return Response("something went wrong",status=status.HTTP_400_BAD_REQUEST)

