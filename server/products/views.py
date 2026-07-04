from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import *


# ============= Products Page =============
def ProductsView(request):
    services = ServiceModel.objects.all().order_by('created_at')

    context = {
        "services": services,
        "page": "products/products.html",
    }

    if request.htmx:
        return render(request, "products/products.html", context)
    return render(request, "client/base.html", context)


# ============= Products Page =============
def ProductDetailsView(request, product_uuid, product_slug):
    product = get_object_or_404(ProductModel, uuid=product_uuid)
    breadcrumb_title = product.catalogue.service.name
    breadcrumb_sub_title = product.catalogue.name

    context = {
        "product": product,
        "breadcrumb_title": breadcrumb_title,
        "breadcrumb_sub_title": breadcrumb_sub_title,
        "page": "products/product_details.html",
    }

    if request.htmx:
        return render(request, "products/product_details.html", context)
    return render(request, "client/base.html", context)


# ============= Request Marketplace Quote Page =============
def RequestQuoteView(request, product_uuid, product_slug):
    product = get_object_or_404(ProductModel, uuid=product_uuid)
    breadcrumb_title = product.catalogue.service.name
    breadcrumb_sub_title = product.catalogue.name
    thank_you_url = request.build_absolute_uri('/thank-you/')
    service_type = 'marketplace'

    context = {
        "product": product,
        "breadcrumb_title": breadcrumb_title,
        "breadcrumb_sub_title": breadcrumb_sub_title,
        "service_type": service_type,
        "thank_you_url": thank_you_url,
        "page": "products/request_quote.html",
    }

    if request.htmx:
        return render(request, "products/request_quote.html", context)
    return render(request, "client/base.html", context)


# ============= Request Service Quote =============
def RequestServiceQuoteView(request, service_id, service_name):
    product = get_object_or_404(ServiceModel, id=service_id)
    breadcrumb_title = product.name
    breadcrumb_sub_title = 'Services'
    thank_you_url = request.build_absolute_uri('/thank-you/')
    service_type = 'service'

    context = {
        "product": product,
        "breadcrumb_title": breadcrumb_title,
        "breadcrumb_sub_title": breadcrumb_sub_title,
        "service_type": service_type,
        "thank_you_url": thank_you_url,
        "page": "products/request_quote.html",
    }

    if request.htmx:
        return render(request, "products/request_quote.html", context)
    return render(request, "client/base.html", context)


@require_POST
def submit_quote(request, uuid, slug):
    product = get_object_or_404(ProductModel, uuid=uuid)

    service = request.POST.get("service")
    full_name = request.POST.get("full_name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    message = request.POST.get("message")

    # ⚡ Basic validation
    if not full_name or not phone or not email:
        messages.error(request, "Please fill in all required fields.")
        return redirect(request.META.get("HTTP_REFERER"))

    # 💾 OPTIONAL: save to database (recommended)
    # Quote.objects.create(
    #     product=product,
    #     service=service,
    #     full_name=full_name,
    #     phone=phone,
    #     email=email,
    #     message=message,
    # )

    # 📧 OPTIONAL: send email
    from django.core.mail import send_mail
    send_mail(
        subject=f"New Quote Request - {service}",
        message=f"""
        Service: {service}
        Name: {full_name}
        Phone: {phone}
        Email: {email}
        Message: {message}
        """,
        from_email=email,
        recipient_list=[
            "sales@offtrackmining.co.za",
            "info@offtrackmining.co.za",
            "bryan@offtrackmining.co.za",
        ],
    )

    # 🎯 Redirect to thank you page
    return redirect("thank-you")


@require_POST
def submit_service_quote(request, service_id, service_name):
    service = request.POST.get("service")
    full_name = request.POST.get("full_name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    message = request.POST.get("message")

    # ⚡ Basic validation
    if not full_name or not phone or not email:
        messages.error(request, "Please fill in all required fields.")
        return redirect(request.META.get("HTTP_REFERER"))

    # 💾 OPTIONAL: save to database (recommended)
    # Quote.objects.create(
    #     product=product,
    #     service=service,
    #     full_name=full_name,
    #     phone=phone,
    #     email=email,
    #     message=message,
    # )

    # 📧 OPTIONAL: send email
    from django.core.mail import send_mail
    send_mail(
        subject=f"New Quote Request - {service}",
        message=f"""
        Service: {service}
        Name: {full_name}
        Phone: {phone}
        Email: {email}
        Message: {message}
        """,
        from_email=email,
        recipient_list=[
            "enquiries@offtrackmining.co.za",
            "info@offtrackmining.co.za",
        ],
    )

    # 🎯 Redirect to thank you page
    return redirect("thank-you")

# ============= Catalogue Page =============


def CataloguePartial(request, query_id):
    if query_id == "14":
        products = ProductModel.objects.all()
        breadcrumb_title = "Marketplace"
        breadcrumb_sub_title = "All"
    else:
        products = ProductModel.objects.filter(catalogue__id=query_id)
        breadcrumb = products.first()
        if breadcrumb:
            breadcrumb_title = breadcrumb.catalogue.service.name
            breadcrumb_sub_title = breadcrumb.catalogue.name
        else:
            breadcrumb_title = "No Products"
            breadcrumb_sub_title = ""

    context = {
        "products": products,
        "breadcrumb_title": breadcrumb_title,
        "breadcrumb_sub_title": breadcrumb_sub_title,
        "page": "partials/catalogue_partial.html",
    }

    if request.htmx:
        return render(request, "partials/catalogue_partial.html", context)
    return render(request, "client/base.html", context)


# ============= Active Invoice Search  =============
def category_filter(request):
    if request.method == "POST":
        query_id = request.POST.get("catalog_id")

    return CataloguePartial(request, query_id)


# ============= Submit Redirect Page =============
def SubmitRedirectPage(request):
    context = {

        "page": "products/submit_redirect_page.html",
    }

    if request.htmx:
        return render(request, "products/submit_redirect_page.html", context)
    return render(request, "client/base.html", context)
