from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.list import ListView
from .models import RolePlayingRoom
from .forms import RolePlayingRoomForm
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.contrib import messages


@method_decorator(staff_member_required, name="dispatch")
class RolePlaylingRoomListAPIView(ListView):
    model = RolePlayingRoom

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
    
role_playing_room_list = RolePlaylingRoomListAPIView.as_view()


@method_decorator(staff_member_required, name="dispatch")
class RolePlaylingRoomDetailAPIView(DetailView):
    model = RolePlayingRoom

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
    
role_playing_room_detail = RolePlaylingRoomDetailAPIView.as_view()


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomCreateView(CreateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm

    def form_valid(self, form):
        role_playing_room = form.save(commit=False)
        role_playing_room.user = self.request.user
        return super().form_valid(form)

role_playing_room_new = RolePlayingRoomCreateView.as_view()


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomUpdateView(UpdateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
role_playing_room_edit = RolePlayingRoomUpdateView.as_view()


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomDeleteView(DeleteView):
    model = RolePlayingRoom
    success_url = reverse_lazy("role_playing_room_list")
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "채팅방을 삭제했습니다.")
        return response
role_playing_room_delete = RolePlayingRoomDeleteView.as_view()