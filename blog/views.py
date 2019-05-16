import markdown
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from .models import Paper, Tag, Comment, Category, User


# Create your views here.
def render_page(request, papers=None, html_path='Index/index.html', paper=None):
    """
    根据所给数据渲染页面
    :param request: url请求包括POST, 和GET
    :param papers: 多篇文章
    :param html_path: html页面路径
    :param paper: 单片文章 --- 详情页
    :return: render(something)
    """
    if papers:
        limit = 3   # 按每页4条分页
        page_number = 3    # 每页页码数量
        paginator = Paginator(papers, limit)
        if request.method == "GET":
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                papers = paginator.page(page)
            # 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                papers = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')

            finally:
                # 生成当前页页码范围

                if papers.number+page_number < papers.paginator.num_pages:
                    page_range = range(papers.number, papers.number+page_number)
                else:
                    page_range = range(papers.number, papers.paginator.num_pages)

    dates = Paper.objects.dates('date', 'month')[0:3]
    tags = Tag.objects.all()
    categories = Category.objects.all()
    all_paper = Paper.objects.all()
    latest_papers = all_paper.order_by('-date')
    latest_papers = latest_papers[0:4]
    return render(request, html_path,
                  {
                      'papers': papers,
                      'dates': dates,
                      'tags': tags,
                      'latest_papers': latest_papers,
                      'categories': categories,
                      'username': request.session.get('username'),
                      'paper': paper,
                      'page_range': page_range
                  })


def detail(request, paper_id):
    if request.method == 'GET':
        paper = Paper.objects.get(pk=paper_id)
        paper.reading += 1
        paper.save()
        return render_page(request, paper=paper, html_path='blog/single.html')

    # comment
    elif request.method == 'POST':
        comment_ = request.POST.get('comment')
        paper = Paper.objects.get(pk=paper_id)
        # TODO 这里的 user 要改成当前登录用户
        user = request.session.get('username')
        user = User.objects.get(name=user)
        comment = Comment(content=comment_, paper=paper, user=user)
        comment.save()
        return redirect(to=reverse('blog:detail', args=paper_id))


def write(request):
    if request.method == 'GET':
        return render_page(request, html_path='blog/write.html')

    elif request.method == 'POST':
        paper = Paper()
        paper.name = request.POST.get('name')
        paper.user = User.objects.get(name=request.session['username'])
        paper.category = Category.objects.get(pk=request.POST.get('category'))
        paper.save()
        # paper.tag_set = tags 不需要save就可以添加多对多字段
        for tag_id in request.POST.getlist('tag'):
            paper.tag.add(tag_id)

        paper.content = request.POST.get('content')
        # markdown渲染
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        paper.content = md.convert(paper.content)
        paper.toc = md.toc
        paper.save()
        return redirect(to=reverse('blog:detail', args=[paper.id]))


def category(request, category_id):
    category_ = Category.objects.get(pk=category_id)
    papers = category_.paper_set.all()
    return render_page(request, papers=papers)


def tag(request, tag_id):
    category_ = Category.objects.get(pk=tag_id)
    papers = category_.paper_set.all()
    return render_page(request, papers=papers)


def date(request, date_):
    year = int(date_[0:4])
    month = int(date_[5:7])
    papers = Paper.objects.filter(date__year=year).filter(date__month=month).all()
    return render_page(request, papers=papers)


class RSSFeed(Feed):
    title = "RSS feed - article"
    link = "/"
    description = "RSS feed - blog posts"

    def items(self):
        return Paper.objects.order_by('-date')

    def item_title(self, item):
        return item.name

    def item_pubdate(self, item):
        return item.date

    def item_description(self, item):
        return item.toc

    def item_link(self, item):
        return reverse('blog:detail', args=(item.id,))
