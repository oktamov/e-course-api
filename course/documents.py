# from django_elasticsearch_dsl import Document # noqa
# from django_elasticsearch_dsl.registries import registry # noqa
#
# from course.models import Course # noqa
#
#
# @registry.register_document # noqa
# class CourseDocument(Document): # noqa
#     class Index: # noqa
#         # Name of the Elasticsearch index # noqa
#         name = "courses" # noqa
#         # See Elasticsearch Indices API reference for available settings # noqa
#         settings = {"number_of_shards": 1, "number_of_replicas": 0} # noqa
#
#     class Django: # noqa
#         model = Course  # The model associated with this Document # noqa
#
#         # The fields of the model you want to be indexed in Elasticsearch
#         fields = ["name", "desc"] # noqa

# CourseDocument.search().filter() # noqa
