from django.shortcuts import render
from rest_framework import viewsets
from .models import Server
from .serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from .schema import server_list_docs


class ServerListViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling operations on the Server model.

    Methods:
        list(request):
            Handles GET requests to retrieve a filtered list of servers.
            Filters include:
                - `qty`: Limit the number of servers returned.
                - `category`: Filter servers by their category name.
                - `by_user`: If true, filters servers where the authenticated user is a member.
                - `by_server_id`: Retrieves a server by its specific ID.
                - `with_num_members`: Annotates each server with the count of its members.
    """

    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
        Handles GET requests for retrieving a filtered list of servers.

        Query Parameters:
            qty (int): Optional. Limit the number of servers returned.
            category (str): Optional. Filter servers by the category name.
            by_user (bool): Optional. If true, filters servers where the authenticated user is a member.
            by_server_id (int): Optional. Retrieve a server with a specific ID.
            with_num_members (bool): Optional. If true, includes the count of members for each server.

        Returns:
            Response: Serialized server data matching the applied filters.

        Raises:
            AuthenticationFailed: If the user is not authenticated but attempts to filter by user or server ID.
            ValidationError: If the provided server ID does not exist or is invalid.
        """
        qty = request.query_params.get("qty")
        category = request.query_params.get("category")
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # if by_user or by_server_id and not request.user.is_authenticated:
        #     raise AuthenticationFailed(detail=f"{request.user} not authenticated")

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed(detail=f"{request.user} not authenticated")

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_server_id:
            if not request.user.is_authenticated:
                raise AuthenticationFailed(detail=f"{request.user} not authenticated")
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_server_id} not found"
                    )
            except ValueError:
                raise ValidationError(detail=f"Server with id {by_server_id} not found")

        if qty:
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
