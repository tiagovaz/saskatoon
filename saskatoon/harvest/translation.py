from modeltranslation.translator import register, TranslationOptions
from harvest.models import Equipment, EquipmentType, TreeType


#@register(Equipment)
#class EquipmentTranslationOptions(TranslationOptions):
#    fields = ['description']
#
#
#@register(EquipmentType)
#class EquipmentTypeTranslationOptions(TranslationOptions):
#    fields = ['name']
#
#
#@register(TreeType)
#class TreeTypeTranslationOptions(TranslationOptions):
#    fields = ['name', 'fruit_name']
