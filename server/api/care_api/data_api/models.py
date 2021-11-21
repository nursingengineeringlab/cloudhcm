from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from data_api.serializers import UserSerializer, GroupSerializer
import uuid

# Create your models here.
class Senior(models.Model):
	user 		= models.OneToOneField(User, on_delete=models.CASCADE)
	name	 	= models.CharField(max_length=30, blank=True)
	gender	 	= models.CharField(max_length=10, blank=True)
	age 		= models.PositiveSmallIntegerField()
	device_id 	= models.CharField(primary_key=True, max_length=30, blank=True)
	device_type = models.CharField(max_length=10, blank=True)
	room_no 	= models.PositiveSmallIntegerField(blank=True)
	birth_date 	= models.DateField(null=True, blank=True)
	comments	= models.CharField(max_length=128, blank=True)		# Any comments for care providers

	@classmethod
	def get_serializer(cls):
		class SeniorSerializer(serializers.HyperlinkedModelSerializer):
			user =UserSerializer() 

			class Meta:
				model = Senior
				fields = ['user', 'name', 'age', 'gender', 'device_id', 'device_type', 'room_no']
				depth = 2

			def create(self, validated_data):
				user_data = validated_data.pop('user')
				new_user  = UserSerializer.create(UserSerializer(), validated_data=user_data)
				senior    = Senior.objects.create(user=new_user, **validated_data)
				return senior

		return SeniorSerializer


class FamilyMember(models.Model):
	user 		= models.OneToOneField(User, on_delete=models.CASCADE)
	age 		= models.PositiveSmallIntegerField()
	id 			= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class CareProvider(models.Model):
	user 		= models.OneToOneField(User, on_delete=models.CASCADE)
	age 		= models.PositiveSmallIntegerField()
	id 			= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Sensor_Data(models.Model):
	ECG 	= "ECG"
	RR  	= "RR"
	TEMP 	= "TEMP"
	SPO2 	= "SPO2"

	TYPES 	= [
		(ECG,  "ELECTROCARIOGRAM"),
		(RR,   "RR_INTERVAL"),
		(TEMP, "TEMPERATURE"),
		(SPO2, "BLOOD_OXYGEN")
	]

	senior 	= models.ForeignKey(Senior, on_delete=models.CASCADE)
	time	= models.PositiveIntegerField()			# Stored as 32bit unix time
	value 	= models.FloatField()
	type    = models.CharField(max_length=5, choices=TYPES)

	class Meta:
		abstract = True


class RR(Sensor_Data):
	type 	= Sensor_Data.RR 

	@classmethod
	def get_serializer(cls):
		class RRSerializer(serializers.ModelSerializer):
			device_id = serializers.CharField(write_only=True)
			senior_id = serializers.CharField(read_only=True, source='senior.device_id')

			class Meta: 
				model = RR 
				fields = ['device_id', 'senior_id', 'time', 'value']

			def create(self, validated_data):
				try:
					senior = Senior.objects.get(device_id=validated_data.pop("device_id"))
					return RR.objects.create(senior=senior, time=validated_data.get("time"), value=validated_data.get("value"))
				except Exception as e:
					raise serializers.ValidationError("User does not exist")

		return RRSerializer


class Temp(Sensor_Data):
	type 	= Sensor_Data.TEMP
	
	@classmethod
	def get_serializer(cls):
		class TempSerializer(serializers.ModelSerializer):
			device_id = serializers.CharField(write_only=True)
			senior_id = serializers.CharField(read_only=True, source='senior.device_id')

			class Meta: 
				model = Temp
				fields = ['device_id', 'senior_id', 'time', 'value']

			def create(self, validated_data):
				try:
					senior = Senior.objects.get(device_id=validated_data.pop("device_id"))
					return Temp.objects.create(senior=senior, time=validated_data.get("time"), value=validated_data.get("value"))
				except Exception as e:
					raise serializers.ValidationError("User does not exist")

		return TempSerializer



class SPO2(Sensor_Data):
	type 	= Sensor_Data.SPO2
	
	@classmethod
	def get_serializer(cls):
		class SPO2Serializer(serializers.ModelSerializer):
			device_id = serializers.CharField(write_only=True)
			senior_id = serializers.CharField(read_only=True, source='senior.device_id')

			class Meta:
				model = SPO2
				fields = ['device_id', 'senior_id', 'time', 'value']

			def create(self, validated_data):
				try:
					senior = Senior.objects.get(device_id=validated_data.pop("device_id"))
					return SPO2.objects.create(senior=senior, time=validated_data.get("time"), value=validated_data.get("value"))
				except Exception as e:
					raise serializers.ValidationError("User does not exist")

		return SPO2Serializer