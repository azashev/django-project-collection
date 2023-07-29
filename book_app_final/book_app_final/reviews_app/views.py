from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme

from book_app_final.reviews_app.models import Review


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST' and review.user == request.user:
        review.delete()
        next_url = request.POST.get('next', reverse_lazy('homepage'))

        if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect('homepage')
    else:
        context = {
            'review': review,
        }
        return render(request, 'reviews_templates/delete_review.html', context)
