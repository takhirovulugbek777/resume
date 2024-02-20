from django.http import HttpResponseServerError
from django.shortcuts import render
import requests
from django.contrib import messages
from .models import (
    UserProfile,
    Blog,
    Portfolio,
    Testimonial,
    Certificate
)

from django.views import generic

from .forms import ContactForm


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        testimonials = Testimonial.objects.filter(is_active=True)
        certificates = Certificate.objects.filter(is_active=True)
        blogs = Blog.objects.filter(is_active=True)
        portfolio = Portfolio.objects.filter(is_active=True)

        context["testimonials"] = testimonials
        context["certificates"] = certificates
        context["blogs"] = blogs
        context["portfolio"] = portfolio
        return context


class ContactView(generic.FormView):
    template_name = "main/contact.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.save()

        self.send_telegram_message(
            form.cleaned_data['name'],
            form.cleaned_data['email'],
            form.cleaned_data['message'],
            form.cleaned_data['phone']
        )

        messages.success(self.request, 'Thank you. We will be in touch soon.')
        return super().form_valid(form)

    def send_telegram_message(self, name, email, message, phone):
        bot_token = '6844513198:AAGrWiZi15u8ZWiX_KDabeDneNaIunzB3aI'  # Replace with your Telegram bot token
        chat_id = '1651940013'  # Replace with your Telegram chat ID

        telegram_message = f"<b>New message:</b>\n<b>Name</b>: {name}\n<b>Email</b>: {email} \n<b>Phone</b>: {phone}\n\n<b>Message:</b>\n{message}"

        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        params = {
            'chat_id': chat_id,
            'text': telegram_message,
            'parse_mode': 'HTML',
        }

        response = requests.post(url, params=params)

        if response.status_code != 200:
            print(f"Failed to send Telegram message. Status code: {response.status_code}")


class PortfolioView(generic.ListView):
    model = Portfolio
    template_name = "main/portfolio.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class PortfolioDetailView(generic.DetailView):
    model = Portfolio
    template_name = "main/portfolio-detail.html"


class BlogView(generic.ListView):
    model = Blog
    template_name = "main/blog.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = "main/blog-detail.html"
