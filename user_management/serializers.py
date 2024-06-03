import re
from rest_framework import serializers
from .models import Users

class RoleSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    role = serializers.CharField()
    
    def validate_role(self, role):
        if role.lower() not in ['admin', 'user']:
            raise serializers.ValidationError("Invalid value for role field.")
        return role.lower()
    
    def validate_id(self, id):
        if id == self.context['request'].user.id:
            raise serializers.ValidationError("You cannot change your own role.")
        return id
    
    class Meta:
        model = Users  
        fields = ('id', 'role')
        
    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'role', 'password', 'profile_picture_url', 'is_verified', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True}, 
            'id': {'read_only': True},  
            'is_verified': {'read_only': True},  
            'role': {'read_only': True},  
        }
 
    def validate_gender(self, value):
        if value.lower() not in ['male', 'female']:
            raise serializers.ValidationError("Invalid value for gender field.")
        return value.lower()
            
    def validate_password(self, password):
        errors = []   
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lower-case letter.")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one upper-case letter.")
        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one digit.")
        if not re.search(r'[@_!#$%^&*()<>?/\|}{~:=+-.,\[\]]', password):
            errors.append("Password must contain at least one special character.")
        if errors:
            raise serializers.ValidationError(errors)
            
        return password
    
    def save(self, **kwargs):
        user = Users(**self.validated_data)
        user.set_password(self.validated_data['password'])
        user.save()
        return user
 
class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    
    def validate_gender(self, value):
        if value.lower() not in ['male', 'female']:
            raise serializers.ValidationError("Invalid value for gender field.")
        return value.lower()
            
    def validate_password(self, password):
        errors = []   
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lower-case letter.")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one upper-case letter.")
        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one digit.")
        if not re.search(r'[@_!#$%^&*()<>?/\|}{~:=+-.,\[\]]', password):
            errors.append("Password must contain at least one special character.")
        if errors:
            raise serializers.ValidationError(errors)
            
        return password
  
    def validate(self, data):
        if 'password' in data and data['password']:
            self.validate_password(data['password'])
            
            if 'old_password' not in data or not data['old_password']:
                raise serializers.ValidationError({"old_password": "Old password is required when updating password."})
                
            if not self.instance.check_password(data['old_password']):
                raise serializers.ValidationError({'old_password': "Old password is incorrect."})
        
        return data

    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'role', 'password', 'old_password', 'profile_picture_url', 'is_verified', 'created_at', 'updated_at')
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'read_only': True},
            'password': {'required': False, 'write_only': True, 'allow_blank': True, 'allow_null': True},
            'first_name': {'required': False, 'allow_blank': True, 'allow_null': True},
            'last_name': {'required': False, 'allow_blank': True, 'allow_null': True},
            'gender': {'required': False, 'allow_blank': True, 'allow_null': True},
            'date_of_birth': {'required': False, 'allow_null': True},
            'role': {'read_only': True},
            'is_verified': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        
        if 'password' in validated_data and validated_data['password']:
            instance.set_password(validated_data['password'])
            
        instance.save()
        return instance
    
class UserProfilePictureUpdateSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()

    class Meta:
        fields = ['profile_picture']

    def validate_profile_picture(self, value):
        max_size = 2 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Profile picture size must be less than 2 MB.")
        return value