import logging

logger = logging.getLogger(__name__)


class DbGenerics:
    @staticmethod
    def get_entity_by_pk(entity_obj, pk):
        try:
            entity = entity_obj.objects.filter(record_id=pk).first()
            return entity
        except Exception as e:
            logger.error('Exception occurred while getting entity by pk')
            logger.error(str(e))
            return None

    @staticmethod
    def get_list_of_entities(entity_obj, sorting_order='asc', start_date=None, end_date=None):
        try:
            if start_date and not end_date:
                list_of_entities = entity_obj.objects.filter(created_at__gte=start_date).order_by('created_at')
                if sorting_order == 'desc':
                    list_of_entities = entity_obj.objects.filter(created_at__gte=start_date).order_by('-created_at')
                return list_of_entities

            if start_date and end_date:
                list_of_entities = entity_obj.objects.filter(created_at__range=(start_date, end_date)).order_by(
                    'created_at')
                if sorting_order == 'desc':
                    list_of_entities = entity_obj.objects.filter(created_at__range=(start_date, end_date)).order_by(
                        '-created_at')
                return list_of_entities

            list_of_entities = entity_obj.objects.all().order_by('created_at')
            if sorting_order == 'desc':
                list_of_entities = entity_obj.objects.all().order_by('-created_at')
            return list_of_entities

        except Exception as e:
            logger.error('Exception occurred while getting entity by pk')
            logger.error(str(e))
            return None
