from modeltranslation.translator import TranslationOptions, translator

from course.models import Course


class CourseTranslationOptions(TranslationOptions):
    fields = ("name", "desc")


translator.register(Course, CourseTranslationOptions)
