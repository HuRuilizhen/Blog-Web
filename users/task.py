from .models import Profile


def update_all_users_rank():
    profiles = Profile.objects.filter(active=True).order_by("-score")
    for i, profile in enumerate(profiles):
        profile.rank = i + 1
        profile.save()
