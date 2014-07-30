# -*- coding: utf-8 -*-
from Products.CMFCore.Expression import Expression, getExprContext


def get_marker_image(context, marker_img):
    try:
        marker_img = Expression(str(marker_img))(getExprContext(context))
    except:
        marker_img = ''
    return marker_img
