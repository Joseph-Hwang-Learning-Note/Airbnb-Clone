# from django.db.models.query import InstanceCheckMeta
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.forms import Form
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

# from django.urls.base import reverse_lazy
from users.mixins import LoggedInOnlyView

# from django.core import paginator
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse

# from django.shortcuts import redirect
# from django.http import Http404
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView

# from django_countries import countries
from . import models, forms

# ccbv 참조


class HomeView(ListView):

    """ HomeView Definition """

    template_name = "rooms/room_list.html"
    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    # page_kwarg = "page"
    context_object_name = "rooms"


# Below is how it's working

# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)

#     try:
#         rooms = paginator.page(int(page))
#         return render(
#             request,
#             "rooms/home.html",
#             {
#                 "page": rooms,
#             },
#         )
#     except EmptyPage:
#         return redirect("/")


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room  # Django gives you the object as model name in lower case
    # pk_url_kwarg = "pk"


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms_gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host.superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                page_obj = paginator.get_page(page)

                rooms = paginator.get_page(page)

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms, "page_obj": page_obj},
                )

        else:
            form = forms.SearchForm()

            return render(request, "rooms/search.html", {"form": form})

    # city = request.GET.get("city", "Anywhere")
    # city = str.capitalize(city)
    # country = request.GET.get("country", "KR")
    # room_type = int(request.GET.get("room_type", 0))
    # price = int(request.GET.get("price", 0))
    # guests = int(request.GET.get("guests", 0))
    # bedrooms = int(request.GET.get("bedrooms", 0))
    # beds = int(request.GET.get("beds", 0))
    # baths = int(request.GET.get("baths", 0))
    # selected_amenities = request.GET.getlist("amenities")
    # selected_facilities = request.GET.getlist("facilities")
    # instant = bool(request.GET.get("instant", False))
    # superhost = bool(request.GET.get("superhost", False))

    # form = {
    #     "city": city,
    #     "selected_room_type": room_type,
    #     "price": price,
    #     "guests": guests,
    #     "bedrooms": bedrooms,
    #     "beds": beds,
    #     "baths": baths,
    #     "selected_amenities": selected_amenities,
    #     "selected_facilities": selected_facilities,
    #     "instant": instant,
    #     "superhost": superhost,
    # }

    # room_types = models.RoomType.objects.all()
    # amenities = models.Amenity.objects.all()
    # facilities = models.Facility.objects.all()

    # choices = {
    #     "selected_country": country,
    #     "room_types": room_types,
    #     "amenities": amenities,
    #     "facilities": facilities,
    #     "countries": countries,
    # }

    # filter_args = {}

    # if city != "Anywhere":
    #     filter_args["city__startswith"] = city

    # filter_args["country"] = country

    # if room_type != 0:
    #     filter_args["room_type__pk"] = room_type

    # if price != 0:
    #     filter_args["price__lte"] = price

    # if guests != 0:
    #     filter_args["guests__gte"] = guests

    # if bedrooms != 0:
    #     filter_args["bedrooms_gte"] = bedrooms

    # if beds != 0:
    #     filter_args["beds__gte"] = beds

    # if baths != 0:
    #     filter_args["baths__gte"] = baths

    # if instant is True:
    #     filter_args["instant_book"] = True

    # if superhost is True:
    #     filter_args["host.superhost"] = True

    # if len(selected_amenities) > 0:
    #     for selected_amenity in selected_amenities:
    #         filter_args["amenities__pk"] = int(selected_amenity)

    # if len(selected_facilities) > 0:
    #     for selected_facility in selected_facilities:
    #         filter_args["facilities__pk"] = int(selected_facility)

    # rooms = models.Room.objects.filter(**filter_args)

    # return render(
    #     request,
    #     "rooms/search.html",
    #     {**form, **choices, "rooms": rooms},
    # )


class EditRoomView(UpdateView):

    # connected to get_absolute_url

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "beds",
        "bedrooms",
        "baths",
        "guests",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(LoggedInOnlyView, RoomDetail):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class EditPhotoView(LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_message = "Photo Updated"

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "rooms/photo_create.html"
    fields = (
        "caption",
        "file",
    )
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(
            pk
        )  # I don't know why should we do like this. Need a further research
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


@login_required
def delete_photo(request, room_pk, photo_pk):

    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.get(pk=photo_pk).delete()
            messages.success(request, "Photo deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


@login_required
@require_http_methods(["POST"])
def delete_room(request, pk):

    user = request.user
    user_pk = user.pk
    try:
        room = models.Room.objects.get(pk=pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete the Room")
        else:
            room.delete()
            messages.success(request, "Room Deleted")
        return redirect(reverse("users:profile", kwargs={"pk": user_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class DeleteRoomView(TemplateView):

    template_name = "rooms/room_delete.html"


class CreateRoomView(LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()  # Important Part!!
        messages.success(self.request, "Room Created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
