from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic import View
from django.http import Http404
from users import models as user_models
from . import models
from django.db.models import Q  # Used in Complexed Queries


def go_conversation(request, host_pk, guest_pk):
    a = host_pk
    b = guest_pk
    try:
        user_one = user_models.User.objects.get(pk=a)
        user_two = user_models.User.objects.get(pk=b)
    except Exception:
        user_one = None
        user_two = None
    if user_one is not None and user_two is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(
    View
):  # By default, DetailView finds kwargs in url for you
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        print(conversation)
        if not conversation:
            raise Http404(0)
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {
                "conversation": conversation,
            },
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        print(conversation)
        if not conversation:
            raise Http404(0)
        if message is not None:
            models.Message.objects.create(
                message=message,
                user=self.request.user,
                conversation=conversation,
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
