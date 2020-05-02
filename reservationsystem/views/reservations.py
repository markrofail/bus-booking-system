from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from reservationsystem.models import Reservation
from reservationsystem.serializers import ReservationSerializer, ReservationPostBodySerializer
from users.permissions import IsCustomer


@api_view(['POST'])
@permission_classes((IsCustomer,))
def create_reservation(request):
    """
    Create a new Reservation
    """
    # [Step1] retrieve and validate body from request
    request_body = ReservationPostBodySerializer(data=request.data)
    if not request_body.is_valid():
        return Response(request_body.errors, status=status.HTTP_400_BAD_REQUEST)
    request_body = request_body.validated_data

    # [Step2] check if trip has a free reservation
    trip = request_body['trip_id']
    if not trip.has_available_seats():
        error = 'this trip has no available seats'
        return Response({'error_message': error}, status=status.HTTP_400_BAD_REQUEST)

    # [Step3] create reservation
    customer = request.user.customer
    new_reservation = Reservation(trip=trip, customer=customer)
    new_reservation.save()

    # [Step4] return reservation data
    serializer = ReservationSerializer(new_reservation)
    return Response(serializer.data)
