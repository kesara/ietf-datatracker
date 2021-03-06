# Copyright The IETF Trust 2014-2019, All Rights Reserved
# -*- coding: utf-8 -*-
# Autogenerated by the mkresources management command 2014-11-13 23:53


from ietf.api import ModelResource
from tastypie.fields import ToOneField
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache

from ietf import api

from ietf.dbtemplate.models import DBTemplate


from ietf.group.resources import GroupResource
from ietf.name.resources import DBTemplateTypeNameResource
class DBTemplateResource(ModelResource):
    type             = ToOneField(DBTemplateTypeNameResource, 'type')
    group            = ToOneField(GroupResource, 'group', null=True)
    class Meta:
        cache = SimpleCache()
        queryset = DBTemplate.objects.all()
        serializer = api.Serializer()
        #resource_name = 'dbtemplate'
        ordering = ['id', ]
        filtering = { 
            "id": ALL,
            "path": ALL,
            "title": ALL,
            "variables": ALL,
            "content": ALL,
            "type": ALL_WITH_RELATIONS,
            "group": ALL_WITH_RELATIONS,
        }
api.dbtemplate.register(DBTemplateResource())

