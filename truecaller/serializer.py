import textdistance as td
from rest_framework import serializers
from .models import RegisterUsers, People, PeopleDetails

class RegisterUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUsers
        fields = ('name','phone_number','email','password')
        extra_kwargs = {"password": {"write_only": True}}

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('phone_number','spam')

    def update(self, instance, validated_data):
        instance.spam = validated_data.get('spam',instance.spam)
        instance.save()
        return PeopleSerializer(instance)

class NumberCheckerSerializer(serializers.ModelSerializer):

    spam = serializers.SerializerMethodField('get_spam_details')

    class Meta:
        model = RegisterUsers
        fields = ('name', 'phone_number','spam')

    def get_spam_details(self,instance):
        try:
            obj = People.objects.get(phone_number=instance.phone_number)
            spam = obj.spam
        except:
            spam = "False"
        return spam

class NumberListSerializer(serializers.ModelSerializer):

    spam = serializers.SerializerMethodField('check_spam')

    class Meta:
        model = PeopleDetails
        fields = ('name','phone_number','spam')

    def check_spam(self,instance):
        try:
            obj = People.objects.get(phone_number=instance.phone_number)
            spam = obj.spam
        except:
            spam = "False"
        return spam

class PeopleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleDetails
        field = ('name','phone_number','friend')

    def add_details(instance):
        friend = RegisterUsers.objects.get(phone_number=instance['friend'])
        obj = PeopleDetails(name=instance['name'],phone_number=instance['phone_number'],friend=friend)
        obj.save()
        return obj

class NameListSerializer(serializers.ModelSerializer):

    spam = serializers.SerializerMethodField('check_spam')

    class Meta:
        model = PeopleDetails
        fields = ('name','phone_number','spam')

    def check_spam(self, instance):
        try:
            obj = People.objects.get(phone_number=instance.phone_number)
            spam = obj.spam
        except:
            spam = "False"
        return spam

class DetailSerializer(serializers.ModelSerializer):

    spam = serializers.SerializerMethodField('check_spam')
    class Meta:
        model = RegisterUsers
        fields = ('name','phone_number','email','spam')

    def check_spam(self, instance):
        try:
            obj = People.objects.get(phone_number=instance.phone_number)
            spam = obj.spam
        except:
            spam = "False"
        return spam

class DetailWithoutEmailSerializer(serializers.ModelSerializer):

    spam = serializers.SerializerMethodField('check_spam')
    class Meta:
        model = RegisterUsers
        fields = ('name','phone_number','spam')

    def check_spam(self, instance):
        try:
            obj = People.objects.get(phone_number=instance.phone_number)
            spam = obj.spam
        except:
            spam = "False"
        return spam
