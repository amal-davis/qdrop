from django.db import models

# Create your models here.



class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    



class SectionContent(models.Model):
    logo = models.ImageField(upload_to='section_content/', null=True, blank=True)
    heading = models.CharField(max_length=255)
    subheading = models.CharField(max_length=255)
    request_quote_url = models.URLField(default="#")
    whatsapp_url = models.URLField(default="https://wa.me/")
    image = models.ImageField(upload_to='section_content/', null=True, blank=True)

    def __str__(self):
        return self.heading
    


class AboutSection(models.Model):
    heading = models.TextField(help_text="Main heading with dynamic content")
    highlight_text = models.CharField(max_length=255, help_text="Highlighted text in the heading")
    subheading = models.TextField(help_text="Subheading or description")
    safe_water_solutions = models.CharField(max_length=50, default="10K+")
    customer_support = models.CharField(max_length=50, default="24/7")
    after_service_guarantee = models.CharField(max_length=50, default="100%")
    image = models.ImageField(upload_to='about_section/', help_text="Upload the image for the right section")

    def __str__(self):
        return f"About Section: {self.heading[:50]}"
    


class Expertise(models.Model):
    title = models.CharField(max_length=255, help_text="Enter the expertise title (e.g., 'Commercial Water Treatment')")
    description_1 = models.TextField(blank=True, help_text="Enter the first description point")
    description_2 = models.TextField(blank=True, help_text="Enter the second description point")
    description_3 = models.TextField(blank=True, help_text="Enter the third description point")
    image = models.ImageField(upload_to='expertise/', help_text="Upload an image for the card")

    def __str__(self):
        return self.title
    

class WaterSolution(models.Model):
    uv_heading = models.CharField(max_length=255, default="Default RO Heading", help_text="Heading for UV Water Purifier")
    uv_description = models.TextField(null=True, default="Default RO Heading", blank=True, help_text="Description for UV Water Purifier")
    uv_image = models.ImageField(upload_to='water_solutions/', null=True,blank=True, help_text="Image for UV Water Purifier")

    ro_heading = models.CharField(max_length=255, default="Default RO Heading", help_text="Heading for RO Water Purifier")
    ro_description = models.TextField(null=True, blank=True, help_text="Description for RO Water Purifier")
    ro_image = models.ImageField(upload_to='water_solutions/',null=True,blank=True,default="Default RO Heading",help_text="Image for RO Water Purifier")

    button_text = models.CharField(max_length=255, default="Download Catalog", help_text="Button text for catalog")
    button_link = models.URLField(null=True, blank=True, help_text="Enter the URL for catalog download",default="Default RO Heading",)

    def __str__(self):
        return self.uv_heading



    



class FiltrationItem(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the filtration item (e.g., 'Dual Media Filter')")
    description = models.TextField(help_text="Description of the filtration item")
    image = models.ImageField(upload_to='filtration_items/', help_text="Image for the filtration item")
    button_text = models.CharField(max_length=255, default="Download Catalog", help_text="Button text")
    button_link = models.URLField(blank=True, null=True, help_text="Optional button link")

    def __str__(self):
        return self.title
    

class Testimonial(models.Model):
    client_name = models.CharField(max_length=255, help_text="Name of the client")
    client_image = models.ImageField(upload_to='testimonials/', help_text="Client's image")
    title = models.CharField(max_length=255, help_text="Title or brief summary of the testimonial")
    message = models.TextField(help_text="Full testimonial message")
    rating = models.PositiveIntegerField(default=5, help_text="Rating out of 5")

    def __str__(self):
        return self.client_name
    


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/', help_text="Upload the gallery image")
    alt_text = models.CharField(max_length=255, help_text="Alt text for the image")

    def __str__(self):
        return f"Gallery Image {self.id}"
    

class ProductShowcase(models.Model):
    image = models.ImageField(upload_to='product_showcase/', help_text="Upload the product image")
    alt_text = models.CharField(max_length=255, help_text="Alt text for the image")

    def __str__(self):
        return f"Product Showcase {self.id}"
    




class WaterTreatmentProcess(models.Model):
    step_number = models.PositiveIntegerField(unique=True, help_text="Step number (e.g., 1, 2, 3, etc.)")
    heading = models.CharField(max_length=255, help_text="Heading for the step")
    points = models.TextField(help_text="Enter each point separated by a semicolon (;)")

    def __str__(self):
        return f"Step {self.step_number}: {self.heading}"

    def get_points_as_list(self):
        return self.points.split(";")