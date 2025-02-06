from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import ChannelSerializer, ServerSerializer


server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            description="Category of servers to retrieve",
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            description="Number of servers to retrieve",
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            description="Include number of members for each servers",
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="by_server_id",
            type=OpenApiTypes.INT,
            description="Include server by id",
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            description="Include server by user",
            location=OpenApiParameter.QUERY,
        ),
    ],
)
