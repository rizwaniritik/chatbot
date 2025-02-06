from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from .validators import validate_icon_image_size, validate_image_file_extension


def server_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icons/{filename}"


def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banners/{filename}"


def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"


class Category(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(
        upload_to=category_icon_upload_path,
        null=True,
        blank=True,
        validators=[validate_icon_image_size, validate_image_file_extension],
    )

    def __str__(self):
        """
        Returns the string representation of the Category object.

        Returns:
            str: The name of the category.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Overrides the save method to delete the old icon file if a new one is uploaded.
        """
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)


class Server(models.Model):
    """
    Represents a server.

    Attributes:
        name (str): The name of the server.
        owner (ForeignKey): The user who owns the server.
        category (ForeignKey): The category to which the server belongs.
        description (str): An optional description of the server.
        member (ManyToManyField): Users who are members of the server.
    """

    name = models.CharField(max_length=30)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category"
    )
    description = models.CharField(max_length=100, null=True, blank=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        """
        Returns the string representation of the Server object.

        Returns:
            str: The name and ID of the server.
        """
        return f"{self.name} - {self.id}"


class Channel(models.Model):
    """
    Represents a channel within a server.

    Attributes:
        name (str): The name of the channel.
        owner (ForeignKey): The user who owns the channel.
        topic (str): The topic of the channel.
        server (ForeignKey): The server to which the channel belongs.
    """

    name = models.CharField(max_length=30)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner"
    )
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channel_server"
    )
    banner = models.ImageField(upload_to=server_banner_upload_path, null=True, blank=True, validators=[validate_image_file_extension])
    icon = models.ImageField(upload_to=server_icon_upload_path, null=True, blank=True, validators=[validate_icon_image_size, validate_image_file_extension])

    def save(self, *args, **kwargs):
        """
        Overrides the save method to delete the old icon file if a new one is uploaded.
        """
        if self.id:
            existing = get_object_or_404(Channel, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)

            if existing.banner != self.banner:
                existing.banner.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Server")
    def category_delete_files(sender, instance, **kwargs):
        """
        Deletes the associated files when a Category object is deleted.

        Args:
            sender (Model): The sender model (Category).
            instance (Category): The instance being deleted.
        """
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        """
        Returns the string representation of the Channel object.

        Returns:
            str: The name of the channel.
        """
        return self.name
