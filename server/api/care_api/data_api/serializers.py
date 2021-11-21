from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
#from data_api.models import Senior, FamilyMember, CareProvider, RR_Data
from rest_framework.exceptions import NotFound

class UserSerializer(serializers.HyperlinkedModelSerializer):
	password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
	)

	class Meta:
		model = User
		fields = ['url', 'username', 'email', 'password']

	def create(self, validated_data):
		validated_data['password'] = make_password(validated_data.get('password'))
		return super(UserSerializer, self).create(validated_data)

	def update(self, instance, validated_data):
		user = super().update(instance, validated_data)
		try:
			user.set_password(validated_data['password'])
			user.save()
		except KeyError:
			pass
		return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
