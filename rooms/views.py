# from django.db.models.query import InstanceCheckMeta
from django.core import paginator
from django.shortcuts import render
from django.core.paginator import Paginator

# from django.shortcuts import redirect
# from django.http import Http404
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django_countries import countries
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