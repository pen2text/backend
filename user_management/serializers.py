import re
from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'role', 'password', 'is_verified', 'created_at', 'updated_at')
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

class UserUpdateSerializer(UserSerializer):
    id = serializers.UUIDField()
    old_password = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
       
    def validate_password(self, password):
        if not password or not password.strip(): 
            return password
        
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
        
        if not 'old_password' in self.initial_data or not self.initial_data['old_password'].strip():
            raise serializers.ValidationError("Old password is required when updating password.")     
            
        return password
    
    def validate_old_password(self, old_password):

        if not old_password or not old_password.strip():
            raise serializers.ValidationError("Old password is required when updating password.")
        
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
            
    def validate(self, data):
        if 'password' not in data or data['password'].strip() == '':
            data.pop('password', None)
            data.pop('old_password', None)
            return data
        
        self.validate_password(data['password'])
        self.validate_old_password(data.get('old_password', ''))
        
        return data
        
    class Meta(UserSerializer.Meta):
        fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'role', 'password', 'old_password', 'is_verified', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'required': False, 'write_only': True, 'allow_blank': True, 'allow_null': True},
            'role': {'read_only': True},
            'is_verified': {'read_only': True},
            'email': {'read_only': True},
        }
        
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        
        if 'password' in validated_data:
            instance.set_password(validated_data.get['password'])
            
        instance.save()
        return instance

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