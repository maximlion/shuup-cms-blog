# This file is part of Shuup CMS Blog Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _

from shuup.simple_cms.models import Page
from shuup.xtheme import TemplatedPlugin
from shuup.xtheme.resources import add_resource


class ShuupCMSBlogArticleListPlugin(TemplatedPlugin):
    identifier = "shuup_cms_blog_articles_list"
    name = _("Blog Articles List")
    template_name = "shuup_cms_blog/plugins/article_list.jinja"

    def get_context_data(self, context):
        context = super(ShuupCMSBlogArticleListPlugin, self).get_context_data(context)
        request = context["request"]
        context["articles"] = Page.objects.visible(request.shop).filter(
            blog_article__is_blog_article=True
        ).order_by("-available_from")
        return context

    def render(self, context):
        add_resource(context, "head_end", static("shuup-cms-blog.css"))
        return super(ShuupCMSBlogArticleListPlugin, self).render(context)


class ShuupCMSBlogSaveArticleButtonPlugin(TemplatedPlugin):
    identifier = "shuup_cms_blog_save_article_button"
    name = _("Blog Save Article Button")
    template_name = "shuup_cms_blog/plugins/save_article.jinja"
    required_context_variables = ("request", "object")

    def is_context_valid(self, context):
        return bool(
            context.get("request") and
            context["request"].customer and
            isinstance(context["object"], Page)
        )

    def get_context_data(self, context):
        context = super(ShuupCMSBlogSaveArticleButtonPlugin, self).get_context_data(context)
        request = context["request"]
        context["is_saved"] = False
        context["article"] = context["object"]
        if request.customer.options and request.customer.options.get("saved_articles"):
            context["is_saved"] = context["article"].pk in request.customer.options["saved_articles"]
        return context
