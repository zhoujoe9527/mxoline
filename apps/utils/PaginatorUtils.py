# -*- coding：utf-8 -*-
__author__ = 'zhoujoe'
__date__ = '2020/5/15 23:00'

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class PaginatorUtils(object):
    """
    该工具类实现分页显示的功能
    request:html的request对象
    comtnet:需要分页的内容,一般是querySet对象
    page_num:每页显示内容的个数
    paging_sign:html中页码的标签名称,字符串
    最终返回的是请求的分页内容,是一个Paginator对象
    """
    @classmethod
    def paginator(cls, request, comtent, page_num, paging_sign = 'page'):
        #获取请求第几分页的页数
        try:
            page = request.GET.get(paging_sign, 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(comtent, page_num, request=request)

        #该分页的内容
        paging_content = p.page(page)

        return paging_content
