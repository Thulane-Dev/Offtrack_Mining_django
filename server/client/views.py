from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import *
from django.db.models import Q, Case, When, IntegerField


# ============= Index Page =============
def IndexView(request):
    # services = ServiceModel.objects.prefetch_related(
    #     "service__catalogue"
    # )

    # services = ServiceModel.objects.filter(
    #     service__catalogue__isnull=False
    # ).prefetch_related(
    #     "service__catalogue"
    # ).annotate(
    #     custom_order=Case(
    #         When(id=6, then=0),
    #         default=1,
    #         output_field=IntegerField(),
    #     )
    # ).order_by('custom_order')

    # services = ServiceModel.objects.filter(
    #     service__catalogue__isnull=False
    # ).prefetch_related(
    #     "service__catalogue"
    # ).annotate(
    #     custom_order=Case(
    #         When(id=6, then=0),
    #         default=1,
    #         output_field=IntegerField(),
    #     )
    # ).order_by('custom_order').distinct()

    # services = ServiceModel.objects.filter(
    #     Q(service__catalogue__isnull=False) | Q(id=6)
    # ).prefetch_related(
    #     "service__catalogue"
    # ).annotate(
    #     custom_order=Case(
    #         When(id=6, then=0),
    #         default=1,
    #         output_field=IntegerField(),
    #     )
    # ).order_by('custom_order').distinct()

    services = ServiceModel.objects.prefetch_related(
        "service__catalogue"
    ).annotate(
        custom_order=Case(
            When(id=6, then=0),
            default=1,
            output_field=IntegerField(),
        )
    ).order_by('custom_order')

    breadcrumb_title = "Marketplace"
    breadcrumb_sub_title = "All"
    products = ProductModel.objects.filter(
        catalogue__service__name="Marketplace")

    thank_you_url = request.build_absolute_uri('/thank-you/')

    context = {
        "services": services,
        "products": products,
        "breadcrumb_title": breadcrumb_title,
        "breadcrumb_sub_title": breadcrumb_sub_title,
        "thank_you_url": thank_you_url,
        "display_labels": True,
        "page": "client/index.html",
    }

    if request.htmx:
        return render(request, "client/index.html", context)
    return render(request, "client/base.html", context)


# ============= About Page =============
def AboutView(request):
    context = {
        "page": "client/about.html",
    }

    if request.htmx:
        return render(request, "client/about.html", context)
    return render(request, "client/base.html", context)


# ============= Marketplace Page =============
def MarketplaceView(request):
    services = ServiceModel.objects.prefetch_related(
        "service__catalogue"
    ).filter(
        name="Marketplace"
    ).annotate(
        custom_order=Case(
            When(id=6, then=0),
            default=1,
            output_field=IntegerField(),
        )
    ).order_by('custom_order')

    breadcrumb_title = "Marketplace"
    breadcrumb_sub_title = "All"
    products = ProductModel.objects.filter(
        catalogue__service__name="Marketplace")

    context = {
        "services": services,
        "products": products,
        "breadcrumb_title": breadcrumb_title,
        "breadcrumb_sub_title": breadcrumb_sub_title,
        "display_labels": False,
        "page": "client/services.html",
    }

    if request.htmx:
        return render(request, "client/services.html", context)
    return render(request, "client/base.html", context)


# ============= Services Page =============
def ServicesView(request):
    services = ServiceModel.objects.prefetch_related(
        "service__catalogue"
    ).annotate(
        custom_order=Case(
            When(id=6, then=0),
            default=1,
            output_field=IntegerField(),
        )
    ).order_by('custom_order').exclude(name="Marketplace")

    first_service = services.first()  # or services[0] if you're sure it exists

    breadcrumb_title = first_service.name
    breadcrumb_sub_title = "Service"
    products = ProductModel.objects.filter(
        catalogue__service=first_service
    )

    context = {
        "services": services,
        "products": products,
        "breadcrumb_title": breadcrumb_title,
        "breadcrumb_sub_title": breadcrumb_sub_title,
        "display_labels": False,
        "page": "client/services_page.html",
    }

    if request.htmx:
        return render(request, "client/services_page.html", context)
    return render(request, "client/base.html", context)


# ============= Contract Page =============
def ContractView(request):
    thank_you_url = request.build_absolute_uri('/thank-you/')

    context = {
        "thank_you_url": thank_you_url,
        "page": "client/contract.html",
    }

    if request.htmx:
        return render(request, "client/contract.html", context)
    return render(request, "client/base.html", context)


@require_POST
def Submit_Contact_Enquiry(request):
    full_name = request.POST.get("full_name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    message = request.POST.get("message")

    # ⚡ Basic validation
    if not full_name or not phone or not email:
        messages.error(request, "Please fill in all required fields.")
        return redirect(request.META.get("HTTP_REFERER"))

    # 📧 OPTIONAL: send email
    from django.core.mail import send_mail
    send_mail(
        subject=f"New Contact Enquiry - {full_name}",
        message=f"""
        Name: {full_name}
        Phone: {phone}
        Email: {email}
        Message: {message}
        """,
        from_email=email,
        recipient_list=["enquiries@offtrackmining.co.za"],
    )

    # 🎯 Redirect to thank you page
    return redirect("thank-you")


# ============= Menu View =============
def MenuView(request):
    context = {
        "show_navbar": False,
        "show_footer": False,
        "page": "client/menu.html",
    }

    if request.htmx:
        return render(request, "client/menu.html", context)
    return render(request, "client/base.html", context)
