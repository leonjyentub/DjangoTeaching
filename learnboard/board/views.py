from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import MessageForm, RegistrationForm
from .models import Message


class MessageListView(ListView):
    model = Message
    template_name = "board/message_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Message.objects.select_related("author")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(Q(content__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


def register(request):
    if request.user.is_authenticated:
        return redirect("board:list")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "註冊成功，歡迎加入學言板！")
        return redirect("board:list")
    return render(request, "registration/register.html", {"form": form})


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "board/message_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "留言已發布。")
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "board/message_form.html"

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "留言已更新。")
        return super().form_valid(form)


class OwnerOrStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    """作者本人可以操作；is_staff 管理員可以管理任何留言。"""

    raise_exception = True

    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.pk or self.request.user.is_staff


class MessageDeleteView(OwnerOrStaffMixin, DeleteView):
    model = Message
    template_name = "board/message_confirm_delete.html"
    success_url = reverse_lazy("board:list")

    def form_valid(self, form):
        messages.success(self.request, "留言已刪除。")
        return super().form_valid(form)
