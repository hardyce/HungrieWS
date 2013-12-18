from ratingManagement.models import Rating
from rest_framework import serializers

class RatingSerializer(serializers.HyperlinkedModelSerializer):
    #user = serializers.Field(source='user.username')
    user            = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    fav_menu_item   = serializers.HyperlinkedRelatedField(default= None, required=False, view_name='menuitem-detail')
    class Meta:
        model = Rating
        fields = ('user', 'restaurant','rating', 'fav_menu_item', 'comment',)
        
    def validate_user(self, attrs, source):
        attrs[source] = self.context['request'].user
        return attrs