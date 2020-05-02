from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservationsystem.models import Trip, Reservation
from reservationsystem.services.reservations import create_reservation
from users import permissions


class ReservationCreateApi(APIView):
    """
    Create a new Reservation
    """

    permission_classes = [permissions.IsCustomer]

    class InputSerializer(serializers.Serializer):
        trip_error_message = "invalid param format 'trip_id'; use GET '/trips' to retreive list of available trips"

        trip = serializers.PrimaryKeyRelatedField(
            queryset=Trip.objects.all(),
            error_messages={
                "does_not_exist": trip_error_message,
                "incorrect_type": trip_error_message,
            })

    class OutputSerializer(serializers.ModelSerializer):
        bus_seat = serializers.SerializerMethodField(read_only=True)

        def get_bus_seat(self, obj):
            return obj.bus_seat.name

        class Meta:
            model = Reservation
            fields = ['id', 'trip', 'bus_seat']

    def post(self, request, format=None):
        # [Step1] retrieve and validate body from request
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_reservation = create_reservation(
            **serializer.validated_data,
            customer=self.request.user.customer,
        )

        if not new_reservation:
            err_json = {'error_message': 'this trip has no available seats'}
            return Response(err_json, status=status.HTTP_400_BAD_REQUEST)

        # [Step4] return reservation data
        serializer = self.OutputSerializer(new_reservation)
        return Response(serializer.data)
