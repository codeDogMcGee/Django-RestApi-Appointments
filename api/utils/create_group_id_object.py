from api.serializers import GroupIdsSerializer

def create_group_id_object(group: object) -> None:
    group_id_object = {'group_name':group.name, 'group_id': group.id}
    serializer = GroupIdsSerializer(data=group_id_object)

    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(f'\nERROR SAVING GROUP ID MODEL: {serializer.errors}\n')