from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User,auth
from .models import *
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
from django.utils.text import slugify
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.contrib.auth import logout  # Correct import
from django.views.decorators.http import require_POST
from django.db.models import Avg
from django.template import Library
from django.conf import settings
# Create your views here.



def index(request):
    content = SectionContent.objects.first()
    about_section = AboutSection.objects.first()
    expertise_list = Expertise.objects.all()
    water_solution = WaterSolution.objects.first()
    filtration_items = FiltrationItem.objects.all() 
    testimonials = Testimonial.objects.all()

    # Prepare testimonials with stars
    testimonials_with_stars = []
    for testimonial in testimonials:
        full_stars = "★" * testimonial.rating
        empty_stars = "☆" * (5 - testimonial.rating)
        testimonials_with_stars.append({
            'client_name': testimonial.client_name,
            'client_image': testimonial.client_image,
            'title': testimonial.title,
            'message': testimonial.message,
            'full_stars': full_stars,
            'empty_stars': empty_stars,
        })

    gallery_images = GalleryImage.objects.all()
    products = ProductShowcase.objects.all()
    steps = WaterTreatmentProcess.objects.order_by("step_number")

    return render(request, 'index.html', {
        'content': content,
        'about_section': about_section,
        'expertise_list': expertise_list,
        'water_solution': water_solution,
        'testimonials': testimonials_with_stars,  # Pass processed testimonials
        'gallery_images': gallery_images,
        'products': products,
        'steps': steps,
        'filtration_items':filtration_items,
    })



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save the data to the database
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        # Send an email
        send_mail(
            subject=f"New Contact Message from {name}",
            message=f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}",
            from_email='amald416@gmail.com',  # Replace with your email
            recipient_list=['travellingiscure@gmail.com'],  # Replace with the recipient email
            fail_silently=False,
        )

        return redirect('index')  # Redirect to a thank-you page after submission




def add_section_content(request):
    if request.method == 'POST':
        heading = request.POST.get('heading')
        subheading = request.POST.get('subheading')
        request_quote_url = request.POST.get('request_quote_url')
        whatsapp_url = request.POST.get('whatsapp_url')
        logo = request.FILES.get('logo')
        image = request.FILES.get('image')

        # Debugging
        print("Logo: ", logo)
        print("Image: ", image)

        # Validate the presence of required fields
        if not logo or not image:
            return render(request, 'add_section_content.html', {
                'error': "Both logo and image are required.",
                'all_content': SectionContent.objects.all(),
            })

        SectionContent.objects.create(
            heading=heading,
            subheading=subheading,
            request_quote_url=request_quote_url,
            whatsapp_url=whatsapp_url,
            logo=logo,
            image=image
        )
        return redirect('add_section_content')  # Redirect to the same page or another
    
    all_content = SectionContent.objects.all()
    return render(request, 'add_section_content.html', {'all_content': all_content})






def edit_section_content(request, content_id):
    content = SectionContent.objects.get(id=content_id)

    if request.method == 'POST':
        content.heading = request.POST.get('heading')
        content.subheading = request.POST.get('subheading')
        content.request_quote_url = request.POST.get('request_quote_url')
        content.whatsapp_url = request.POST.get('whatsapp_url')

        if request.FILES.get('logo'):
            content.logo = request.FILES.get('logo')

        if request.FILES.get('image'):
            content.image = request.FILES.get('image')

        content.save()
        return redirect('add_section_content')  # Redirect to the list page or another

    return render(request, 'edit_section_content.html', {'content': content})




def delete_section_content(request, content_id):
    content = SectionContent.objects.get(id=content_id)
    content.delete()
    return redirect('add_section_content')





def add_about_section(request):
    if request.method == 'POST':
        heading = request.POST.get('heading')
        highlight_text = request.POST.get('highlight_text')
        subheading = request.POST.get('subheading')
        safe_water_solutions = request.POST.get('safe_water_solutions')
        customer_support = request.POST.get('customer_support')
        after_service_guarantee = request.POST.get('after_service_guarantee')
        image = request.FILES.get('image')

        AboutSection.objects.create(
            heading=heading,
            highlight_text=highlight_text,
            subheading=subheading,
            safe_water_solutions=safe_water_solutions,
            customer_support=customer_support,
            after_service_guarantee=after_service_guarantee,
            image=image,
        )
        return redirect('add_about_section')  # Redirect to refresh the page

    about_sections = AboutSection.objects.all()
    return render(request, 'add_about_section.html', {'about_sections': about_sections})






def edit_about_section(request, section_id):
    section = AboutSection.objects.get(id=section_id)

    if request.method == 'POST':
        section.heading = request.POST.get('heading')
        section.highlight_text = request.POST.get('highlight_text')
        section.subheading = request.POST.get('subheading')
        section.safe_water_solutions = request.POST.get('safe_water_solutions')
        section.customer_support = request.POST.get('customer_support')
        section.after_service_guarantee = request.POST.get('after_service_guarantee')

        if request.FILES.get('image'):
            section.image = request.FILES.get('image')

        section.save()
        return redirect('add_about_section')

    return render(request, 'edit_about_section.html', {'section': section})





def delete_about_section(request, section_id):
    section = AboutSection.objects.get(id=section_id)
    section.delete()
    return redirect('add_about_section')





# Add Expertise
def add_expertise_view(request):
    expertise_list = Expertise.objects.all()  # Fetch all expertise entries
    if request.method == 'POST':
        title = request.POST.get('title')
        description_1 = request.POST.get('description_1')
        description_2 = request.POST.get('description_2')
        description_3 = request.POST.get('description_3')
        image = request.FILES.get('image')

        expertise = Expertise(
            title=title,
            description_1=description_1,
            description_2=description_2,
            description_3=description_3,
            image=image
        )
        expertise.save()
        return redirect('add_expertise_view')

    return render(request, 'add_expertise.html',{'expertise_list':expertise_list})

# Edit Expertise
def edit_expertise_view(request, pk):
    expertise = get_object_or_404(Expertise, pk=pk)

    if request.method == 'POST':
        expertise.title = request.POST.get('title')
        expertise.description_1 = request.POST.get('description_1')
        expertise.description_2 = request.POST.get('description_2')
        expertise.description_3 = request.POST.get('description_3')
        if request.FILES.get('image'):
            expertise.image = request.FILES.get('image')
        expertise.save()
        return redirect('add_expertise_view')

    return render(request, 'edit_expertise.html', {'expertise': expertise})

# Delete Expertise
def delete_expertise_view(request, pk):
    expertise = get_object_or_404(Expertise, pk=pk)
    expertise.delete()
    return redirect('add_expertise_view')





# Add Water Solution
def add_water_solution(request):
    water_solutions = WaterSolution.objects.all()  # Retrieve the first entry
    if request.method == "POST":
        uv_heading = request.POST.get("uv_heading")
        uv_description = request.POST.get("uv_description")
        uv_image = request.FILES.get("uv_image")

        ro_heading = request.POST.get("ro_heading")
        ro_description = request.POST.get("ro_description")
        ro_image = request.FILES.get("ro_image")

        button_text = request.POST.get("button_text", "Download Catalog")
        button_link = request.POST.get("button_link")

        if water_solutions:
            water_solutions.uv_heading = uv_heading
            water_solutions.uv_description = uv_description
            if uv_image:
                water_solutions.uv_image = uv_image

            water_solutions.ro_heading = ro_heading
            water_solutions.ro_description = ro_description
            if ro_image:
                water_solutions.ro_image = ro_image

            water_solutions.button_text = button_text
            water_solutions.button_link = button_link
            water_solutions.save()
        else:
            WaterSolution.objects.create(
                uv_heading=uv_heading,
                uv_description=uv_description,
                uv_image=uv_image,
                ro_heading=ro_heading,
                ro_description=ro_description,
                ro_image=ro_image,
                button_text=button_text,
                button_link=button_link,
            )

        return redirect('add_water_solution')

    return render(request, 'add_water_solution.html', {'water_solutions': water_solutions})


# Edit Water Solution
def edit_water_solution(request,solution_id):
    water_solution = get_object_or_404(WaterSolution, id=solution_id) # Get the first row
    if not water_solution:
        return redirect('add_water_solution')  # Redirect if no data exists

    if request.method == "POST":
        water_solution.uv_heading = request.POST.get("uv_heading")
        water_solution.uv_description = request.POST.get("uv_description")
        if 'uv_image' in request.FILES:
            water_solution.uv_image = request.FILES.get("uv_image")

        water_solution.ro_heading = request.POST.get("ro_heading")
        water_solution.ro_description = request.POST.get("ro_description")
        if 'ro_image' in request.FILES:
            water_solution.ro_image = request.FILES.get("ro_image")

        water_solution.button_text = request.POST.get("button_text")
        water_solution.button_link = request.POST.get("button_link")
        water_solution.save()

        return redirect('add_water_solution')

    return render(request, 'edit_water_solution.html', {'solution': water_solution})


# Delete Water Solution
def delete_water_solution(request, solution_id):
    solution = get_object_or_404(WaterSolution, id=solution_id)
    solution.delete()
    return redirect('add_water_solution')



# Add Filtration Item
def add_filtration_item(request):
    items = FiltrationItem.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        button_text = request.POST.get("button_text", "Download Catalog")
        button_link = request.POST.get("button_link")

        item = FiltrationItem(
            title=title,
            description=description,
            image=image,
            button_text=button_text,
            button_link=button_link,
        )
        item.save()
        return redirect('add_filtration_item')

    return render(request, 'add_filtration_item.html', {'items': items})

# Edit Filtration Item
def edit_filtration_item(request, item_id):
    item = get_object_or_404(FiltrationItem, id=item_id)
    if request.method == "POST":
        item.title = request.POST.get("title")
        item.description = request.POST.get("description")
        if 'image' in request.FILES:
            item.image = request.FILES.get("image")
        item.button_text = request.POST.get("button_text")
        item.button_link = request.POST.get("button_link")
        item.save()
        return redirect('add_filtration_item')

    return render(request, 'edit_filtration_item.html', {'item': item})

# Delete Filtration Item
def delete_filtration_item(request, item_id):
    item = get_object_or_404(FiltrationItem, id=item_id)
    item.delete()
    return redirect('add_filtration_item')





# Add Testimonial
def add_testimonial(request):
    testimonials = Testimonial.objects.all()
    if request.method == "POST":
        client_name = request.POST.get("client_name")
        title = request.POST.get("title")
        message = request.POST.get("message")
        rating = int(request.POST.get("rating", 5))
        client_image = request.FILES.get("client_image")

        testimonial = Testimonial(
            client_name=client_name,
            client_image=client_image,
            title=title,
            message=message,
            rating=rating,
        )
        testimonial.save()
        return redirect('add_testimonial')

    return render(request, 'add_testimonial.html', {'testimonials': testimonials})

# Edit Testimonial
def edit_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    if request.method == "POST":
        testimonial.client_name = request.POST.get("client_name")
        testimonial.title = request.POST.get("title")
        testimonial.message = request.POST.get("message")
        testimonial.rating = int(request.POST.get("rating", 5))
        if 'client_image' in request.FILES:
            testimonial.client_image = request.FILES.get("client_image")
        testimonial.save()
        return redirect('add_testimonial')

    return render(request, 'edit_testimonial.html', {'testimonial': testimonial})

# Delete Testimonial
def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.delete()
    return redirect('add_testimonial')




# Add Gallery Image
def add_gallery_image(request):
    gallery_images = GalleryImage.objects.all()
    if request.method == "POST":
        image = request.FILES.get("image")
        alt_text = request.POST.get("alt_text")

        if image and alt_text:
            gallery_image = GalleryImage(image=image, alt_text=alt_text)
            gallery_image.save()
            return redirect('add_gallery_image')

    return render(request, 'add_gallery_image.html', {'gallery_images': gallery_images})

# Edit Gallery Image
def edit_gallery_image(request, image_id):
    gallery_image = get_object_or_404(GalleryImage, id=image_id)
    if request.method == "POST":
        gallery_image.alt_text = request.POST.get("alt_text")
        if 'image' in request.FILES:
            gallery_image.image = request.FILES.get("image")
        gallery_image.save()
        return redirect('add_gallery_image')

    return render(request, 'edit_gallery_image.html', {'gallery_image': gallery_image})

# Delete Gallery Image
def delete_gallery_image(request, image_id):
    gallery_image = get_object_or_404(GalleryImage, id=image_id)
    gallery_image.delete()
    return redirect('add_gallery_image')




# Add Product
def add_product(request):
    products = ProductShowcase.objects.all()
    if request.method == "POST":
        image = request.FILES.get("image")
        alt_text = request.POST.get("alt_text")

        if image and alt_text:
            product = ProductShowcase(image=image, alt_text=alt_text)
            product.save()
            return redirect('add_product')

    return render(request, 'add_product.html', {'products': products})

# Edit Product
def edit_product(request, product_id):
    product = get_object_or_404(ProductShowcase, id=product_id)
    if request.method == "POST":
        product.alt_text = request.POST.get("alt_text")
        if 'image' in request.FILES:
            product.image = request.FILES.get("image")
        product.save()
        return redirect('add_product')

    return render(request, 'edit_product.html', {'product': product})

# Delete Product
def delete_product(request, product_id):
    product = get_object_or_404(ProductShowcase, id=product_id)
    product.delete()
    return redirect('add_product')





# Add Content
def add_process_step(request):
    steps = WaterTreatmentProcess.objects.order_by("step_number")
    if request.method == "POST":
        step_number = request.POST.get("step_number")
        heading = request.POST.get("heading")
        points = request.POST.get("points")
        
        if step_number and heading and points:
            WaterTreatmentProcess.objects.create(
                step_number=step_number,
                heading=heading,
                points=points
            )
            return redirect("add_process_step")

    return render(request, "add_process_step.html", {"steps": steps})

# Edit Content
def edit_process_step(request, step_id):
    step = get_object_or_404(WaterTreatmentProcess, id=step_id)
    if request.method == "POST":
        step.heading = request.POST.get("heading")
        step.points = request.POST.get("points")
        step.save()
        return redirect("add_process_step")

    return render(request, "edit_process_step.html", {"step": step})

# Delete Content
def delete_process_step(request, step_id):
    step = get_object_or_404(WaterTreatmentProcess, id=step_id)
    step.delete()
    return redirect("add_process_step")



@login_required(login_url='login_user')
def admin_page(request):
    return render(request,'admin_page.html')



def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_page')  # Redirect to the Django admin page after login
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")





def contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')  # Fetch messages in descending order
    return render(request, 'contact_messages.html', {'messages': messages})




def delete_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    if request.method == "POST":
        message.delete()
        return redirect('contact_messages') 
    


def terms_and_conditions(request):
    return render(request,'terms_and_conditions.html')