from django.contrib.auth.models import Group, User


def check_user_group(user):
    group = Group.objects.get(name='my_group')
    return group in user.groups.all()

def add_user_to_group(user_id, group_name):
    user = User.objects.get(id=user_id)
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)

def remove_user_from_group(user_id, group_name):
    user = User.objects.get(id=user_id)
    group = Group.objects.get(name=group_name)
    user.groups.remove(group)
    user.save()