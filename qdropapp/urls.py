from django.urls import path
from  qdropapp import views




urlpatterns = [
    path('',views.index,name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('add-section/', views.add_section_content, name='add_section_content'),
    path('edit-section/<int:content_id>/', views.edit_section_content, name='edit_section_content'),
    path('delete-section/<int:content_id>/', views.delete_section_content, name='delete_section_content'),
    path('add-about-section/', views.add_about_section, name='add_about_section'),
    path('edit-about-section/<int:section_id>/', views.edit_about_section, name='edit_about_section'),
    path('delete-about-section/<int:section_id>/', views.delete_about_section, name='delete_about_section'),
    path('expertise/add/', views.add_expertise_view, name='add_expertise_view'),
    path('expertise/edit/<int:pk>/', views.edit_expertise_view, name='edit_expertise'),
    path('expertise/delete/<int:pk>/', views.delete_expertise_view, name='delete_expertise'),
    path('add_water_solution/', views.add_water_solution, name='add_water_solution'),
    path('edit_water_solution/<int:solution_id>/', views.edit_water_solution, name='edit_water_solution'),
    path('delete_water_solution/<int:solution_id>/', views.delete_water_solution, name='delete_water_solution'),
    path('add_filtration_item/', views.add_filtration_item, name='add_filtration_item'),
    path('edit_filtration_item/<int:item_id>/', views.edit_filtration_item, name='edit_filtration_item'),
    path('delete_filtration_item/<int:item_id>/', views.delete_filtration_item, name='delete_filtration_item'),
    path('add_testimonial/', views.add_testimonial, name='add_testimonial'),
    path('edit_testimonial/<int:testimonial_id>/', views.edit_testimonial, name='edit_testimonial'),
    path('delete_testimonial/<int:testimonial_id>/', views.delete_testimonial, name='delete_testimonial'),
    path('add_gallery_image/', views.add_gallery_image, name='add_gallery_image'),
    path('edit_gallery_image/<int:image_id>/', views.edit_gallery_image, name='edit_gallery_image'),
    path('delete_gallery_image/<int:image_id>/', views.delete_gallery_image, name='delete_gallery_image'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add_process_step/', views.add_process_step, name='add_process_step'),
    path('edit_process_step/<int:step_id>/', views.edit_process_step, name='edit_process_step'),
    path('delete_process_step/<int:step_id>/', views.delete_process_step, name='delete_process_step'),
    path('login_user',views.login_user,name='login_user'),
    path('contact-messages/', views.contact_messages, name='contact_messages'),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('admin_page',views.admin_page,name='admin_page'),
    path('terms_and_conditions',views.terms_and_conditions,name='terms_and_conditions'),
] 